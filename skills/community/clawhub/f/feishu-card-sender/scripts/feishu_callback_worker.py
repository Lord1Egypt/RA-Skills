#!/usr/bin/env python3
import json
import os
import time
import hashlib
import re
import base64
import tempfile
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import subprocess
from pathlib import Path

HOST = '0.0.0.0'
PORT = 18081

ROUTER = '/root/.openclaw/workspace-dev/skills/feishu-card-sender/scripts/card_callback_router.py'
USER_ID_FALLBACK = os.getenv('FEISHU_CALLBACK_USER_FALLBACK', '').strip()
ACCOUNT_ID = os.getenv('FEISHU_CALLBACK_ACCOUNT_ID', '1').strip() or '1'
ENCRYPT_KEY = os.getenv('FEISHU_CALLBACK_ENCRYPT_KEY', '').strip()
MAX_SKEW_SECONDS = int(os.getenv('FEISHU_CALLBACK_MAX_SKEW_SECONDS', '300'))


class H(BaseHTTPRequestHandler):
    def _log(self, event, **kwargs):
        payload = {'event': event, 'ts': int(time.time()), **kwargs}
        print(json.dumps(payload, ensure_ascii=False), flush=True)


    def _parse_ts_to_epoch(self, ts: str):
        # 1) epoch seconds / milliseconds
        try:
            n = int(float(ts))
            if n > 10_000_000_000:
                n = n // 1000
            return n
        except Exception:
            pass

        # 2) Go-style datetime: "2026-03-05 22:25:56.839226736 +0800 CST m=+..."
        m = re.search(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})(?:\.(\d{1,9}))?\s+([+-]\d{4})', ts)
        if m:
            base, frac, offset = m.group(1), (m.group(2) or ''), m.group(3)
            frac6 = (frac + '000000')[:6]
            dt = datetime.strptime(f"{base}.{frac6} {offset}", "%Y-%m-%d %H:%M:%S.%f %z")
            return int(dt.timestamp())

        raise ValueError(f'invalid_timestamp:{ts}')

    def _decrypt_if_needed(self, req_obj):
        # Feishu may send encrypted envelope: {"encrypt": "..."}
        if not isinstance(req_obj, dict) or 'encrypt' not in req_obj:
            return req_obj
        if not ENCRYPT_KEY:
            raise ValueError('encrypt_key_not_configured')

        enc = str(req_obj.get('encrypt') or '')
        raw = base64.b64decode(enc)
        iv, ct = raw[:16], raw[16:]
        keyhex = hashlib.sha256(ENCRYPT_KEY.encode('utf-8')).hexdigest()
        ivhex = iv.hex()

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(ct)
            inpath = f.name
        try:
            res = subprocess.run(
                ['openssl', 'enc', '-d', '-aes-256-cbc', '-K', keyhex, '-iv', ivhex, '-in', inpath],
                capture_output=True,
                timeout=10,
            )
            if res.returncode != 0:
                raise ValueError(f'decrypt_failed:{res.stderr.decode("utf-8", errors="replace")[:120]}')
            txt = res.stdout.decode('utf-8', errors='replace')
            return json.loads(txt)
        finally:
            try:
                os.unlink(inpath)
            except Exception:
                pass

    def _verify_signature(self, raw_body: str):
        if not ENCRYPT_KEY:
            return True, 'no_encrypt_key'
        ts = self.headers.get('X-Lark-Request-Timestamp') or self.headers.get('X-Lark-Request-Ts')
        nonce = self.headers.get('X-Lark-Request-Nonce')
        sig = self.headers.get('X-Lark-Signature')
        if not ts or not nonce or not sig:
            return False, 'missing_signature_headers'
        try:
            ts_i = self._parse_ts_to_epoch(ts)
        except Exception as ex:
            return False, str(ex)
        if abs(int(time.time()) - ts_i) > MAX_SKEW_SECONDS:
            return False, 'timestamp_skew'
        base = f"{ts}{nonce}{ENCRYPT_KEY}{raw_body}".encode('utf-8')
        calc = hashlib.sha256(base).hexdigest()
        if calc != sig:
            return False, 'signature_mismatch'
        return True, 'ok'

    def _send(self, code=200, obj=None):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(obj or {}, ensure_ascii=False).encode('utf-8'))

    def _send_html(self, code=200, html=''):
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()
        if html:
            self.wfile.write(html.encode('utf-8'))

    def do_HEAD(self):
        p = urlparse(self.path)
        if p.path == '/feishu/callback':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            return
        self.send_response(404)
        self.end_headers()

    def do_GET(self):
        p = urlparse(self.path)
        if p.path != '/feishu/callback':
            return self._send_html(404, '<h1>404 Not Found</h1>')

        qs = parse_qs(p.query or '')
        lang_force = ((qs.get('lang') or [''])[0]).strip().lower()
        if lang_force in ('zh', 'zh-cn', 'cn'):
            use_zh = True
        elif lang_force in ('en', 'en-us', 'en-gb'):
            use_zh = False
        else:
            accept_lang = (self.headers.get('Accept-Language') or '').lower()
            use_zh = ('zh' in accept_lang) or not accept_lang

        t = {
            'lang': 'zh-CN' if use_zh else 'en',
            'title': '飞书回调 · 太空网关' if use_zh else 'Feishu Callback · Space Gateway',
            'badge': '太空网关在线' if use_zh else 'SPACE GATEWAY ONLINE',
            'h1_left': '飞书回调' if use_zh else 'Feishu Callback',
            'h1_right': '接口已就绪' if use_zh else 'Endpoint is Ready',
            'desc': '这里是飞书事件回调入口，专用于服务端 POST 调用。你在浏览器看到这个页面，说明域名解析、HTTPS 与反向代理都已连通。' if use_zh else 'This is the Feishu event callback endpoint for server-side POST calls. Seeing this page in your browser means DNS, HTTPS, and reverse proxy are all reachable.',
            'endpoint_k': '回调路径' if use_zh else 'Endpoint',
            'proto_k': '协议状态' if use_zh else 'Protocol',
            'proto_v': 'HTTPS · 反向代理已启用' if use_zh else 'HTTPS · Reverse Proxy Active',
            'hint': '提示：此页面仅用于可达性确认；真实回调由飞书服务器触发，无需人工访问。' if use_zh else 'Note: This page is only for reachability checks. Real callbacks are triggered by Feishu servers, no manual access required.'
        }

        html = """
<!doctype html>
<html lang=\"{t['lang']}\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover\" />
  <title>{t['title']}</title>
  <style>
    :root{
      --bg:#030712;
      --bg2:#0b1020;
      --txt:#eaf2ff;
      --muted:#b8c7e6;
      --primary:#78c7ff;
      --line:rgba(150,190,255,.28);
      --glass:rgba(8,14,33,.55);
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      overflow:hidden;
      font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
      color:var(--txt);
      background:
        radial-gradient(1200px 700px at 10% 90%, rgba(79,118,255,.22), transparent 60%),
        radial-gradient(900px 600px at 90% 10%, rgba(0,210,255,.18), transparent 62%),
        radial-gradient(1000px 800px at 50% 50%, #0b1331 0%, var(--bg) 68%);
    }
    .stars,.stars2,.stars3{position:fixed; inset:-20%; pointer-events:none;}
    .stars:before,.stars2:before,.stars3:before{
      content:""; position:absolute; inset:0;
      background-repeat:repeat;
      animation:drift linear infinite;
      opacity:.65;
    }
    .stars:before{background-image:radial-gradient(2px 2px at 20px 30px,#fff,transparent),radial-gradient(1px 1px at 120px 80px,#d7e8ff,transparent),radial-gradient(1.5px 1.5px at 220px 150px,#fff,transparent);background-size:260px 220px;animation-duration:120s}
    .stars2:before{background-image:radial-gradient(1px 1px at 40px 60px,#9fd8ff,transparent),radial-gradient(2px 2px at 180px 120px,#fff,transparent),radial-gradient(1px 1px at 260px 40px,#c8dcff,transparent);background-size:320px 260px;animation-duration:180s;opacity:.4}
    .stars3:before{background-image:radial-gradient(2px 2px at 80px 20px,#fff,transparent),radial-gradient(1px 1px at 200px 200px,#c2f2ff,transparent);background-size:400px 320px;animation-duration:240s;opacity:.28}
    @keyframes drift{from{transform:translate3d(0,0,0)}to{transform:translate3d(-220px,-160px,0)}}

    .nebula{position:fixed; inset:0; pointer-events:none; filter:blur(30px); opacity:.55}
    .nebula:before,.nebula:after{content:""; position:absolute; border-radius:50%}
    .nebula:before{width:42vw;height:42vw;left:-10vw;top:50vh;background:radial-gradient(circle,#4f70ff88,transparent 70%)}
    .nebula:after{width:34vw;height:34vw;right:-8vw;top:8vh;background:radial-gradient(circle,#2dd4ff77,transparent 72%)}

    .wrap{position:relative; z-index:2; height:100vh; min-height:100dvh; display:flex; align-items:center; justify-content:center; padding:max(16px,env(safe-area-inset-top)) max(16px,env(safe-area-inset-right)) max(16px,env(safe-area-inset-bottom)) max(16px,env(safe-area-inset-left))}
    .panel{
      width:min(980px,96vw);
      padding:18px 18px 16px;
      position:relative;
      text-align:center;
      margin:0 auto;
      display:flex;
      flex-direction:column;
      align-items:center;
      justify-content:center;
    }
    .badge{display:inline-flex;align-items:center;gap:8px;padding:6px 12px;border:1px solid rgba(143,214,255,.35);border-radius:999px;background:rgba(31,56,95,.35);color:#cde9ff;font-size:12px;letter-spacing:.3px}
    .dot{width:8px;height:8px;border-radius:50%;background:#5cf2a5;box-shadow:0 0 12px #5cf2a5}
    h1{margin:14px 0 12px;font-size:38px;line-height:1.12;letter-spacing:.3px}
    .grad{background:linear-gradient(90deg,#f4f9ff,#8cd2ff 35%,#7db2ff 70%,#d8e9ff);-webkit-background-clip:text;background-clip:text;color:transparent}
    p{margin:10px 0;color:var(--muted);font-size:16px;line-height:1.75}
    .meta{margin-top:18px;display:grid;grid-template-columns:1fr 1fr;gap:12px}
    .cell{padding:8px 10px;border:1px solid rgba(141,180,255,.20);border-radius:999px;background:transparent}
    .k{display:block;font-size:12px;color:#9db4df;margin-bottom:4px}
    code{color:var(--primary);background:rgba(8,16,36,.8);border:1px solid rgba(120,170,255,.25);padding:2px 7px;border-radius:8px}
    .hint{margin-top:16px;font-size:13px;color:#93a9d3}
    @media (max-width:760px){
      h1{font-size:30px}
      .meta{grid-template-columns:1fr}
      .panel{padding:24px 20px}
    }
  </style>
</head>
<body>
  <div class=\"stars\"></div>
  <div class=\"stars2\"></div>
  <div class=\"stars3\"></div>
  <div class=\"nebula\"></div>

  <main class=\"wrap\">
    <section class=\"panel\">
      <span class=\"badge\"><span class=\"dot\"></span>{t['badge']}</span>
      <h1><span class=\"grad\">{t['h1_left']}</span> {t['h1_right']}</h1>
      <p>{t['desc'].replace('POST', '<code>POST</code>')}</p>
      <div class=\"meta\">
        <div class=\"cell\"><span class=\"k\">{t['endpoint_k']}</span><code>/feishu/callback</code></div>
        <div class=\"cell\"><span class=\"k\">{t['proto_k']}</span><code>{t['proto_v']}</code></div>
      </div>
      <p class=\"hint\">{t['hint']}</p>
    </section>
  </main>
  <script>
    // Hard-disable pinch zoom for in-app webviews (iOS/Android)
    (function(){
      document.addEventListener('gesturestart', function(e){ e.preventDefault(); }, {passive:false});
      document.addEventListener('gesturechange', function(e){ e.preventDefault(); }, {passive:false});
      document.addEventListener('gestureend', function(e){ e.preventDefault(); }, {passive:false});
      document.addEventListener('touchmove', function(e){ if (e.touches && e.touches.length > 1) e.preventDefault(); }, {passive:false});
      let lastTouchEnd = 0;
      document.addEventListener('touchend', function(e){
        const now = Date.now();
        if (now - lastTouchEnd <= 300) e.preventDefault(); // prevent double-tap zoom
        lastTouchEnd = now;
      }, {passive:false});
    })();
  </script>
</body>
</html>
""".strip()
        html = (html
                .replace("{t['lang']}", t['lang'])
                .replace("{t['title']}", t['title'])
                .replace("{t['badge']}", t['badge'])
                .replace("{t['h1_left']}", t['h1_left'])
                .replace("{t['h1_right']}", t['h1_right'])
                .replace("{t['desc'].replace('POST', '<code>POST</code>')}", t['desc'].replace('POST', '<code>POST</code>'))
                .replace("{t['endpoint_k']}", t['endpoint_k'])
                .replace("{t['proto_k']}", t['proto_k'])
                .replace("{t['proto_v']}", t['proto_v'])
                .replace("{t['hint']}", t['hint']))
        return self._send_html(200, html)

    def do_POST(self):
        p = urlparse(self.path)
        if p.path != '/feishu/callback':
            return self._send(404, {'error': 'not_found'})

        n = int(self.headers.get('Content-Length', '0'))
        raw = self.rfile.read(n).decode('utf-8', errors='replace')

        ok_sig, reason = self._verify_signature(raw)
        if not ok_sig:
            self._log('callback_rejected', reason=reason, path=p.path)
            return self._send(401, {'error': 'invalid_signature', 'reason': reason})

        try:
            req = json.loads(raw)
            req = self._decrypt_if_needed(req)
        except Exception as ex:
            self._log('callback_rejected', reason='invalid_json_or_decrypt_failed', detail=str(ex), path=p.path)
            return self._send(400, {'error': 'invalid_json_or_decrypt_failed'})

        # url_verification
        if req.get('type') == 'url_verification':
            self._log('url_verification', path=p.path)
            return self._send(200, {'challenge': req.get('challenge', '')})

        # Strict mode: follow Feishu latest encrypted callback payload
        # Expected shape after decrypt: {header:{event_type}, event:{token, action.value, operator.open_id}}
        header = req.get('header') or {}
        event = req.get('event') or {}
        event_type = header.get('event_type')
        action_value = ((event.get('action') or {}).get('value') or {})
        token = str(event.get('token') or '')
        user_id = ((event.get('operator') or {}).get('open_id')) or USER_ID_FALLBACK

        if event_type != 'card.action.trigger' or not token or not isinstance(action_value, dict):
            self._log('callback_rejected', reason='invalid_payload_shape', event_type=event_type, keys=list(req.keys())[:20])
            return self._send(200, {'toast': {'type': 'error', 'content': '回调结构不符合预期'}})

        if not user_id:
            self._log('callback_rejected', reason='missing_user_id', token=token)
            return self._send(200, {'toast': {'type': 'error', 'content': '缺少用户信息，无法处理'}})

        # 1) immediate ack in <3s (toast only)
        self._send(200, {'toast': {'type': 'info', 'content': '处理中...'}})

        # 2) async heavy work
        payload = json.dumps(action_value, ensure_ascii=False)
        msg_id = f'card-action-{token}' if token else ''
        self._log('callback_accepted', token=token, user_id=user_id, account_id=ACCOUNT_ID)
        subprocess.Popen([
            'python3', ROUTER,
            '--channel', 'feishu',
            '--user-id', user_id,
            '--account-id', ACCOUNT_ID,
            '--message-id', msg_id,
            '--payload', payload,
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    server = ThreadingHTTPServer((HOST, PORT), H)
    print(f'feishu_callback_worker listening on {HOST}:{PORT}')
    server.serve_forever()


if __name__ == '__main__':
    main()
