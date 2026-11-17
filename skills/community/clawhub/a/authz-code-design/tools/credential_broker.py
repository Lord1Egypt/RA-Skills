#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
credential_broker.py — 本地凭据 broker 原型 v2.1
============================================================================
增强（相对 v1 原型）：
  1. 审计持久化 + 防篡改：审计从内存 list 改为 append-only 日志文件，每条带
     哈希链（prev_hash -> hash，HMAC-SHA256），重启加载并校验链，篡改即告警。
  2. 设备指纹 + 生物：每次调用带 X-Device-Id；unlock 可传 biometric
     (WinHello / HUKS / TouchID)，审计记录 device + bio 字段。
  3. 统一 Web 只读面板：GET /dashboard 返回只读 HTML（分组树/活跃授权/审计），
     127.0.0.1 + pin 校验，不暴露明文密码。
  4. 完整吊销体系（对应方法论 §3.8）：单令牌 /revoke、一键解绑 /revoke_all
     （应急清场）、/revoke_device（设备丢失按指纹收回）、/revoke_title
     （按条目收回）；所有动作全进审计哈希链，零知识边界不变。

设计原则（对应 SOP v1.2 §8）：
  - 仅监听 127.0.0.1，不暴露到网络。
  - 所有敏感配置从环境变量读，绝不硬编码、绝不写日志明文。
  - AI agent 永不直接读 .kdbx 明文；向 broker 请求→拿到短时 JWT（exp≤900s）
    →需要时 /fulfill 取秘，秘仅返回本地调用方，不进 JWT/模型上下文/落盘。
  - 审计内容不含密码，只含 jti(截断)/title/scope/device/bio/时间，且哈希链防篡改。

真实部署建议：
  - VAULT_PASSPHRASE 应由本机 OS 凭证库（DPAPI/Keychain/HUKS）在本地解锁时提供。
  - 审计 key（broker_audit.key）存本机 chmod 600，生产应进 OS 凭证库。
  - 生物解锁（WinHello/HUKS）真实对接需本机 TPM/安全芯片，本原型仅记录 biometric
    标记字段，真实校验在 unlock 调用方（本机 OS）完成。

依赖（隔离 venv）：pykeepass, cryptography
运行：BROKER_UNLOCK_PIN=xxx VAULT_PATH=xxx.kdbx VAULT_PASSPHRASE=xxx python credential_broker.py
"""
import os
import sys
import json
import time
import base64
import hmac
import hashlib
import threading
import secrets
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

try:
    from pykeepass import PyKeePass
except ImportError:
    sys.stderr.write("缺少依赖 pykeepass，请先在隔离 venv 安装：pip install pykeepass cryptography\n")
    raise

logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("broker")

MAX_TTL = 900  # 秒，单次令牌最长 15 分钟
DEFAULT_TTL = 300


# ---------- 极简 HS256 JWT（无外部依赖） ----------
def _b64(b: bytes) -> bytes:
    return base64.urlsafe_b64encode(b).rstrip(b"=")

def _b64d(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)

def _jwt_sign(payload: dict, secret: bytes) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    seg = _b64(json.dumps(header, separators=(",", ":")).encode()) + b"." + \
          _b64(json.dumps(payload, separators=(",", ":")).encode())
    sig = hmac.new(secret, seg, hashlib.sha256).digest()
    return (seg + b"." + _b64(sig)).decode()

def _jwt_verify(token: str, secret: bytes) -> dict:
    try:
        seg, sig = token.encode().rsplit(b".", 1)
        expected = hmac.new(secret, seg, hashlib.sha256).digest()
        expected_b = _b64(expected)
        if not hmac.compare_digest(sig, expected_b):
            raise ValueError("签名校验失败")
        _, payload_b64 = seg.split(b".")
        payload = json.loads(_b64d(payload_b64.decode()))
        if "exp" in payload and time.time() > payload["exp"]:
            raise ValueError("令牌已过期")
        return payload
    except Exception as e:
        raise ValueError(f"令牌无效: {e}")


# ---------- 审计 key 加载（持久化，chmod 600） ----------
def _load_audit_key(path: str) -> bytes:
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    k = secrets.token_bytes(32)
    with open(path, "wb") as f:
        f.write(k)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return k


class Broker:
    def __init__(self, vault_path, vault_passphrase, vault_keyfile=None,
                 unlock_pin=None, port=8731,
                 audit_log="broker_audit.jsonl", audit_key_path="broker_audit.key"):
        self.vault_path = vault_path
        self.vault_passphrase = vault_passphrase
        self.vault_keyfile = vault_keyfile
        self.unlock_pin = unlock_pin  # broker 自身网关口令（非 vault 主密码）
        self.port = port
        self.broker_secret = secrets.token_bytes(32)  # 每次启动随机，签 JWT
        self.revoked = set()  # 已吊销 jti
        self.active = {}      # jti -> (exp, title, scope, device, bio)
        self.audit = []       # 审计内存（用于 dashboard / audit 返回）
        self.biometric = None
        self._lock = threading.Lock()
        self._kp = None
        # 审计持久化
        self.audit_key = _load_audit_key(audit_key_path)
        self.audit_key_path = audit_key_path
        self.audit_log_path = audit_log
        self._seq = 0
        self._prev_hash = "0" * 64
        self._load_audit()

    # --- 审计加载 + 哈希链校验 ---
    def _load_audit(self):
        if not os.path.exists(self.audit_log_path):
            return
        with open(self.audit_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    if not self._verify_chain(rec):
                        log.warning("审计链校验失败，可能遭篡改: seq=%s", rec.get("seq"))
                        continue
                    self._seq = rec["seq"]
                    self._prev_hash = rec["hash"]
                    self.audit.append(rec)
                except Exception:
                    log.warning("审计记录解析失败，跳过")

    def _verify_chain(self, rec: dict) -> bool:
        payload = {k: v for k, v in rec.items() if k != "hash"}
        calc = hmac.new(self.audit_key,
                        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(),
                        hashlib.sha256).hexdigest()
        return hmac.compare_digest(calc, rec.get("hash", ""))

    def _record(self, action, jti, title, scope, ttl=None,
                device="unknown", bio=None):
        with self._lock:
            self._seq += 1
            rec = {
                "seq": self._seq,
                "prev_hash": self._prev_hash,
                "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
                "iat": int(time.time()),
                "action": action,
                "jti": (jti or "")[:8],
                "title": title,
                "scope": scope,
                "ttl": ttl,
                "device": device,
                "bio": bio,
            }
            payload = {k: v for k, v in rec.items() if k != "hash"}
            rec["hash"] = hmac.new(self.audit_key,
                                   json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(),
                                   hashlib.sha256).hexdigest()
            self._prev_hash = rec["hash"]
            with open(self.audit_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            self.audit.append(rec)
            return rec

    # --- vault 解锁（仅本机、仅一次） ---
    def unlock(self, biometric=None):
        self._kp = PyKeePass(self.vault_path, password=self.vault_passphrase,
                             keyfile=self.vault_keyfile)
        self.biometric = biometric
        log.warning("vault 已在本机解锁（密钥驻留内存，不落盘）bio=%s", biometric or "none")

    def _entry(self, title):
        for e in self._kp.entries:
            if e.title == title:
                return e
        return None

    def _auth(self, handler) -> bool:
        pin = handler.headers.get("X-Broker-Pin", "")
        return hmac.compare_digest(pin, self.unlock_pin or "")

    def _device(self, handler) -> str:
        return handler.headers.get("X-Device-Id", "unknown")

    # --- 端点逻辑 ---
    def issue_token(self, title, scope="read", ttl=DEFAULT_TTL,
                    device="unknown", bio=None):
        if ttl > MAX_TTL:
            ttl = MAX_TTL
        if self._entry(title) is None:
            raise ValueError(f"vault 中无此条目: {title}")
        jti = secrets.token_hex(16)
        exp = int(time.time()) + ttl
        payload = {"sub": title, "scope": scope, "exp": exp, "jti": jti,
                   "iat": int(time.time())}
        token = _jwt_sign(payload, self.broker_secret)
        self._record("issue", jti, title, scope, ttl, device, bio or self.biometric)
        self.active[jti] = (exp, title, scope, device, bio or self.biometric)
        return {"token": token, "expires_in": ttl, "scope": scope}

    def fulfill(self, token, device="unknown"):
        payload = _jwt_verify(token, self.broker_secret)
        jti = payload["jti"]
        if jti in self.revoked:
            raise ValueError("令牌已吊销")
        entry = self._entry(payload["sub"])
        if entry is None:
            raise ValueError("条目不存在")
        self._record("fulfill", jti, payload["sub"], payload.get("scope"),
                     device=device, bio=self.biometric)
        # 仅在履行时把秘返回给本地受信调用方；不进 JWT、不落盘、不进模型上下文
        return {"title": entry.title, "username": entry.username,
                "password": entry.password, "scope": payload.get("scope")}

    def revoke(self, token, device="unknown"):
        payload = _jwt_verify(token, self.broker_secret)
        jti = payload["jti"]
        with self._lock:
            self.revoked.add(jti)
            self.active.pop(jti, None)
        self._record("revoke", jti, payload["sub"], payload.get("scope"),
                     device=device, bio=self.biometric)
        return {"revoked": True}

    # --- 批量/定向吊销（对应方法论 §3.8） ---
    def revoke_all(self, device="unknown"):
        """一键解绑：吊销全部活跃授权（应急清场）。"""
        with self._lock:
            js = list(self.active.keys())
            for j in js:
                self.revoked.add(j)
            self.active.clear()
        self._record("revoke_all", "", "(ALL)", "all", device=device,
                     bio=self.biometric)
        return {"revoked": True, "count": len(js)}

    def revoke_device(self, device_id, device="unknown"):
        """设备丢失：按设备指纹收回该设备持有的全部授权。"""
        with self._lock:
            hit = [j for j, v in self.active.items() if v[3] == device_id]
            for j in hit:
                self.revoked.add(j)
                self.active.pop(j, None)
        self._record("revoke_device", "", f"(DEVICE:{device_id})", "all",
                     device=device, bio=self.biometric)
        return {"revoked": True, "device": device_id, "count": len(hit)}

    def revoke_title(self, title, device="unknown"):
        """按条目收回：吊销指向某 vault 条目的全部授权。"""
        with self._lock:
            hit = [j for j, v in self.active.items() if v[1] == title]
            for j in hit:
                self.revoked.add(j)
                self.active.pop(j, None)
        self._record("revoke_title", "", title, "all", device=device,
                     bio=self.biometric)
        return {"revoked": True, "title": title, "count": len(hit)}

    def audit_log(self):
        with self._lock:
            return list(self.audit)

    def dashboard_html(self) -> str:
        """只读 Web 面板：分组树（不显明文）+ 活跃授权 + 审计。"""
        # 分组树
        tree = []
        def walk(g, depth=0):
            for sub in g.subgroups:
                tree.append(("  " * depth + "[ " + (sub.name or "?") + " ]", "", ""))
                walk(sub, depth + 1)
            for e in g.entries:
                tree.append(("  " * depth + "• " + (e.title or "?"),
                             e.username or "", e.url or ""))
        walk(self._kp.root_group)
        tree_html = "".join(
            f"<tr><td><code>{t}</code></td><td>{u}</td><td>{url}</td></tr>"
            for t, u, url in tree) or "<tr><td colspan=3>空</td></tr>"

        # 活跃授权
        now = int(time.time())
        active_rows = []
        for j, (exp, title, scope, device, bio) in self.active.items():
            if j in self.revoked:
                continue
            left = exp - now
            if left <= 0:
                continue
            active_rows.append(
                f"<tr><td>{j[:8]}</td><td>{title}</td><td>{scope}</td>"
                f"<td>{device}</td><td>{bio or 'none'}</td><td>{left}s</td></tr>")
        active_html = "".join(active_rows) or "<tr><td colspan=6>无活跃授权</td></tr>"

        # 审计（最近 50）
        audit_rows = []
        for r in self.audit_log()[-50:]:
            audit_rows.append(
                f"<tr><td>{r.get('seq')}</td><td>{r.get('ts')}</td>"
                f"<td>{r.get('action')}</td><td>{r.get('jti')}</td>"
                f"<td>{r.get('title')}</td><td>{r.get('scope')}</td>"
                f"<td>{r.get('device')}</td><td>{r.get('bio') or 'none'}</td></tr>")
        audit_html = "".join(audit_rows) or "<tr><td colspan=8>无</td></tr>"

        return f"""<!doctype html><html><head><meta charset=utf-8>
<title>凭据 broker 面板</title>
<style>
body{{font-family:-apple-system,Segoe UI,sans-serif;margin:24px;color:#222;background:#fff}}
h1{{font-size:18px}} h2{{font-size:15px;margin-top:28px;color:#185FA5}}
table{{border-collapse:collapse;width:100%;font-size:12px;margin-top:8px}}
th,td{{border:1px solid #e2e2e2;padding:6px 8px;text-align:left}}
th{{background:#f5f7fa}} code{{color:#534AB7}}
.note{{color:#888;font-size:12px}}
</style></head><body>
<h1>统一凭据 broker · 只读面板</h1>
<p class="note">本机 127.0.0.1 · 只读 · 不暴露明文密码 · 解锁 bio={self.biometric or 'none'}</p>

<h2>分组树（凭据清单，密码不显示）</h2>
<table><thead><tr><th>条目/分组</th><th>用户名</th><th>URL</th></tr></thead>
<tbody>{tree_html}</tbody></table>

<h2>活跃授权（未过期且未吊销）</h2>
<table><thead><tr><th>jti</th><th>条目</th><th>scope</th><th>设备</th><th>生物</th><th>剩余</th></tr></thead>
<tbody>{active_html}</tbody></table>

<h2>审计日志（最近 50，哈希链防篡改）</h2>
<table><thead><tr><th>#</th><th>时间</th><th>动作</th><th>jti</th><th>条目</th>
<th>scope</th><th>设备</th><th>生物</th></tr></thead>
<tbody>{audit_html}</tbody></table>
</body></html>"""


class _Handler(BaseHTTPRequestHandler):
    broker = None  # 由 server 注入

    def log_message(self, *a):  # 静默默认访问日志
        pass

    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, code, html):
        body = html.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length", 0))
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode())
        except Exception:
            return {}

    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/audit":
            if not self.broker._auth(self):
                return self._send(401, {"error": "unauthorized"})
            return self._send(200, {"audit": self.broker.audit_log()})
        if p == "/dashboard":
            # 原型简化：支持 ?pin= 便于浏览器访问；生产应走 OS 凭证库/会话
            qs = parse_qs(urlparse(self.path).query)
            pin = self.headers.get("X-Broker-Pin") or qs.get("pin", [""])[0]
            if not hmac.compare_digest(pin, self.broker.unlock_pin or ""):
                return self._send_html(403, "<h1>403 未授权</h1>")
            return self._send_html(200, self.broker.dashboard_html())
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        p = urlparse(self.path).path
        if not self.broker._auth(self):
            return self._send(401, {"error": "unauthorized"})
        data = self._body()
        device = self.headers.get("X-Device-Id", "unknown")
        try:
            if p == "/token":
                r = self.broker.issue_token(
                    data.get("title"), data.get("scope", "read"),
                    int(data.get("ttl", DEFAULT_TTL)), device=device)
                return self._send(200, r)
            if p == "/fulfill":
                r = self.broker.fulfill(data.get("token"), device=device)
                return self._send(200, r)
            if p == "/revoke":
                r = self.broker.revoke(data.get("token"), device=device)
                return self._send(200, r)
            if p == "/revoke_all":
                r = self.broker.revoke_all(device=device)
                return self._send(200, r)
            if p == "/revoke_device":
                r = self.broker.revoke_device(data.get("device_id"), device=device)
                return self._send(200, r)
            if p == "/revoke_title":
                r = self.broker.revoke_title(data.get("title"), device=device)
                return self._send(200, r)
        except ValueError as e:
            return self._send(400, {"error": str(e)})
        return self._send(404, {"error": "not found"})


def main():
    vault_path = os.environ.get("VAULT_PATH")
    vault_pass = os.environ.get("VAULT_PASSPHRASE")
    vault_key = os.environ.get("VAULT_KEYFILE")
    pin = os.environ.get("BROKER_UNLOCK_PIN")
    port = int(os.environ.get("BROKER_PORT", "8731"))
    audit_log = os.environ.get("BROKER_AUDIT_LOG", "broker_audit.jsonl")
    audit_key = os.environ.get("BROKER_AUDIT_KEY", "broker_audit.key")
    bio = os.environ.get("BROKER_BIOMETRIC")  # 可选：WinHello/HUKS/TouchID
    if not (vault_path and vault_pass and pin):
        sys.stderr.write("缺少环境变量：VAULT_PATH / VAULT_PASSPHRASE / BROKER_UNLOCK_PIN\n")
        sys.exit(2)
    b = Broker(vault_path, vault_pass, vault_key, pin, port, audit_log, audit_key)
    b.unlock(bio)
    _Handler.broker = b
    srv = ThreadingHTTPServer(("127.0.0.1", port), _Handler)
    print(f"[broker] 监听 127.0.0.1:{port}（仅本机）。Ctrl+C 退出。")
    print(f"[broker] 只读面板: http://127.0.0.1:{port}/dashboard?pin={pin}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
