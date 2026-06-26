import os
import sys
import requests
import json
import time

API_URL_V1 = "https://api.meshy.ai/openapi/v1"
API_URL_V2 = "https://api.meshy.ai/openapi/v2"

def get_headers():
    # Try environment variable first
    api_key = os.environ.get("MESHY_API_KEY")
    
    # Try local .env file in the skill directory
    if not api_key:
        try:
            env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
            if os.path.exists(env_path):
                with open(env_path, "r") as f:
                    for line in f:
                        if line.startswith("MESHY_API_KEY="):
                            api_key = line.split("=", 1)[1].strip()
                            break
        except Exception:
            pass

    if not api_key:
        print("Error: MESHY_API_KEY not set. Set env var or create a .env file in the skill root.")
        sys.exit(1)
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

def set_key(api_key):
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    with open(env_path, "w") as f:
        f.write(f"MESHY_API_KEY={api_key}\n")
    print(f"API key saved to {env_path}")

def create_text_to_3d(prompt, mode="preview"):
    headers = get_headers()
    payload = {
        "prompt": prompt,
        "mode": mode
    }
    response = requests.post(f"{API_URL_V2}/text-to-3d", headers=headers, json=payload)
    return response.json()

def create_image_to_3d(image_urls, prompt=""):
    headers = get_headers()
    # Support for multi-image v6
    if isinstance(image_urls, str):
        image_urls = [image_urls]
    
    payload = {
        "image_urls": image_urls,
        "ai_model": "meshy-6",
        "object_prompt": prompt
    }
    response = requests.post(f"{API_URL_V1}/image-to-3d", headers=headers, json=payload)
    return response.json()

def get_task(task_id, version="v2"):
    headers = get_headers()
    url = f"{API_URL_V2}/text-to-3d/{task_id}" if version == "v2" else f"{API_URL_V1}/image-to-3d/{task_id}"
    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python meshy_client.py <command> [args]")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "text-to-3d":
        print(json.dumps(create_text_to_3d(sys.argv[2])))
    elif command == "image-to-3d":
        print(json.dumps(create_image_to_3d(sys.argv[2])))
    elif command == "status":
        print(json.dumps(get_task(sys.argv[2])))
    elif command == "set-key":
        set_key(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
