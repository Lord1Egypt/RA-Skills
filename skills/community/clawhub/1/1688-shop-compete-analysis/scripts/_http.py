#!/usr/bin/env python3
"""
MCP 工具调用传输层

职责：通过 `accio-mcp-cli` 调用已注册的 MCP 工具，统一解包
「MCP CallToolResult 信封 → 业务信封 {success,data,msgInfo} → data」，并做错误映射。

改造依据《Newton 技能迁移改造技术方案·三、方式 2》：
- 在 python 脚本里编排 `accio-mcp-cli`，**不直接调用 /mcp/proxy**；
- **不再使用 requests**（客户端未安装），改用标准库 subprocess；
- 鉴权与商家身份由本地网关登录态自动注入，**不再需要 AK / HMAC 签名 / userId**。

对上层保持与旧 `api_post` 一致的返回契约：成功返回业务 `data`，
失败抛 AuthError / ParamError / RateLimitError / ServiceError。
"""

import json
import re
import shutil
import subprocess
import time

from _errors import AuthError, ParamError, RateLimitError, ServiceError

CLI_NAME = "accio-mcp-cli"
DEFAULT_TIMEOUT = 90

# 传输层可重试错误（网关未就绪 / 超时 / 5xx），指数退避后重发
_MAX_RETRIES = 2
_RETRY_DELAY_BASE = 0.2
_RETRY_MAX_DELAY = 1.0

# 命中以下标记时，错误文本完整保留、禁止截断
# （CONNECTOR_AUTH_REQUIRED / ask_user 是网关要求用户授权的指令，截断会导致 Agent 无法执行）
_PRESERVE_MARKERS = ("connector_auth_required", "ask_user", "auth_required")


class _Retryable(Exception):
    """标记传输层可重试错误。"""


def _resolve_cli() -> str:
    executable = shutil.which(CLI_NAME)
    if not executable:
        raise AuthError(
            "accio-mcp-cli 不可用：请在 Accio Desktop 环境内运行"
            "（本地网关未就绪或未登录）"
        )
    return executable


def _brief(text: str, limit: int = 500) -> str:
    """错误文本裁剪；命中授权/ask_user 标记时完整保留，禁止截断。"""
    if not text:
        return ""
    lowered = text.lower()
    if any(marker in lowered for marker in _PRESERVE_MARKERS):
        return text
    return text if len(text) <= limit else text[:limit]


def _map_cli_error(text: str):
    """把 CLI 退出码非 0 的 stderr/stdout 归类为 SkillError / _Retryable。"""
    lowered = (text or "").lower()
    if "unknown tool" in lowered or "not registered" in lowered:
        return ServiceError(f"MCP 工具未注册或名称错误：{_brief(text)}")
    if any(k in lowered for k in ("connector_auth_required", "ask_user", "auth_required",
                                  "unauthorized", "401", "403", "token", "鉴权", "登录")):
        return AuthError(_brief(text) or "本地网关鉴权失败或登录态失效")
    # 登录态失效时网关会把请求 302 跳到平台错误页（实测
    # "Redirect 302 -> https://err.taobao.com/error2.html"）。原文只有一个跳转地址、
    # 不含任何鉴权关键词，旧逻辑会落到末尾的 ServiceError，把裸 URL 吐给商家。
    # 这类重定向应归为鉴权失效，提示重新登录。
    if "redirect" in lowered and re.search(r"\b30[12378]\b", lowered):
        return AuthError("平台登录态已失效（接口被重定向到错误页），请重新登录 1688 后重试")
    if "err.taobao.com" in lowered or "error2.html" in lowered:
        return AuthError("平台登录态已失效（接口返回平台错误页），请重新登录 1688 后重试")
    if "429" in lowered or "rate limit" in lowered or "限流" in (text or ""):
        return RateLimitError(_brief(text) or "请求被限流（429），请稍后重试")
    if any(k in lowered for k in ("connection refused", "connect", "econnrefused",
                                  "no such file", "network", "temporarily", "502", "503", "504")):
        return _Retryable(text)
    if "timeout" in lowered or "timed out" in lowered:
        return _Retryable(text)
    return ServiceError(_brief(text) or "MCP 调用失败")


def _run_cli_once(executable: str, tool_name: str, arguments: dict, timeout: int) -> str:
    """执行一次 `accio-mcp-cli call <tool> --json <args> --raw`，返回 stdout 原文。"""
    cmd = [
        executable, "call", tool_name,
        "--json", json.dumps(arguments or {}, ensure_ascii=False),
        "--raw",
    ]
    try:
        proc = subprocess.run(
            cmd,
            shell=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        raise _Retryable(f"调用 {tool_name} 超时（{timeout}s）")

    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    if proc.returncode != 0:
        raise _map_cli_error(stderr or stdout or f"{CLI_NAME} 退出码 {proc.returncode}")
    if not stdout:
        raise _Retryable(f"{tool_name} 返回空响应")
    return stdout


def _run_cli(tool_name: str, arguments: dict, timeout: int) -> str:
    """带指数退避重试的 CLI 调用：仅重试传输层可恢复错误。"""
    executable = _resolve_cli()
    last_exc = None
    delay = _RETRY_DELAY_BASE
    for attempt in range(_MAX_RETRIES + 1):
        if attempt:
            time.sleep(delay)
            delay = min(delay * 2, _RETRY_MAX_DELAY)
        try:
            return _run_cli_once(executable, tool_name, arguments, timeout)
        except _Retryable as e:
            last_exc = e
        except (AuthError, ParamError, RateLimitError, ServiceError):
            raise
    raise ServiceError(f"调用 {tool_name} 失败，已重试 {_MAX_RETRIES} 次：{_brief(str(last_exc))}")


def _join_text(content) -> str:
    """拼接 MCP content[] 中所有 type=text 片段。"""
    if not isinstance(content, list):
        return ""
    texts = []
    for item in content:
        if (isinstance(item, dict) and item.get("type") == "text"
                and isinstance(item.get("text"), str) and item["text"].strip()):
            texts.append(item["text"])
    return "\n".join(texts)


def _extract_business_json(stdout: str):
    """解开 `--raw` 的 MCP CallToolResult 信封，返回业务 JSON（dict / list / str）。

    兼容形态：顶层即业务对象、{result:{...}}、content[].text（业务 JSON 字符串）、
    structuredContent。isError=true 时按错误抛出（完整保留授权/ask_user 指令）。
    """
    try:
        result = json.loads(stdout)
    except (ValueError, TypeError):
        return stdout

    if isinstance(result, dict) and isinstance(result.get("result"), dict):
        result = result["result"]
    if not isinstance(result, dict):
        return result

    if result.get("isError") is True:
        text = _join_text(result.get("content"))
        raise _map_cli_error(text or json.dumps(result, ensure_ascii=False))

    if result.get("structuredContent") is not None:
        return result["structuredContent"]

    text = _join_text(result.get("content"))
    if text:
        try:
            return json.loads(text)
        except (ValueError, TypeError):
            return text
    return result


def _raise_biz_error(payload: dict):
    """业务信封 success=false → SkillError（沿用旧网关的 msgCode 归类）。"""
    msg_code = str(payload.get("msgCode") or "")
    msg_info = payload.get("msgInfo")
    code_match = re.search(r"\b(400|401|429|500)\b", msg_code)
    normalized = code_match.group(1) if code_match else ""

    if normalized == "401":
        raise AuthError("本地网关登录态失效或未授权（401）")
    if normalized == "429":
        raise RateLimitError("请求被限流（429），请稍后重试")
    if normalized == "400":
        raise ParamError("请求参数不合法（400）")
    if normalized == "500":
        raise ServiceError("服务异常（500），请稍后重试")

    detail = msg_info or msg_code or payload.get("message") or "未知业务错误"
    raise ServiceError(_brief(str(detail)))


def _handle_biz_envelope(payload):
    """业务信封 {success,data,msgInfo,errorMsg} → 返回 data。

    - success=false：映射为 SkillError；
    - success=true 且有 data：返回其 data 字段；
    - success=true 但**没有 data 键**：这是「查询成功但无数据」的信封，实测形如
      {"success":true,"msgInfo":"查询成功","errorMsg":"生意参谋数据回溯 2 天仍无数据,
      apiPath=flow/getShopKeyWordWithWeb"}。此时把 errorMsg 包成 {"errorMsg": ...}
      返回，供上层按 SKILL.md 解析规则⑧ 透传给用户，而不是静默返回空 dict
      让商家只看到「暂无数据」却不知道是平台侧回溯失败；
    - 非信封（工具直接返回最内层数据）：原样返回。
    """
    if isinstance(payload, dict) and "success" in payload:
        if payload.get("success") is False:
            _raise_biz_error(payload)
        if "data" not in payload:
            err = payload.get("errorMsg")
            if err:
                return {"errorMsg": err}
        return payload.get("data", {})
    return payload


def call_tool(tool_name: str, arguments: dict = None, timeout: int = DEFAULT_TIMEOUT):
    """调用一个 MCP 工具，返回业务 data。

    Args:
        tool_name:  MCP 工具名（见 _const，如 1688_query_shop_data）
        arguments:  工具入参 dict（如 {"dataSource","apiPath","params"}）
        timeout:    单次调用超时秒数

    Returns:
        业务 data（dict / list / str），等价于旧网关响应中的 data 字段

    Raises:
        AuthError / ParamError / RateLimitError / ServiceError
    """
    stdout = _run_cli(tool_name, arguments, timeout)
    payload = _extract_business_json(stdout)
    return _handle_biz_envelope(payload)
