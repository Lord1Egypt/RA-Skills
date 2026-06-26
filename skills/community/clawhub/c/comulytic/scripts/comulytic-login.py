#!/usr/bin/env python3
"""
Comulytic MCP Login — 自动完成 OAuth 2.0 流程，获取 MCP access token。

用法:
    comulytic-login              # 交互式输入邮箱密码
    comulytic-login --status     # 查看当前 token 状态
    comulytic-login --logout     # 清除已保存的 token
"""

import hashlib, base64, getpass, json, os, secrets, sys, urllib.request, urllib.error

API_BASE = "https://api.comulytic.ai"
TOKEN_FILE = os.path.expanduser("~/.comulytic/mcp-token.json")
SCOPES = "read:meetings:summary read:meetings:transcript read:contacts read:actions search:conversations"


def api_post(path, body, token=None):
    url = API_BASE + path
    data = json.dumps(body).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        print(f"\n❌ API 错误 ({e.code}): {err_body}", file=sys.stderr)
        sys.exit(1)


def api_get(path, token=None):
    url = API_BASE + path
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        print(f"\n❌ API 错误 ({e.code}): {err_body}", file=sys.stderr)
        sys.exit(1)


def generate_pkce():
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).rstrip(b"=").decode()
    return verifier, challenge


def save_token(data):
    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=2)
    os.chmod(TOKEN_FILE, 0o600)


def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE) as f:
        return json.load(f)


def do_login():
    print("🎙️  Comulytic MCP 登录\n")

    email = input("邮箱: ").strip()
    if not email:
        print("❌ 邮箱不能为空")
        sys.exit(1)
    password = getpass.getpass("密码: ")
    if not password:
        print("❌ 密码不能为空")
        sys.exit(1)

    # Step 1: 用邮箱密码登录，获取 kirby JWT
    print("\n⏳ 正在登录...")
    login_resp = api_post("/api/kirby/v1/auth/login/email", {
        "email": email,
        "password": password,
    })
    kirby_token = login_resp.get("data", {}).get("accessToken") or login_resp.get("accessToken")
    if not kirby_token:
        print("❌ 登录失败，请检查邮箱和密码")
        sys.exit(1)
    print("✅ 登录成功")

    # Step 2: 注册 OAuth 客户端
    print("⏳ 注册 MCP 客户端...")
    client = api_post("/mcp/oauth/register", {
        "client_name": "OpenClaw-Desktop",
        "redirect_uris": "http://127.0.0.1/callback",
    })
    client_id = client["client_id"]
    print(f"✅ 客户端已注册 ({client_id[:8]}...)")

    # Step 3: PKCE + 授权
    print("⏳ 获取授权...")
    verifier, challenge = generate_pkce()
    auth_resp = api_get(
        f"/mcp/oauth/authorize"
        f"?client_id={client_id}"
        f"&scope={SCOPES.replace(' ', '+')}"
        f"&code_challenge={challenge}"
        f"&code_challenge_method=S256",
        token=kirby_token,
    )
    code = auth_resp.get("code")
    if not code:
        print(f"❌ 授权失败: {auth_resp}")
        sys.exit(1)
    print("✅ 授权成功")

    # Step 4: 用 code 换 access_token
    print("⏳ 获取 MCP Token...")
    token_resp = api_post("/mcp/oauth/token", {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "code_verifier": verifier,
    })
    access_token = token_resp.get("access_token")
    if not access_token:
        print(f"❌ Token 获取失败: {token_resp}")
        sys.exit(1)

    # Step 5: 保存
    save_token({
        "access_token": access_token,
        "refresh_token": token_resp.get("refresh_token"),
        "client_id": client_id,
        "email": email,
        "expires_in": token_resp.get("expires_in"),
    })

    print(f"✅ MCP Token 已保存到 {TOKEN_FILE}")
    print(f"\n🎉 完成！你的 OpenClaw 现在可以访问 Comulytic 数据了。")

    # 提示设置环境变量
    shell_rc = "~/.zshrc" if os.environ.get("SHELL", "").endswith("zsh") else "~/.bashrc"
    print(f"\n如果环境变量未自动生效，运行:")
    print(f'  export COMULYTIC_MCP_TOKEN="{access_token[:20]}..."')


def do_status():
    token = load_token()
    if not token:
        print("❌ 未登录。运行 comulytic-login 登录。")
        sys.exit(1)
    print(f"✅ 已登录: {token.get('email', 'unknown')}")
    print(f"   Token 文件: {TOKEN_FILE}")
    print(f"   Client ID: {token.get('client_id', 'unknown')[:8]}...")
    at = token.get("access_token", "")
    print(f"   Access Token: {at[:20]}..." if at else "   Access Token: (空)")


def do_logout():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print("✅ 已登出，Token 已清除。")
    else:
        print("ℹ️  未找到已保存的 Token。")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--status" in args:
        do_status()
    elif "--logout" in args:
        do_logout()
    else:
        do_login()
