#!/usr/bin/env python3
"""
CDP File Upload Script - 通用版
用法: python3 cdp_upload.py <file_path> [url_keyword]
- file_path: 要上传的文件路径
- url_keyword: 目标 tab 的 URL 关键词（默认: joyarti）

原理: 通过 Chrome DevTools Protocol 直接设置 input[type=file] 的文件，
      并触发 React onChange 事件，绕过 browser.upload() 无法触发 React 的问题。

自动重试: 如果 daemon 不存在，自动启动后再重试（最多 2 次）。
"""

import asyncio
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error
import websockets

FILE_PATH = sys.argv[1] if len(sys.argv) > 1 else "/tmp/openclaw/uploads/pet_image.jpg"
URL_KEYWORD = sys.argv[2] if len(sys.argv) > 2 else "joyarti"
CDP_HTTP = "http://127.0.0.1:18800"
MAX_RETRIES = 2

def is_daemon_running():
    """检查 daemon 是否在运行"""
    try:
        urllib.request.urlopen(f"{CDP_HTTP}/json/list", timeout=2)
        return True
    except:
        return False

def start_daemon():
    """启动 agent-browser daemon"""
    print("Starting agent-browser daemon...")
    subprocess.Popen(
        ["npx", "agent-browser", "open", "about:blank"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd="/tmp"
    )
    time.sleep(3)  # 等待 daemon 启动
    return is_daemon_running()

def get_target_id(url_keyword):
    """从 CDP /json/list 找到匹配 URL 的 tab"""
    resp = urllib.request.urlopen(f"{CDP_HTTP}/json/list", timeout=5)
    tabs = json.loads(resp.read())
    for tab in tabs:
        if url_keyword in tab.get("url", ""):
            return tab["id"]
    return None

def get_ws_url():
    """获取 browser 级别的 WebSocket URL"""
    resp = urllib.request.urlopen(f"{CDP_HTTP}/json/version", timeout=5)
    data = json.loads(resp.read())
    return data.get("webSocketDebuggerUrl")

async def send_recv(ws, msg, session_id=None):
    if session_id:
        msg["sessionId"] = session_id
    await ws.send(json.dumps(msg))
    for _ in range(20):
        resp = json.loads(await asyncio.wait_for(ws.recv(), timeout=10))
        if resp.get("id") == msg["id"]:
            return resp
    return None

async def upload(target_id, file_path):
    ws_url = get_ws_url()
    if not ws_url:
        print("ERR: Cannot get WebSocket URL")
        sys.exit(1)

    async with websockets.connect(ws_url) as ws:
        # Attach to target
        resp = await send_recv(ws, {
            "id": 1,
            "method": "Target.attachToTarget",
            "params": {"targetId": target_id, "flatten": True}
        })
        if not resp or "result" not in resp:
            print(f"ERR: Failed to attach to target: {resp}")
            sys.exit(1)
        session_id = resp["result"]["sessionId"]

        # Get document root
        resp = await send_recv(ws, {"id": 2, "method": "DOM.getDocument", "params": {}}, session_id)
        root_node_id = resp["result"]["root"]["nodeId"]

        # Find file input
        resp = await send_recv(ws, {
            "id": 3,
            "method": "DOM.querySelector",
            "params": {"nodeId": root_node_id, "selector": "input[type=file]"}
        }, session_id)
        node_id = resp["result"]["nodeId"] if resp and "result" in resp else None

        if not node_id:
            print("ERR: input[type=file] not found")
            sys.exit(1)

        # Set file via CDP
        resp = await send_recv(ws, {
            "id": 4,
            "method": "DOM.setFileInputFiles",
            "params": {"files": [file_path], "nodeId": node_id}
        }, session_id)
        if resp and "error" in resp:
            print(f"ERR: setFileInputFiles failed: {resp['error']}")
            sys.exit(1)

        # Dispatch React change event
        resp = await send_recv(ws, {
            "id": 5,
            "method": "Runtime.evaluate",
            "params": {
                "expression": """(() => {
                    const input = document.querySelector('input[type=file]');
                    if (!input) return 'ERR: no input';
                    const e = new Event('change', {bubbles: true});
                    input.dispatchEvent(e);
                    return 'OK: files=' + input.files.length;
                })()"""
            }
        }, session_id)

        result = resp["result"]["result"]["value"] if resp and "result" in resp else "unknown"
        print(result)
        if result.startswith("OK"):
            sys.exit(0)
        else:
            sys.exit(1)

def main():
    # 检查 daemon 是否运行，若不运行则启动
    if not is_daemon_running():
        print("Daemon not running, starting...")
        if not start_daemon():
            print("ERR: Failed to start daemon")
            sys.exit(1)
    
    for attempt in range(MAX_RETRIES):
        target_id = get_target_id(URL_KEYWORD)
        if target_id:
            print(f"Target: {target_id}")
            asyncio.run(upload(target_id, FILE_PATH))
            return
        
        if attempt < MAX_RETRIES - 1:
            print(f"No tab found (attempt {attempt+1}/{MAX_RETRIES}), retrying in 2s...")
            time.sleep(2)
            # 重试前确保 daemon 还在
            if not is_daemon_running():
                start_daemon()
    
    print(f"ERR: No tab found with URL keyword '{URL_KEYWORD}'")
    sys.exit(1)

if __name__ == "__main__":
    main()
