#!/usr/bin/env python3
"""
submit_script_review.py
DeepSOP 场景+TTS+机器人设定 一站式创建/审核脚本。

UTF-8 安全 + pre-flight 校验 + HTTP 提交 + 阿里云审核状态轮询。

调用方式（必须 heredoc + 单引号定界符）:

  python3 scripts/submit_script_review.py <<'SCRIPT_BODY_EOF'
  {"agentParams": {...}, "scriptParams": {...}}
  SCRIPT_BODY_EOF

可选参数:
  --no-poll              提交后立即返回，不轮询审核状态
  --max-wait-seconds N   最长等待审核时间（默认 600s）
  --poll-interval N      轮询间隔秒数（默认 10s，对齐前端 Vue）
  --dry-run              只跑 pre-flight 校验

输出 stdout 单行 JSON。退出码:
  0 — 已 PUBLISHED
  1 — 校验失败
  2 — 网络/超时
  3 — 服务端非 2xx
  4 — 输入格式错误 / API key 缺失
  5 — 提交成功但审核未在 max-wait-seconds 内完成
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import api_paths  # noqa: E402
import validate_script_params as vsp  # noqa: E402


CREATE_URL = api_paths.build_url("outbound_create_or_modify_script")
DESCRIBE_URL = api_paths.build_url("outbound_describe_script")
GET_AGENT_PROFILE_URL = api_paths.build_url("outbound_get_agent_profile")
api_paths.assert_url_matches(CREATE_URL, "outbound_create_or_modify_script")
api_paths.assert_url_matches(DESCRIBE_URL, "outbound_describe_script")
api_paths.assert_url_matches(GET_AGENT_PROFILE_URL, "outbound_get_agent_profile")

HTTP_TIMEOUT_SEC = 30
DEFAULT_MAX_WAIT_SEC = 600
DEFAULT_POLL_INTERVAL_SEC = 10


def emit(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def read_body_text(args: argparse.Namespace) -> str:
    if args.file:
        path = Path(args.file)
        if not path.is_file():
            raise FileNotFoundError(f"--file 指定的文件不存在: {path}")
        return path.read_text(encoding="utf-8-sig")

    if sys.stdin.isatty():
        raise ValueError(
            "未通过 stdin 提供 body 数据。请使用 heredoc 或 --file。"
        )
    raw = sys.stdin.buffer.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        try:
            text = raw.decode("cp936")
            sys.stderr.write(
                "[submit_script_review] 警告：stdin 不是合法 UTF-8，已按 cp936 兜底解码。\n"
            )
            return text
        except UnicodeDecodeError:
            raise exc


def parse_body(raw: str) -> dict:
    raw = raw.strip()
    if not raw:
        raise ValueError("body 为空：请通过 stdin 或 --file 传入完整请求体 JSON")
    return json.loads(raw)


def http_post_json(url: str, body: dict, api_key: str) -> tuple[int, str]:
    """显式 UTF-8 字节体 + charset 头提交。"""
    body_bytes = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body_bytes,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "x-api-key": api_key,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
            status = resp.status
            data = resp.read()
    except urllib.error.HTTPError as e:
        status = e.code
        try:
            data = e.read()
        except Exception:
            data = b""
    text = data.decode("utf-8", errors="replace")
    return status, text


def extract_create_response(resp_json: Any) -> dict:
    """
    阿里云审核接口返回结构假设:
      {"code":200, "data":{"scriptId":"...", "agentProfileId":"..."}, "msg":"..."}
    若实际返回结构不同，仍尽量从 data / data.script / 顶层兜底取值。
    """
    out: dict[str, Any] = {"raw": resp_json}
    if not isinstance(resp_json, dict):
        return out
    data = resp_json.get("data")
    candidates: list[Any] = []
    if isinstance(data, dict):
        candidates.append(data)
        # 兜底：data.body.script（与 describeScript 同结构）
        body = data.get("body")
        if isinstance(body, dict):
            candidates.append(body)
            script = body.get("script")
            if isinstance(script, dict):
                candidates.append(script)
    candidates.append(resp_json)

    for c in candidates:
        if not isinstance(c, dict):
            continue
        if "scriptId" not in out and isinstance(c.get("scriptId"), str):
            out["scriptId"] = c["scriptId"]
        if "agentProfileId" not in out and isinstance(c.get("agentProfileId"), str):
            out["agentProfileId"] = c["agentProfileId"]
    return out


def extract_describe_status(resp_json: Any) -> str | None:
    """
    describeScript 返回 {"data":{"body":{"script":{"status": "...", ...}}}, "code":200}
    返回 status 字符串（如 PUBLISHED / TO_BE_REVIEWED / FAIL_REVIEW），异常时返回 None。
    """
    if not isinstance(resp_json, dict):
        return None
    data = resp_json.get("data") or {}
    body = data.get("body") if isinstance(data, dict) else None
    script = body.get("script") if isinstance(body, dict) else None
    status = script.get("status") if isinstance(script, dict) else None
    if isinstance(status, str):
        return status
    return None


def find_agent_profile_node(value: Any) -> dict | None:
    if not isinstance(value, dict):
        return None
    for key in ("agentProfile", "agentProfileInfo", "profile"):
        node = value.get(key)
        if isinstance(node, dict) and "promptJson" in node:
            return node
    if "promptJson" in value:
        return value
    data = value.get("data")
    if isinstance(data, dict):
        found = find_agent_profile_node(data)
        if found is not None:
            return found
    body = value.get("body")
    if isinstance(body, dict):
        found = find_agent_profile_node(body)
        if found is not None:
            return found
    return None


def validate_agent_profile_prompt_response(resp_json: Any) -> dict:
    profile = find_agent_profile_node(resp_json)
    if profile is None:
        return {
            "ok": False,
            "stage": "agent_profile",
            "summary": "getAgentProfile 响应中未找到 agentProfile.promptJson，无法确认机器人 prompt 是否已落库",
            "response": resp_json,
        }

    prompt_raw = profile.get("promptJson")
    if isinstance(prompt_raw, str):
        text = prompt_raw.strip()
        if not text:
            prompt = {}
        else:
            try:
                prompt = json.loads(text)
            except json.JSONDecodeError as exc:
                return {
                    "ok": False,
                    "stage": "agent_profile",
                    "summary": f"getAgentProfile 返回的 promptJson 不是合法 JSON 字符串：{exc}",
                    "response": resp_json,
                }
    elif isinstance(prompt_raw, dict):
        prompt = prompt_raw
    else:
        prompt = {}

    missing = []
    for key in ("openingPrompt", "goals"):
        value = prompt.get(key) if isinstance(prompt, dict) else None
        if not isinstance(value, str) or not value.strip():
            missing.append(key)

    if missing:
        return {
            "ok": False,
            "stage": "agent_profile",
            "summary": f"场景已 PUBLISHED，但 getAgentProfile 返回的 promptJson 为空或缺少必填内容：{', '.join(missing)}",
            "response": resp_json,
        }

    return {
        "ok": True,
        "stage": "agent_profile",
        "summary": "getAgentProfile 已确认 promptJson 包含 openingPrompt/goals",
    }


def verify_agent_profile_prompt(agent_profile_id: str, api_key: str) -> dict:
    try:
        status, resp_text = http_post_json(
            GET_AGENT_PROFILE_URL,
            {"agentProfileId": agent_profile_id},
            api_key,
        )
    except (urllib.error.URLError, OSError) as exc:
        return {
            "ok": False,
            "stage": "agent_profile",
            "summary": f"查询 getAgentProfile 时网络失败：{exc}",
            "agentProfileId": agent_profile_id,
        }

    try:
        resp_json = json.loads(resp_text) if resp_text else None
    except json.JSONDecodeError:
        resp_json = None

    if not (200 <= status < 300):
        return {
            "ok": False,
            "stage": "agent_profile",
            "status_code": status,
            "summary": f"查询 getAgentProfile 时服务端返回 HTTP {status}",
            "agentProfileId": agent_profile_id,
            "response": resp_json if resp_json is not None else resp_text,
        }

    result = validate_agent_profile_prompt_response(resp_json)
    result.setdefault("agentProfileId", agent_profile_id)
    return result


def poll_describe_until_published(
    script_id: str,
    api_key: str,
    *,
    max_wait_seconds: int,
    poll_interval: int,
) -> dict:
    """
    轮询 describeScript 直至 status === 'PUBLISHED' 或超时。
    返回 {ok, status, elapsed_seconds, last_response}。
    """
    deadline = time.time() + max_wait_seconds
    last_status: str | None = None
    last_resp_json: Any = None
    last_resp_text: str = ""

    while True:
        body = {"scriptId": script_id}
        try:
            status, resp_text = http_post_json(DESCRIBE_URL, body, api_key)
        except (urllib.error.URLError, OSError) as exc:
            return {
                "ok": False,
                "stage": "polling",
                "summary": f"轮询审核状态时网络失败：{exc}",
                "scriptId": script_id,
                "status": last_status,
                "elapsed_seconds": int(time.time() - (deadline - max_wait_seconds)),
            }

        last_resp_text = resp_text
        try:
            last_resp_json = json.loads(resp_text) if resp_text else None
        except json.JSONDecodeError:
            last_resp_json = None

        # describeScript 接口本身可能是 200 但内部 code 非 200，做一次浅检查
        if not (200 <= status < 300):
            return {
                "ok": False,
                "stage": "polling",
                "status_code": status,
                "summary": f"轮询时服务端返回 HTTP {status}",
                "response": last_resp_json if last_resp_json is not None else last_resp_text,
                "scriptId": script_id,
                "status": last_status,
            }

        cur_status = extract_describe_status(last_resp_json)
        if cur_status is not None:
            last_status = cur_status
            if cur_status == "PUBLISHED":
                return {
                    "ok": True,
                    "stage": "done",
                    "scriptId": script_id,
                    "status": "PUBLISHED",
                    "summary": "场景已通过阿里云审核（PUBLISHED）",
                    "elapsed_seconds": int(time.time() - (deadline - max_wait_seconds)),
                }
            if cur_status in {"FAIL_REVIEW", "REJECT", "FAILED"}:
                return {
                    "ok": False,
                    "stage": "polling",
                    "scriptId": script_id,
                    "status": cur_status,
                    "summary": f"阿里云审核未通过（status={cur_status}），请检查 prompt/敏感词后重新提交",
                    "response": last_resp_json,
                }

        if time.time() >= deadline:
            return {
                "ok": False,
                "stage": "polling",
                "scriptId": script_id,
                "status": last_status or "UNKNOWN",
                "summary": (
                    f"审核未在 {max_wait_seconds}s 内完成，最后状态={last_status or 'UNKNOWN'}。"
                    f"可在用户确认后告诉我「再查一次场景审核 scriptId={script_id}」。"
                ),
                "response": last_resp_json,
            }

        time.sleep(poll_interval)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="DeepSOP 场景+TTS+机器人设定 创建/审核（UTF-8 安全 + 轮询）",
    )
    parser.add_argument("--file", help="从 UTF-8 文件读取 body（替代 stdin）")
    parser.add_argument("--dry-run", action="store_true", help="只跑 pre-flight 校验")
    parser.add_argument("--no-poll", action="store_true", help="提交后立即返回，不轮询审核")
    parser.add_argument(
        "--max-wait-seconds",
        type=int,
        default=DEFAULT_MAX_WAIT_SEC,
        help=f"最长等待审核秒数（默认 {DEFAULT_MAX_WAIT_SEC}s）",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=DEFAULT_POLL_INTERVAL_SEC,
        help=f"轮询间隔秒数（默认 {DEFAULT_POLL_INTERVAL_SEC}s）",
    )
    args = parser.parse_args()

    # 读 body
    try:
        raw = read_body_text(args)
    except (FileNotFoundError, ValueError, UnicodeDecodeError) as exc:
        emit({"ok": False, "stage": "validate", "summary": str(exc)})
        return 4

    try:
        body = parse_body(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        emit({
            "ok": False,
            "stage": "validate",
            "summary": f"body JSON 解析失败：{exc}",
        })
        return 4

    # Pre-flight 校验
    result = vsp.run(body)
    if not result["ok"]:
        emit({
            "ok": False,
            "stage": "validate",
            "summary": result["summary"],
            "errors": result["errors"],
        })
        return 1

    if args.dry_run:
        emit({
            "ok": True,
            "stage": "validate",
            "summary": "校验全部通过（--dry-run 跳过 HTTP 提交）",
        })
        return 0

    # API Key
    api_key = os.environ.get("DEEPSOP_API_KEY", "").strip()
    if not api_key:
        emit({
            "ok": False,
            "stage": "validate",
            "summary": "环境变量 DEEPSOP_API_KEY 未设置，无法提交",
        })
        return 4

    # HTTP 提交
    submit_started_at = time.time()
    try:
        status, resp_text = http_post_json(CREATE_URL, body, api_key)
    except (urllib.error.URLError, OSError) as exc:
        emit({
            "ok": False,
            "stage": "http",
            "summary": f"HTTP 请求失败（网络/超时）：{exc}",
        })
        return 2

    try:
        resp_json = json.loads(resp_text) if resp_text else None
    except json.JSONDecodeError:
        resp_json = None

    if not (200 <= status < 300):
        emit({
            "ok": False,
            "stage": "http",
            "status": status,
            "summary": f"服务端返回 HTTP {status}",
            "response": resp_json if resp_json is not None else resp_text,
        })
        return 3

    extracted = extract_create_response(resp_json)
    script_id = extracted.get("scriptId")
    agent_profile_id = extracted.get("agentProfileId")

    if not script_id:
        emit({
            "ok": False,
            "stage": "http",
            "status": status,
            "summary": (
                "提交成功但响应中未解析到 scriptId（response 已附），"
                "请人工检查接口响应结构是否变化"
            ),
            "response": resp_json if resp_json is not None else resp_text,
        })
        return 3

    if args.no_poll:
        emit({
            "ok": True,
            "stage": "submitted",
            "scriptId": script_id,
            "agentProfileId": agent_profile_id,
            "summary": (
                "已提交，未轮询审核（--no-poll）。"
                "继续前请确认 status === 'PUBLISHED'。"
            ),
            "response": resp_json,
        })
        return 0

    # 轮询审核
    poll_result = poll_describe_until_published(
        script_id,
        api_key,
        max_wait_seconds=args.max_wait_seconds,
        poll_interval=args.poll_interval,
    )
    poll_result.setdefault("agentProfileId", agent_profile_id)
    poll_result.setdefault("submit_response", resp_json)
    if "elapsed_seconds" not in poll_result:
        poll_result["elapsed_seconds"] = int(time.time() - submit_started_at)

    if poll_result.get("ok"):
        if not agent_profile_id:
            poll_result = {
                "ok": False,
                "stage": "agent_profile",
                "scriptId": script_id,
                "status": poll_result.get("status"),
                "summary": "场景已 PUBLISHED，但提交响应中没有 agentProfileId，无法校验机器人 promptJson 是否已落库",
                "submit_response": resp_json,
            }
        else:
            profile_result = verify_agent_profile_prompt(agent_profile_id, api_key)
            if not profile_result.get("ok"):
                profile_result.setdefault("scriptId", script_id)
                profile_result.setdefault("status", poll_result.get("status"))
                profile_result.setdefault("submit_response", resp_json)
                poll_result = profile_result
            else:
                poll_result["agent_profile_check"] = profile_result["summary"]

    emit(poll_result)

    if poll_result.get("ok"):
        return 0
    if poll_result.get("status") in {"FAIL_REVIEW", "REJECT", "FAILED"}:
        return 3
    return 5


if __name__ == "__main__":
    sys.exit(main())
