#!/usr/bin/env python3
"""
Bangumi Tracker - Local user edition with OAuth authentication
Manage collections and track watch progress
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# Fix Windows console encoding for emoji output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from typing import Optional, Dict, Any
import platform

# Windows Credential Manager (no third-party dependency)
if platform.system() == "Windows":
    import ctypes
    from ctypes import wintypes

    CRED_TYPE_GENERIC = 1
    CRED_PERSIST_LOCAL_MACHINE = 2

    class CREDENTIAL(ctypes.Structure):
        _fields_ = [
            ("Flags", wintypes.DWORD),
            ("Type", wintypes.DWORD),
            ("TargetName", wintypes.LPCWSTR),
            ("Comment", wintypes.LPCWSTR),
            ("LastWritten", wintypes.FILETIME),
            ("CredentialBlobSize", wintypes.DWORD),
            ("CredentialBlob", ctypes.POINTER(wintypes.BYTE)),
            ("Persist", wintypes.DWORD),
            ("AttributeCount", wintypes.DWORD),
            ("Attributes", ctypes.POINTER(ctypes.c_void_p)),
            ("TargetAlias", wintypes.LPCWSTR),
            ("UserName", wintypes.LPCWSTR),
        ]

    advapi32 = ctypes.windll.advapi32
    CredReadW = advapi32.CredReadW
    CredWriteW = advapi32.CredWriteW
    CredDeleteW = advapi32.CredDeleteW
    CredFree = advapi32.CredFree

# Constants
BASE_URL = "https://api.bgm.tv/v0"
OAUTH_URL = "https://bgm.tv/oauth"
DEFAULT_REDIRECT_URI = "http://localhost:17321/callback"
DEFAULT_PORT = 17321
CONFIG_DIR = Path.home() / ".bangumi"
CONFIG_FILE = CONFIG_DIR / "config.json"
TOKEN_FILE = CONFIG_DIR / "token.json"
HEADERS = {"User-Agent": "MountLynx/bangumi_skill (https://github.com/MountLynx/bangumi_skill)"}

# Credential target names for Windows Credential Manager
CRED_TARGET_CLIENT_SECRET = "BangumiTracker:client_secret"
CRED_TARGET_ACCESS_TOKEN = "BangumiTracker:access_token"
CRED_TARGET_REFRESH_TOKEN = "BangumiTracker:refresh_token"


def is_windows() -> bool:
    """Check if running on Windows"""
    return platform.system() == "Windows"


def save_credential(target: str, username: str, password: str) -> bool:
    """Save credential to Windows Credential Manager"""
    if not is_windows():
        return False
    try:
        credential = CREDENTIAL()
        credential.Type = CRED_TYPE_GENERIC
        credential.TargetName = target
        credential.UserName = username
        password_bytes = password.encode('utf-8')
        credential.CredentialBlobSize = len(password_bytes)
        credential.CredentialBlob = ctypes.cast(
            ctypes.create_string_buffer(password_bytes),
            ctypes.POINTER(wintypes.BYTE)
        )
        credential.Persist = CRED_PERSIST_LOCAL_MACHINE
        CredWriteW(ctypes.byref(credential), 0)
        return True
    except Exception as e:
        print(f"Failed to save credential: {e}")
        return False


def load_credential(target: str) -> Optional[tuple]:
    """Load credential from Windows Credential Manager. Returns (username, password) or None"""
    if not is_windows():
        return None
    try:
        credential = ctypes.POINTER(CREDENTIAL)()
        if CredReadW(target, CRED_TYPE_GENERIC, 0, ctypes.byref(credential)):
            username = credential.contents.UserName
            blob_size = credential.contents.CredentialBlobSize
            blob = ctypes.string_at(credential.contents.CredentialBlob, blob_size)
            password = blob.decode('utf-8')
            CredFree(credential)
            return (username, password)
    except Exception as e:
        print(f"Failed to load credential: {e}")
    return None


def delete_credential(target: str) -> bool:
    """Delete credential from Windows Credential Manager"""
    if not is_windows():
        return False
    try:
        CredDeleteW(target, CRED_TYPE_GENERIC, 0)
        return True
    except Exception as e:
        print(f"Failed to delete credential: {e}")
        return False


def ensure_config_dir():
    """Ensure config directory exists"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Optional[Dict[str, Any]]:
    """Load OAuth config from file (only client_id, client_secret is in Credential Manager)"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {}

    # Load client_secret from Windows Credential Manager
    if is_windows():
        cred = load_credential(CRED_TARGET_CLIENT_SECRET)
        if cred and cred[1]:
            config["client_secret"] = cred[1]

    return config if config else None


def save_config(config: Dict[str, Any]):
    """Save OAuth config to file (only client_id) and Credential Manager (client_secret)"""
    ensure_config_dir()

    # Save only non-sensitive data to file
    config_to_save = {
        "client_id": config.get("client_id"),
        "redirect_uri": config.get("redirect_uri")
    }
    config_to_save = {k: v for k, v in config_to_save.items() if v}

    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config_to_save, f, indent=2)
    print(f"✅ Config saved to {CONFIG_FILE}")

    # Save client_secret to Windows Credential Manager
    if config.get("client_secret"):
        save_credential(CRED_TARGET_CLIENT_SECRET, "client_secret", config["client_secret"])
        print(f"✅ Client secret saved to Windows Credential Manager")


def load_token() -> Optional[Dict[str, Any]]:
    """Load access token from Windows Credential Manager"""
    if not is_windows():
        # Fallback to file for non-Windows
        if TOKEN_FILE.exists():
            with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    access_token = load_credential(CRED_TARGET_ACCESS_TOKEN)
    refresh_token = load_credential(CRED_TARGET_REFRESH_TOKEN)

    if access_token:
        token_data = {"access_token": access_token[1]}
        if refresh_token:
            token_data["refresh_token"] = refresh_token[1]

        # Try to load expires_at from file (non-sensitive)
        if TOKEN_FILE.exists():
            try:
                with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
                    cached = json.load(f)
                    if "expires_at" in cached:
                        token_data["expires_at"] = cached["expires_at"]
            except:
                pass

        # Default expires_at if not found
        if "expires_at" not in token_data:
            token_data["expires_at"] = 0

        return token_data

    return None


def save_token(token: Dict[str, Any]):
    """Save access token to Windows Credential Manager"""
    ensure_config_dir()

    if is_windows():
        # Save sensitive data to Credential Manager
        if token.get("access_token"):
            save_credential(CRED_TARGET_ACCESS_TOKEN, "access_token", token["access_token"])
            print(f"✅ Access token saved to Windows Credential Manager")

        if token.get("refresh_token"):
            save_credential(CRED_TARGET_REFRESH_TOKEN, "refresh_token", token["refresh_token"])
            print(f"✅ Refresh token saved to Windows Credential Manager")

        # Save expires_at to file (non-sensitive)
        if "expires_at" in token:
            with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
                json.dump({"expires_at": token["expires_at"]}, f, indent=2)
    else:
        # Fallback to file for non-Windows
        with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
            json.dump(token, f, indent=2)
        print(f"✅ Token saved to {TOKEN_FILE}")


def remove_token():
    """Remove saved token from Windows Credential Manager"""
    if is_windows():
        deleted = False
        if delete_credential(CRED_TARGET_ACCESS_TOKEN):
            deleted = True
            print("✅ Access token removed from Windows Credential Manager")
        if delete_credential(CRED_TARGET_REFRESH_TOKEN):
            deleted = True
            print("✅ Refresh token removed from Windows Credential Manager")

        # Clear expires_at file
        if TOKEN_FILE.exists():
            TOKEN_FILE.unlink()

        if not deleted:
            print("ℹ️ No token to remove")
    else:
        # Fallback to file for non-Windows
        if TOKEN_FILE.exists():
            TOKEN_FILE.unlink()
            print("✅ Token removed")
        else:
            print("ℹ️ No token to remove")


def api_get(path: str, params: Optional[Dict] = None, token: Optional[str] = None) -> Dict:
    """Make authenticated GET request"""
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url, headers=HEADERS)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}


def api_post(path: str, data: Dict, token: Optional[str] = None) -> Dict:
    """Make authenticated POST request"""
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(url, data=body, headers=HEADERS, method='POST')
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req) as response:
            response_body = response.read()
            if response_body:
                return json.loads(response_body.decode('utf-8'))
            return {"success": True}  # Empty response is success for POST
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}


def get_valid_token() -> Optional[str]:
    """Get valid access token, refresh if expired"""
    token_data = load_token()
    if not token_data:
        return None
    
    # Check if token is expired (with 5 min buffer)
    if token_data.get("expires_at", 0) - time.time() < 300:
        print("🔄 Token expired, refreshing...")
        return refresh_access_token(token_data.get("refresh_token"))
    
    return token_data.get("access_token")


def refresh_access_token(refresh_token: str) -> Optional[str]:
    """Refresh access token using refresh token"""
    config = load_config()
    if not config:
        print("❌ No config found. Run 'config' first.")
        return None
    
    data = {
        "grant_type": "refresh_token",
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "refresh_token": refresh_token
    }
    
    url = f"{OAUTH_URL}/access_token"
    body = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers=HEADERS, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            new_token = json.loads(response.read().decode('utf-8'))
            new_token["expires_at"] = time.time() + new_token.get("expires_in", 3600)
            save_token(new_token)
            return new_token["access_token"]
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to refresh token: {e.reason}")
        return None


# Command implementations
def cmd_config(args):
    """Save OAuth configuration"""
    config = {
        "client_id": args.client_id,
        "client_secret": args.client_secret,
        "redirect_uri": args.redirect_uri or DEFAULT_REDIRECT_URI
    }
    save_config(config)
    print("\nNext step: Run 'python bangumi_tracker.py auth' to authorize")


def cmd_auth(args):
    """Run OAuth authorization flow"""
    config = load_config()
    if not config:
        print("❌ No config found. Run 'config' first:")
        print("   python bangumi_tracker.py config --client-id <id> --client-secret <secret>")
        return 1
    
    # Build authorization URL
    auth_params = {
        "client_id": config["client_id"],
        "response_type": "code",
        "redirect_uri": config.get("redirect_uri", DEFAULT_REDIRECT_URI)
    }
    auth_url = f"{OAUTH_URL}/authorize?{urllib.parse.urlencode(auth_params)}"
    
    print("=" * 60)
    print("Bangumi OAuth Authorization")
    print("=" * 60)
    print(f"\n1. Opening browser to: {auth_url}")
    print("2. Login to Bangumi and authorize the app")
    print("3. You will be redirected to localhost")
    print("\n⚠️  Note: This requires a local HTTP server to receive the callback.")
    print("   The server will run on port 17321.")
    print("=" * 60)
    
    # Open browser
    import webbrowser
    webbrowser.open(auth_url)
    
    # Start temporary server to receive callback
    print("\n🚀 Starting callback server...")
    return start_callback_server(config)


def start_callback_server(config: Dict) -> int:
    """Start temporary HTTP server to receive OAuth callback"""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import threading
    
    authorization_code = None
    server_running = True
    
    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal authorization_code, server_running
            
            if "/callback" in self.path:
                # Parse query parameters
                query = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(query)
                
                if "code" in params:
                    authorization_code = params["code"][0]
                    self.send_response(200)
                    self.end_headers()
                    html = '''<html>
<body style="font-family: sans-serif; text-align: center; padding: 50px;">
    <h1>Authorization Successful!</h1>
    <p>You can close this window and return to the terminal.</p>
</body>
</html>'''
                    self.wfile.write(html.encode('utf-8'))
                    server_running = False
                elif "error" in params:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(f"Error: {params['error'][0]}".encode())
                    server_running = False
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Missing authorization code")
            else:
                self.send_response(404)
                self.end_headers()
        
        def log_message(self, format, *args):
            pass  # Suppress log output
    
    port = DEFAULT_PORT
    server = HTTPServer(("localhost", port), CallbackHandler)
    
    # Run server in thread
    def run_server():
        while server_running:
            server.handle_request()
    
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
    
    print(f"🌐 Waiting for callback on http://localhost:{port}/callback ...")
    print("   (Press Ctrl+C to cancel)\n")
    
    # Wait for authorization code
    try:
        while server_running and authorization_code is None:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        return 1
    
    server.server_close()
    
    if not authorization_code:
        print("❌ Failed to get authorization code")
        return 1
    
    print(f"✅ Got authorization code")
    
    # Exchange code for token
    print("🔄 Exchanging code for token...")
    token_data = {
        "grant_type": "authorization_code",
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "code": authorization_code,
        "redirect_uri": config.get("redirect_uri", DEFAULT_REDIRECT_URI)
    }
    
    url = f"{OAUTH_URL}/access_token"
    body = urllib.parse.urlencode(token_data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers=HEADERS, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            token = json.loads(response.read().decode('utf-8'))
            token["expires_at"] = time.time() + token.get("expires_in", 3600)
            save_token(token)
            print("\n🎉 Authorization successful!")
            print(f"   User ID: {token.get('user_id', 'N/A')}")
            return 0
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to get token: {e.reason}")
        return 1


def cmd_status(args):
    """Check login status"""
    config = load_config()
    token = load_token()

    print("=" * 60)
    print("Bangumi Tracker Status")
    print("=" * 60)

    # Config status
    if config:
        print(f"✅ Config: {CONFIG_FILE}")
        print(f"   Client ID: {config.get('client_id', 'N/A')[:20]}...")
        if is_windows() and config.get("client_secret"):
            print(f"   Client Secret: 🔐 Windows Credential Manager")
        else:
            print(f"   Client Secret: ⚠️ Not set")
    else:
        print(f"❌ Config: Not found ({CONFIG_FILE})")

    # Token status
    if token:
        storage = "Windows Credential Manager" if is_windows() else str(TOKEN_FILE)
        print(f"✅ Token: {storage}")
        print(f"   Expires: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(token.get('expires_at', 0)))}")

        # Try to get user info
        access_token = get_valid_token()
        if access_token:
            user = api_get("/me", token=access_token)
            if "error" not in user:
                print(f"   Logged in as: {user.get('nickname', user.get('username', 'Unknown'))}")
            else:
                print(f"   ⚠️  Token may be invalid: {user['error']}")
        else:
            print("   ⚠️  Token expired and refresh failed")
    else:
        storage = "Windows Credential Manager" if is_windows() else str(TOKEN_FILE)
        print(f"❌ Token: Not found ({storage})")

    print("=" * 60)
    return 0


def cmd_logout(args):
    """Logout and remove token"""
    remove_token()
    return 0


def cmd_collections(args):
    """List user's collections"""
    token = get_valid_token()
    if not token:
        print("❌ Not logged in. Run 'auth' first.")
        return 1

    # Get user info first
    user = api_get("/me", token=token)
    if "error" in user:
        print(f"❌ Failed to get user info: {user['error']}")
        return 1

    username = user.get("username")
    nickname = user.get('nickname', username)
    print(f"📚 Collections for {nickname}\n")

    # Build params
    # Bangumi API: type=收藏状态(1=wish,2=doing,3=collect,4=on_hold,5=dropped)
    # subject_type=条目类型(1=book,2=anime,3=music,4=game,6=real)
    params = {}
    if args.type:
        type_map = {"anime": 2, "book": 1, "game": 4, "music": 3, "real": 6}
        params["subject_type"] = type_map.get(args.type, 2)
    if args.status:
        # Convert status string to numeric
        status_map = {"wish": 1, "doing": 2, "collect": 3, "on_hold": 4, "dropped": 5}
        params["type"] = status_map.get(args.status)

    # Get collections using username (as per official API spec)
    collections = api_get(f"/users/{username}/collections", params=params, token=token)
    
    if "error" in collections:
        print(f"❌ Failed to get collections: {collections['error']}")
        return 1
    
    data = collections.get("data", [])
    if not data:
        print("ℹ️ No collections found")
        return 0
    
    # Format output
    # Status mapping: numeric to string
    status_map = {
        1: "wish",
        2: "doing",
        3: "collect",
        4: "on_hold",
        5: "dropped"
    }
    status_emoji = {
        "wish": "🔖",
        "collect": "✅",
        "doing": "▶️",
        "on_hold": "⏸️",
        "dropped": "❌"
    }

    for item in data:
        subject = item.get("subject", {})
        # Convert numeric type to string
        type_num = item.get("type")
        status = status_map.get(type_num, "unknown")
        emoji = status_emoji.get(status, "❓")

        # Use 'or' to handle empty string for name_cn
        title = subject.get("name_cn") or subject.get("name", "Unknown")
        print(f"{emoji} [{status.upper()}] {title}")
        print(f"   ID: {subject.get('id')} | Score: {subject.get('score', 'N/A')}")
        if item.get("ep_status"):
            print(f"   Progress: {item['ep_status']}/{subject.get('eps', '?')} eps")
        print()
    
    print(f"Total: {len(data)} items")
    return 0


def cmd_collect(args):
    """Add or update collection"""
    token = get_valid_token()
    if not token:
        print("❌ Not logged in. Run 'auth' first.")
        return 1

    subject_id = args.subject_id
    status = args.status

    # Validate status
    valid_statuses = ["wish", "doing", "collect", "on_hold", "dropped"]
    if status not in valid_statuses:
        print(f"❌ Invalid status. Use: {', '.join(valid_statuses)}")
        return 1

    # Convert status string to numeric type
    status_map = {"wish": 1, "doing": 2, "collect": 3, "on_hold": 4, "dropped": 5}

    print(f"📝 Setting collection status to '{status}' for subject {subject_id}...")

    # Bangumi API: POST for new collections, PATCH for updates
    data = {"type": status_map[status]}
    result = api_post(f"/users/-/collections/{subject_id}", data, token=token)

    if "error" in result:
        # Try PATCH for update (as per official API spec)
        url = f"{BASE_URL}/users/-/collections/{subject_id}"
        body = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers={**HEADERS, "Authorization": f"Bearer {token}"}, method='PATCH')
        req.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(req) as response:
                print("✅ Collection updated successfully")
                return 0
        except urllib.error.HTTPError as e:
            print(f"❌ Failed to update collection: {e.reason}")
            return 1
    else:
        print("✅ Collection added successfully")
        return 0


def cmd_uncollect(args):
    """Remove from collection"""
    token = get_valid_token()
    if not token:
        print("❌ Not logged in. Run 'auth' first.")
        return 1

    # Get user info to get username
    user = api_get("/me", token=token)
    if "error" in user:
        print(f"❌ Failed to get user info: {user['error']}")
        return 1

    subject_id = args.subject_id
    print(f"🗑️  Removing subject {subject_id} from collections...")

    # Official API: No DELETE endpoint exists, use PATCH with type=0 to remove
    # type=0 means "not in any collection"
    url = f"{BASE_URL}/users/-/collections/{subject_id}"
    data = {"type": 0}  # 0 = no collection status (remove from collection)
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={**HEADERS, "Authorization": f"Bearer {token}"}, method='PATCH')
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as response:
            print("✅ Removed from collection")
            return 0
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to remove: {e.reason}")
        return 1


def cmd_progress(args):
    """Get watch progress"""
    token = get_valid_token()
    if not token:
        print("❌ Not logged in. Run 'auth' first.")
        return 1

    # Get user info to get username
    user = api_get("/me", token=token)
    if "error" in user:
        print(f"❌ Failed to get user info: {user['error']}")
        return 1

    username = user.get("username")
    subject_id = args.subject_id

    # Get collection info using username (as per official API spec)
    result = api_get(f"/users/{username}/collections/{subject_id}", token=token)
    
    if "error" in result:
        print(f"❌ Failed to get progress: {result['error']}")
        return 1

    subject = result.get("subject", {})
    # Convert numeric status to string
    status_map = {1: "wish", 2: "doing", 3: "collect", 4: "on_hold", 5: "dropped"}
    status_str = status_map.get(result.get('type'), 'unknown')

    print(f"📺 {subject.get('name_cn') or subject.get('name', 'Unknown')}")
    print(f"   Status: {status_str}")
    print(f"   Progress: {result.get('ep_status', 0)}/{subject.get('eps', '?')} episodes")
    
    if result.get("vol_status"):
        print(f"   Volumes: {result['vol_status']}/{subject.get('volumes', '?')}")
    
    return 0


def cmd_me(args):
    """Get current user info"""
    token = get_valid_token()
    if not token:
        print("❌ Not logged in. Run 'auth' first.")
        return 1
    
    user = api_get("/me", token=token)
    
    if "error" in user:
        print(f"❌ Failed to get user info: {user['error']}")
        return 1
    
    print("=" * 60)
    print("User Profile")
    print("=" * 60)
    print(f"Username: {user.get('username')}")
    print(f"Nickname: {user.get('nickname')}")
    print(f"ID: {user.get('id')}")
    
    if user.get('user_group'):
        group_names = {1: "管理员", 2: "Bangumi 管理猿", 3: "天窗联盟管理猿", 
                       4: "禁言用户", 5: "禁止访问用户", 6: "人物管理猿", 7: "维基条目管理猿",
                       8: "用户", 9: "维基人", 10: "目录管理猿", 11: "天窗用户"}
        print(f"Group: {group_names.get(user['user_group'], user['user_group'])}")
    
    print("=" * 60)
    return 0


def cmd_collect_character(args):
    """Collect/uncollect a character"""
    token = get_valid_token()
    if not token:
        print("❌ Not logged in. Run 'auth' first.")
        return 1

    character_id = args.character_id
    action = args.action  # "collect" or "uncollect"

    if action == "collect":
        url = f"{BASE_URL}/characters/{character_id}/collect"
        method = "POST"
        print(f"⭐ Collecting character {character_id}...")
    else:
        url = f"{BASE_URL}/characters/{character_id}/collect"
        method = "DELETE"
        print(f"🗑️  Removing character {character_id} from collection...")

    req = urllib.request.Request(url, headers={
        **HEADERS,
        "Authorization": f"Bearer {token}"
    }, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            if action == "collect":
                print("✅ Character collected!")
            else:
                print("✅ Character removed from collection!")
            return 0
    except urllib.error.HTTPError as e:
        print(f"❌ Failed: {e.reason}")
        return 1


def cmd_collect_person(args):
    """Collect/uncollect a person"""
    token = get_valid_token()
    if not token:
        print("❌ Not logged in. Run 'auth' first.")
        return 1

    person_id = args.person_id
    action = args.action  # "collect" or "uncollect"

    if action == "collect":
        url = f"{BASE_URL}/persons/{person_id}/collect"
        method = "POST"
        print(f"⭐ Collecting person {person_id}...")
    else:
        url = f"{BASE_URL}/persons/{person_id}/collect"
        method = "DELETE"
        print(f"🗑️  Removing person {person_id} from collection...")

    req = urllib.request.Request(url, headers={
        **HEADERS,
        "Authorization": f"Bearer {token}"
    }, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            if action == "collect":
                print("✅ Person collected!")
            else:
                print("✅ Person removed from collection!")
            return 0
    except urllib.error.HTTPError as e:
        print(f"❌ Failed: {e.reason}")
        return 1


def cmd_episodes(args):
    """Get episode collection status"""
    token = get_valid_token()
    if not token:
        print("❌ Not logged in. Run 'auth' first.")
        return 1

    subject_id = args.subject_id

    # Get subject info first
    subject = api_get(f"/subjects/{subject_id}", token=token)
    if "error" in subject:
        print(f"❌ Failed to get subject: {subject['error']}")
        return 1

    subject_name = subject.get("name_cn") or subject.get("name", "Unknown")

    # Get episode collection
    result = api_get(f"/users/-/collections/{subject_id}/episodes", token=token)

    if "error" in result:
        print(f"❌ Failed to get episodes: {result['error']}")
        return 1

    data = result.get("data", [])
    if not data:
        print(f"📺 {subject_name}")
        print("   No episode progress recorded")
        return 0

    # Group by episode type (本篇, SP, OP, ED, etc)
    ep_types = {0: "本篇", 1: "SP", 2: "OP", 3: "ED", 4: "预告", 5: "MAD", 6: "其他"}
    groups = {}
    for item in data:
        ep_data = item.get("episode", {})
        # episode type is in episode.type, not item.type
        t = ep_data.get("type", 0)
        groups.setdefault(t, []).append({**item, "episode": ep_data})

    print(f"📺 {subject_name}")
    print(f"   Total episodes: {subject.get('total_episodes', len(data))}")
    print()

    for type_id, type_name in ep_types.items():
        eps = groups.get(type_id, [])
        if not eps:
            continue
        # status: 1=wish, 2=watched
        watched = sum(1 for ep in eps if ep.get("type") == 2)  # type=2 means watched
        print(f"— {type_name} ({watched}/{len(eps)}) —")
        for ep in eps:
            ep_data = ep.get("episode", {})
            ep_num = ep_data.get("ep", ep_data.get("sort", "?"))
            # collection status: 1=wish, 2=watched
            status = ep.get("type", 0)
            status_str = "✅" if status == 2 else "⬜"
            name = ep_data.get("name_cn") or ep_data.get("name", "")
            print(f"   {status_str} 第{ep_num}集 {name}")
        print()

    return 0


def cmd_watch(args):
    """Mark episode as watched/not watched"""
    token = get_valid_token()
    if not token:
        print("❌ Not logged in. Run 'auth' first.")
        return 1

    episode_id = args.episode_id
    status = args.status  # "watched" or "unwatched"

    # Get episode info first
    episode = api_get(f"/episodes/{episode_id}", token=token)
    if "error" in episode:
        print(f"❌ Failed to get episode: {episode['error']}")
        return 1

    ep_name = episode.get("name_cn") or episode.get("name", f"Episode {episode_id}")

    # Status mapping: 1=wish, 2=watched
    status_map = {"watched": 2, "unwatched": 1}
    type_val = status_map[status]

    if status == "watched":
        print(f"✅ Marking {ep_name} as watched...")
    else:
        print(f"⬜ Marking {ep_name} as not watched...")

    url = f"{BASE_URL}/users/-/collections/-/episodes/{episode_id}"
    data = {"type": type_val}
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={
        **HEADERS,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }, method='PUT')

    try:
        with urllib.request.urlopen(req) as response:
            print(f"✅ Episode status updated!")
            return 0
    except urllib.error.HTTPError as e:
        print(f"❌ Failed: {e.reason}")
        return 1


def cmd_my_characters(args):
    """List collected characters"""
    token = get_valid_token()
    if not token:
        print("❌ Not logged in. Run 'auth' first.")
        return 1

    # Get user info
    user = api_get("/me", token=token)
    if "error" in user:
        print(f"❌ Failed to get user: {user['error']}")
        return 1

    username = user.get("username")

    # Get character collections
    result = api_get(f"/users/{username}/collections/-/characters", token=token)

    if "error" in result:
        print(f"❌ Failed to get characters: {result['error']}")
        return 1

    data = result.get("data", [])
    if not data:
        print("⭐ No collected characters")
        return 0

    print(f"⭐ Collected Characters ({len(data)})")
    print()
    for item in data:
        # API返回的直接是角色信息，不是嵌套结构
        name = item.get("name", "Unknown")
        name_cn = item.get("name_cn", "")
        if name_cn and name_cn != name:
            name = f"{name} / {name_cn}"
        print(f"  {name} (ID: {item.get('id')})")

    print()
    print(f"Total: {len(data)} characters")
    return 0


def cmd_my_persons(args):
    """List collected persons"""
    token = get_valid_token()
    if not token:
        print("❌ Not logged in. Run 'auth' first.")
        return 1

    # Get user info
    user = api_get("/me", token=token)
    if "error" in user:
        print(f"❌ Failed to get user: {user['error']}")
        return 1

    username = user.get("username")

    # Get person collections
    result = api_get(f"/users/{username}/collections/-/persons", token=token)

    if "error" in result:
        print(f"❌ Failed to get persons: {result['error']}")
        return 1

    data = result.get("data", [])
    if not data:
        print("⭐ No collected persons")
        return 0

    print(f"⭐ Collected Persons ({len(data)})")
    print()
    for item in data:
        # API返回的直接是人物信息，不是嵌套结构
        name = item.get("name", "Unknown")
        name_cn = item.get("name_cn", "")
        if name_cn and name_cn != name:
            name = f"{name} / {name_cn}"
        print(f"  {name} (ID: {item.get('id')})")

    print()
    print(f"Total: {len(data)} persons")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Bangumi Tracker - OAuth edition")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Configure OAuth credentials")
    config_parser.add_argument("--client-id", required=True, help="OAuth client ID")
    config_parser.add_argument("--client-secret", required=True, help="OAuth client secret")
    config_parser.add_argument("--redirect-uri", default=DEFAULT_REDIRECT_URI, help="Redirect URI")
    config_parser.set_defaults(func=cmd_config)
    
    # Auth command
    auth_parser = subparsers.add_parser("auth", help="Authorize with Bangumi")
    auth_parser.set_defaults(func=cmd_auth)
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check login status")
    status_parser.set_defaults(func=cmd_status)
    
    # Logout command
    logout_parser = subparsers.add_parser("logout", help="Logout and remove token")
    logout_parser.set_defaults(func=cmd_logout)
    
    # Collections command
    collections_parser = subparsers.add_parser("collections", help="List my collections")
    collections_parser.add_argument("--type", choices=["anime", "book", "game", "music", "real"], help="Subject type")
    collections_parser.add_argument("--status", choices=["wish", "doing", "collect", "on_hold", "dropped"], help="Collection status")
    collections_parser.set_defaults(func=cmd_collections)
    
    # Collect command
    collect_parser = subparsers.add_parser("collect", help="Add/update collection")
    collect_parser.add_argument("subject_id", type=int, help="Subject ID")
    collect_parser.add_argument("status", choices=["wish", "doing", "collect", "on_hold", "dropped"], help="Status")
    collect_parser.set_defaults(func=cmd_collect)
    
    # Uncollect command
    uncollect_parser = subparsers.add_parser("uncollect", help="Remove from collection")
    uncollect_parser.add_argument("subject_id", type=int, help="Subject ID")
    uncollect_parser.set_defaults(func=cmd_uncollect)
    
    # Progress command
    progress_parser = subparsers.add_parser("progress", help="Get watch progress")
    progress_parser.add_argument("subject_id", type=int, help="Subject ID")
    progress_parser.set_defaults(func=cmd_progress)
    
    # Me command
    me_parser = subparsers.add_parser("me", help="Get user info")
    me_parser.set_defaults(func=cmd_me)

    # Collect character command
    char_parser = subparsers.add_parser("collect-character", help="Collect/uncollect a character")
    char_parser.add_argument("character_id", type=int, help="Character ID")
    char_parser.add_argument("action", choices=["collect", "uncollect"], help="Action")
    char_parser.set_defaults(func=cmd_collect_character)

    # My characters command
    my_chars_parser = subparsers.add_parser("my-characters", help="List collected characters")
    my_chars_parser.set_defaults(func=cmd_my_characters)

    # Collect person command
    person_parser = subparsers.add_parser("collect-person", help="Collect/uncollect a person")
    person_parser.add_argument("person_id", type=int, help="Person ID")
    person_parser.add_argument("action", choices=["collect", "uncollect"], help="Action")
    person_parser.set_defaults(func=cmd_collect_person)

    # My persons command
    my_persons_parser = subparsers.add_parser("my-persons", help="List collected persons")
    my_persons_parser.set_defaults(func=cmd_my_persons)

    # Episodes command
    eps_parser = subparsers.add_parser("episodes", help="Get episode collection status")
    eps_parser.add_argument("subject_id", type=int, help="Subject ID")
    eps_parser.set_defaults(func=cmd_episodes)

    # Watch command
    watch_parser = subparsers.add_parser("watch", help="Mark episode as watched/unwatched")
    watch_parser.add_argument("episode_id", type=int, help="Episode ID")
    watch_parser.add_argument("status", choices=["watched", "unwatched"], help="Status")
    watch_parser.set_defaults(func=cmd_watch)

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
