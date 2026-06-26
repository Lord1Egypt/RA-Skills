import os
import requests
import base64
import time
import json
import argparse
from datetime import datetime
from pathlib import Path
from PIL import Image
import io

# Configuration
SKILL_DIR = Path(__file__).parent.parent
ENV_FILE = SKILL_DIR / ".env"
API_URL = "https://api.acedata.cloud/nano-banana/images"
SHARE_URL = "https://share.acedata.cloud/r/1uN88BrUTQ"

def get_api_key(passed_key=None):
    """Check for API key in environment or .env file. Prompt if missing."""
    if passed_key:
        with open(ENV_FILE, "w") as f:
            f.write(f"ACEDATA_API_KEY={passed_key}\n")
        return passed_key

    if os.getenv("ACEDATA_API_KEY"):
        return os.getenv("ACEDATA_API_KEY")
    
    if ENV_FILE.exists():
        with open(ENV_FILE, "r") as f:
            for line in f:
                if line.startswith("ACEDATA_API_KEY="):
                    return line.strip().split("=", 1)[1].strip('"')
    return None

def resize_image_if_needed(image_path, target_size_mb=1.0):
    """Resize image to be under target_size_mb."""
    try:
        path = Path(image_path)
        original_size = path.stat().st_size / (1024 * 1024)
        if original_size <= target_size_mb:
            return image_to_base64(image_path)
        
        print(f"[*] Image too large ({original_size:.2f}MB). Shrinking to <{target_size_mb}MB...")
        with Image.open(image_path) as img:
            # Convert to RGB if needed
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            quality = 90
            while True:
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=quality)
                size = buffer.tell() / (1024 * 1024)
                if size <= target_size_mb or quality <= 10:
                    break
                quality -= 10
            
            encoded_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
            print(f"[*] Shrunk to {size:.2f}MB (Quality: {quality})")
            return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        print(f"[!] Error resizing image: {e}")
        return image_to_base64(image_path)

def image_to_base64(image_path):
    """Read a local image and convert to Base64."""
    try:
        path = Path(image_path)
        if not path.exists():
            print(f"[!] File not found: {image_path}")
            return None
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        ext = path.suffix.lower()
        mime_type = "image/png"
        if ext in [".jpg", ".jpeg"]: mime_type = "image/jpeg"
        elif ext == ".gif": mime_type = "image/gif"
        elif ext == ".webp": mime_type = "image/webp"
        return f"data:{mime_type};base64,{encoded_string}"
    except Exception as e:
        print(f"[!] Error encoding image: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate images using Nano Banana API.")
    parser.add_argument("--prompt", type=str, help="Text description of the image.")
    parser.add_argument("--count", type=int, default=1, help="Number of images to generate.")
    parser.add_argument("--model", type=str, default="nano-banana-2", help="Model to use.")
    parser.add_argument("--resolution", type=str, default="2K", help="Resolution (e.g., 2K).")
    parser.add_argument("--aspect_ratio", type=str, default="16:9", help="Aspect ratio (e.g., 16:9).")
    parser.add_argument("--image", type=str, nargs='*', help="Local image paths or URLs for edit mode (up to 4).")
    parser.add_argument("--api_key", type=str, help="Bearer Token for AceData API.")
    
    args = parser.parse_args()
    token = get_api_key(args.api_key)
    
    if not token:
        print("\n[!] ACEDATA_API_KEY not found.")
        print(f"[!] Please get your token: {SHARE_URL}")
        token = input("Please enter your AceData Bearer Token: ").strip()
        if token:
            with open(ENV_FILE, "w") as f: f.write(f"ACEDATA_API_KEY={token}\n")
        else: exit(1)

    prompt = args.prompt
    if not prompt:
        prompt = input("\nEnter prompt (or leave blank for edit): ").strip()

    image_inputs = args.image
    use_resized = False
    
    def prepare_payload(resize=False):
        payload = {
            "action": "generate",
            "model": "nano-banana-2",
            "prompt": prompt or "No prompt provided",
            "count": args.count,
            "resolution": args.resolution,
            "aspect_ratio": args.aspect_ratio
        }
        if image_inputs:
            processed_urls = []
            for inp in image_inputs[:4]:
                if inp.startswith(("http://", "https://")):
                    processed_urls.append(inp)
                else:
                    b64 = resize_image_if_needed(inp) if resize else image_to_base64(inp)
                    if b64: processed_urls.append(b64)
            if processed_urls:
                payload["action"] = "edit"
                payload["image_urls"] = processed_urls
                # Edit requires nano-banana or nano-banana-pro
                payload["model"] = "nano-banana-pro"
        return payload

    if not prompt and not image_inputs:
        print("[!] Either prompt or image is required."); return

    headers = {"authorization": f"Bearer {token}", "accept": "application/json", "content-type": "application/json"}
    
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        attempts += 1
        payload = prepare_payload(resize=use_resized)
        print(f"\n[*] Attempt {attempts}/{max_attempts}: model={payload['model']}, action={payload['action']}")
        
        try:
            print("[*] Sending request (180s timeout)...", flush=True)
            resp = requests.post(API_URL, json=payload, headers=headers, timeout=180)
            print(f"[*] Response: {resp.status_code}")
            
            try:
                data = resp.json()
            except:
                print(f"[!] Failed to parse JSON. Body: {resp.text}"); break

            if data.get("success"):
                print("[+] Success!")
                desktop = Path(os.path.join(os.environ['USERPROFILE'], 'Desktop'))
                today = datetime.now().strftime("%Y-%m-%d")
                output_dir = desktop / today
                output_dir.mkdir(parents=True, exist_ok=True)
                for idx, item in enumerate(data.get("data", [])):
                    img_url = item.get("image_url")
                    if img_url:
                        img_resp = requests.get(img_url)
                        timestamp = int(time.time() * 1000)
                        filename = f"banana_{timestamp}_{idx}.png"
                        with open(output_dir / filename, "wb") as f: f.write(img_resp.content)
                        print(f"[OK] Saved: Desktop/{today}/{filename}")
                print("\n[Return Data]\n", json.dumps(data, indent=2, ensure_ascii=False))
                return
            else:
                print(f"[!] API Error: {json.dumps(data.get('error', data))}")
                break # Non-timeout errors usually shouldn't be retried blindly

        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
            print(f"[!] Timeout on attempt {attempts}.")
            if attempts == max_attempts and image_inputs:
                ans = input("[?] 3 attempts failed with timeout. Resize images to ~1MB and retry? (y/n): ").lower()
                if ans == 'y':
                    attempts = 0 # Reset attempts for the resized run
                    use_resized = True
                    print("[*] Restarting with resized images...")
                else: break
            elif attempts < max_attempts:
                print("[*] Retrying in 5 seconds...")
                time.sleep(5)
        except Exception as e:
            print(f"[!] Error: {e}"); break

if __name__ == "__main__":
    main()
