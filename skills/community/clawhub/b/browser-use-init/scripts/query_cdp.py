"""
query_cdp.py - 查询 Chrome CDP 连接信息（browser-use-init skill 工具脚本）

环境变量配置:
    CDP_PORT    CDP 调试端口（默认 9222）

用法:
    python query_cdp.py
    python query_cdp.py --port 9223
"""

import urllib.request, json, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DEFAULT_PORT = int(os.getenv("CDP_PORT", "9222"))

def get_cdp_info(port=9222):
    try:
        resp = urllib.request.urlopen(f"http://localhost:{port}/json/version", timeout=3)
        data = json.loads(resp.read())
        return data
    except Exception as e:
        print(f"[ERROR] CDP 不可用: {e}")
        return None


def list_tabs(port=9222):
    try:
        resp = urllib.request.urlopen(f"http://localhost:{port}/json/list", timeout=3)
        targets = json.loads(resp.read())
        pages = [t for t in targets if t.get("type") == "page"]
        return pages
    except Exception as e:
        print(f"[ERROR] 获取标签页列表失败: {e}")
        return []


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, 
                       help=f"CDP 调试端口（默认来自 $CDP_PORT 环境变量或 {DEFAULT_PORT}）")
    args = parser.parse_args()

    info = get_cdp_info(args.port)
    if not info:
        sys.exit(1)

    print(f"Browser: {info.get('Browser')}")
    print(f"WS URL: {info.get('webSocketDebuggerUrl')}")
    print(f"Version: {info.get('V8-Version')}")

    pages = list_tabs(args.port)
    print(f"\n标签页 ({len(pages)}):")
    for p in pages:
        print(f"  - {p.get('title', '?')[:60]} | {p.get('url', '?')[:80]}")
