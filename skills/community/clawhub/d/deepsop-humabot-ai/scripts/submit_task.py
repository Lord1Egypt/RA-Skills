#!/usr/bin/env python3
"""
submit_task.py
DeepSOP agentSubmitTask 一站式提交脚本：UTF-8 安全 + 双重 pre-flight 校验 + HTTP 提交。

为什么需要这个脚本（替代 LLM 直接写 curl）:
  - LLM 在 Windows bash 里写 `curl -d '{中文 JSON}'` 会触发 ANSI 代码页（cp936）
    与 UTF-8 之间的转码歧义，导致 taskName/taskDescription 提交后变成乱码。
  - 用本脚本后，body 通过 **stdin 字节流**进入 Python，统一按 UTF-8 解码；
    HTTP 请求体使用 `Content-Type: application/json; charset=utf-8` 显式声明编码，
    彻底闭合编码链路。

调用方式（SKILL.md Step 5 的"提交"环节固定使用此模板）:

  python3 scripts/submit_task.py <<'TASK_BODY_EOF'
  {
    "completed": true,
    "collaborationSubmitTaskParam": { ... }
  }
  TASK_BODY_EOF

也支持文件路径作为退路（当 bash 不支持 heredoc 时）:

  python3 scripts/submit_task.py --file /tmp/task_body.json

输出（stdout 单行 JSON）:
  {
    "ok": bool,
    "stage": "validate" | "http" | "done",
    "phase": "employee_params" | "sms_template" | null,
    "summary": "...",
    "status": int|null,
    "response": ...|null,
    "errors": [...]|null
  }

退出码:
  0 — 全流程成功（HTTP 2xx）
  1 — 校验阶段失败（结构 / 内容）
  2 — HTTP 请求失败（网络/超时/连接拒绝）
  3 — 服务端返回非 2xx
  4 — 输入格式错误（stdin 非 UTF-8 / JSON 不可解析 / API key 缺失）

依赖：仅 Python 标准库（urllib），不依赖 requests。
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 让本脚本可以 import 同目录下的两个 validator
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import validate_employee_params as vep  # noqa: E402
import validate_sms_template_params as vstp  # noqa: E402
import api_paths  # noqa: E402  —— SKILL.md「API 路径权威清单」的代码侧单一来源

import urllib.error  # noqa: E402
import urllib.request  # noqa: E402


# ⚠️ 强约束：本脚本提交任务的 URL 必须与 SKILL.md「API 路径权威清单」#2 一致；
# 不得在此文件硬编码 URL，任何路径变更只能在 api_paths.py 中改，并同步更新 SKILL.md。
API_URL = api_paths.build_url("preset_employee_submit_task")
api_paths.assert_url_matches(API_URL, "preset_employee_submit_task")
TIMEOUT_SEC = 30


def emit(payload: dict) -> None:
    """标准化输出：单行 JSON 到 stdout，不带 ANSI/控制字符。"""
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    sys.stdout.write("\n")
    sys.stdout.flush()


def read_body_text(args: argparse.Namespace) -> str:
    """
    从 stdin（首选）或 --file 路径读取 body 原文。
    强制按 UTF-8 解码 stdin 字节，规避 Windows cp936 默认值。
    """
    if args.file:
        path = Path(args.file)
        if not path.is_file():
            raise FileNotFoundError(f"--file 指定的文件不存在: {path}")
        # 显式 UTF-8；BOM 也允许（utf-8-sig 在没有 BOM 时与 utf-8 等价）
        return path.read_text(encoding="utf-8-sig")

    # 走 stdin。读字节后手动 UTF-8 解码（避免 sys.stdin 的文本模式被宿主代码页污染）
    if sys.stdin.isatty():
        raise ValueError(
            "未通过 stdin 提供 body 数据。请使用 heredoc:\n"
            "  python3 scripts/submit_task.py <<'TASK_BODY_EOF'\n"
            "  { ...JSON... }\n"
            "  TASK_BODY_EOF\n"
            "或使用 --file <path> 指定 UTF-8 文件。"
        )
    raw = sys.stdin.buffer.read()
    # 去除可能的 UTF-8 BOM
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        # 兜底：尝试 cp936 解码（个别 Windows 环境下 LLM 输出会被 shell 重新编码）
        try:
            text = raw.decode("cp936")
            sys.stderr.write(
                "[submit_task] 警告：stdin 不是合法 UTF-8，已按 cp936 兜底解码。"
                "为避免乱码，请检查 LLM 输出端的编码是否锁定 UTF-8。\n"
            )
            return text
        except UnicodeDecodeError:
            raise exc


def parse_body(raw: str) -> dict:
    raw = raw.strip()
    if not raw:
        raise ValueError("body 为空：请通过 stdin 或 --file 传入完整请求体 JSON")
    return json.loads(raw)


def run_employee_params_check(body: dict) -> dict | None:
    """跑结构层校验。失败时返回 errors payload；成功返回 None。"""
    result = vep.run(body)
    if result["ok"]:
        return None
    return {
        "ok": False,
        "stage": "validate",
        "phase": "employee_params",
        "summary": result["summary"],
        "errors": result["errors"],
    }


def run_sms_template_check(body: dict) -> dict | None:
    """仅当 Lisa 存在且 templateParamList 非空时跑短信变量内容层校验。"""
    cstp = body.get("collaborationSubmitTaskParam") or {}
    ep = cstp.get("employeeParams") or {}
    lisa = ep.get("Lisa")
    if not isinstance(lisa, dict):
        return None
    tpl = lisa.get("templateParamList")
    if not (isinstance(tpl, list) and tpl):
        return None

    results = [vstp.validate_one(item) for item in tpl]
    fail_count = sum(1 for r in results if r.get("status") == "FAIL")
    if fail_count == 0:
        return None
    return {
        "ok": False,
        "stage": "validate",
        "phase": "sms_template",
        "summary": f"{fail_count}/{len(results)} 短信模板变量校验失败，禁止提交",
        "results": results,
    }


def post_task(body: dict, api_key: str) -> tuple[int, str]:
    """显式 UTF-8 字节体 + charset 头提交。返回 (status, response_text)。"""
    body_bytes = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body_bytes,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "x-api-key": api_key,
            # 一些反向代理依赖 Content-Length 而非 Transfer-Encoding，stdlib 会自填
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
            status = resp.status
            data = resp.read()
    except urllib.error.HTTPError as e:
        status = e.code
        try:
            data = e.read()
        except Exception:
            data = b""
    # 后端通常返回 UTF-8 JSON；兜底用 replace 防止脚本崩溃
    text = data.decode("utf-8", errors="replace")
    return status, text


def main() -> int:
    parser = argparse.ArgumentParser(
        description="DeepSOP agentSubmitTask 一站式提交（UTF-8 安全 + pre-flight）",
    )
    parser.add_argument(
        "--file",
        help="从 UTF-8 编码文件读取 body（不传则从 stdin 读取）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只跑校验，不发起 HTTP 请求（用于本地排查）",
    )
    args = parser.parse_args()

    # 读 body
    try:
        raw = read_body_text(args)
    except (FileNotFoundError, ValueError, UnicodeDecodeError) as exc:
        emit({"ok": False, "stage": "validate", "summary": str(exc)})
        return 4

    # 解析 JSON
    try:
        body = parse_body(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        emit({
            "ok": False,
            "stage": "validate",
            "summary": f"body JSON 解析失败：{exc}",
        })
        return 4

    # Pre-flight 1: 结构 / 取值
    err_payload = run_employee_params_check(body)
    if err_payload is not None:
        emit(err_payload)
        return 1

    # Pre-flight 2: 短信模板内容
    err_payload = run_sms_template_check(body)
    if err_payload is not None:
        emit(err_payload)
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
    try:
        status, resp_text = post_task(body, api_key)
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

    cstp = body.get("collaborationSubmitTaskParam") or {}
    body_preview = {
        "taskName": cstp.get("taskName"),
        "taskDescription_first_40": (cstp.get("taskDescription") or "")[:40],
        "employees": list((cstp.get("employeeParams") or {}).keys()),
    }

    if 200 <= status < 300:
        emit({
            "ok": True,
            "stage": "done",
            "status": status,
            "summary": f"任务已提交（HTTP {status}）",
            "response": resp_json if resp_json is not None else resp_text,
            "body_preview": body_preview,
        })
        return 0

    emit({
        "ok": False,
        "stage": "http",
        "status": status,
        "summary": f"服务端返回 HTTP {status}",
        "response": resp_json if resp_json is not None else resp_text,
        "body_preview": body_preview,
    })
    return 3


if __name__ == "__main__":
    sys.exit(main())
