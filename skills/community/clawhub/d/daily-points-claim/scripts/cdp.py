"""极简 CDP 客户端（纯标准库，无第三方依赖）。

只实现本项目需要的三件事：连上某个 page target、发 Runtime.evaluate、读回结果。
之所以手写 WebSocket，是因为本机没有 websocket-client / websockets，也不想为一次
签到引入依赖。
"""
import base64
import json
import os
import socket
import struct
import time
import urllib.request

__all__ = ["CDP", "launch_edge", "wait_cdp", "kill_tree"]


def _recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("socket closed")
        buf += chunk
    return buf


class _WS:
    def __init__(self, url, timeout=45):
        assert url.startswith("ws://")
        rest = url[5:]
        host_port, _, path = rest.partition("/")
        host, _, port = host_port.partition(":")
        port = int(port or 80)
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET /{path} HTTP/1.1\r\n"
            f"Host: {host_port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode())
        head = b""
        while b"\r\n\r\n" not in head:
            chunk = self.sock.recv(1)
            if not chunk:
                raise ConnectionError("handshake closed")
            head += chunk
        if b" 101 " not in head.split(b"\r\n")[0]:
            raise ConnectionError("handshake failed: " + head[:120].decode("latin1"))
        self._id = 0

    def _send_frame(self, payload, opcode=0x1):
        data = payload if isinstance(payload, bytes) else payload.encode()
        header = bytearray([0x80 | opcode])
        mask = os.urandom(4)
        n = len(data)
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header += struct.pack("!H", n)
        else:
            header.append(0x80 | 127)
            header += struct.pack("!Q", n)
        header += mask
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        self.sock.sendall(bytes(header) + masked)

    def _read_frame(self):
        b1, b2 = _recv_exact(self.sock, 2)
        opcode = b1 & 0x0F
        masked = b2 & 0x80
        n = b2 & 0x7F
        if n == 126:
            n = struct.unpack("!H", _recv_exact(self.sock, 2))[0]
        elif n == 127:
            n = struct.unpack("!Q", _recv_exact(self.sock, 8))[0]
        mask = _recv_exact(self.sock, 4) if masked else b""
        data = _recv_exact(self.sock, n) if n else b""
        if masked:
            data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        return opcode, data

    def call(self, method, params=None, timeout=45):
        self._id += 1
        mid = self._id
        self._send_frame(json.dumps({"id": mid, "method": method, "params": params or {}}))
        deadline = time.time() + timeout
        while time.time() < deadline:
            opcode, data = self._read_frame()
            if opcode == 0x9:
                self._send_frame(data, opcode=0xA)
                continue
            if opcode == 0x8:
                raise ConnectionError("server closed")
            if opcode not in (0x1, 0x2):
                continue
            msg = json.loads(data.decode("utf-8", "ignore"))
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(json.dumps(msg["error"])[:300])
                return msg.get("result", {})
        raise TimeoutError(f"{method} timeout")

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass


class CDP:
    def __init__(self, port):
        self.port = port

    def _get(self, path):
        return json.loads(urllib.request.urlopen(
            f"http://127.0.0.1:{self.port}{path}", timeout=10).read())

    def page_ws(self, url=None, timeout=30):
        """拿到一个 page target 的 ws 地址；必要时新开一个。"""
        if url:
            req = urllib.request.Request(
                f"http://127.0.0.1:{self.port}/json/new?{urllib.parse.quote(url, safe=':/?=&')}",
                method="PUT")
            try:
                t = json.loads(urllib.request.urlopen(req, timeout=10).read())
                return t["webSocketDebuggerUrl"]
            except Exception:
                pass
        deadline = time.time() + timeout
        while time.time() < deadline:
            for t in self._get("/json/list"):
                if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                    return t["webSocketDebuggerUrl"]
            time.sleep(1)
        raise TimeoutError("no page target")

    def evaluate(self, expr, await_promise=True, timeout=45):
        ws = _WS(self.page_ws(), timeout=timeout)
        try:
            ws.call("Runtime.enable", timeout=10)
            r = ws.call("Runtime.evaluate", {
                "expression": expr,
                "returnByValue": True,
                "awaitPromise": await_promise,
                "userGesture": True,
            }, timeout=timeout)
            if r.get("exceptionDetails"):
                raise RuntimeError(json.dumps(r["exceptionDetails"])[:400])
            return r.get("result", {}).get("value")
        finally:
            ws.close()

    def cookies(self, urls=None):
        ws = _WS(self.page_ws(), timeout=30)
        try:
            res = ws.call("Network.getCookies", {"urls": urls or [
                "https://www.workbuddy.cn", "https://www.workbuddy.cn/app"]}, timeout=20)
            return res.get("cookies", [])
        finally:
            ws.close()


def launch_edge(exe, profile, port, headless=True, url="about:blank"):
    import subprocess
    args = [exe, f"--remote-debugging-port={port}", f"--user-data-dir={profile}",
            "--no-first-run", "--no-default-browser-check", "--disable-features=Translate",
            "--window-size=1280,900"]
    if headless:
        args.append("--headless=new")
    args.append(url)
    kwargs = {}
    if os.name == "nt":
        kwargs["creationflags"] = 0x00000008 | 0x00000200  # DETACHED | NEW_GROUP
    p = subprocess.Popen(args, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, **kwargs)
    return p


def wait_cdp(port, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=2).read()
            return True
        except Exception:
            time.sleep(1)
    return False


def kill_tree(port):
    """通过 CDP Browser.close 优雅关闭，失败则按端口找进程强杀。"""
    try:
        ws = _WS(f"ws://127.0.0.1:{port}/json/version", timeout=5)
        return
    except Exception:
        pass
    try:
        import subprocess
        out = subprocess.run(["netstat", "-ano"], capture_output=True, text=True).stdout
        pids = set()
        for line in out.splitlines():
            if f":{port}" in line and "LISTENING" in line:
                pids.add(line.split()[-1])
        for pid in pids:
            subprocess.run(["taskkill", "/PID", pid, "/T", "/F"], capture_output=True)
    except Exception:
        pass


import urllib.parse  # noqa: E402  (放在末尾避免循环导入告警)
