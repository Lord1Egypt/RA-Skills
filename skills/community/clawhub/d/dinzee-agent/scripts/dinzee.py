#!/usr/bin/env python3
"""
dinzee.py — DinzeeAgent skill CLI. Invokes third-party MCP tools (SIF, and
future providers) through the dinzee_service gateway. The gateway authenticates
the user, charges their points, and forwards to the upstream MCP server — the
upstream endpoint and credentials are never exposed to the caller.

Architecture (MCP tool 级，由 openclaw/hermes 的 LLM 自由编排):
    openclaw/hermes ──> this skill ──> dinzee_service /v1/mcp/* ──> MCP server (SIF…)
                                            │
                                            └─> ai_web (扣点)

Token resolution (in order):
    1. Environment variable DINZEE_USER_TOKEN (or legacy DINZEEAGENT_API_KEY)
    2. ~/.dinzee/credentials.json with {"user_token": "sut_xxx"}
    3. Clear error message

CLI:
    dinzee.py login <sut_token>             save token to ~/.dinzee/credentials.json
    dinzee.py logout                        delete saved token
    dinzee.py status                        print where the token comes from
    dinzee.py providers                     list registered MCP providers
    dinzee.py list-tools [--provider sif]   list available MCP tools for a provider
    dinzee.py describe <tool>               show a tool's availability / charge flag
    dinzee.py call <tool> --args '<json>'   invoke a tool (json may also come from stdin via --stdin)

Environment overrides:
    DINZEE_GATEWAY_BASE_URL   default https://gateway.dinzee.ai/
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import shutil
import stat
import sys
import time
import uuid
import zipfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://gateway.dinzee.ai/"
DEFAULT_PROVIDER = "sif"

USER_TOKEN_HEADER = "x-user-integration-token"

CREDENTIALS_PATH = Path.home() / ".dinzee" / "credentials.json"

PROVIDERS_PATH = "v1/mcp/providers"
TOOLS_PATH = "v1/mcp/tools"
CALLS_PATH = "v1/mcp/calls"

CATALOG_PATH = "v1/skill-center/catalog"
INSTALL_PATH = "v1/skill-center/install"


# ---------------------------------------------------------------------------
# Token resolution
# ---------------------------------------------------------------------------

def base_url() -> str:
    raw = (os.environ.get("DINZEE_GATEWAY_BASE_URL") or DEFAULT_BASE_URL).strip() or DEFAULT_BASE_URL
    return raw.rstrip("/") + "/"


def _read_credentials_file() -> dict:
    if not CREDENTIALS_PATH.is_file():
        return {}
    try:
        with CREDENTIALS_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _resolve_token() -> tuple[str | None, str]:
    """Returns (token, source). source ∈ {env, file, missing}."""
    env_token = (os.environ.get("DINZEE_USER_TOKEN") or os.environ.get("DINZEEAGENT_API_KEY") or "").strip()
    if env_token:
        return env_token, "env"
    file_token = str(_read_credentials_file().get("user_token") or "").strip()
    if file_token:
        return file_token, "file"
    return None, "missing"


def _require_token() -> str:
    token, source = _resolve_token()
    if not token:
        print(
            "Error: 找不到用户接入 token (sut_xxx)。两种设置方式：\n"
            "  1. 临时：export DINZEE_USER_TOKEN=sut_xxx\n"
            "  2. 永久：python3 dinzee.py login sut_xxx\n"
            "         （会保存到 ~/.dinzee/credentials.json，权限 0600）",
            file=sys.stderr,
        )
        sys.exit(1)
    if not token.startswith("sut_"):
        print(
            f"Warning: token doesn't start with 'sut_' (source={source}). 网关只接受用户接入 token。",
            file=sys.stderr,
        )
    return token


def _save_token(token: str) -> Path:
    CREDENTIALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = _read_credentials_file()
    data["user_token"] = token
    data["updated_at"] = int(time.time())
    tmp = CREDENTIALS_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    tmp.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 0600
    tmp.replace(CREDENTIALS_PATH)
    return CREDENTIALS_PATH


def _clear_token() -> bool:
    if CREDENTIALS_PATH.is_file():
        try:
            CREDENTIALS_PATH.unlink()
            return True
        except OSError:
            return False
    return False


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def _request(method: str, path: str, query: dict | None = None, body: dict | None = None, timeout: int = 240) -> tuple[int, dict]:
    url = base_url() + path.lstrip("/")
    if query:
        from urllib.parse import urlencode
        url += "?" + urlencode({k: v for k, v in query.items() if v is not None})
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {
        "Accept": "application/json",
        "User-Agent": "DinzeeAgent-Skill/1.0",
        USER_TOKEN_HEADER: _require_token(),
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return resp.getcode(), (json.loads(raw) if raw else {})
    except HTTPError as e:
        raw = e.read().decode("utf-8") if e.fp else ""
        parsed: dict = {}
        if raw:
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = {"error_body": raw}
        return e.code, parsed
    except URLError as e:
        return 0, {"error": f"Connection failed: {e.reason}"}
    except Exception as e:
        return 0, {"error": str(e)}


def _print_json(value, fmt: str = "json") -> None:
    if fmt == "text":
        # Pretty key/value print for top-level dicts; falls back to json for everything else.
        if isinstance(value, dict):
            for k, v in value.items():
                print(f"{k}: {v if not isinstance(v, (dict, list)) else json.dumps(v, ensure_ascii=False)}")
            return
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _fail(code: int, body: dict) -> None:
    msg = (body or {}).get("error") or (body or {}).get("message") or (body or {}).get("error_body") or json.dumps(body or {}, ensure_ascii=False)
    print(f"Error: HTTP {code}: {msg}", file=sys.stderr)
    if code in (401, 403, 410):
        token, source = _resolve_token()
        print(
            f"\nHint: 鉴权失败。token 来源={source}，前缀正常应为 sut_。\n"
            f"  网关地址: {base_url()}\n"
            f"  若要重新设置 token: python3 dinzee.py login sut_xxx",
            file=sys.stderr,
        )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_login(args) -> None:
    token = args.token.strip()
    if not token:
        print("Error: token 不能为空", file=sys.stderr)
        sys.exit(2)
    if not token.startswith("sut_"):
        print("Warning: token 不以 sut_ 开头，仍然保存。", file=sys.stderr)
    path = _save_token(token)
    print(f"✅ Token saved to {path} (mode 0600).")


def cmd_logout(args) -> None:
    if _clear_token():
        print(f"✅ Token removed from {CREDENTIALS_PATH}.")
    else:
        print(f"No saved token at {CREDENTIALS_PATH}.")


def cmd_status(args) -> None:
    token, source = _resolve_token()
    print(f"Gateway base URL : {base_url()}")
    print(f"Token source     : {source}")
    if token:
        masked = token[:6] + "…" + token[-4:] if len(token) > 12 else "(short token)"
        print(f"Token preview    : {masked}")
        print(f"Credentials file : {CREDENTIALS_PATH} ({'exists' if CREDENTIALS_PATH.is_file() else 'absent'})")
    else:
        print("No token configured. Run `login <sut_token>` or `export DINZEE_USER_TOKEN=sut_xxx`.")


def cmd_providers(args) -> None:
    code, body = _request("GET", PROVIDERS_PATH)
    if code != 200:
        _fail(code, body)
    _print_json(body, args.format)


def cmd_list_tools(args) -> None:
    code, body = _request("GET", TOOLS_PATH, query={"provider": args.provider})
    if code != 200:
        _fail(code, body)
    if args.format == "text":
        tools = (body or {}).get("tools") or []
        for t in tools:
            mark = "" if t.get("available") else " [unavailable]"
            charge = "" if t.get("chargeable") else " [free]"
            print(f"{t.get('tool')}{charge}{mark}")
        print(f"\nTotal: {len(tools)}")
    else:
        _print_json(body, args.format)


def cmd_describe(args) -> None:
    # The gateway doesn't expose tool input schemas directly. The closest we
    # can do is route an MCP "tools/list" via /v1/mcp/tools and surface the
    # `available` flag plus the policy capability. Real input schemas live on
    # the upstream MCP server; if you need them, call `tools/list` with the
    # gateway's call endpoint or read SIF's docs (references/sif.md).
    code, body = _request("GET", TOOLS_PATH, query={"provider": args.provider})
    if code != 200:
        _fail(code, body)
    tools = (body or {}).get("tools") or []
    match = next((t for t in tools if str(t.get("tool")) == args.tool), None)
    if not match:
        print(f"Tool '{args.tool}' not found in provider '{args.provider}'.", file=sys.stderr)
        print(f"\nAvailable tools:", file=sys.stderr)
        for t in tools:
            print(f"  - {t.get('tool')}", file=sys.stderr)
        sys.exit(1)
    print(f"Tool       : {match.get('tool')}")
    print(f"Available  : {match.get('available')}")
    print(f"Chargeable : {match.get('chargeable')}")
    print(f"\n参数 schema：网关侧不暴露 inputSchema，请参考 references/sif.md 或上游 SIF 文档。")


def cmd_call(args) -> None:
    raw_args: str
    if args.stdin:
        raw_args = sys.stdin.read().strip()
        if not raw_args:
            print("Error: --stdin specified but stdin was empty", file=sys.stderr)
            sys.exit(2)
    else:
        raw_args = args.args or "{}"
    try:
        arguments = json.loads(raw_args)
    except json.JSONDecodeError as e:
        print(f"Error: --args JSON parse failed: {e}", file=sys.stderr)
        print(f"Received: {raw_args[:200]}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(arguments, dict):
        print("Error: --args must decode to a JSON object", file=sys.stderr)
        sys.exit(2)

    payload = {
        "provider": args.provider,
        "tool": args.tool,
        "arguments": arguments,
        "idempotencyKey": args.idempotency_key or f"sif_{uuid.uuid4().hex}",
    }
    code, body = _request("POST", CALLS_PATH, body=payload, timeout=max(60, int(args.timeout)))
    if code != 200:
        _fail(code, body)
    if args.format == "text":
        if (body or {}).get("ok"):
            print(f"Status        : {body.get('status')}")
            print(f"Provider/Tool : {body.get('provider')} / {body.get('tool')}")
            if body.get("authority_correlation_id"):
                print(f"Charge corr id: {body.get('authority_correlation_id')}")
            print()
            print(json.dumps(body.get("result") or {}, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(body, ensure_ascii=False, indent=2))
    else:
        _print_json(body, args.format)


# ---------------------------------------------------------------------------
# Skill center：装/更新付费数据 skill（经计费网关，按版本扣点）
# ---------------------------------------------------------------------------

def _skills_dir(args) -> Path:
    """openclaw 的 skills 目录。本脚本在 <skills>/dinzeeagent/scripts/dinzee.py，
    故 parents[2] = <skills>。可用 --skills-dir / env DINZEE_SKILLS_DIR 覆盖。"""
    override = getattr(args, "skills_dir", None) or os.environ.get("DINZEE_SKILLS_DIR")
    if override:
        return Path(override).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def _write_package(target: Path, package_b64: str) -> int:
    """把网关返回的 zip（base64）解压到 target（先清后写）。zip 内文件在根层。"""
    data = base64.b64decode(package_b64)
    zf = zipfile.ZipFile(io.BytesIO(data))
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    count = 0
    for name in zf.namelist():
        if name.endswith("/"):
            continue
        segments = name.split("/")
        if name.startswith("/") or any(s in ("", "..") for s in segments):
            continue  # path-traversal guard
        dest = target / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(zf.read(name))
        count += 1
    return count


def cmd_skills(args) -> None:
    code, body = _request("GET", CATALOG_PATH)
    if code != 200:
        _fail(code, body)
    if args.format == "text":
        skills = (body or {}).get("skills") or []
        for s in skills:
            price = int(s.get("points_cost") or 0)
            tag = f"{price}点/次" if price > 0 else "免费"
            print(f"{s.get('slug')}  v{s.get('latestVersion') or '?'}  [{tag}]  {s.get('displayName') or ''}")
        print(f"\nTotal: {len(skills)}（首次安装与每次更新各扣一次，同版本不重复扣）")
    else:
        _print_json(body, args.format)


def cmd_skill_install(args) -> None:
    slug = args.slug.strip().lower()
    if slug == "dinzeeagent":
        print("Error: dinzeeagent 是客户端本体，请用 clawhub 安装/更新，不经此命令。", file=sys.stderr)
        sys.exit(2)
    payload: dict = {"slug": slug}
    if getattr(args, "version", None):
        payload["version"] = args.version
    code, body = _request("POST", INSTALL_PATH, body=payload)
    if code != 200:
        _fail(code, body)
    pkg = (body or {}).get("package_b64")
    if not pkg:
        print(f"Error: 网关未返回 package（body={json.dumps(body, ensure_ascii=False)[:200]}）", file=sys.stderr)
        sys.exit(1)
    target = _skills_dir(args) / slug
    n = _write_package(target, pkg)
    ver = (body or {}).get("version")
    charged = int((body or {}).get("points_charged") or 0)
    if (body or {}).get("already_owned"):
        print(f"✅ {slug}@{ver}：你已拥有此版本，未重复扣点。已写入 {target}（{n} 个文件）。")
    else:
        print(f"✅ 已交付 {slug}@{ver}，扣 {charged} 点。已写入 {target}（{n} 个文件）。")
    print("（openclaw 热加载会自动识别该 skill；若未启用 watch，重启 agent 即可）")


def cmd_skill_update(args) -> None:
    sdir = _skills_dir(args)
    if args.all:
        targets = []
        if sdir.is_dir():
            for child in sorted(sdir.iterdir()):
                if child.is_dir() and child.name != "dinzeeagent" and (child / "SKILL.md").is_file():
                    targets.append(child.name)
        if not targets:
            print("没有已安装的内容 skill。")
            return
    else:
        if not args.slug:
            print("Error: 提供 <slug> 或 --all", file=sys.stderr)
            sys.exit(2)
        targets = [args.slug.strip().lower()]
    for slug in targets:
        ns = argparse.Namespace(
            slug=slug, version=None, format=args.format,
            skills_dir=getattr(args, "skills_dir", None),
        )
        try:
            cmd_skill_install(ns)
        except SystemExit:
            # --all 时单个失败（如余额不足）不中断其余；错误信息 _fail 已打印
            if not args.all:
                raise


# ---------------------------------------------------------------------------
# CLI entry
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(
        prog="dinzee",
        description="DinzeeAgent — call third-party MCP tools via dinzee_service gateway",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--format", "-f", choices=["json", "text"], default="text")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("login", help="save sut_ token to ~/.dinzee/credentials.json")
    sp.add_argument("token")
    sp.set_defaults(func=cmd_login)

    sp = sub.add_parser("logout", help="delete saved token")
    sp.set_defaults(func=cmd_logout)

    sp = sub.add_parser("status", help="show token source / gateway URL")
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("providers", help="list registered MCP providers")
    sp.set_defaults(func=cmd_providers)

    sp = sub.add_parser("list-tools", help="list available tools for a provider")
    sp.add_argument("--provider", default=DEFAULT_PROVIDER)
    sp.set_defaults(func=cmd_list_tools)

    sp = sub.add_parser("describe", help="describe a specific tool")
    sp.add_argument("tool")
    sp.add_argument("--provider", default=DEFAULT_PROVIDER)
    sp.set_defaults(func=cmd_describe)

    sp = sub.add_parser("call", help="invoke a tool")
    sp.add_argument("tool")
    sp.add_argument("--provider", default=DEFAULT_PROVIDER)
    sp.add_argument("--args", help="tool input as JSON object (default: {})")
    sp.add_argument("--stdin", action="store_true", help="read --args JSON from stdin")
    sp.add_argument("--idempotency-key", help="caller idempotency key (default: random uuid)")
    sp.add_argument("--timeout", type=int, default=240)
    sp.set_defaults(func=cmd_call)

    sp = sub.add_parser("skills", help="list installable data skills (catalog + price)")
    sp.set_defaults(func=cmd_skills)

    sp = sub.add_parser("skill-install", help="install a data skill into the agent (charges points)")
    sp.add_argument("slug")
    sp.add_argument("--version", help="specific version (default: latest)")
    sp.add_argument("--skills-dir", help="override skills dir (default: sibling of dinzeeagent)")
    sp.set_defaults(func=cmd_skill_install)

    sp = sub.add_parser("skill-update", help="update installed skill(s) to latest (charges per new version)")
    sp.add_argument("slug", nargs="?", help="skill slug; omit with --all")
    sp.add_argument("--all", action="store_true", help="update every installed content skill")
    sp.add_argument("--skills-dir", help="override skills dir")
    sp.set_defaults(func=cmd_skill_update)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
