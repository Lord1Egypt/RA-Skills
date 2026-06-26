#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prana 封装技能 — 薄客户端（无业务逻辑，仅负责与 Prana 服务通信）
从 GitHub / Claw Hub 等下载本技能包后，通过本脚本将用户输入转发到 Prana 执行真实能力。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import uuid
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlencode

# 技能根目录（本脚本位于 scripts/ 下）
SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = SKILL_ROOT / "config"
API_KEY_FILE = CONFIG_DIR / "api_key.txt"
SKILL_MD_FILE = SKILL_ROOT / "SKILL.md"

# 封装打包时由服务端替换为 dict（见锚点注释）；仓库模板为 None，仅供开发或旧版 frontmatter 回退。
_ENCAPSULATION_EMBEDDED: Optional[Dict[str, Any]] = {"public_skill_key": "getmeastock_public", "original_skill_key": "getmeastock", "encapsulation_target": "prana"}

DEFAULT_PRANA_BASE = "https://claw-uat.ebonex.io/"

# agent-run 为长连接场景；超时或失败后改查 agent-result（同一 request_id）
HTTP_TIMEOUT_SEC = 7200
# agent-run 非合法 JSON 或需改查时，按固定间隔轮询 POST /api/claw/agent-result（默认每 2 分钟）
AGENT_RESULT_POLL_INTERVAL_SEC = int(os.environ.get("PRANA_AGENT_RESULT_POLL_INTERVAL_SEC", "120"))
AGENT_RESULT_POLL_MAX_ATTEMPTS = int(os.environ.get("PRANA_AGENT_RESULT_POLL_MAX_ATTEMPTS", "20"))
# 自动拉取 API key（GET /api/v1/api-keys）超时
API_KEYS_FETCH_TIMEOUT_SEC = 60


def _auto_fetch_api_key_disabled() -> bool:
    """PRANA_SKILL_NO_AUTO_API_KEY=1 时不在本地缺省时自动请求 create_key 接口。"""
    v = os.environ.get("PRANA_SKILL_NO_AUTO_API_KEY", "").strip().lower()
    return v in ("1", "true", "yes", "on")


def _skip_write_fetched_api_key() -> bool:
    """PRANA_SKILL_SKIP_WRITE_API_KEY=1 时不把接口拉取的 key 写入磁盘（默认会写入 config/api_key.txt）。"""
    v = os.environ.get("PRANA_SKILL_SKIP_WRITE_API_KEY", "").strip().lower()
    return v in ("1", "true", "yes", "on")


def _normalize_encapsulation_target(raw: Optional[str]) -> str:
    """与后端 encapsulation target_system 一致：默认 prana；clawHub 等归一为 claw_hub。"""
    s = (raw or "").strip().lower().replace("-", "_")
    if not s:
        return "prana"
    aliases = {"clawhub": "claw_hub", "openclaw": "claw_hub", "open_claw": "claw_hub"}
    key = aliases.get(s, s)
    return key[:64] if len(key) > 64 else key


def _load_encapsulation_runtime() -> Optional[Dict[str, Any]]:
    """封装包内写入 `prana_skill_client.py` 的 `_ENCAPSULATION_EMBEDDED`；未封装/模板为 None。"""
    emb = _ENCAPSULATION_EMBEDDED
    if isinstance(emb, dict) and emb:
        return dict(emb)
    return None


def _extract_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], str]:
    if not content.strip().startswith("---"):
        return None, content
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not match:
        return None, content
    try:
        import yaml

        fm = yaml.safe_load(match.group(1))
        return (fm if isinstance(fm, dict) else None), match.group(2)
    except Exception:
        return None, content


def load_skill_config() -> Dict[str, Any]:
    """
    从本脚本内嵌 `_ENCAPSULATION_EMBEDDED` 与 SKILL.md frontmatter 合并读取配置。
    agent-run 使用的 skill_key：优先内嵌 `original_skill_key`，其次旧版 SKILL.md 字段。
    """
    if not SKILL_MD_FILE.exists():
        print(
            "错误: 未找到 SKILL.md，请使用完整封装技能包解压后运行。",
            file=sys.stderr,
        )
        sys.exit(1)
    runtime = _load_encapsulation_runtime()
    raw = SKILL_MD_FILE.read_text(encoding="utf-8")
    frontmatter, _ = _extract_frontmatter(raw)
    if not frontmatter:
        print("错误: SKILL.md 缺少有效的 YAML frontmatter。", file=sys.stderr)
        sys.exit(1)
    original = str((runtime or {}).get("original_skill_key") or "").strip()
    pub_fm = str(frontmatter.get("original_skill_key") or "").strip()
    pub_key_fm = str(frontmatter.get("skill_key") or "").strip()
    if not original:
        original = pub_fm
    pub = str((runtime or {}).get("public_skill_key") or "").strip()
    if not pub:
        pub = pub_key_fm
    # 调用远端：优先 original_skill_key；再回退旧包仅含 skill_key
    sk = original if original else pub
    if not sk:
        print(
            "错误: 缺少远端技能标识。请使用服务端封装生成的技能包（脚本内已写入 _ENCAPSULATION_EMBEDDED），"
            "或为旧版包在 SKILL.md frontmatter 中保留 original_skill_key / skill_key。",
            file=sys.stderr,
        )
        sys.exit(1)
    sip = ""
    for key in ("input_format", "input_schema", "params"):
        v = frontmatter.get(key)
        if v is not None and str(v).strip():
            sip = str(v).strip()[:16000]
            break
    if not sip:
        d = frontmatter.get("description")
        if d is not None and str(d).strip():
            sip = str(d).strip()[:8000]
    enc = _normalize_encapsulation_target(
        str((runtime or {}).get("encapsulation_target") or frontmatter.get("encapsulation_target") or "")
    )
    return {"skill_key": sk, "skill_invocation_params": sip, "encapsulation_target": enc}


def _parse_credentials_json(text: str) -> Optional[Tuple[str, str]]:
    """解析 GET /api/v1/api-keys/ 完整响应，或仅含 public_key / secret_key 的 JSON。"""
    t = text.strip()
    if not t.startswith("{"):
        return None
    try:
        obj = json.loads(t)
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict):
        return None
    data = obj.get("data")
    ak = None
    if isinstance(data, dict):
        ak = data.get("api_key")
    if isinstance(ak, dict) and ak.get("public_key") and ak.get("secret_key"):
        return str(ak["public_key"]).strip(), str(ak["secret_key"]).strip()
    ak = obj.get("api_key")
    if isinstance(ak, dict) and ak.get("public_key") and ak.get("secret_key"):
        return str(ak["public_key"]).strip(), str(ak["secret_key"]).strip()
    if obj.get("public_key") and obj.get("secret_key"):
        return str(obj["public_key"]).strip(), str(obj["secret_key"]).strip()
    return None


def _parse_credentials_line(line: str) -> Optional[Tuple[str, str]]:
    """单行 public_key:secret_key（取首个冒号分割，避免密钥中含冒号时误拆）。"""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if ":" not in line:
        return None
    pub, _, sec = line.partition(":")
    pub, sec = pub.strip(), sec.strip()
    if pub and sec:
        return pub, sec
    return None


def _headers_x_api_key(public_key: str, secret_key: str) -> dict[str, str]:
    """Claw 接口要求：x-api-key 为 public_key:secret_key。"""
    return {
        "Content-Type": "application/json",
        "x-api-key": f"{public_key}:{secret_key}",
    }


def _encapsulation_target_for_api_keys_request() -> str:
    """
    GET /api/v1/api-keys 的 target_system：环境变量优先，否则本脚本内嵌字段，再 SKILL.md，默认 prana。
    非 prana 平台不应带 account_id（由服务端忽略误传的 account_id）。
    """
    v = (
        os.environ.get("ENCAPSULATION_TARGET")
        or os.environ.get("SKILL_ENCAPSULATION_TARGET")
        or os.environ.get("PRANA_ENCAPSULATION_TARGET")
        or ""
    ).strip()
    if v:
        return _normalize_encapsulation_target(v)
    rt = _load_encapsulation_runtime()
    if rt and str(rt.get("encapsulation_target") or "").strip():
        return _normalize_encapsulation_target(str(rt.get("encapsulation_target") or ""))
    if SKILL_MD_FILE.exists():
        try:
            raw = SKILL_MD_FILE.read_text(encoding="utf-8")
            fm, _ = _extract_frontmatter(raw)
            if fm:
                return _normalize_encapsulation_target(str(fm.get("encapsulation_target") or ""))
        except OSError:
            pass
    return "prana"


def _build_api_keys_fetch_url(base_url: str) -> str:
    """
    组装 GET /api/v1/api-keys 完整 URL。
    始终传 target_system；仅 platform=prana 时附加 account_id（ACCOUNT_ID / PRANA_ACCOUNT_ID）。
    """
    root = base_url.rstrip("/")
    path = f"{root}/api/v1/api-keys"
    q: Dict[str, str] = {}
    ts = _encapsulation_target_for_api_keys_request()
    q["target_system"] = ts
    if ts == "prana":
        aid = (os.environ.get("ACCOUNT_ID") or os.environ.get("PRANA_ACCOUNT_ID") or "").strip()
        if aid:
            q["account_id"] = aid
    if q:
        path = f"{path}?{urlencode(q)}"
    return path


def fetch_prana_api_keys_via_get(base_url: str) -> Optional[Tuple[str, str]]:
    """
    调用 Prana GET /api/v1/api-keys（无需 JWT），解析 data.api_key 的 public_key、secret_key。
    """
    url = _build_api_keys_fetch_url(base_url)
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=API_KEYS_FETCH_TIMEOUT_SEC) as resp:
            text = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(
            f"错误: 自动获取 API key 失败（HTTP {e.code}）：{err[:2000]}",
            file=sys.stderr,
        )
        return None
    except urllib.error.URLError as e:
        print(f"错误: 自动获取 API key 失败（网络）：{e.reason}", file=sys.stderr)
        return None
    except TimeoutError:
        print("错误: 自动获取 API key 超时。", file=sys.stderr)
        return None
    parsed = _parse_credentials_json(text)
    if not parsed:
        print(
            "错误: 自动获取 API key 成功但响应无法解析出 public_key/secret_key。",
            file=sys.stderr,
        )
        return None
    return parsed


def _persist_fetched_api_key_txt(public_key: str, secret_key: str) -> None:
    """将 public_key:secret_key 写入 config/api_key.txt（首行为注释，与现有读取逻辑兼容）。"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Auto-saved by prana_skill_client after GET /api/v1/api-keys; do not commit to public repos.",
        f"{public_key}:{secret_key}",
        "",
    ]
    API_KEY_FILE.write_text("\n".join(lines), encoding="utf-8")


def load_prana_credentials(prana_base_url: Optional[str] = None) -> Tuple[str, str]:
    """
    从环境变量或配置文件读取 public_key、secret_key（来自 GET /api/v1/api-keys 返回的 data.api_key）。
    自动拉取时带 target_system（脚本内嵌、SKILL.md 或 ENCAPSULATION_TARGET）；仅 prana 时附加 account_id（ACCOUNT_ID）。
    若以上皆无且未禁止自动拉取，则发起 GET /api/v1/api-keys（见 _build_api_keys_fetch_url）。
    优先级：
      PRANA_SKILL_PUBLIC_KEY + PRANA_SKILL_SECRET_KEY
      PRANA_SKILL_API_KEY（整段 JSON，或单行 public_key:secret_key）
      config/api_key.txt（单行 public_key:secret_key，或粘贴整段 JSON）
      GET /api/v1/api-keys（需可达的 base_url；成功后默认写入 config/api_key.txt）
    """
    pk = os.environ.get("PRANA_SKILL_PUBLIC_KEY", "").strip()
    sk = os.environ.get("PRANA_SKILL_SECRET_KEY", "").strip()
    if pk and sk:
        return pk, sk

    raw = os.environ.get("PRANA_SKILL_API_KEY", "").strip()
    if raw:
        parsed = _parse_credentials_json(raw)
        if parsed:
            return parsed
        p = _parse_credentials_line(raw)
        if p:
            return p

    if API_KEY_FILE.exists():
        txt = API_KEY_FILE.read_text(encoding="utf-8")
        lines = [ln for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith("#")]
        joined = "\n".join(lines).strip()
        if joined:
            parsed = _parse_credentials_json(joined)
            if parsed:
                return parsed
            for line in lines:
                p = _parse_credentials_line(line)
                if p:
                    return p

    base = (prana_base_url or os.environ.get("NEXT_PUBLIC_URL") or DEFAULT_PRANA_BASE or "").strip()
    if base and not _auto_fetch_api_key_disabled():
        fetched = fetch_prana_api_keys_via_get(base)
        if fetched:
            pub, sec = fetched
            if not _skip_write_fetched_api_key():
                try:
                    _persist_fetched_api_key_txt(pub, sec)
                except OSError as e:
                    print(f"警告: 无法写入 config/api_key.txt：{e}", file=sys.stderr)
            return pub, sec

    print(
        "错误: 未配置 API 凭证（public_key + secret_key），且自动 GET /api/v1/api-keys 失败或未启用。\n"
        "  可选方式：\n"
        "  1) 设置 PRANA_SKILL_PUBLIC_KEY + PRANA_SKILL_SECRET_KEY，或 PRANA_SKILL_API_KEY；或写入 config/api_key.txt。\n"
        "  2) 保证 --base-url（或 NEXT_PUBLIC_URL）可访问，并确保未设置 PRANA_SKILL_NO_AUTO_API_KEY；"
        "请求会带 target_system；仅 prana 时可设 ACCOUNT_ID；成功后默认写入 config/api_key.txt（"
        "若不想写盘可设 PRANA_SKILL_SKIP_WRITE_API_KEY=1）。",
        file=sys.stderr,
    )
    sys.exit(2)


def build_invoke_content(cfg: dict, user_message: str) -> str:
    """
    组装请求 question：参数说明 + 用户消息。
    skill_key 来自 SKILL.md frontmatter，由调用方单独传入 HTTP body。
    """
    params_from_skill = (cfg.get("skill_invocation_params") or "").strip()
    lines = [
        f"参数：{params_from_skill}",
        f"用户消息：{user_message}",
    ]
    return "\n".join(lines)


def fetch_agent_result(
    base_url: str,
    request_id: str,
    public_key: str,
    secret_key: str,
) -> dict:
    """
    当 agent-run 超时或失败时，用同一 request_id 查询运行结果。
    POST /api/claw/agent-result  body: request_id（鉴权见 x-api-key）
    Header: x-api-key: public_key:secret_key
    """
    url = base_url.rstrip("/") + "/api/claw/agent-result"
    body = {"request_id": request_id}
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers=_headers_x_api_key(public_key, secret_key),
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(err_body)
        except json.JSONDecodeError:
            return {
                "error": True,
                "status": e.code,
                "detail": err_body,
                "_from": "agent-result",
            }
    except urllib.error.URLError as e:
        return {"error": True, "detail": str(e.reason), "_from": "agent-result"}


def _agent_result_payload_still_running(payload: dict) -> bool:
    """Claw 返回 data.status == running 时继续轮询。"""
    if payload.get("error") is True:
        return False
    data = payload.get("data")
    if not isinstance(data, dict):
        return False
    return str(data.get("status") or "").strip().lower() == "running"


def _poll_agent_result_until_settled(
    base_url: str,
    request_id: str,
    public_key: str,
    secret_key: str,
    *,
    trigger_reason: str = "需通过 agent-result 拉取结果",
) -> dict:
    """
    每隔 AGENT_RESULT_POLL_INTERVAL_SEC 秒请求一次 POST /api/claw/agent-result，
    直至 data.status 不为 running（或响应不含 running）、或达到最大次数。
    首次请求前也会先等待一个间隔（agent-run 刚返回非 JSON 时任务往往尚未写入结果）。
    """
    interval = max(1, AGENT_RESULT_POLL_INTERVAL_SEC)
    max_attempts = max(1, AGENT_RESULT_POLL_MAX_ATTEMPTS)
    last: dict = {}
    for attempt in range(1, max_attempts + 1):
        if attempt == 1:
            print(
                f"提示: {trigger_reason}，{interval} 秒后首次 POST /api/claw/agent-result … "
                f"(request_id={request_id}, 最多 {max_attempts} 次，每 {interval}s)",
                file=sys.stderr,
            )
        else:
            print(
                f"提示: 第 {attempt} 次查询 agent-result（间隔 {interval}s）…",
                file=sys.stderr,
            )
        time.sleep(interval)
        last = fetch_agent_result(base_url, request_id, public_key, secret_key)
        if _agent_result_payload_still_running(last):
            continue
        return _mark_recovered(last)

    print(
        f"警告: agent-result 已轮询 {max_attempts} 次仍未结束，返回最后一次响应。",
        file=sys.stderr,
    )
    return _mark_recovered(last)


def _mark_recovered(d: dict) -> dict:
    d = dict(d)
    d["_recovered_via"] = "agent-result"
    return d


def invoke_prana(
    base_url: str,
    skill_key: str,
    content: str,
    thread_id: str | None,
    request_id: str,
    public_key: str,
    secret_key: str,
) -> dict:
    """
    调用 Prana 技能执行接口。
    body: skill_key, question, thread_id, request_id（不含 api_key）
    Header: x-api-key: public_key:secret_key
    若 HTTP 超时、连接失败，或网关类错误（5xx / 408 / 504），或 200 但响应非合法 JSON，则改调 agent-result：
    自首次查询起按 AGENT_RESULT_POLL_INTERVAL_SEC（默认 120s）间隔轮询，直至非 running 或达上限。
    """
    url = base_url.rstrip("/") + "/api/claw/agent-run"
    body = {
        "skill_key": skill_key,
        "question": content,
        "thread_id": thread_id or "",
        "request_id": request_id,
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers=_headers_x_api_key(public_key, secret_key),
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except json.JSONDecodeError:
        return _poll_agent_result_until_settled(
            base_url,
            request_id,
            public_key,
            secret_key,
            trigger_reason="agent-run 响应非合法 JSON",
        )
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        # 网关/服务端错误或超时类状态：任务可能已在服务端执行，改查 agent-result
        if e.code >= 500 or e.code in (408, 504):
            return _poll_agent_result_until_settled(
                base_url,
                request_id,
                public_key,
                secret_key,
                trigger_reason=f"agent-run HTTP {e.code}，改查 agent-result",
            )
        try:
            return json.loads(err_body)
        except json.JSONDecodeError:
            return {"error": True, "status": e.code, "detail": err_body}
    except urllib.error.URLError:
        # 含连接失败、DNS、超时等
        return _poll_agent_result_until_settled(
            base_url,
            request_id,
            public_key,
            secret_key,
            trigger_reason="agent-run 网络异常",
        )
    except TimeoutError:
        return _poll_agent_result_until_settled(
            base_url,
            request_id,
            public_key,
            secret_key,
            trigger_reason="agent-run 超时",
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 Prana 远程技能服务")
    parser.add_argument("--message", "-m", required=True, help="用户消息 / 任务描述")
    parser.add_argument("--thread-id", "-t", default="", help="对话 thread_id，首轮可留空")
    parser.add_argument("--base-url", "-b", default=DEFAULT_PRANA_BASE, help="Prana API 根地址")
    args = parser.parse_args()

    cfg = load_skill_config()
    skill_key = cfg.get("skill_key") or ""
    if not skill_key:
        print(
            "错误: 配置中缺少远端 skill_key（请检查脚本内 _ENCAPSULATION_EMBEDDED 或旧版 SKILL.md）",
            file=sys.stderr,
        )
        sys.exit(1)

    public_key, secret_key = load_prana_credentials(args.base_url)
    request_id = str(uuid.uuid4())
    content = build_invoke_content(cfg, args.message)
    result = invoke_prana(
        args.base_url,
        skill_key,
        content,
        args.thread_id or None,
        request_id,
        public_key,
        secret_key,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
