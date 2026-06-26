#!/usr/bin/env python3
"""
ALAPI CLI - 接口搜索、查询文档、直接调用的命令行工具。

用法:
    python alapi.py search <keyword>           搜索接口
    python alapi.py explore                    浏览全部接口（按分类）
    python alapi.py detail <id>                获取接口基本信息
    python alapi.py openapi <id>               获取接口 OpenAPI Spec
    python alapi.py call <path> [options]       调用接口

调用接口选项:
    --token <token>      API Token（最高优先级）
    --param <key=value>  请求参数（可多次使用）
    --method <GET|POST>  请求方法，默认 GET

环境变量:
    ALAPI_TOKEN          未指定 --token 时使用

示例:
    python alapi.py search "IP"
    python alapi.py openapi 27
    python alapi.py call ip --token ALAPI_TOKEN --param ip=8.8.8.8
    ALAPI_TOKEN=your_token python alapi.py call hitokoto --param type=a
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://v3.alapi.cn"
OUTPUT_JSON = False


def _request(url, method="GET", data=None, headers=None):
    """发起 HTTP 请求，返回解析后的 JSON 或原始文本。"""
    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", "ALAPI-CLI/1.0")

    body = None
    if data and method == "POST":
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif data and method == "GET":
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(data)

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            err = json.loads(raw)
            print(json.dumps(err, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(f"HTTP {e.code}: {raw}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def _emit(payload, render_text=None):
    """根据输出模式返回 JSON 或文本。"""
    if OUTPUT_JSON:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    if render_text is None:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(render_text(payload))


def _search_payload(result):
    payload = {
        "command": "search",
        "success": False,
        "keyword": None,
        "count": 0,
        "items": [],
        "raw": result,
    }
    if isinstance(result, dict) and result.get("data"):
        apis = result["data"].get("list", [])
        payload["success"] = True
        payload["count"] = len(apis)
        payload["items"] = [
            {
                "id": api.get("id"),
                "name": api.get("name"),
                "description": api.get("description"),
                "doc_url": f"https://www.alapi.cn/api/{api.get('id')}/introduction",
            }
            for api in apis
        ]
    return payload


def _render_search(payload):
    if not payload["items"]:
        return "未找到匹配的接口。"

    lines = [f"找到 {payload['count']} 个接口:\n"]
    for api in payload["items"]:
        lines.append(f"  ID: {api.get('id', '')}  | {api.get('name', '')}")
        desc = api.get("description")
        if desc:
            lines.append(f"           {desc[:80]}")
        lines.append(f"           文档: {api.get('doc_url')}")
        lines.append("")
    return "\n".join(lines).rstrip()


def _explore_payload(result):
    payload = {
        "command": "explore",
        "success": False,
        "categories": [],
        "groups": [],
        "raw": result,
    }
    if isinstance(result, dict) and result.get("data"):
        data = result["data"]
        payload["success"] = True
        payload["categories"] = data.get("categories", [])
        payload["groups"] = data.get("apis", [])
    return payload


def _render_explore(payload):
    if not payload["success"]:
        return json.dumps(payload["raw"], indent=2, ensure_ascii=False)

    lines = ["=== ALAPI 接口分类 ===\n"]
    for cat in payload["categories"]:
        lines.append(f"  {cat.get('name', '')} ({cat.get('apis_count', 0)} 个)")
    lines.append("")
    for group in payload["groups"]:
        lines.append(f"【{group.get('category', '')}】")
        for api in group.get("apis", []):
            lines.append(f"  ID: {api.get('id', '')}  | {api.get('name', '')}")
        lines.append("")
    return "\n".join(lines).rstrip()


def _detail_payload(api_id, result):
    return {
        "command": "detail",
        "success": isinstance(result, dict) and bool(result.get("data")),
        "api_id": api_id,
        "data": result.get("data") if isinstance(result, dict) else None,
        "raw": result,
    }


def _openapi_payload(api_id, result):
    return {
        "command": "openapi",
        "success": isinstance(result, dict),
        "api_id": api_id,
        "spec": result if isinstance(result, dict) else None,
        "raw": result,
    }


def _call_payload(path, method, result):
    return {
        "command": "call",
        "success": isinstance(result, dict) and bool(result.get("success")),
        "path": path,
        "method": method,
        "response": result,
    }


def _resolve_token(explicit_token):
    """解析 token，显式参数优先，其次环境变量。"""
    if explicit_token:
        return explicit_token
    return os.environ.get("ALAPI_TOKEN")


def cmd_search(keyword):
    """搜索接口。"""
    url = f"{BASE_URL}/frontend/api/search"
    result = _request(url, data={"keywords": keyword})
    payload = _search_payload(result)
    payload["keyword"] = keyword
    _emit(payload, _render_search)


def cmd_explore():
    """浏览全部接口（按分类）。"""
    url = f"{BASE_URL}/frontend/api/explore"
    result = _request(url)
    _emit(_explore_payload(result), _render_explore)


def cmd_detail(api_id):
    """获取接口基本信息。"""
    url = f"{BASE_URL}/frontend/api/find/{api_id}"
    result = _request(url)
    payload = _detail_payload(api_id, result)
    _emit(payload["data"] if not OUTPUT_JSON and payload["success"] else payload)


def cmd_openapi(api_id):
    """获取接口 OpenAPI Spec。"""
    url = f"{BASE_URL}/openapi/{api_id}.json"
    result = _request(url)
    payload = _openapi_payload(api_id, result)
    _emit(payload["spec"] if not OUTPUT_JSON and payload["success"] else payload)


def cmd_call(path, token, params, method="GET"):
    """直接调用接口。"""
    token = _resolve_token(token)
    if not token:
        print("错误: 调用接口必须提供 --token 参数，或设置环境变量 ALAPI_TOKEN。", file=sys.stderr)
        print("创建 Token: https://www.alapi.cn/dashboard/data/token", file=sys.stderr)
        sys.exit(1)

    url = f"{BASE_URL}/api/{path}"
    params["token"] = token

    if method == "POST":
        result = _request(url, method="POST", data=params)
    else:
        result = _request(url, method="GET", data=params)
    payload = _call_payload(path, method, result)
    _emit(result if not OUTPUT_JSON else payload)


def main():
    global OUTPUT_JSON

    args = sys.argv[1:]
    if "--json" in args:
        OUTPUT_JSON = True
        args = [arg for arg in args if arg != "--json"]

    if len(args) < 1:
        print(__doc__)
        sys.exit(0)

    command = args[0].lower()

    if command == "search":
        if len(args) < 2:
            print("用法: python alapi.py search <keyword>", file=sys.stderr)
            sys.exit(1)
        cmd_search(args[1])

    elif command == "explore":
        cmd_explore()

    elif command == "detail":
        if len(args) < 2:
            print("用法: python alapi.py detail <id>", file=sys.stderr)
            sys.exit(1)
        cmd_detail(args[1])

    elif command == "openapi":
        if len(args) < 2:
            print("用法: python alapi.py openapi <id>", file=sys.stderr)
            sys.exit(1)
        cmd_openapi(args[1])

    elif command == "call":
        if len(args) < 2:
            print("用法: python alapi.py call <path> --token <token> [--param k=v ...]", file=sys.stderr)
            sys.exit(1)
        path = args[1]
        token = None
        params = {}
        method = "GET"
        i = 2
        while i < len(args):
            arg = args[i]
            if arg == "--token" and i + 1 < len(args):
                token = args[i + 1]
                i += 2
            elif arg == "--param" and i + 1 < len(args):
                kv = args[i + 1]
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    params[k] = v
                i += 2
            elif arg == "--method" and i + 1 < len(args):
                method = args[i + 1].upper()
                i += 2
            else:
                print(f"未知参数: {arg}", file=sys.stderr)
                i += 1
        cmd_call(path, token, params, method)

    else:
        print(f"未知命令: {command}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
