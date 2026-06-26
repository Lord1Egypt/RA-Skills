#!/usr/bin/env python3
"""
Frameo API Client - Reverse Engineered from iOS app v1.36.20
Supports: auto token refresh, list frames, send images

Usage:
  python3 frameo_client.py --login        # Get fresh token
  python3 frameo_client.py --frames       # List your frames
  python3 frameo_client.py --send image.jpg  # Send image to frame
  python3 frameo_client.py --send image.jpg --caption "Hello!"

Setup:
  pip3 install requests
"""

import requests
import argparse
import json
import os
import sys
from pathlib import Path

# --- YOUR CREDENTIALS ---
# Set these or use environment variables FRAMEO_EMAIL / FRAMEO_PASSWORD

FRAMEO_EMAIL = os.environ.get("FRAMEO_EMAIL", "")
FRAMEO_PASSWORD = os.environ.get("FRAMEO_PASSWORD", "")

# --- DEVICE IDENTIFIERS ---
# These can be captured from Proxyman or left as defaults

CLIENT_DEVICE_ID = os.environ.get("FRAMEO_DEVICE_ID", "00000000-0000-0000-0000-000000000000")
CLIENT_PEER_ID = os.environ.get("FRAMEO_PEER_ID", "0000000000000000000000000000000000000000000000000000000000000000")
CLIENT_USER_ID = os.environ.get("FRAMEO_USER_ID", "00000000-0000-0000-0000-000000000000")
FCM_TOKEN = os.environ.get("FRAMEO_FCM_TOKEN", "")

TOKEN_FILE = Path.home() / ".frameo_token"
BASE_API = "https://api.frameo.net"
AUTH_URL = "https://auth.frameo.net/auth/realms/frameo/protocol/openid-connect/token"

# --- HEADERS ---

def get_headers(token, content_type="application/json"):
    return {
        "Authorization": f"Bearer {token}",
        "client_application_id": "net.frameo.app",
        "client_platform_version": "26.4",
        "client_software_version_name": "1.36.20",
        "client_software_version_code": "3914",
        "client_type": "frameo_client",
        "client_platform": "iOS",
        "client_device_id": CLIENT_DEVICE_ID,
        "client_peer_id": CLIENT_PEER_ID,
        "client_user_id": CLIENT_USER_ID,
        "client_hardware_model": "iPhone17,2",
        "client_preferred_language": "en-US",
        "Accept": "application/json",
        "Accept-Language": "en-US;q=1.0",
        "Accept-Encoding": "gzip;q=0.9, deflate;q=0.8",
        "Content-Type": content_type,
        "Connection": "keep-alive",
        "User-Agent": "Frameo/1.36.20 (net.frameo.app; build:3914; iOS 26.4.0) Alamofire/5.10.2",
    }

# --- AUTH ---

def login(email, password):
    print(f"Logging in as {email}...")
    data = {
        "client_id": "frameo-app",
        "grant_type": "password",
        "username": email,
        "password": password,
        "scope": "offline_access email profile",
    }
    r = requests.post(AUTH_URL, data=data)
    if r.status_code != 200:
        print(f"Login failed: {r.status_code}")
        print(r.text[:500])
        sys.exit(1)
    token_data = r.json()
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)
    print("Login successful! Token cached.")
    return token_data["access_token"]

def refresh_token(refresh_tok):
    data = {
        "client_id": "frameo-app",
        "grant_type": "refresh_token",
        "refresh_token": refresh_tok,
    }
    r = requests.post(AUTH_URL, data=data)
    if r.status_code != 200:
        return None
    token_data = r.json()
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)
    return token_data["access_token"]

def get_token():
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE) as f:
            token_data = json.load(f)
        # Try refresh token first
        if "refresh_token" in token_data:
            token = refresh_token(token_data["refresh_token"])
            if token:
                print("Token refreshed.")
                return token
        # Fall back to access_token if available
        if "access_token" in token_data:
            print("Using cached access token.")
            return token_data["access_token"]
    if not FRAMEO_PASSWORD:
        print("ERROR: Set FRAMEO_PASSWORD in the script, then run --login first.")
        sys.exit(1)
    return login(FRAMEO_EMAIL, FRAMEO_PASSWORD)

# --- API CALLS ---

def register_client(token):
    body = {"deviceId": CLIENT_DEVICE_ID, "peerId": CLIENT_PEER_ID}
    r = requests.post(f"{BASE_API}/v1/managed-pairings/client",
                      headers=get_headers(token), json=body)
    return r.status_code in [200, 204]

def get_frames(token):
    r = requests.get(f"{BASE_API}/v1/managed-pairings/frames",
                     headers=get_headers(token))
    r.raise_for_status()
    return r.json()

def get_user_account(token):
    r = requests.get(f"{BASE_API}/v1/useraccount",
                     headers=get_headers(token))
    r.raise_for_status()
    return r.json()

def send_image(token, image_path, frame_id, caption=""):
    image_path = Path(image_path)
    if not image_path.exists():
        print(f"Image not found: {image_path}")
        sys.exit(1)
    with open(image_path, "rb") as f:
        image_data = f.read()

    filename = image_path.name
    print(f"Sending {filename} ({len(image_data)//1024}KB) to frame {frame_id}...")

    # Try known endpoint patterns
    endpoints = [
        f"{BASE_API}/v1/managed-pairings/frames/{frame_id}/media",
        f"{BASE_API}/v1/managed-pairings/frames/{frame_id}/photos",
        f"{BASE_API}/v1/media",
        f"{BASE_API}/v1/photos",
        f"{BASE_API}/v1/managed-pairings/media",
    ]

    headers = get_headers(token)
    del headers["Content-Type"]

    for endpoint in endpoints:
        print(f"Trying: {endpoint}")
        files = {"file": (filename, image_data, "image/jpeg")}
        data = {"frameId": frame_id, "caption": caption}
        r = requests.post(endpoint, headers=headers, files=files, data=data)
        print(f"  -> {r.status_code}: {r.text[:150]}")
        if r.status_code in [200, 201, 204]:
            print("✓ Image sent successfully!")
            return r.json() if r.content else {"status": "sent"}
        elif r.status_code == 404:
            continue
        else:
            break

    print("\nUpload endpoint not found via REST API.")
    print("Frameo likely uses FCM (Firebase) for peer-to-peer delivery.")
    print("Next step: capture traffic on the frame side at 192.168.0.171")
    return None

# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="Frameo API Client")
    parser.add_argument("--login", action="store_true", help="Force fresh login")
    parser.add_argument("--frames", action="store_true", help="List paired frames")
    parser.add_argument("--account", action="store_true", help="Show account info")
    parser.add_argument("--send", metavar="IMAGE", help="Send image to frame")
    parser.add_argument("--frame-id", metavar="ID", help="Target frame ID")
    parser.add_argument("--caption", default="", help="Image caption")
    args = parser.parse_args()

    if args.login:
        if not FRAMEO_PASSWORD:
            print("Set FRAMEO_PASSWORD in the script first.")
            sys.exit(1)
        login(FRAMEO_EMAIL, FRAMEO_PASSWORD)
        return

    token = get_token()
    register_client(token)

    if args.frames:
        frames = get_frames(token)
        print(json.dumps(frames, indent=2))
        if isinstance(frames, list):
            print(f"\n{len(frames)} frame(s) found:")
            for f in frames:
                fid = f.get("id") or f.get("frameId") or f.get("peer_id")
                print(f"  ID: {fid}  Name: {f.get('name','unknown')}")

    elif args.account:
        print(json.dumps(get_user_account(token), indent=2))

    elif args.send:
        if not args.frame_id:
            frames_response = get_frames(token)
            # Handle both {"frames": [...]} and [...] formats
            if isinstance(frames_response, dict) and "frames" in frames_response:
                frames = frames_response["frames"]
            else:
                frames = frames_response
            if not frames:
                print("No frames found.")
                sys.exit(1)
            frame = frames[0]
            frame_id = frame.get("peerId") or frame.get("id") or frame.get("frameId") or frame.get("peer_id")
            print(f"Auto-selected frame: {frame_id} ({frame.get('name','')})")
        else:
            frame_id = args.frame_id
        send_image(token, args.send, frame_id, args.caption)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
