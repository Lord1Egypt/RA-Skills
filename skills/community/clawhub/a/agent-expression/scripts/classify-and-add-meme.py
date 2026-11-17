#!/usr/bin/env python3
"""Vision-classify an image into a meme pack tag, then add it."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Same-directory helpers (filename has a hyphen → load via importlib)
import importlib.util

_SCRIPTS = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "add_meme", _SCRIPTS / "add-meme.py"
)
am = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(am)

TAG_RE = am.TAG_RE
JSON_RE = re.compile(r"\{[^{}]*\}", re.DOTALL)


def _expand_env(value: str, env: dict[str, str]) -> str:
    def repl(m: re.Match[str]) -> str:
        return env.get(m.group(1), os.environ.get(m.group(1), m.group(0)))

    return re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}", repl, value or "")


def _load_mdb():
    spec = importlib.util.spec_from_file_location("meme_db", _SCRIPTS / "meme_db.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load_vision_config() -> dict[str, str]:
    """OpenAI-compatible vision: env first, optional Hermes config.yaml fallback."""
    mdb = _load_mdb()
    env = mdb.load_dotenv_merged()

    cfg: dict = {}
    for home_key in ("MEME_HOME", "AGENT_EXPRESSION_HOME", "HERMES_HOME"):
        home_v = os.environ.get(home_key, "").strip()
        if home_v:
            homes = [Path(home_v).expanduser()]
            break
    else:
        homes = [mdb.data_home(), Path("~/.hermes").expanduser()]

    for home in homes:
        cfg_path = home / "config.yaml"
        if not cfg_path.is_file():
            continue
        try:
            import yaml  # type: ignore

            raw = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
            cfg = ((raw.get("auxiliary") or {}).get("vision") or {})
        except Exception:
            text = cfg_path.read_text(encoding="utf-8")
            block = False
            for line in text.splitlines():
                if re.match(r"^\s+vision:\s*$", line):
                    block = True
                    continue
                if block:
                    m = re.match(r"^\s{4}([a-z_]+):\s*(.+)$", line)
                    if m:
                        cfg[m.group(1)] = m.group(2).strip().strip('"').strip("'")
                    elif re.match(r"^\S", line) or (
                        re.match(r"^\s{0,2}\S", line) and not line.startswith("    ")
                    ):
                        if not line.strip().startswith("#"):
                            block = False
        if cfg:
            break

    base_url = _expand_env(
        str(
            cfg.get("base_url")
            or env.get("VISION_BASE_URL")
            or env.get("OPENAI_BASE_URL")
            or ""
        ),
        env,
    ).rstrip("/")
    api_key = _expand_env(str(cfg.get("api_key") or ""), env)
    model = _expand_env(
        str(cfg.get("model") or env.get("VISION_MODEL") or ""),
        env,
    )
    if not api_key:
        api_key = (
            env.get("VISION_API_KEY")
            or env.get("ARK_API_KEY")
            or env.get("OPENAI_API_KEY")
            or ""
        )
    if not base_url:
        base_url = "https://ark.cn-beijing.volces.com/api/v3"
    if not model:
        model = "doubao-seed-2-0-mini-260428"
    return {"base_url": base_url, "api_key": api_key, "model": model}


def category_catalog(pack_dir: Path) -> list[dict[str, str]]:
    manifest = am.load_manifest(pack_dir)
    cats = manifest.get("categories") or {}
    memes_root = pack_dir / "memes"
    names = sorted(cats.keys()) if cats else sorted(
        p.name for p in memes_root.iterdir() if p.is_dir()
    ) if memes_root.is_dir() else []
    out = []
    for name in names:
        meta = cats.get(name, {})
        desc = meta.get("description", "") if isinstance(meta, dict) else str(meta)
        count = len(am.list_images(memes_root / name)) if hasattr(am, "list_images") else 0
        if not hasattr(am, "list_images"):
            # fallback
            d = memes_root / name
            count = (
                len([p for p in d.iterdir() if p.is_file() and p.suffix.lower() in am.IMAGE_EXTS])
                if d.is_dir()
                else 0
            )
        out.append({"tag": name, "count": str(count), "desc": desc})
    return out


def list_images_fallback(pack_dir: Path, tag: str) -> int:
    d = pack_dir / "memes" / tag
    if not d.is_dir():
        return 0
    return sum(1 for p in d.iterdir() if p.is_file() and p.suffix.lower() in am.IMAGE_EXTS)


def image_to_data_url(path: Path) -> str:
    data = path.read_bytes()
    if len(data) > am.MAX_BYTES:
        raise ValueError(f"image larger than {am.MAX_BYTES} bytes")
    ext = am.detect_ext(data, path.suffix.lower())
    if not ext:
        raise ValueError("not a supported image")
    mime = mimetypes.types_map.get(ext, "application/octet-stream")
    if ext == ".jpg":
        mime = "image/jpeg"
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def source_to_local(source: str, tmp_dir: Path) -> Path:
    source = source.strip()
    if source.startswith(("http://", "https://")):
        data, hint = am.fetch_bytes(source)
        ext = am.detect_ext(data, Path(hint).suffix.lower()) or ".png"
        path = tmp_dir / f"download{ext}"
        path.write_bytes(data)
        return path
    path = Path(source).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"file not found: {path}")
    return path


def vision_classify(data_url: str, catalog: list[dict[str, str]], vision: dict[str, str]) -> dict:
    if not vision.get("api_key"):
        raise RuntimeError(
            "no vision api_key (set VISION_API_KEY / OPENAI_API_KEY / ARK_API_KEY)"
        )

    cat_lines = "\n".join(
        f"- {c['tag']}: {c['desc']} (n={c['count']})" for c in catalog
    ) or "(no categories yet)"

    prompt = f"""你在给表情包自动打标签。只输出一个 JSON 对象，不要 markdown，不要解释。

已有分类（优先选用）：
{cat_lines}

规则：
1. 尽量选已有 tag；只有都不贴切才新建。
2. tag 必须匹配 ^[a-z][a-z0-9_-]{{0,31}}$
3. 新建时 create=true，并给一句中文 desc（场景说明）。
4. 选已有时 create=false，desc 可空。
5. 不要选 color / givemoney，除非画面明显是调情或讨钱。
6. 可爱卖萌偏 happy/meow/like/shy；无语 sigh；生气 angry；委屈 sad；困惑 confused。

输出格式严格如下：
{{"tag":"happy","create":false,"desc":"","reason":"一句话中文理由"}}
"""

    body = {
        "model": vision["model"],
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": data_url}},
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        "temperature": 0.2,
    }
    url = vision["base_url"].rstrip("/") + "/chat/completions"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {vision['api_key']}",
            "Content-Type": "application/json",
            "User-Agent": "agent-expression/classify",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:400]
        raise RuntimeError(f"vision HTTP {e.code}: {detail}") from e
    except Exception as e:
        raise RuntimeError(f"vision request failed: {e}") from e

    text = (
        (((payload.get("choices") or [{}])[0].get("message") or {}).get("content"))
        or ""
    ).strip()
    if not text:
        raise RuntimeError(f"empty vision response: {payload!r}"[:300])

    # strip ```json fences if any
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        m = JSON_RE.search(text)
        if not m:
            raise RuntimeError(f"vision did not return JSON: {text[:300]}")
        data = json.loads(m.group(0))

    tag = str(data.get("tag", "")).strip().lower()
    if not TAG_RE.match(tag):
        raise RuntimeError(f"invalid tag from vision: {tag!r}")
    create = bool(data.get("create"))
    desc = str(data.get("desc") or "").strip()
    reason = str(data.get("reason") or "").strip()
    known = {c["tag"] for c in catalog}
    if tag not in known:
        create = True
        if not desc:
            desc = reason or f"自定义分类 {tag}"
    else:
        create = False
    return {"tag": tag, "create": create, "desc": desc, "reason": reason, "raw": text}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Classify image with vision, then add to local meme pack."
    )
    parser.add_argument("source", help="Local image path or http(s) URL")
    parser.add_argument("--pack", help="Meme pack root")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only classify; print JSON, do not write files",
    )
    parser.add_argument(
        "--force-tag",
        default="",
        help="Skip vision and use this tag (still can --create)",
    )
    parser.add_argument(
        "--create",
        action="store_true",
        help="Allow creating category when using --force-tag",
    )
    parser.add_argument("--desc", default="", help="Description when creating")
    args = parser.parse_args(argv)

    pack_dir = Path(args.pack).expanduser() if args.pack else am.default_pack_dir()
    if not pack_dir.is_dir():
        print(f"ERROR: pack not found: {pack_dir}", file=sys.stderr)
        return 1

    # build catalog with counts
    manifest = am.load_manifest(pack_dir)
    cats = manifest.get("categories") or {}
    memes_root = pack_dir / "memes"
    catalog = []
    names = sorted(cats.keys()) if cats else (
        sorted(p.name for p in memes_root.iterdir() if p.is_dir())
        if memes_root.is_dir()
        else []
    )
    for name in names:
        meta = cats.get(name, {})
        desc = meta.get("description", "") if isinstance(meta, dict) else str(meta)
        catalog.append(
            {
                "tag": name,
                "count": str(list_images_fallback(pack_dir, name)),
                "desc": desc,
            }
        )

    tmp_dir = _load_mdb().temp_workdir()

    try:
        local = source_to_local(args.source, tmp_dir)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if args.force_tag:
        decision = {
            "tag": args.force_tag.strip().lower(),
            "create": bool(args.create)
            or not (pack_dir / "memes" / args.force_tag.strip().lower()).is_dir(),
            "desc": args.desc or f"自定义分类 {args.force_tag}",
            "reason": "force-tag",
        }
        if not TAG_RE.match(decision["tag"]):
            print("ERROR: invalid --force-tag", file=sys.stderr)
            return 1
    else:
        vision = load_vision_config()
        try:
            data_url = image_to_data_url(local)
            decision = vision_classify(data_url, catalog, vision)
        except Exception as e:
            print(f"ERROR: classify failed: {e}", file=sys.stderr)
            print(
                "HINT: fallback — use vision_analyze then add-meme.py <tag> <path>",
                file=sys.stderr,
            )
            return 1

    result = {
        "tag": decision["tag"],
        "create": decision["create"],
        "desc": decision.get("desc") or "",
        "reason": decision.get("reason") or "",
        "source": str(local),
    }

    if args.dry_run:
        print(json.dumps(result, ensure_ascii=False))
        return 0

    rc = am.cmd_add(
        pack_dir,
        decision["tag"],
        str(local),
        create=bool(decision["create"]),
        description=decision.get("desc") or "",
    )
    if rc == 0:
        # also print machine-readable summary on stderr-free second line style
        print(f"CLASSIFIED\t{decision['tag']}\t{decision.get('reason', '')}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
