"""Microsoft Graph authentication using MSAL with PKCE (no client secret needed)."""

import html
import webbrowser
import http.server
import urllib.parse
import msal
import requests

import config


def _get_msal_app() -> msal.PublicClientApplication:
    """Create MSAL public client application (uses PKCE, no secret required)."""
    if not config.MS_CLIENT_ID or not config.MS_TENANT_ID:
        print("ERROR: Microsoft credentials not configured.")
        print("Set in ~/.calintegration/.env:")
        print("  CALINT_MS_CLIENT_ID=<your-client-id>")
        print("  CALINT_MS_TENANT_ID=<your-tenant-id>")
        raise SystemExit(1)

    cache = msal.SerializableTokenCache()
    if config.MS_TOKEN_FILE.exists():
        cache.deserialize(config.MS_TOKEN_FILE.read_text())

    app = msal.PublicClientApplication(
        config.MS_CLIENT_ID,
        authority=config.MS_AUTHORITY,
        token_cache=cache,
    )
    return app


def _save_cache(app: msal.PublicClientApplication):
    """Save MSAL token cache with restricted permissions."""
    if app.token_cache.has_state_changed:
        config.write_restricted(config.MS_TOKEN_FILE, app.token_cache.serialize())


def _capture_auth_code(port: int = 8400) -> str:
    """Start a local HTTP server to capture the OAuth redirect."""
    auth_code = None

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal auth_code
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            if "error" in params:
                error_desc = params.get("error_description", ["Unknown error"])[0]
                self.send_response(400)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(f"<html><body><h2>Authentication failed</h2><p>{html.escape(error_desc)}</p></body></html>".encode())
            elif "code" in params:
                auth_code = params["code"][0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body><h2>Authentication successful!</h2><p>You can close this tab.</p></body></html>")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Error: no code received")

        def log_message(self, format, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", port), Handler)
    server.timeout = 120
    server.handle_request()
    server.server_close()

    if not auth_code:
        raise RuntimeError("Failed to capture authorization code")
    return auth_code


def get_access_token() -> str:
    """Get a valid access token, using cached tokens or interactive login."""
    app = _get_msal_app()

    # Try cached accounts first
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(config.MS_SCOPES, account=accounts[0])
        if result and "access_token" in result:
            _save_cache(app)
            return result["access_token"]

    # Interactive login with PKCE
    redirect_uri = "http://localhost:8400"
    flow = app.initiate_auth_code_flow(
        config.MS_SCOPES, redirect_uri=redirect_uri
    )

    auth_url = flow["auth_uri"]
    print("Opening browser for Microsoft login...")
    print(f"If the browser doesn't open, visit this URL:\n{auth_url}")
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    code = _capture_auth_code()
    # Build the response dict that MSAL expects
    result = app.acquire_token_by_auth_code_flow(
        flow,
        {"code": code, "state": flow.get("state", "")},
    )

    if "access_token" not in result:
        error_msg = result.get("error_description", "Unknown error")
        print(f"ERROR: Authentication failed: {error_msg}")
        raise SystemExit(1)

    _save_cache(app)
    print("Microsoft authentication successful.")
    return result["access_token"]


def graph_request(method: str, endpoint: str, **kwargs) -> requests.Response:
    """Make an authenticated request to Microsoft Graph API."""
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    url = f"https://graph.microsoft.com/v1.0{endpoint}"
    resp = requests.request(method, url, headers=headers, verify=True, timeout=30, **kwargs)
    return resp


def setup():
    """Run interactive setup for Microsoft Graph."""
    print("=== Microsoft Graph Setup ===")

    if not config.MS_CLIENT_ID:
        print("\nYou need to register an app in Azure AD:")
        print("1. Go to https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade")
        print("2. Click '+ New registration'")
        print("3. Name: 'CalIntegration'")
        print("4. Supported account types: 'Accounts in this organizational directory only'")
        print("5. Redirect URI: Public client/native (Mobile & desktop) → http://localhost:8400")
        print("6. After creation, note the Application (client) ID and Directory (tenant) ID")
        print("7. Go to 'API permissions' → Add: Microsoft Graph → Delegated → Calendars.ReadWrite")
        print("\nNo client secret needed (uses PKCE).")
        print("\nAdd to ~/.calintegration/.env:")
        print("  CALINT_MS_CLIENT_ID=<your-client-id>")
        print("  CALINT_MS_TENANT_ID=<your-tenant-id>")
        raise SystemExit(1)

    get_access_token()

    # Verify access
    resp = graph_request("GET", "/me/calendars")
    if resp.status_code != 200:
        print(f"ERROR: Could not list calendars (HTTP {resp.status_code})")
        raise SystemExit(1)

    calendars = resp.json().get("value", [])
    print(f"\nSuccess! Found {len(calendars)} calendars:")
    for cal in calendars:
        default = " <-- syncing to this" if cal.get("isDefaultCalendar") else ""
        print(f"  - {cal['name']}{default}")
    print()
