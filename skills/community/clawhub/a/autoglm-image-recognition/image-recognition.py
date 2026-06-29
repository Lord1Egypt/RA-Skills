#!/usr/bin/env python3
# image_recognition.py — AutoGLM Image Recognition
# Usage: python image_recognition.py "<image_url>" ["<prompt>"]

import sys
import json
import hashlib
import time
import urllib.request

# Configuration
APP_ID    = "100003"
APP_KEY   = "38d2391985e2369a5fb8227d8e6cd5e5"
URL       = "https://autoglm-api.autoglm.ai/agentdr/v1/assistant/skills/image-recognition"
TOKEN_URL = "http://127.0.0.1:18432/get_token"

# Step 1: Retrieve the token
try:
    with urllib.request.urlopen(TOKEN_URL) as resp:
        token = resp.read().decode("utf-8").strip()
except Exception as e:
    print(f"ERROR: Failed to retrieve token from the local service: {e}")
    sys.exit(1)

if not token:
    print("ERROR: The retrieved token is empty.")
    sys.exit(1)

# Ensure the token is in the format "Bearer xxx"
if not token.lower().startswith("bearer "):
    token = f"Bearer {token}"

# Step 2: Read the arguments
if len(sys.argv) < 2:
    print("Usage: python image_recognition.py \"<image_url>\" [\"<prompt>\"]")
    sys.exit(1)

image_url = sys.argv[1]
prompt    = sys.argv[2] if len(sys.argv) >= 3 else "Describe the image"

# Step 3: Generate the signed headers
timestamp = str(int(time.time()))
sign_data = f"{APP_ID}&{timestamp}&{APP_KEY}"
sign      = hashlib.md5(sign_data.encode("utf-8")).hexdigest()

# Step 4: Send the request
payload = json.dumps({
    "prompt":    prompt,
    "image_url": image_url,
}).encode("utf-8")

headers = {
    "Authorization":    token,
    "Content-Type":     "application/json",
    "X-Auth-Appid":     APP_ID,
    "X-Auth-TimeStamp": timestamp,
    "X-Auth-Sign":      sign,
}

req = urllib.request.Request(URL, data=payload, headers=headers, method="POST")
with urllib.request.urlopen(req, timeout=300) as resp:
    result = json.loads(resp.read().decode("utf-8"))
    print(json.dumps(result, ensure_ascii=False, indent=2))
