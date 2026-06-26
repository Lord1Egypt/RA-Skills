#!/usr/bin/env python3
"""AirplaneAI v1.1 — 断网离线 AI 助手 (小白友好版)
A self-contained offline chat server. Zero dependencies beyond Python stdlib.
"""
import socket, json, threading, webbrowser, urllib.request, os, sys, argparse, re, time
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────
HOST = os.environ.get("AIRPLANE_HOST", "127.0.0.1")
PORT = int(os.environ.get("AIRPLANE_PORT", "8765"))
LLM_URL = os.environ.get("AIRPLANE_LLM_URL", "http://127.0.0.1:1234/v1/chat/completions")
LLM_MODEL = os.environ.get("AIRPLANE_LLM_MODEL", "")  # auto-detect if empty
PERSONA_FILE = os.environ.get("AIRPLANE_PERSONA_FILE", "")
MAX_HISTORY = int(os.environ.get("AIRPLANE_MAX_HISTORY", "20"))
MAX_TEMP = float(os.environ.get("AIRPLANE_TEMP", "0.7"))
MAX_TOKENS = int(os.environ.get("AIRPLANE_MAX_TOKENS", "2048"))

DEFAULT_PERSONA = """You are AirplaneAI, a helpful offline AI assistant running on a local LLM.
You cannot browse the web. Answer concisely and directly. If you don't know, say so honestly.
You can read local files: <<READ:/path/to/file>> — the system will feed content back."""

# ── Health Check ─────────────────────────────────────────────────────
def health_check(llm_url):
    """Check if everything is working."""
    issues = []
    base = re.sub(r"/v1/chat/completions$", "", llm_url.rstrip("/"))
    models_url = f"{base}/v1/models"

    print("🩺 AirplaneAI Health Check\n")

    # Python version
    py = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    ok = sys.version_info >= (3, 8)
    icon = "✅" if ok else "❌"
    print(f"{icon} Python {py}")
    if not ok:
        issues.append("Python 3.8+ required")

    # Port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.bind(("127.0.0.1", PORT))
        s.close()
        print(f"✅ Port {PORT} available")
    except OSError:
        print(f"⚠️  Port {PORT} already in use (AirplaneAI might be running)")
    s.close()

    # LLM endpoint
    try:
        req = urllib.request.Request(f"{base}/v1/models", headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
            models = [m["id"] for m in data.get("data", [])]
        print(f"✅ LLM reachable: {base}/v1/models")
        if models:
            print(f"   Available models:")
            for m in models[:10]:
                marker = " ← auto-selected" if not LLM_MODEL and models.index(m) == 0 else ""
                print(f"   • {m}{marker}")
    except Exception as e:
        print(f"❌ LLM not reachable: {e}")
        issues.append(f"Cannot reach {base}/v1/models")

    # Chat API
    try:
        test_body = json.dumps({
            "model": LLM_MODEL or (models[0] if models else "unknown"),
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 5
        }).encode()
        req2 = urllib.request.Request(llm_url, data=test_body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req2, timeout=10) as r:
            json.loads(r.read())
        print(f"✅ Chat API working: {llm_url}")
    except Exception as e:
        print(f"❌ Chat API failed: {e}")
        issues.append(f"Chat API test failed")

    # WiFi check
    try:
        urllib.request.urlopen("https://clawhub.ai", timeout=3)
        print("⚠️  WiFi is ON — offline mode not verified. Disconnect to test.")
    except Exception:
        print("✅ WiFi is OFF — true offline mode confirmed.")

    print()
    if issues:
        print("❌ Issues found:")
        for i in issues:
            print(f"   - {i}")
        return False
    else:
        print("🟢 All checks passed! Run without --check to start chatting.")
        return True


# ── Auto-detect model ────────────────────────────────────────────────
def detect_model(llm_url):
    base = re.sub(r"/v1/chat/completions$", "", llm_url.rstrip("/"))
    try:
        req = urllib.request.Request(f"{base}/v1/models", headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
            models = [m["id"] for m in data.get("data", []) if isinstance(m, dict)]
            return models[0] if models else None
    except Exception:
        return None

# ── CLI ──────────────────────────────────────────────────────────────
def parse_args():
    ap = argparse.ArgumentParser(description="AirplaneAI — Offline Chat Server")
    ap.add_argument("--host", default=HOST)
    ap.add_argument("--port", type=int, default=PORT)
    ap.add_argument("--llm-url", default=LLM_URL, help="LLM endpoint (default: LM Studio localhost:1234)")
    ap.add_argument("--llm-model", default=LLM_MODEL, help="Model name (auto-detected if omitted)")
    ap.add_argument("--persona-file", default=PERSONA_FILE, help="Custom system prompt (.txt)")
    ap.add_argument("--no-browser", action="store_true", help="Don't open browser")
    ap.add_argument("--check", action="store_true", help="Run health check and exit")
    return ap.parse_args()


# ── Build the HTML page ──────────────────────────────────────────────
def build_page(llm_model_display, llm_url_display):
    title = os.environ.get("AIRPLANE_TITLE", "🛫 AirplaneAI")
    return f"""HTTP/1.1 200 OK\r
Content-Type: text/html; charset=utf-8\r
\r
<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{title}</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif;background:#1a1a2e;color:#e0e0e0;height:100vh;display:flex;flex-direction:column}}
.header{{background:#16213e;padding:10px 16px;border-bottom:1px solid #0f3460;display:flex;align-items:center;gap:10px;font-size:13px}}
.header .status-dot{{width:8px;height:8px;border-radius:50%;margin-right:6px}}
.header .status-dot.online{{background:#4ecca3;box-shadow:0 0 6px rgba(78,204,163,0.6)}}
.header .status-dot.offline{{background:#e74c3c;box-shadow:0 0 6px rgba(231,76,60,0.6)}}
.header .model-tag{{margin-left:auto;font-size:11px;color:#666;background:rgba(78,204,163,0.08);padding:3px 10px;border-radius:10px;border:1px solid rgba(78,204,163,0.15)}}
.chat{{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}}
.msg{{max-width:85%;padding:10px 14px;border-radius:12px;font-size:14px;line-height:1.6;white-space:pre-wrap;word-break:break-word}}
.msg.user{{background:#0f3460;align-self:flex-end;border-bottom-right-radius:4px}}
.msg.assistant{{background:#16213e;align-self:flex-start;border-bottom-left-radius:4px}}
.msg.system{{background:#2d1b3d;align-self:center;border-radius:8px;font-size:12px;color:#a088c0;max-width:90%;text-align:center}}
.input-area{{display:flex;gap:8px;padding:12px 16px;background:#16213e;border-top:1px solid #0f3460}}
.input-area input{{flex:1;padding:10px 14px;border-radius:20px;border:1px solid #0f3460;background:#1a1a2e;color:#e0e0e0;font-size:14px;outline:none}}
.input-area input:focus{{border-color:#4ecca3}}
.input-area button{{padding:10px 20px;border-radius:20px;border:none;background:#4ecca3;color:#1a1a2e;font-weight:700;font-size:14px;cursor:pointer}}
.input-area button:disabled{{opacity:0.5;cursor:not-allowed}}
</style></head><body>
<div class="header">
<span class="status-dot online" id="statusDot" title="Connected"></span>
<b>🛫 AirplaneAI</b>
<span style="font-size:11px;color:#888" id="statusText">Connected</span>
<span class="model-tag">{llm_model_display}</span>
</div>
<div class="chat" id="chat">
<div class="msg system">🛫 AirplaneAI ready — chatting with {llm_model_display} via {llm_url_display}</div>
</div>
<div class="input-area">
<input id="input" placeholder="输入消息…" autofocus onkeydown="if(event.key==='Enter')send()">
<button id="sendbtn" onclick="send()">Send</button>
</div>
<script>
const API="/api/chat";let messages=[];
function add(r,c){{let d=document.createElement("div");d.className="msg "+r;d.textContent=c;let ch=document.getElementById("chat");ch.appendChild(d);ch.scrollTop=ch.scrollHeight}}
function setStatus(ok){{let dot=document.getElementById("statusDot");let txt=document.getElementById("statusText");if(ok){{dot.className="status-dot online";txt.textContent="Connected"}}else{{dot.className="status-dot offline";txt.textContent="Disconnected"}}}}
async function send(){{
let i=document.getElementById("input"),t=i.value.trim();if(!t)return;
i.value="";i.disabled=true;document.getElementById("sendbtn").disabled=true;
add("user",t);messages.push({{role:"user",content:t}});
try{{
let r=await fetch(API,{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{messages}})}});
let d=await r.json();
add("assistant",d.content);
setStatus(true);
let read_match=d.content.match(/<<READ:(.+?)>>/);
if(read_match){{
let fp=read_match[1].trim();
add("system","📂 Reading: "+fp);
let fr=await fetch("/api/read",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{path:fp}})}});
let fd=await fr.json();
if(fd.content){{
let truncated=fd.content.length>4000?fd.content.substring(0,4000)+"\\n... [truncated, "+fd.content.length+" chars total]":fd.content;
messages.push({{role:"user",content:"File content ("+fp+"):\\n"+truncated}});
add("system","✅ Read: "+fp+" ("+fd.content.length+" chars)");
let r2=await fetch(API,{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{messages}})}});
let d2=await r2.json();
add("assistant",d2.content);
messages.push({{role:"assistant",content:d2.content}});
setStatus(true);
}}else{{add("system","⚠️ "+fd.error);}}
}}else{{messages.push({{role:"assistant",content:d.content}});}}
}}catch(e){{add("system","⚠️ Connection to LLM failed: "+e.message);setStatus(false);}}
i.disabled=false;document.getElementById("sendbtn").disabled=false;
}}

// Periodic health ping
setInterval(async()=>{{try{{let r=await fetch("/api/health");let d=await r.json();setStatus(d.ok)}}catch(e){{setStatus(false)}}}},15000);
</script></body></html>""".encode()


# ── LLM call ─────────────────────────────────────────────────────────
def call_llm(system_prompt, messages, llm_url, llm_model):
    msgs = [{"role": "system", "content": system_prompt}] + messages[-MAX_HISTORY:]
    body = json.dumps({
        "model": llm_model,
        "messages": msgs,
        "temperature": MAX_TEMP,
        "max_tokens": MAX_TOKENS,
    }, ensure_ascii=False).encode()
    req = urllib.request.Request(llm_url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]


# ── File reading ─────────────────────────────────────────────────────
def read_file(filepath):
    path = Path(filepath).expanduser().resolve()
    if not path.exists():
        return {"error": f"File not found: {filepath}"}
    try:
        content = path.read_text(encoding="utf-8")
        return {"content": content, "size": len(content)}
    except Exception as e:
        return {"error": str(e)}


# ── HTTP handler ─────────────────────────────────────────────────────
def handle(conn, page_bytes, system_prompt, llm_url, llm_model):
    try:
        data = conn.recv(65536).decode("utf-8", errors="replace")
        if not data: return
        lines = data.split("\r\n")
        first = lines[0] if lines else ""

        if first.startswith("GET") and "/api/health" in first:
            # Health check from UI
            try:
                req = urllib.request.Request(f"{re.sub(r'/v1/chat/completions$','',llm_url.rstrip('/'))}/v1/models")
                with urllib.request.urlopen(req, timeout=3):
                    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"ok\":true}")
            except Exception:
                conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"ok\":false}")
            return

        if first.startswith("GET"):
            conn.sendall(page_bytes)
            return

        if not first.startswith("POST"):
            conn.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
            return

        body_start = data.find("\r\n\r\n")
        if body_start < 0:
            conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            return
        body = data[body_start + 4:]

        if "/api/read" in first:
            try:
                req = json.loads(body)
                result = read_file(req.get("path", ""))
                resp = json.dumps(result, ensure_ascii=False)
                conn.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: {len(resp.encode())}\r\n\r\n{resp}".encode())
            except Exception as e:
                err = json.dumps({"error": str(e)}, ensure_ascii=False)
                conn.sendall(f"HTTP/1.1 500 OK\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: {len(err.encode())}\r\n\r\n{err}".encode())
            return

        try:
            msgs = json.loads(body).get("messages", [])
            reply = call_llm(system_prompt, msgs, llm_url, llm_model)
            resp = json.dumps({"content": reply}, ensure_ascii=False)
            conn.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: {len(resp.encode())}\r\n\r\n{resp}".encode())
        except Exception as e:
            err = json.dumps({"content": f"⚠️ LLM error: {e}"}, ensure_ascii=False)
            conn.sendall(f"HTTP/1.1 500 OK\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: {len(err.encode())}\r\n\r\n{err}".encode())
    except Exception:
        pass
    finally:
        conn.close()


# ── Main ─────────────────────────────────────────────────────────────
def main():
    global HOST, PORT, LLM_URL, LLM_MODEL
    args = parse_args()
    HOST, PORT = args.host, args.port
    LLM_URL = args.llm_url
    LLM_MODEL = args.llm_model

    # Health check mode
    if args.check:
        ok = health_check(LLM_URL)
        sys.exit(0 if ok else 1)

    # Auto-detect model
    if not LLM_MODEL:
        detected = detect_model(LLM_URL)
        if detected:
            LLM_MODEL = detected
            print(f"🔍 Auto-detected model: {LLM_MODEL}")
        else:
            print("⚠️  Could not auto-detect model. Use --llm-model to specify.")

    # Load persona
    persona = DEFAULT_PERSONA
    persona_file = args.persona_file or PERSONA_FILE
    if persona_file and Path(persona_file).exists():
        persona = Path(persona_file).read_text(encoding="utf-8")
        print(f"📝 Loaded persona: {persona_file}")

    # Display
    url_display = re.sub(r"https?://", "", LLM_URL.split("/v1")[0])
    page_bytes = build_page(LLM_MODEL, url_display)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)

    chat_url = f"http://{HOST}:{PORT}"
    print(f"🛫 AirplaneAI v1.1 → {chat_url}")
    print(f"   Model: {LLM_MODEL}")
    print(f"   LLM: {LLM_URL}")
    print(f"   Tip: Run with --check to diagnose issues first.")

    if not args.no_browser:
        threading.Thread(target=lambda: webbrowser.open(chat_url), daemon=True).start()

    while True:
        conn, _ = sock.accept()
        threading.Thread(target=handle, args=(conn, page_bytes, persona, LLM_URL, LLM_MODEL), daemon=True).start()


if __name__ == "__main__":
    main()
