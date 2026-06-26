#!/usr/bin/env python3
"""
Re-authenticate Colab OAuth with Drive scope added.

Run this ONCE on a machine with a browser (or use the URL it prints).
It will update ~/.colab-mcp-auth-token.json with the new scopes.

Usage:
    python3 tools/colab/reauth_with_drive.py

If running headless (no browser), it will print a URL — open it in any browser,
authorize, and paste the code back.
"""

import os
import sys
import json

VENV_PYTHON = os.path.join(os.path.dirname(__file__), ".colab-venv", "bin", "python")
if os.path.exists(VENV_PYTHON) and sys.executable != VENV_PYTHON:
    os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

TOKEN_PATH = os.path.expanduser("~/.colab-mcp-auth-token.json")
CLIENT_CONFIG = os.path.expanduser("~/colab-mcp-oauth-config.json")

# Original scopes + Drive file access
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/colaboratory",
    "https://www.googleapis.com/auth/drive.file",
    "openid",
]

def main():
    print(f"Current token: {TOKEN_PATH}")
    
    # Check current scopes
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH) as f:
            current = json.load(f)
        current_scopes = current.get("scopes", [])
        print(f"Current scopes: {current_scopes}")
        
        if "https://www.googleapis.com/auth/drive.file" in current_scopes:
            print("✅ Drive scope already present!")
            return
    
    print(f"\nAdding scope: https://www.googleapis.com/auth/drive.file")
    print(f"Using client config: {CLIENT_CONFIG}")
    
    if not os.path.exists(CLIENT_CONFIG):
        print(f"Error: {CLIENT_CONFIG} not found", file=sys.stderr)
        sys.exit(1)
    
    # Run OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_CONFIG, SCOPES)
    
    # Use local server with a fresh port to avoid CSRF state mismatch
    creds = flow.run_local_server(
        port=0,           # Use any available port
        open_browser=True,
        timeout_seconds=120,
    )
    
    # Save updated token
    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())
    
    print(f"\n✅ Token updated with Drive scope!")
    print(f"Scopes: {SCOPES}")
    print(f"Saved to: {TOKEN_PATH}")


if __name__ == "__main__":
    main()
