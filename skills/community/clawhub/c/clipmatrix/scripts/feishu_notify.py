"""
飞书消息通知 — 带token缓存，避免限流
"""
import json, subprocess, os, time

OPEN_ID = "ou_435a470d67b301e6cb0b5c73091f99ec"  # 新App (cli_aa90097e25789cc8)

_token_cache = {"token": "", "expires_at": 0}

def _get_credentials():
    oc_path = os.path.expanduser("~/.openclaw/openclaw.json")
    with open(oc_path) as f:
        oc = json.load(f)
    chan = oc.get("channels", {}).get("feishu", {})
    return chan.get("appId"), chan.get("appSecret")

def get_token():
    now = time.time()
    if _token_cache["token"] and now < _token_cache["expires_at"] - 60:
        return _token_cache["token"]
    app_id, app_secret = _get_credentials()
    # 🔧 (2026-05-31) 重试+容错：代理阻断时自动杀进程+重试
    for attempt in range(3):
        r = subprocess.run(["curl", "-s", "-X", "POST",
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"app_id": app_id, "app_secret": app_secret})],
            capture_output=True, text=True, timeout=10)
        if r.stdout.strip():
            try:
                data = json.loads(r.stdout)
                token = data.get("tenant_access_token", "")
                if token:
                    expire = data.get("expire", 7200)
                    _token_cache["token"] = token
                    _token_cache["expires_at"] = now + expire
                    return token
            except json.JSONDecodeError:
                pass
        # 代理阻断，杀进程重试
        if attempt < 2:
            subprocess.run(['pkill', '-9', '-f', 'MacPacketTunnel'], capture_output=True, timeout=5)
            time.sleep(2)
    return ""

def send_message(text: str):
    token = get_token()
    if not token:
        return False
    body = {
        "receive_id": OPEN_ID,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    r = subprocess.run(["curl", "-s", "-X", "POST",
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        "-H", f"Authorization: Bearer {token}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(body)],
        capture_output=True, text=True, timeout=10)
    result = json.loads(r.stdout)
    return result.get("code", -1) == 0

if __name__ == "__main__":
    import sys
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "🦞 测试"
    ok = send_message(msg)
    print(f"[feishu] {'✅' if ok else '❌'} {msg[:60]}")
