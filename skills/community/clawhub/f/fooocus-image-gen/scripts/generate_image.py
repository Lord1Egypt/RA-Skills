#!/usr/bin/env python3
"""
Main image generation script for Fooocus.
Provides a command-line interface to Fooocus's Gradio API.
"""

import os
import sys
import json
import time
import base64
import argparse
import requests
from pathlib import Path
from typing import Optional, List, Dict, Any
from PIL import Image
import io


# Default Fooocus API endpoint
DEFAULT_API_URL = "http://localhost:7865"

# Preset configurations
PRESETS = {
    "default": {
        "base_model": "juggernautXL_v8Rundiffusion.safetensors",
        "refiner_model": "None",
        "performance": "Quality",
    },
    "anime": {
        "base_model": "animaPencilXL_v100.safetensors",
        "refiner_model": "None",
        "performance": "Quality",
        "styles": ["Anime"],
    },
    "realistic": {
        "base_model": "realisticStockPhoto_v20.safetensors",
        "refiner_model": "None",
        "performance": "Quality",
        "styles": ["Photographic"],
    },
    "lcm": {
        "base_model": "juggernautXL_v8Rundiffusion.safetensors",
        "refiner_model": "None",
        "performance": "Speed",
    },
    "lightning": {
        "base_model": "juggernautXL_v8Rundiffusion.safetensors",
        "refiner_model": "None",
        "performance": "Extreme Speed",
    },
    "playground_v2.5": {
        "base_model": "playground-v2.5-1024px-aesthetic.safetensors",
        "refiner_model": "None",
        "performance": "Quality",
    },
    "pony_v6": {
        "base_model": "ponyDiffusionV6XL.safetensors",
        "refiner_model": "None",
        "performance": "Quality",
    },
    "sai": {
        "base_model": "sd_xl_base_1.0.safetensors",
        "refiner_model": "None",
        "performance": "Quality",
    },
}

# Aspect ratio to dimensions mapping
ASPECT_RATIOS = {
    "1:1": (1024, 1024),
    "4:3": (1024, 768),
    "3:4": (768, 1024),
    "16:9": (1024, 576),
    "9:16": (576, 1024),
    "21:9": (1024, 448),
    "9:21": (448, 1024),
    "3:2": (1024, 683),
    "2:3": (683, 1024),
}

# Quality to steps mapping
QUALITY_STEPS = {
    1: 30,
    2: 60,
    3: 100,
}


class FooocusClient:
    """Client for Fooocus Gradio API."""
    
    def __init__(self, api_url: str = DEFAULT_API_URL):
        self.api_url = api_url
        self.predict_url = f"{api_url}/api/predict"
        self.session = requests.Session()
    
    def check_connection(self) -> bool:
        """Check if Fooocus is running."""
        try:
            response = self.session.get(self.api_url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def get_api_info(self) -> Dict:
        """Get API information."""
        try:
            response = self.session.get(f"{self.api_url}/api/info", timeout=10)
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to get API info: {e}")
    
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64."""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    
    def decode_image(self, image_data: str) -> Image.Image:
        """Decode base64 image data."""
        image_bytes = base64.b64decode(image_data)
        return Image.open(io.BytesIO(image_bytes))
    
    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        steps: int = 30,
        guidance_scale: float = 7.0,
        sharpness: float = 2.0,
        seed: int = -1,
        base_model: str = "juggernautXL_v8Rundiffusion.safetensors",
        refiner_model: str = "None",
        performance: str = "Quality",
        styles: Optional[List[str]] = None,
        input_image: Optional[str] = None,
        mask_image: Optional[str] = None,
        image_prompt: Optional[str] = None,
        image_prompt_weight: float = 1.0,
        variation_strength: float = 0.5,
        upscale: int = 1,
        outpaint: bool = False,
        outpaint_direction: str = "all",
        face_swap: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate image using Fooocus API."""
        
        # Build the request payload for Fooocus
        # Note: This is a simplified version - actual API may vary
        payload = {
            "fn_index": 0,  # May need to be determined dynamically
            "data": [
                prompt,  # Prompt
                negative_prompt,  # Negative prompt
                styles or [],  # Styles
                performance,  # Performance
                width,  # Width
                height,  # Height
                guidance_scale,  # Guidance scale
                sharpness,  # Sharpness
                steps,  # Steps
                seed if seed >= 0 else -1,  # Random seed
                base_model,  # Base model
                refiner_model,  # Refiner model
            ]
        }
        
        # Add image inputs if provided
        if input_image:
            encoded = self.encode_image(input_image)
            payload["data"].append(encoded)
        
        if mask_image:
            encoded = self.encode_image(mask_image)
            payload["data"].append(encoded)
        
        if image_prompt:
            encoded = self.encode_image(image_prompt)
            payload["data"].append(encoded)
            payload["data"].append(image_prompt_weight)
        
        try:
            response = self.session.post(
                self.predict_url,
                json=payload,
                timeout=300  # 5 minute timeout for generation
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Generation failed: {e}")


def parse_aspect_ratio(ratio_str: str) -> tuple:
    """Parse aspect ratio string to dimensions."""
    if ratio_str in ASPECT_RATIOS:
        return ASPECT_RATIOS[ratio_str]
    
    # Try to parse custom ratio like "1024x768"
    if "x" in ratio_str:
        parts = ratio_str.split("x")
        return (int(parts[0]), int(parts[1]))
    
    raise ValueError(f"Unknown aspect ratio: {ratio_str}")


def get_preset_config(preset_name: str) -> Dict:
    """Get preset configuration."""
    if preset_name not in PRESETS:
        available = ", ".join(PRESETS.keys())
        raise ValueError(f"Unknown preset: {preset_name}. Available: {available}")
    return PRESETS[preset_name]


def natural_language_to_params(prompt: str) -> Dict:
    """Convert natural language hints to parameters."""
    params = {}
    prompt_lower = prompt.lower()
    
    # Detect style hints
    if any(word in prompt_lower for word in ["anime", "manga", "cartoon", "chibi"]):
        params["preset"] = "anime"
    elif any(word in prompt_lower for word in ["photo", "realistic", "photorealistic", "portrait"]):
        params["preset"] = "realistic"
    elif any(word in prompt_lower for word in ["fast", "quick", "draft"]):
        params["preset"] = "lcm"
    
    # Detect aspect ratio hints
    if any(word in prompt_lower for word in ["landscape", "panoramic", "wide"]):
        params["aspect_ratio"] = "16:9"
    elif any(word in prompt_lower for word in ["portrait", "vertical", "tall"]):
        params["aspect_ratio"] = "9:16"
    
    return params


def generate_single(
    client: FooocusClient,
    args: argparse.Namespace,
    output_path: str,
    seed: Optional[int] = None
) -> str:
    """Generate a single image."""
    
    # Get preset configuration
    preset = get_preset_config(args.preset)
    
    # Parse aspect ratio
    width, height = parse_aspect_ratio(args.aspect_ratio)
    if args.width:
        width = args.width
    if args.height:
        height = args.height
    
    # Determine steps from quality or explicit steps
    if args.steps:
        steps = args.steps
    else:
        steps = QUALITY_STEPS.get(args.quality, 30)
    
    # Use provided seed or random
    if seed is None:
        seed = args.seed if args.seed >= 0 else -1
    
    print(f"Generating image...")
    print(f"  Prompt: {args.prompt[:60]}...")
    print(f"  Size: {width}x{height}")
    print(f"  Steps: {steps}")
    print(f"  Preset: {args.preset}")
    
    try:
        result = client.generate(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            width=width,
            height=height,
            steps=steps,
            guidance_scale=args.guidance_scale,
            sharpness=args.sharpness,
            seed=seed,
            base_model=preset.get("base_model", "juggernautXL_v8Rundiffusion.safetensors"),
            refiner_model=preset.get("refiner_model", "None"),
            performance=preset.get("performance", "Quality"),
            styles=preset.get("styles"),
            input_image=args.input_image,
            mask_image=args.mask_image,
            image_prompt=args.image_prompt,
            image_prompt_weight=args.image_prompt_weight,
            variation_strength=args.variation_strength,
            upscale=args.upscale,
            outpaint=args.outpaint,
            outpaint_direction=args.outpaint_direction,
            face_swap=args.face_swap,
        )
        
        # Extract and save image
        # Note: Actual response format may vary based on Fooocus version
        if "data" in result and len(result["data"]) > 0:
            image_data = result["data"][0]
            if isinstance(image_data, str) and image_data.startswith("data:image"):
                # Extract base64 data
                image_data = image_data.split(",")[1]
            
            image = client.decode_image(image_data)
            image.save(output_path)
            print(f"✓ Saved: {output_path}")
            return output_path
        else:
            raise RuntimeError("No image data in response")
            
    except Exception as e:
        print(f"✗ Generation failed: {e}")
        raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate images using Fooocus",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic text-to-image
  %(prog)s --prompt "a beautiful sunset" --output sunset.png
  
  # With style preset
  %(prog)s --prompt "anime girl" --preset anime --output anime.png
  
  # Image variation
  %(prog)s --prompt "different lighting" --input-image photo.png --output variation.png
  
  # Batch generation
  %(prog)s --prompt "fantasy castle" --batch-size 4 --output-dir ./batch
        """
    )
    
    # Core parameters
    parser.add_argument("--prompt", "-p", required=True, help="Text prompt for generation")
    parser.add_argument("--negative-prompt", "-np", default="", help="Negative prompt")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--output-dir", "-d", help="Output directory for batch generation")
    parser.add_argument("--filename-prefix", default="fooocus", help="Filename prefix for batch")
    
    # Style and preset
    parser.add_argument("--preset", default="default", 
                       choices=list(PRESETS.keys()),
                       help="Style preset to use")
    
    # Image dimensions
    parser.add_argument("--aspect-ratio", "-ar", default="1:1",
                       help="Aspect ratio (1:1, 4:3, 16:9, etc.)")
    parser.add_argument("--width", type=int, help="Image width (overrides aspect-ratio)")
    parser.add_argument("--height", type=int, help="Image height (overrides aspect-ratio)")
    
    # Quality parameters
    parser.add_argument("--quality", "-q", type=int, default=1, choices=[1, 2, 3],
                       help="Quality level (1=fast, 2=balanced, 3=best)")
    parser.add_argument("--steps", type=int, help="Number of sampling steps")
    parser.add_argument("--guidance-scale", "-cfg", type=float, default=7.0,
                       help="Classifier-free guidance scale")
    parser.add_argument("--sharpness", "-s", type=float, default=2.0,
                       help="Image sharpness")
    
    # Seed
    parser.add_argument("--seed", type=int, default=-1,
                       help="Random seed (-1 for random)")
    
    # Image-to-image parameters
    parser.add_argument("--input-image", "-i", help="Input image path")
    parser.add_argument("--mask-image", "-m", help="Mask image for inpainting")
    parser.add_argument("--variation-strength", type=float, default=0.5,
                       help="Variation strength for img2img (0.0-1.0)")
    parser.add_argument("--upscale", type=int, default=1, choices=[1, 2, 4],
                       help="Upscale factor")
    
    # Outpainting
    parser.add_argument("--outpaint", action="store_true",
                       help="Enable outpainting")
    parser.add_argument("--outpaint-direction", default="all",
                       choices=["left", "right", "top", "bottom", "all"],
                       help="Outpaint direction")
    
    # Image prompt (IP-Adapter)
    parser.add_argument("--image-prompt", help="Reference image for style transfer")
    parser.add_argument("--image-prompt-weight", type=float, default=1.0,
                       help="Weight for image prompt")
    
    # Face swap
    parser.add_argument("--face-swap", help="Source face image for face swap")
    
    # Batch generation
    parser.add_argument("--batch-size", "-b", type=int, default=1,
                       help="Number of images to generate")
    
    # API configuration
    parser.add_argument("--api-url", default=DEFAULT_API_URL,
                       help="Fooocus API URL")
    parser.add_argument("--natural", action="store_true",
                       help="Parse natural language for parameters")
    
    args = parser.parse_args()
    
    # Create client
    client = FooocusClient(args.api_url)
    
    # Check connection
    print("Checking Fooocus connection...")
    if not client.check_connection():
        print(f"❌ Cannot connect to Fooocus at {args.api_url}")
        print("   Make sure Fooocus is running:")
        print("   cd ~/Fooocus && python entry_with_update.py")
        sys.exit(1)
    print("✓ Connected to Fooocus")
    
    # Apply natural language parsing if requested
    if args.natural:
        nl_params = natural_language_to_params(args.prompt)
        if "preset" in nl_params and args.preset == "default":
            args.preset = nl_params["preset"]
        if "aspect_ratio" in nl_params and args.aspect_ratio == "1:1":
            args.aspect_ratio = nl_params["aspect_ratio"]
        print(f"Detected style: {args.preset}")
    
    # Determine output path
    if args.batch_size > 1:
        # Batch mode
        output_dir = args.output_dir or "."
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nGenerating {args.batch_size} images...")
        for i in range(args.batch_size):
            seed = args.seed if args.seed >= 0 else -1
            if seed >= 0:
                seed = seed + i
            
            output_path = os.path.join(
                output_dir,
                f"{args.filename_prefix}_{i+1:03d}.png"
            )
            
            try:
                generate_single(client, args, output_path, seed)
            except Exception as e:
                print(f"Failed to generate image {i+1}: {e}")
                continue
        
        print(f"\n✓ Batch complete. Images saved to {output_dir}")
    else:
        # Single image mode
        if not args.output:
            print("Error: --output required for single image generation")
            sys.exit(1)
        
        output_path = generate_single(client, args, args.output)
        print(f"\n✓ Generation complete!")


if __name__ == "__main__":
    main()
