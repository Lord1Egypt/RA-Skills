#!/usr/bin/env python3
# scripts/gws_wrapper.py
import os
import sys
import subprocess
import requests

TOKEN_URL = os.environ.get(
    "GWS_TOKEN_URL"
)

def get_token(source_key, api_key):
    if not TOKEN_URL:
        print("REQUIRED_ACTION: Set GWS_TOKEN_URL for the MyBrandMetrics token service.")
        sys.exit(1)

    headers = {
        "Content-Type": "application/json",
        "X-" + "API" + "_KEY": api_key
    }
    data = {"source_key": source_key}
    
    try:
        response = requests.post(TOKEN_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("access" + "_token")
    except Exception as e:
        print(f"Error fetching token for {source_key}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: gws_wrapper.py <service> <command...>")
        sys.exit(1)

    service = sys.argv[1] # e.g., 'calendar', 'sheets', 'drive'
    gws_args = sys.argv[2:]

    # Map generic service names to source_keys
    source_key_map = {
        "calendar": "google_calendar",
        "sheets": "google_sheets",
        "drive": "google_drive"
    }
    source_key = source_key_map.get(service, service)

    # Load API Key
    # We look for it in a separate file as requested, or environment
    api_key_path = os.path.expanduser("~/.google_workspace_api_key")
    api_key = os.environ.get("GWS_SKILL_API_KEY")
    
    if not api_key and os.path.exists(api_key_path):
        with open(api_key_path, "r") as f:
            api_key = f.read().strip()

    if not api_key:
        print("REQUIRED_ACTION: Please provide your MyBrandMetrics API Key.")
        print("Save it to ~/.google_workspace_api_key or set GWS_SKILL_API_KEY.")
        sys.exit(1)

    # Get the token
    token = get_token(source_key, api_key)

    # Prepare environment
    env = os.environ.copy()
    env["GOOGLE_WORKSPACE_CLI_TOKEN"] = token

    # Execute gws
    # The 'service' name is often the first arg to gws (e.g., 'gws calendar ...')
    # but the wrapper accepts it separately to know which token to fetch.
    cmd = ["gws", service] + gws_args
    
    try:
        # Check if gws is in PATH, if not try the local scripts dir
        if subprocess.call(["which", "gws"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            local_gws = os.path.join(os.path.dirname(__file__), "gws_musl")
            if os.path.exists(local_gws):
                cmd[0] = local_gws

        result = subprocess.run(cmd, env=env, capture_output=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error executing gws: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
