#!/usr/bin/env python3
"""粉象 MCP Streamable HTTP 最小客户端（仅标准库）。

用法：
  python3 fenxiang_mcp.py buy_advice '{"goodsUrl":"<商品链接或分享文案>"}'
  python3 fenxiang_mcp.py compare_by_name '{"productName":"iPhone 17 Pro 256G"}'
  python3 fenxiang_mcp.py tools/list
  python3 fenxiang_mcp.py initialize        # 看服务端下发的使用说明
  python3 fenxiang_mcp.py prompts/list

环境变量：
  FENXIANG_MCP_URL          默认 https://api.fenxianglife.com/njia/mcp
  FENXIANG_MCP_API_KEY      可选；当前服务不需要鉴权

TLS：默认严格校验证书；仅内网自签名测试环境可显式加 --insecure。
"""

import argparse
import itertools
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

DEFAULT_URL = "https://api.fenxianglife.com/njia/mcp"
TOOLS = (
    "buy_advice", "batch_analyze", "compare_by_name", "recommend_goods",
    "goods_search", "history_price", "compare_price", "saving_plan",
)


class McpError(RuntimeError):
    pass


class McpClient:
    def __init__(self, url, api_key, timeout=60, insecure=False):
        self.url = url
        self.api_key = api_key
        self.timeout = timeout
        self.context = ssl._create_unverified_context() if insecure else None
        self._ids = itertools.count(1)

    def rpc(self, method, params=None):
        payload = {"jsonrpc": "2.0", "id": next(self._ids), "method": method, "params": params or {}}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.api_key:
            headers["Authorization"] = "Bearer " + self.api_key
        request = urllib.request.Request(
            self.url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout, context=self.context) as response:
                body = response.read().decode("utf-8")
                content_type = response.headers.get("Content-Type", "")
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            raise McpError("HTTP %s: %s" % (error.code, body[:500])) from error
        except (urllib.error.URLError, OSError) as error:
            # 读超时（TimeoutError）不是 URLError，一并转成 McpError，调用方统一按失败处理
            raise McpError("connection failed: %s" % error) from error

        if "text/event-stream" in content_type:
            body = _last_sse_data(body)
        try:
            data = json.loads(body)
        except json.JSONDecodeError as error:
            raise McpError("invalid JSON response: %s" % body[:500]) from error
        if data.get("error"):
            raise McpError(json.dumps(data["error"], ensure_ascii=False))
        return data.get("result") or {}

    def initialize(self):
        return self.rpc("initialize", {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "fenxiang-skill-script", "version": "2.0.0"},
        })

    def list_tools(self):
        result = self.rpc("tools/list")
        return result.get("tools") or []

    def list_prompts(self):
        result = self.rpc("prompts/list")
        return result.get("prompts") or []

    def call_tool(self, name, arguments):
        result = self.rpc("tools/call", {"name": name, "arguments": arguments})
        if result.get("isError"):
            raise McpError(_first_text(result) or "tool returned isError=true")
        text = _first_text(result)
        structured = result.get("structuredContent")
        return text, parse_text(text), structured


def _first_text(result):
    content = result.get("content") or []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            return block.get("text")
    return None


def _last_sse_data(body):
    data_lines = []
    for line in body.splitlines():
        if line.startswith("data:"):
            data_lines.append(line[5:].strip())
    if not data_lines:
        return body
    for value in reversed(data_lines):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict) and ("result" in parsed or "error" in parsed):
            return json.dumps(parsed, ensure_ascii=False)
    return data_lines[-1]


def parse_text(text):
    if not text:
        return None
    try:
        data = json.loads(text)
    except (TypeError, json.JSONDecodeError):
        return None
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data
    return data


def load_api_key(path=None):
    key = os.environ.get("FENXIANG_MCP_API_KEY", "").strip()
    if not key and path:
        with open(os.path.expanduser(path), "r", encoding="utf-8") as handle:
            key = handle.read().strip()
    return key


def build_client(args):
    url = args.url or os.environ.get("FENXIANG_MCP_URL") or DEFAULT_URL
    return McpClient(url, load_api_key(args.api_key_file), timeout=args.timeout, insecure=args.insecure)


def main():
    parser = argparse.ArgumentParser(description="粉象 MCP HTTP 客户端")
    parser.add_argument("tool", help=" / ".join(TOOLS) + " / tools/list / prompts/list / initialize")
    parser.add_argument("arguments", nargs="?", default="{}", help="工具参数 JSON，默认 {}")
    parser.add_argument("--url", help="MCP 地址，默认 FENXIANG_MCP_URL 或生产地址")
    parser.add_argument("--api-key-file", help="只包含 API Key 的文件")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--insecure", action="store_true",
                        help="仅内网自签名测试环境使用：跳过证书校验，生产环境不要使用")
    parser.add_argument("--pretty", action="store_true", help="尝试格式化 JSON 输出")
    args = parser.parse_args()

    try:
        client = build_client(args)
        if args.tool in ("tools/list", "tools_list", "list"):
            for tool in client.list_tools():
                print("%s\t%s" % (tool.get("name"), tool.get("title") or ""))
            return 0
        if args.tool in ("prompts/list", "prompts_list"):
            for prompt in client.list_prompts():
                print("%s\t%s" % (prompt.get("name"), prompt.get("title") or ""))
            return 0
        if args.tool == "initialize":
            result = client.initialize()
            info = result.get("serverInfo") or {}
            print("%s %s" % (info.get("name"), info.get("version")))
            print(result.get("instructions") or "")
            return 0

        try:
            arguments = json.loads(args.arguments)
        except json.JSONDecodeError as error:
            raise McpError("工具参数不是合法 JSON: %s" % error) from error
        text, parsed, structured = client.call_tool(args.tool, arguments)
        if args.pretty and parsed is not None:
            print(json.dumps(parsed, ensure_ascii=False, indent=2))
        elif args.pretty and structured is not None:
            print(json.dumps(structured, ensure_ascii=False, indent=2))
        else:
            print(text if text is not None else json.dumps(structured, ensure_ascii=False))
        return 0
    except McpError as error:
        print("ERROR: %s" % error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
