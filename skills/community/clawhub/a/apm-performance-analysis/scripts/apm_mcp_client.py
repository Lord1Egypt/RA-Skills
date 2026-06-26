#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云 APM MCP 客户端（云API版 - 官方SDK）

通过腾讯云官方 SDK 的 ApmClient.SendMCPMessage 接口与 APM MCP Server 交互，
支持工具发现（tools/list）、工具调用（tools/call）和连通检测（ping）。

凭证配置：
    通过 shell 环境变量 TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY 配置，
    建议写入 ~/.zshrc 永久生效。凭证通过云API标准签名（TC3-HMAC-SHA256）自动鉴权。

Endpoint 配置：
    默认使用公网 apm.tencentcloudapi.com，
    可通过环境变量 APM_API_ENDPOINT 切换为内网地址。

依赖：
    使用内嵌（vendored）的腾讯云官方 SDK，无需 pip install 外部包。

用法示例:
    # 检测连通性
    python apm_mcp_client.py ping

    # 列出 MCP Server 提供的所有工具
    python apm_mcp_client.py list-tools

    # 调用指定工具
    python apm_mcp_client.py call-tool --name DescribeApmOverview --args '{"start_time":"1744786829","end_time":"1744787429","region":"ap-beijing"}'
"""

import argparse
import json
import logging
import os
import stat
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# 环境变量和日志
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent.resolve()

# 将 scripts/ 目录加入 sys.path，使内嵌的 tencentcloud 包可被导入
sys.path.insert(0, str(SCRIPT_DIR))

# 客户端 Region 固定为 ap-guangzhou
CLIENT_REGION = "ap-guangzhou"

# 默认公网 Endpoint
DEFAULT_ENDPOINT = "apm.tencentcloudapi.com"


def check_credentials():
    """检查腾讯云凭证环境变量是否已配置。返回 (secret_id, secret_key) 或 (None, None)。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    return secret_id, secret_key


def _get_log_dir():
    log_dir = os.environ.get("APM_ERROR_LOG_DIR")
    if log_dir:
        return os.path.abspath(log_dir)
    return os.path.join(os.getcwd(), "logs")


def _init_logger():
    logger = logging.getLogger("apm_ops")
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        log_dir = _get_log_dir()
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "apm_error.log")
        fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
        logger.addHandler(fh)
        try:
            os.chmod(log_file, stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass
    return logger


def log_error(action, error_code=None, error_message=None, request_id=None, extra=None):
    logger = _init_logger()
    entry = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "action": action, "error_code": error_code,
        "error_message": error_message, "request_id": request_id,
    }
    if extra:
        entry["extra"] = extra
    logger.error(json.dumps(entry, ensure_ascii=False))


def log_exception(action, exception, extra=None):
    logger = _init_logger()
    entry = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "action": action, "exception_type": type(exception).__name__,
        "exception_message": str(exception), "traceback": traceback.format_exc(),
    }
    if extra:
        entry["extra"] = extra
    logger.error(json.dumps(entry, ensure_ascii=False))


# ---------------------------------------------------------------------------
# SDK 导入（使用内嵌 vendored 官方 SDK）
# ---------------------------------------------------------------------------

try:
    from tencentcloud.common import credential
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.apm.v20210622.apm_client import ApmClient
    from tencentcloud.apm.v20210622.models import (
        SendMCPMessageRequest,
        SendMCPMessageResponse,
        APMKVItem,
    )
    SDK_AVAILABLE = True
except ImportError as e:
    SDK_AVAILABLE = False
    _SDK_IMPORT_ERROR = str(e)


def check_sdk():
    """检查内嵌 SDK 是否可正常导入。"""
    if not SDK_AVAILABLE:
        msg = f"内嵌官方 SDK 导入失败: {_SDK_IMPORT_ERROR}"
        log_error("check_sdk", error_code="SDK_IMPORT_ERROR", error_message=msg)
        print(f"错误: {msg}")
        print("请检查 scripts/tencentcloud/ 目录是否完整。")
        sys.exit(1)


# ---------------------------------------------------------------------------
# 客户端初始化
# ---------------------------------------------------------------------------

def create_client(cli_secret_id=None, cli_secret_key=None):
    """
    创建官方 ApmClient 实例。

    凭证优先级：
    1. 命令行参数 --secret-id / --secret-key
    2. 环境变量 TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY

    Returns:
        ApmClient 实例
    """
    check_sdk()

    secret_id = cli_secret_id or os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = cli_secret_key or os.environ.get("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        print(
            "错误: 未找到腾讯云凭证 (TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY)。\n"
            "请在终端执行以下命令配置凭证（永久生效）:\n"
            "\n"
            "  echo 'export TENCENTCLOUD_SECRET_ID=\"your-secret-id\"' >> ~/.zshrc\n"
            "  echo 'export TENCENTCLOUD_SECRET_KEY=\"your-secret-key\"' >> ~/.zshrc\n"
            "  source ~/.zshrc\n"
        )
        sys.exit(1)

    cred = credential.Credential(secret_id, secret_key)

    # 配置 Endpoint
    endpoint = os.environ.get("APM_API_ENDPOINT", DEFAULT_ENDPOINT)

    httpProfile = HttpProfile()
    httpProfile.endpoint = endpoint

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile

    client = ApmClient(cred, CLIENT_REGION, clientProfile)
    return client


# ---------------------------------------------------------------------------
# 核心操作
# ---------------------------------------------------------------------------

def send_mcp_message(client, method, tool_name=None, arguments=None):
    """
    调用 SendMCPMessage 接口。

    Args:
        client: ApmClient 实例
        method: "tools/list" | "tools/call" | "ping"
        tool_name: 工具名称（method 为 "tools/call" 时必填）
        arguments: 工具参数列表，APMKVItem 对象列表

    Returns:
        dict: 解析后的响应内容
    """
    req = SendMCPMessageRequest()
    req.Method = method

    if tool_name:
        req.ToolName = tool_name

    if arguments:
        req.Arguments = arguments

    try:
        resp = client.SendMCPMessage(req)

        # 官方 SDK 响应结构：resp.MCPMessage.Result（JSON 字符串）
        content = None
        if resp.MCPMessage and resp.MCPMessage.Result:
            content = resp.MCPMessage.Result

        result = {
            "request_id": resp.RequestId,
            "content": content,
        }

        # 尝试解析 Result 为 JSON
        if content:
            try:
                result["parsed_content"] = json.loads(content)
            except (json.JSONDecodeError, TypeError):
                result["parsed_content"] = content

        return {"success": True, **result}

    except TencentCloudSDKException as e:
        log_error(
            action=f"SendMCPMessage:{method}",
            error_code=e.code,
            error_message=e.message,
            request_id=e.requestId,
            extra={"method": method, "tool_name": tool_name},
        )
        return {
            "success": False,
            "error_code": e.code,
            "error_message": e.message,
            "request_id": e.requestId,
        }

    except Exception as e:
        log_exception(
            action=f"SendMCPMessage:{method}",
            exception=e,
            extra={"method": method, "tool_name": tool_name},
        )
        return {
            "success": False,
            "error_code": type(e).__name__,
            "error_message": str(e),
            "request_id": None,
        }


def list_tools(client):
    """
    列出 MCP Server 提供的所有工具。

    Returns:
        dict: 包含工具列表的结果
    """
    result = send_mcp_message(client, method="tools/list")

    if not result["success"]:
        return result

    # 解析工具列表
    parsed = result.get("parsed_content")
    if isinstance(parsed, dict) and "tools" in parsed:
        tools = parsed["tools"]
    elif isinstance(parsed, list):
        tools = parsed
    else:
        tools = parsed

    return {"success": True, "tools": tools, "request_id": result.get("request_id")}


def call_tool(client, tool_name, arguments=None):
    """
    调用指定 MCP 工具。

    Args:
        client: ApmClient 实例
        tool_name: 工具名称
        arguments: 参数字典 {"key": "value"}，内部自动转换为 APMKVItem 列表

    Returns:
        dict: 工具调用结果
    """
    # 将 dict 参数转换为官方 SDK 的 APMKVItem 对象列表
    kv_items = None
    if arguments:
        kv_items = []
        for k, v in arguments.items():
            item = APMKVItem()
            item.Key = str(k)
            item.Value = str(v)
            kv_items.append(item)

    result = send_mcp_message(client, method="tools/call", tool_name=tool_name, arguments=kv_items)

    if not result["success"]:
        return {
            "success": False,
            "content": f"调用工具 {tool_name} 失败: [{result.get('error_code')}] {result.get('error_message')}",
            "isError": True,
            "tool_name": tool_name,
            "arguments": arguments,
            "request_id": result.get("request_id"),
        }

    return {
        "success": True,
        "content": result.get("content", ""),
        "parsed_content": result.get("parsed_content"),
        "isError": False,
        "tool_name": tool_name,
        "arguments": arguments,
        "request_id": result.get("request_id"),
    }


def ping(client):
    """
    检测 MCP Server 连通性。

    Returns:
        dict: ping 结果
    """
    result = send_mcp_message(client, method="ping")
    return result


# ---------------------------------------------------------------------------
# 输出格式化
# ---------------------------------------------------------------------------

def _get_required_fields(schema):
    """从 JSON Schema 中提取必填字段列表。"""
    required = set()
    top_required = schema.get("required")
    if isinstance(top_required, (list, set)):
        required.update(top_required)

    properties = schema.get("properties", {})
    for param_name, param_info in properties.items():
        if isinstance(param_info, dict) and param_info.get("required") is True:
            required.add(param_name)

    return required


def format_tools_list(tools, output_format="table"):
    """格式化工具列表输出。"""
    if output_format == "json":
        print(json.dumps(tools, indent=2, ensure_ascii=False))
        return

    if not tools:
        print("MCP Server 未返回任何工具。")
        return

    tool_list = tools if isinstance(tools, list) else []
    print(f"MCP APM 工具列表 (共 {len(tool_list)} 个)")
    print("=" * 100)

    for i, tool in enumerate(tool_list, 1):
        name = tool.get("name", "N/A")
        desc = tool.get("description", "(无描述)")
        schema = tool.get("inputSchema", {})

        print(f"\n  [{i}] {name}")
        print(f"      描述: {desc}")

        properties = schema.get("properties", {})
        required = _get_required_fields(schema)

        if properties:
            print(f"      参数:")
            for param_name, param_info in properties.items():
                param_type = param_info.get("type", "any") if isinstance(param_info, dict) else "any"
                param_desc = param_info.get("description", "") if isinstance(param_info, dict) else ""
                is_required = "必填" if param_name in required else "可选"
                print(f"        - {param_name} ({param_type}, {is_required}): {param_desc}")
        else:
            print(f"      参数: 无")

    print("\n" + "=" * 100)


def format_tool_result(result, output_format="text"):
    """格式化工具调用结果输出。"""
    if output_format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    tool_name = result.get("tool_name", "N/A")
    success = result.get("success", False)
    content = result.get("content", "")
    is_error = result.get("isError", False)
    request_id = result.get("request_id", "N/A")

    status = "成功" if success else "失败"
    print(f"\n工具调用结果: {tool_name} [{status}]")
    print(f"RequestId: {request_id}")
    print("-" * 60)

    if is_error:
        log_dir = _get_log_dir()
        log_file = os.path.join(log_dir, "apm_error.log")
        print(f"错误: {content}")
        print(f"错误日志: {log_file}")
    else:
        # 优先使用 parsed_content
        parsed = result.get("parsed_content")
        if parsed and isinstance(parsed, (dict, list)):
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
        else:
            # 尝试美化 JSON 输出
            try:
                data = json.loads(content)
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except (json.JSONDecodeError, TypeError):
                print(content)

    print("-" * 60)


# ---------------------------------------------------------------------------
# 命令行入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="腾讯云 APM MCP 客户端（云API版 - 官方SDK）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "凭证配置:\n"
            "  通过 shell 环境变量 TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY 配置，\n"
            "  建议写入 ~/.zshrc 永久生效。\n"
            "\n"
            "Endpoint 配置:\n"
            "  默认公网: apm.tencentcloudapi.com\n"
            "  可通过环境变量 APM_API_ENDPOINT 切换（如内网: apm.ap-guangzhou.tencentcloudapi.woa.com）\n"
            "\n"
            "SDK:\n"
            "  使用内嵌（vendored）腾讯云官方 SDK，无需额外安装。\n"
            "\n"
            "错误日志:\n"
            "  默认写入 ./logs/apm_error.log\n"
        ),
    )

    parser.add_argument(
        "--secret-id",
        help="腾讯云 SecretId（覆盖环境变量 TENCENTCLOUD_SECRET_ID）",
    )
    parser.add_argument(
        "--secret-key",
        help="腾讯云 SecretKey（覆盖环境变量 TENCENTCLOUD_SECRET_KEY）",
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # ping
    subparsers.add_parser(
        "ping",
        help="检测 MCP Server 连通性",
    )

    # list-tools
    list_parser = subparsers.add_parser(
        "list-tools",
        help="列出 MCP Server 提供的所有工具",
    )
    list_parser.add_argument(
        "--output",
        choices=["table", "json"],
        default="table",
        help="输出格式，默认 table",
    )

    # call-tool
    call_parser = subparsers.add_parser(
        "call-tool",
        help="调用 MCP Server 的指定工具",
    )
    call_parser.add_argument(
        "--name",
        required=True,
        help="要调用的工具名称",
    )
    call_parser.add_argument(
        "--args",
        default="{}",
        help='工具参数（JSON 格式字符串），默认 {}',
    )
    call_parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="输出格式，默认 text",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 1. 初始化日志
    _init_logger()

    # 2. 创建客户端
    client = create_client(
        cli_secret_id=getattr(args, "secret_id", None),
        cli_secret_key=getattr(args, "secret_key", None),
    )

    # 3. 执行命令
    if args.command == "ping":
        result = ping(client)
        if result["success"]:
            print("MCP Server 连通性检测: 成功")
            print(f"RequestId: {result.get('request_id', 'N/A')}")
            if result.get("parsed_content"):
                print(json.dumps(result["parsed_content"], indent=2, ensure_ascii=False))
        else:
            print(f"MCP Server 连通性检测: 失败")
            print(f"错误码: {result.get('error_code')}")
            print(f"错误信息: {result.get('error_message')}")
            sys.exit(1)

    elif args.command == "list-tools":
        result = list_tools(client)
        if not result["success"]:
            log_dir = _get_log_dir()
            log_file = os.path.join(log_dir, "apm_error.log")
            print(f"获取工具列表失败: [{result.get('error_code')}] {result.get('error_message')}")
            print(f"错误日志: {log_file}")
            sys.exit(1)

        tools = result.get("tools", [])
        format_tools_list(tools, args.output)

    elif args.command == "call-tool":
        try:
            arguments = json.loads(args.args)
        except json.JSONDecodeError as e:
            print(f"参数 JSON 解析失败: {e}")
            print(f"请确保 --args 参数为有效的 JSON 字符串")
            sys.exit(1)

        result = call_tool(client, args.name, arguments)
        format_tool_result(result, args.output)

        if result.get("isError"):
            sys.exit(1)


if __name__ == "__main__":
    main()
