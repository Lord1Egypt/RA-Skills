#!/usr/bin/env python3
"""
Fooocus Image Generation with Fallback Support
Supports local Fooocus, CPU mode, and cloud alternatives
"""

import os
import sys
import json
import time
import base64
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
import urllib.request
import urllib.error

# Default configuration
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 7865
DEFAULT_OUTPUT_DIR = "."

# Cloud alternatives (for environments without GPU)
CLOUD_ALTERNATIVES = {
    "huggingface": {
        "name": "Hugging Face Inference API",
        "url": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
        "requires_key": True
    },
    "replicate": {
        "name": "Replicate",
        "url": "https://api.replicate.com/v1/predictions",
        "requires_key": True
    }
}


def check_environment():
    """Check if we can run Fooocus locally"""
    results = {
        "can_run_local": False,
        "has_cuda": False,
        "fooocus_running": False,
        "issues": []
    }
    
    # Check PyTorch
    try:
        import torch
        results["has_pytorch"] = True
        results["has_cuda"] = torch.cuda.is_available()
        if results["has_cuda"]:
            results["vram_gb"] = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    except ImportError:
        results["has_pytorch"] = False
        results["issues"].append("PyTorch not installed")
    
    # Check Fooocus
    try:
        req = urllib.request.Request(
            f"http://{DEFAULT_HOST}:{DEFAULT_PORT}/",
            method="HEAD",
            timeout=3
        )
        with urllib.request.urlopen(req) as _:
            results["fooocus_running"] = True
    except:
        results["issues"].append("Fooocus not running")
    
    # Determine if we can run locally
    results["can_run_local"] = results.get("has_pytorch", False) and results["fooocus_running"]
    
    return results


def generate_with_fooocus(
    prompt: str,
    negative_prompt: str = "",
    width: int = 1024,
    height: int = 1024,
    steps: int = 30,
    cfg: float = 4.0,
    seed: int = -1,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    timeout: int = 300
) -> Optional[str]:
    """
    Generate image using local Fooocus API
    Returns base64 image string or None if failed
    """
    url = f"http://{host}:{port}/api/predict"
    
    # Prepare request
    payload = {
        "fn_index": 13,
        "data": [
            prompt,
            negative_prompt,
            ["Fooocus V2"],
            "Quality",
            width,
            height,
            1,
            seed,
            2.0,
            cfg,
            "dpmpp_2m_sde_gpu",
            "karras",
            "",
            None,
            None,
            False,
            None,
            None
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Fooocus-Client/1.0"
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
            
            if "data" in result and len(result["data"]) > 0:
                return result["data"][0]
            else:
                print("Warning: No image data in response")
                return None
                
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.read().decode()[:200]}")
        return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None


def save_base64_image(b64_data: str, output_path: str) -> str:
    """Save base64 encoded image to file"""
    if "," in b64_data:
        b64_data = b64_data.split(",")[1]
    
    img_data = base64.b64decode(b64_data)
    
    # Ensure directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "wb") as f:
        f.write(img_data)
    
    return output_path


def print_generation_info(env: Dict):
    """Print environment information"""
    print("=" * 60)
    print("Fooocus Generation Environment")
    print("=" * 60)
    
    if env.get("can_run_local"):
        print("✅ Local Fooocus detected and running")
        if env.get("has_cuda"):
            print(f"✅ CUDA available ({env.get('vram_gb', 0):.1f}GB VRAM)")
        else:
            print("⚠️  CPU mode (slow)")
    else:
        print("❌ Cannot run Fooocus locally:")
        for issue in env.get("issues", []):
            print(f"   - {issue}")
        print("\n💡 Options:")
        print("   1. Start Fooocus: cd ~/Fooocus && python entry_with_update.py")
        print("   2. Install Fooocus: python check_env.py --install")
        print("   3. Use cloud alternative (requires API key)")
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Fooocus with fallback support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic generation (auto-detect environment)
  python generate.py --prompt "a beautiful sunset"
  
  # Force specific resolution
  python generate.py --prompt "cyberpunk city" --width 1024 --height 576
  
  # CPU mode (if no GPU)
  python generate.py --prompt "anime character" --steps 10 --width 512
        """
    )
    
    # Connection
    parser.add_argument("--host", default=DEFAULT_HOST, help="Fooocus host")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Fooocus port")
    
    # Generation parameters
    parser.add_argument("--prompt", "-p", required=True, help="Generation prompt")
    parser.add_argument("--negative", "-n", default="", help="Negative prompt")
    parser.add_argument("--width", type=int, default=1024, help="Image width")
    parser.add_argument("--height", type=int, default=1024, help="Image height")
    parser.add_argument("--steps", type=int, default=30, help="Sampling steps")
    parser.add_argument("--cfg", type=float, default=4.0, help="Guidance scale")
    parser.add_argument("--seed", type=int, default=-1, help="Random seed")
    
    # Output
    parser.add_argument("--output", "-o", help="Output path")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Output directory")
    
    # Behavior
    parser.add_argument("--skip-check", action="store_true", help="Skip environment check")
    parser.add_argument("--cpu-optimize", action="store_true", help="Optimize for CPU mode")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--timeout", type=int, default=300, help="Request timeout")
    
    args = parser.parse_args()
    
    # Check environment
    if not args.skip_check:
        env = check_environment()
        if args.verbose:
            print_generation_info(env)
        
        if not env.get("can_run_local"):
            print("\n❌ Cannot generate: Fooocus is not running")
            print("\nTo start Fooocus:")
            print("  cd ~/Fooocus")
            print("  python entry_with_update.py")
            print("\nOr install Fooocus:")
            print("  python check_env.py --install")
            sys.exit(1)
    
    # CPU optimizations
    if args.cpu_optimize or (not check_environment().get("has_cuda", False)):
        print("⚠️  CPU mode detected - optimizing parameters")
        if args.steps > 20:
            print(f"   Reducing steps from {args.steps} to 20")
            args.steps = 20
        if args.width > 512 or args.height > 512:
            print(f"   Reducing resolution to 512x512")
            args.width = 512
            args.height = 512
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        timestamp = int(time.time())
        safe_prompt = "".join(c for c in args.prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_prompt = safe_prompt.replace(' ', '_')
        output_path = os.path.join(args.output_dir, f"fooocus_{safe_prompt}_{timestamp}.png")
    
    # Generate
    if args.verbose:
        print(f"\nGenerating image...")
        print(f"  Prompt: {args.prompt[:60]}...")
        print(f"  Size: {args.width}x{args.height}")
        print(f"  Steps: {args.steps}")
    
    try:
        result = generate_with_fooocus(
            prompt=args.prompt,
            negative_prompt=args.negative,
            width=args.width,
            height=args.height,
            steps=args.steps,
            cfg=args.cfg,
            seed=args.seed,
            host=args.host,
            port=args.port,
            timeout=args.timeout
        )
        
        if result:
            save_base64_image(result, output_path)
            print(f"✅ Image saved to: {output_path}")
            
            # Print file info
            file_size = os.path.getsize(output_path) / 1024
            print(f"   Size: {file_size:.1f} KB")
        else:
            print("❌ Generation failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
