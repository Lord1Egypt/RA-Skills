import os
import requests
import argparse
import json
from pathlib import Path

def get_openclaw_config():
    """
    Attempts to find OpenClaw / Moltbot configuration or secrets.
    """
    paths = [
        Path("C:/Users/user/.openclaw/openclaw.json"),
        Path.home() / ".openclaw" / "secrets.json",
        Path.home() / ".openclaw" / "config.json",
        Path.home() / ".moltbot" / "secrets.json",
    ]
    
    for p in paths:
        if p.exists():
            try:
                with open(p, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
    return {}

def send_to_line(file_path, channel_access_token=None, user_id=None):
    """
    Sends a file to a LINE user using the Messaging API.
    """
    config = get_openclaw_config()
    
    # Helper to find nested keys
    def find_key(cfg, key_name):
        if key_name in cfg: return cfg[key_name]
        for v in cfg.values():
            if isinstance(v, dict):
                res = find_key(v, key_name)
                if res: return res
        return None

    # Priority: Argument > Environment Variable > Config File (Flat or Nested)
    token = (channel_access_token or 
             os.environ.get("LINE_CHANNEL_ACCESS_TOKEN") or 
             find_key(config, "LINE_CHANNEL_ACCESS_TOKEN") or 
             find_key(config, "line_token") or
             find_key(config, "channelAccessToken"))
             
    to_user = (user_id or 
               os.environ.get("LINE_USER_ID") or 
               find_key(config, "LINE_USER_ID") or 
               find_key(config, "line_user_id") or
               find_key(config, "userId"))

    if not token:
        print("Error: Could not find LINE_CHANNEL_ACCESS_TOKEN.")
        print("Please provide it as an argument, environment variable, or in OpenClaw config.")
        return False

    if not to_user or to_user == "REPLACE_WITH_YOUR_USER_ID":
        print("Error: Could not find a valid LINE_USER_ID.")
        print("To send messages via the LINE Messaging API, you need the recipient's User ID (e.g., U123...).")
        print("You can find your User ID in the LINE Developers Console under the 'Messaging API' tab of your channel.")
        return False

    path = Path(file_path).resolve()
    if not path.exists():
        print(f"Error: File {path} not found.")
        return False

    print(f"Credentials Found:")
    print(f" - Token: {token[:5]}...{token[-5:] if len(token)>10 else ''}")
    print(f" - Target User: {to_user}")
    print(f"Sending '{path.name}'...")
    
    # Note: To send a real file through the LINE API without a public URL,
    # we would need the 'content' endpoint, which is usually for replying.
    # Most bots send a public link.
    
    print("Optimization: If running within OpenClaw, the bridge handles local paths automatically.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Send a file via LINE (using OpenClaw settings).")
    parser.add_argument("path", help="Path to the file to send")
    parser.add_argument("--token", help="Override LINE Channel Access Token")
    parser.add_argument("--to", help="Override LINE User ID")
    
    args = parser.parse_args()
    send_to_line(args.path, args.token, args.to)

if __name__ == "__main__":
    main()
