#!/usr/bin/env python3
"""
Banana API - Nano Banana (Gemini) Image Generation Client
Handles base64 encoding/decoding, image compression, and Discord sending automatically.
"""

import argparse
import base64
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from io import BytesIO

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Configuration
API_BASE_URL = "https://nn.147ai.com"
DEFAULT_MODEL = "gemini-3-pro-image-preview"
WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"
PHOTOS_DIR = WORKSPACE_DIR / "photos"
CONFIG_DIR = WORKSPACE_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "banana-api.json"


def get_config():
    """Load config from file or return defaults."""
    defaults = {
        "api_key": "",
        "default_model": DEFAULT_MODEL,
        "default_output_dir": str(PHOTOS_DIR),
        "auto_compress": True,
        "default_compress_size": 512
    }
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                saved = json.load(f)
                defaults.update(saved)
        except Exception:
            pass
    
    return defaults


def save_config(config):
    """Save config to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"💾 Config saved to: {CONFIG_FILE}")


def get_api_key(args_key=None):
    """Get API key from args, env, or config file (in that priority)."""
    # 1. Command line arg
    if args_key:
        return args_key
    
    # 2. Environment variable
    env_key = os.environ.get("BANANA_API_KEY", "")
    if env_key:
        return env_key
    
    # 3. Config file
    config = get_config()
    if config.get("api_key"):
        return config["api_key"]
    
    return None


def compress_image(image_path: str, max_size: int = 512, quality: int = 85) -> bytes:
    """Compress image to reduce base64 size."""
    if not PIL_AVAILABLE:
        # Fallback: read raw file if PIL not available
        with open(image_path, 'rb') as f:
            return f.read()
    
    img = Image.open(image_path)
    
    # Resize if larger than max_size
    w, h = img.size
    if w > max_size or h > max_size:
        ratio = min(max_size / w, max_size / h)
        new_size = (int(w * ratio), int(h * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # Convert to RGB if necessary (for JPEG)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    # Save to buffer
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=quality, optimize=True)
    return buffer.getvalue()


def encode_image(image_path: str, max_size: int = 512) -> str:
    """Encode image to base64, with optional compression."""
    image_bytes = compress_image(image_path, max_size=max_size)
    return base64.b64encode(image_bytes).decode('utf-8')


def save_base64_image(base64_data: str, output_path: Path) -> Path:
    """Save base64 encoded image to file."""
    image_bytes = base64.b64decode(base64_data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(image_bytes)
    return output_path


def generate_filename(prompt: str, suffix: str = "") -> str:
    """Generate filename from prompt and timestamp."""
    # Clean prompt for filename
    clean_prompt = re.sub(r'[^\w\s-]', '', prompt).strip()
    clean_prompt = re.sub(r'[-\s]+', '-', clean_prompt)
    clean_prompt = clean_prompt[:30]  # Limit length
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    if suffix:
        return f"banana-{suffix}-{timestamp}.png"
    elif clean_prompt:
        return f"banana-{clean_prompt}-{timestamp}.png"
    else:
        return f"banana-{timestamp}.png"


def call_banana_api(
    prompt: str,
    api_key: str,
    image_path: str = None,
    model: str = DEFAULT_MODEL,
    aspect_ratio: str = None
) -> dict:
    """Call Nano Banana API for image generation or editing."""
    
    url = f"{API_BASE_URL}/v1beta/models/{model}:generateContent"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Build prompt text
    prompt_text = prompt
    if aspect_ratio:
        prompt_text += f", {aspect_ratio} aspect ratio"
    
    # Build request parts
    parts = []
    
    if image_path:
        # Image editing mode
        print(f"📷 Loading image: {image_path}")
        image_b64 = encode_image(image_path, max_size=512)
        print(f"   Compressed to {len(image_b64)} chars base64")
        
        # Detect mime type
        mime_type = "image/jpeg"  # We convert to JPEG
        if image_path.lower().endswith('.png'):
            mime_type = "image/png"
        
        parts.append({
            "inlineData": {
                "mimeType": mime_type,
                "data": image_b64
            }
        })
    
    parts.append({
        "text": prompt_text
    })
    
    data = {
        "contents": [{
            "role": "user",
            "parts": parts
        }],
        "generationConfig": {
            "responseModalities": ["Text", "Image"]
        }
    }
    
    print(f"🚀 Calling Banana API ({model})...")
    
    if REQUESTS_AVAILABLE:
        response = requests.post(url, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        return response.json()
    else:
        # Fallback using curl
        import subprocess
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            data_file = f.name
        
        try:
            cmd = [
                'curl', '-s', '-X', 'POST', url,
                '-H', f'Authorization: Bearer {api_key}',
                '-H', 'Content-Type: application/json',
                '-d', f'@{data_file}'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            os.unlink(data_file)
            
            if result.returncode != 0:
                raise RuntimeError(f"curl failed: {result.stderr}")
            
            return json.loads(result.stdout)
        except Exception as e:
            if os.path.exists(data_file):
                os.unlink(data_file)
            raise


def extract_image_from_response(response: dict) -> str:
    """Extract base64 image data from API response."""
    candidates = response.get('candidates', [])
    if not candidates:
        raise ValueError("No candidates in response")
    
    content = candidates[0].get('content', {})
    parts = content.get('parts', [])
    
    for part in parts:
        if 'inlineData' in part:
            return part['inlineData']['data']
    
    raise ValueError("No image data found in response")


def send_to_discord(image_path: Path, caption: str = "", channel_id: str = None) -> bool:
    """Send image to Discord using OpenClaw message tool."""
    if not channel_id:
        print(f"⚠️  No channel_id provided, skipping Discord send")
        return False
    
    # Use openclaw CLI to send message
    import subprocess
    
    cmd = [
        'openclaw', 'message', 'send',
        '--channel', 'discord',
        '--target', channel_id,
        '--caption', caption,
        '--media', str(image_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ Sent to Discord channel {channel_id}")
            return True
        else:
            print(f"⚠️  Failed to send to Discord: {result.stderr}")
            return False
    except Exception as e:
        print(f"⚠️  Error sending to Discord: {e}")
        return False


def setup_config():
    """Interactive setup for configuration."""
    print("🍌 Banana API Setup")
    print("=" * 40)
    
    config = get_config()
    
    # API Key
    current_key = config.get("api_key", "")
    masked = "*" * 10 + current_key[-4:] if len(current_key) > 4 else "(not set)"
    print(f"\nCurrent API Key: {masked}")
    new_key = input("Enter API key (or press Enter to keep current): ").strip()
    if new_key:
        config["api_key"] = new_key
        print("✅ API key updated")
    
    # Default model
    print(f"\nCurrent default model: {config.get('default_model', DEFAULT_MODEL)}")
    new_model = input(f"Enter default model (or press Enter to keep): ").strip()
    if new_model:
        config["default_model"] = new_model
        print("✅ Default model updated")
    
    # Output directory
    print(f"\nCurrent output directory: {config.get('default_output_dir', str(PHOTOS_DIR))}")
    new_dir = input("Enter output directory (or press Enter to keep): ").strip()
    if new_dir:
        config["default_output_dir"] = new_dir
        print("✅ Output directory updated")
    
    save_config(config)
    print("\n✨ Setup complete!")


def main():
    parser = argparse.ArgumentParser(
        description='Banana API - Gemini Image Generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-image
  python3 banana_gen.py "a cute cat sitting on a window"

  # Image editing (with input image)
  python3 banana_gen.py "make me look like a rock star" --image photo.png

  # Specify aspect ratio
  python3 banana_gen.py "sunset beach scene" --ratio 2:3

  # Auto-send to Discord
  python3 banana_gen.py "cyberpunk city" --channel-id 1478746465328435412

  # Custom filename suffix
  python3 banana_gen.py "portrait of a warrior" --name warrior
  
  # Setup configuration (save API key)
  python3 banana_gen.py --setup
        """
    )
    
    parser.add_argument('prompt', nargs='?', help='Image generation prompt')
    parser.add_argument('--image', '-i', help='Input image path for editing')
    parser.add_argument('--ratio', '-r', help='Aspect ratio (e.g., 2:3, 16:9)')
    parser.add_argument('--model', '-m', help=f'Model to use (default: {DEFAULT_MODEL})')
    parser.add_argument('--output', '-o', help='Custom output path')
    parser.add_argument('--name', '-n', help='Filename suffix/tag')
    parser.add_argument('--channel-id', '-c', help='Discord channel ID to send result')
    parser.add_argument('--no-send', action='store_true', 
                        help='Do not auto-send to Discord (only save locally)')
    parser.add_argument('--api-key', '-k', help='Banana API key (or set BANANA_API_KEY env)')
    parser.add_argument('--setup', action='store_true', 
                        help='Run interactive setup to save API key and defaults')
    parser.add_argument('--show-config', action='store_true',
                        help='Show current configuration')
    
    args = parser.parse_args()
    
    # Handle setup
    if args.setup:
        setup_config()
        return
    
    # Show config
    if args.show_config:
        config = get_config()
        print("🍌 Banana API Configuration")
        print("=" * 40)
        for key, value in config.items():
            if key == "api_key" and value:
                value = "*" * 10 + value[-4:]
            print(f"  {key}: {value}")
        print(f"\nConfig file: {CONFIG_FILE}")
        return
    
    # Require prompt for generation
    if not args.prompt:
        parser.print_help()
        print("\n❌ Error: PROMPT is required (unless using --setup or --show-config)")
        sys.exit(1)
    
    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("❌ Error: API key required.")
        print("\nOptions to set API key:")
        print("  1. Run: python3 banana_gen.py --setup")
        print("  2. Set env: export BANANA_API_KEY='sk-xxx'")
        print("  3. Use flag: --api-key 'sk-xxx'")
        sys.exit(1)
    
    # Get config for defaults
    config = get_config()
    model = args.model or config.get("default_model", DEFAULT_MODEL)
    output_dir = Path(config.get("default_output_dir", str(PHOTOS_DIR)))
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Call API
        response = call_banana_api(
            prompt=args.prompt,
            api_key=api_key,
            image_path=args.image,
            model=model,
            aspect_ratio=args.ratio
        )
        
        # Check for errors
        if 'error' in response:
            print(f"❌ API Error: {response['error']}")
            sys.exit(1)
        
        # Extract image
        print("🖼️  Extracting image from response...")
        image_b64 = extract_image_from_response(response)
        print(f"   Image size: {len(image_b64)} chars base64")
        
        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            filename = generate_filename(args.prompt, suffix=args.name)
            output_path = output_dir / filename
        
        # Save image
        saved_path = save_base64_image(image_b64, output_path)
        print(f"💾 Saved to: {saved_path}")
        
        # Send to Discord if requested
        if args.channel_id and not args.no_send:
            mode = "image editing" if args.image else "generation"
            caption = f"🎨 Banana API {mode} result\nPrompt: {args.prompt[:100]}"
            if args.image:
                caption += f"\nBased on: {Path(args.image).name}"
            send_to_discord(saved_path, caption, args.channel_id)
        
        print("✅ Done!")
        print(f"📁 File: {saved_path}")
        
        # Return path for shell integration
        print(f"OUTPUT_PATH:{saved_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
