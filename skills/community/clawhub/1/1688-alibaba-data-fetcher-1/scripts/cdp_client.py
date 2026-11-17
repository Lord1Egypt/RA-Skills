#!/usr/bin/env python3
"""
1688 Data Claw - CDP 客户端模块
通过 Chrome DevTools Protocol 连接浏览器，与插件交互获取数据。

用法示例:
    from cdp_client import CdpClient
    
    client = CdpClient()
    client.ensure_tab()
    data = client.fetch_data(mode='full', limit=50)
    print(data)

    # 导航到页面
    client.navigate("https://work.1688.com/", wait=5)
    
    # 截图
    client.screenshot("page.png", clip={'x': 100, 'y': 100, 'w': 300, 'h': 200})
"""

import json
import os
import sys
import socket
import struct
import urllib.request
import base64
import time
import re

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# --- 默认配置（可通过环境变量覆盖） ---
CDP_HOST = os.environ.get('CDP_HOST', '127.0.0.1')
CDP_PORT = int(os.environ.get('CDP_PORT', '9222'))
EXTENSION_ID = os.environ.get('EXTENSION_ID', 'ekmgnempbbamlmaolijdfjakeopniion')


# ============ WebSocket 工具 ============

def _connect_ws(ws_url):
    """连接到 CDP WebSocket target"""
    m = re.match(r'ws://([^:]+):(\d+)(/.*)', ws_url)
    host, port, path = m.group(1), int(m.group(2)), m.group(3)
    sock = socket.create_connection((host, port))
    key = base64.b64encode(os.urandom(16)).decode()
    sock.send(
        f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\n"
        f"Upgrade: websocket\r\nConnection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode()
    )
    while b"\r\n\r\n" not in sock.recv(4096):
        pass
    return sock


def _send_ws(sock, msg):
    """发送 WebSocket 帧（masked）"""
    payload = msg.encode('utf-8')
    frame = bytearray([0x81])
    l = len(payload)
    if l <= 125:
        frame.append(l | 0x80)
    elif l <= 65535:
        frame.append(126 | 0x80)
        frame.extend(struct.pack('>H', l))
    else:
        frame.append(127 | 0x80)
        frame.extend(struct.pack('>Q', l))
    mask = os.urandom(4)
    frame.extend(mask)
    frame.extend(bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))
    sock.send(bytes(frame))


def _recv_ws(sock):
    """接收 WebSocket 帧"""
    header = b""
    while len(header) < 2:
        header += sock.recv(2 - len(header))
    length = header[1] & 0x7f
    offset = 2
    if length == 126:
        while len(header) < offset + 2:
            header += sock.recv(2)
        length = struct.unpack('>H', header[offset:offset + 2])[0]
        offset += 2
    elif length == 127:
        while len(header) < offset + 8:
            header += sock.recv(8)
        length = struct.unpack('>Q', header[offset:offset + 8])[0]
        offset += 8
    if header[1] & 0x80:
        while len(header) < offset + 4:
            header += sock.recv(4)
        mask = header[offset:offset + 4]
        offset += 4
    payload = b""
    while len(payload) < length:
        chunk = sock.recv(min(4096, length - len(payload)))
        payload += chunk
    if header[1] & 0x80:
        payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    return payload


# ============ CDP 命令 ============

def _cdp_call(sock, method, params=None, timeout_ms=15000):
    """发送 CDP 命令并等待响应"""
    _msg_counter = [1]  # mutable closure

    msg_id = _msg_counter[0]
    _msg_counter[0] += 1
    _send_ws(sock, json.dumps({
        "id": msg_id,
        "method": method,
        "params": params or {},
    }))
    resp = json.loads(_recv_ws(sock).decode())
    return resp.get('result', {})


def _cdp_eval(sock, expression, timeout_ms=15000):
    """在页面中执行 JS（支持 Promise），返回 value"""
    result = _cdp_call(sock, 'Runtime.evaluate', {
        'expression': expression,
        'returnByValue': True,
        'awaitPromise': True,
        'timeout': timeout_ms,
    })
    return result.get('result', {}).get('value')


# ============ 高级 API ============


class CdpClient:
    """高级 CDP 客户端，封装常见操作"""

    def __init__(self, host=None, port=None):
        self.host = host or CDP_HOST
        self.port = port or CDP_PORT
        self._sock = None
        self._tab = None

    # ---- 浏览器状态 ----

    @staticmethod
    def is_running(host=None, port=None):
        """检查 CDP 端口是否可用，且确认是独立 Chromium 实例
        
        验证逻辑：
        1. CDP 端口有响应
        2. user-data-dir 目录下存在标记文件 .openclaw_browser_marker
        3. 进程启动参数中 user-data-dir 匹配（Linux: /proc 检查）
        """
        h = host or CDP_HOST
        p = port or CDP_PORT
        try:
            with urllib.request.urlopen(f'http://{h}:{p}/json/version', timeout=3):
                pass
        except Exception:
            return False
        
        # 检查标记文件
        user_data = os.environ.get('USER_DATA', 'C:\\isolated-profiles\\1688-agent' if os.name == 'nt' else '/tmp/chromium')
        marker_file = os.path.join(user_data, '.openclaw_browser_marker')
        if not os.path.exists(marker_file):
            return False
        
        # Linux: 验证 user-data-dir 匹配
        if os.path.exists('/proc'):
            try:
                import subprocess
                result = subprocess.run(
                    ['pgrep', '-f', f'chrome.*remote-debugging-port={p}'],
                    capture_output=True, text=True, timeout=5
                )
                pid = result.stdout.strip().split('\n')[0] if result.stdout.strip() else None
                if pid:
                    with open(f'/proc/{pid}/cmdline', 'rb') as f:
                        cmdline = f.read().replace(b'\x00', b' ').decode(errors='replace')
                        if user_data not in cmdline:
                            return False
            except Exception:
                pass  # 无法验证时仍信任标记文件
        
        # Windows: 信任标记文件（进程验证较复杂，标记文件已足够隔离）
        
        return True

    def list_tabs(self):
        """列出所有页面标签"""
        with urllib.request.urlopen(f'http://{self.host}:{self.port}/json/list') as resp:
            return json.loads(resp.read())

    def find_1688_tab(self):
        """查找第一个 1688 页面标签"""
        tabs = self.list_tabs()
        for t in tabs:
            if t.get('type') == 'page' and '1688.com' in t.get('url', ''):
                return t
        return None

    # ---- 连接管理 ----

    def connect(self, tab=None):
        """连接到指定标签（或自动找 1688 标签）的 WebSocket"""
        if tab:
            self._tab = tab
        else:
            self._tab = self.find_1688_tab()

        if not self._tab:
            raise RuntimeError("没有找到 1688 页面标签，请先导航到 work.1688.com 或 sycm.1688.com")

        ws_url = self._tab.get('webSocketDebuggerUrl')
        self._sock = _connect_ws(ws_url)

    def close(self):
        """断开 WebSocket 连接"""
        if self._sock:
            self._sock.close()
            self._sock = None
        self._tab = None

    def ensure_tab(self, retries=5, delay=2):
        """确保有 1688 标签页连接，没有则创建新标签页"""
        for i in range(retries):
            tab = self.find_1688_tab()
            if tab:
                self.connect(tab)
                return
            print(f"⏳ 等待 1688 标签页... ({i + 1}/{retries})")
            time.sleep(delay)
        # 没有找到 1688 标签页，创建一个新的
        print("创建新标签页...")
        tab = self.create_tab("https://work.1688.com/")
        if tab:
            time.sleep(3)
            self.connect(tab)
            return
        raise RuntimeError(f"在 {retries * delay}s 内未找到 1688 标签页，且创建失败")

    def create_tab(self, url="about:blank"):
        """通过 CDP HTTP API 创建新的浏览器标签页"""
        try:
            req = urllib.request.Request(
                f'http://{self.host}:{self.port}/json/new?url={urllib.request.quote(url)}',
                method='PUT'
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read())
        except Exception as e:
            print(f"创建标签页失败: {e}")
            return None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    # ---- CDP 操作 ----

    def eval(self, expression, timeout_ms=15000):
        """在页面中执行 JS"""
        return _cdp_eval(self._sock, expression, timeout_ms)

    def navigate(self, url, wait_seconds=8):
        """导航到 URL 并等待页面加载 + content script 采集"""
        _cdp_call(self._sock, 'Page.navigate', {'url': url})
        time.sleep(wait_seconds)

    def screenshot(self, filepath, clip=None):
        """截图保存到文件，可选裁剪区域 clip={'x', 'y', 'w', 'h'}"""
        params = {"format": "png", "captureBeyondViewport": True}
        if clip:
            params["clip"] = {
                "x": clip['x'], "y": clip['y'],
                "width": clip['w'], "height": clip['h'],
                "scale": 1
            }
        result = _cdp_call(self._sock, 'Page.captureScreenshot', params)
        img = base64.b64decode(result['data'])
        with open(filepath, 'wb') as f:
            f.write(img)
        return len(img)

    def clear_cookies(self):
        """清空浏览器 cookies"""
        _cdp_call(self._sock, 'Network.clearBrowserCookies')

    # ---- 插件数据获取 ----

    def fetch_data(self, mode='full', limit=50):
        """通过 1688 Data Claw 插件 API 获取采集数据

        mode 可选: full / sycm / work / summary
        """
        js = f"""
        new Promise((resolve) => {{
            chrome.runtime.sendMessage('{EXTENSION_ID}', {{
                action: 'OPEN_CLAW_API',
                mode: '{mode}',
                limit: {limit}
            }}, (response) => {{
                resolve(JSON.stringify(response || {{error: 'no response'}}));
            }});
        }})
        """
        result = self.eval(js)
        if result:
            return json.loads(result)
        return {"success": False, "error": "No result"}


# ============ 快捷函数（兼容旧用法） ============

def get_1688_tab():
    """快捷函数：获取当前1688页面的 CDP 连接信息"""
    with urllib.request.urlopen(f'http://{CDP_HOST}:{CDP_PORT}/json/list') as resp:
        tabs = json.loads(resp.read())
    for t in tabs:
        if t['type'] == 'page' and '1688.com' in t.get('url', ''):
            return t
    return None


def fetch_claw_data(mode='full', limit=50):
    """快捷函数：通过插件 API 获取采集的数据"""
    tab = get_1688_tab()
    if not tab:
        return {"success": False, "error": "No 1688 tab found"}
    ws_url = tab['webSocketDebuggerUrl']
    sock = _connect_ws(ws_url)
    result = _cdp_eval(sock, f"""
    new Promise((resolve) => {{
        chrome.runtime.sendMessage('{EXTENSION_ID}', {{
            action: 'OPEN_CLAW_API',
            mode: '{mode}',
            limit: {limit}
        }}, (response) => {{
            resolve(JSON.stringify(response || {{error: 'no response'}}));
        }});
    }})
    """)
    sock.close()
    if result:
        return json.loads(result)
    return {"success": False, "error": "No result"}


def navigate_and_wait(url, wait_seconds=8):
    """快捷函数：导航到页面并等待 content script 采集"""
    tab = get_1688_tab()
    if not tab:
        return False
    ws_url = tab['webSocketDebuggerUrl']
    sock = _connect_ws(ws_url)
    _cdp_call(sock, 'Page.navigate', {'url': url})
    sock.close()
    time.sleep(wait_seconds)
    return True


if __name__ == '__main__':
    # 命令行测试
    import sys
    print(f"CDP: {CDP_HOST}:{CDP_PORT}")
    print(f"扩展 ID: {EXTENSION_ID}")
    print(f"浏览器运行中: {CdpClient.is_running()}")

    if len(sys.argv) > 1 and sys.argv[1] in ('start', 'verify'):
        if not CdpClient.is_running():
            print("❌ 浏览器未运行，请先执行 start-browser.sh / start-browser.ps1")
            sys.exit(1)
        print("✅ 浏览器正常运行")

    if len(sys.argv) > 1 and sys.argv[1] in ('fetch', 'verify'):
        with CdpClient() as c:
            try:
                c.ensure_tab(retries=3)
                data = c.fetch_data(mode='summary')
                print(f"✅ 数据获取结果: {json.dumps(data, ensure_ascii=False)[:200]}")
            except RuntimeError as e:
                print(f"❌ {e}")