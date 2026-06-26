#!/usr/bin/env python3
"""
Generate images using Dreamina (即梦) CLI.
Wrapper for jimeng/dreamina CLI integration.
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

def check_login():
    """Check if user is logged in to Dreamina."""
    result = subprocess.run(
        ["dreamina", "user_credit"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def get_credit():
    """Get remaining credit."""
    result = subprocess.run(
        ["dreamina", "user_credit"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        return json.loads(result.stdout)
    return None

def generate_image(prompt, ratio="16:9", model_version="5.0", 
                   resolution_type="2k", poll_seconds=60):
    """
    Generate image using Dreamina text2image.
    
    Args:
        prompt: Image generation prompt
        ratio: Aspect ratio (16:9, 9:16, 3:4, 1:1, etc.)
        model_version: 3.0, 3.1, 4.0, 4.1, 4.5, 4.6, 5.0, lab
        resolution_type: 2k or 4k
        poll_seconds: Wait for result up to N seconds
    
    Returns:
        dict with submit_id, status, and result_url
    """
    cmd = [
        "dreamina", "text2image",
        f"--prompt={prompt}",
        f"--ratio={ratio}",
        f"--model_version={model_version}",
        f"--resolution_type={resolution_type}",
        f"--poll={poll_seconds}"
    ]
    
    print(f"🎨 Generating image...")
    print(f"   Prompt: {prompt[:60]}...")
    print(f"   Ratio: {ratio}, Model: {model_version}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Generation failed: {result.stderr}")
        return None
    
    try:
        response = json.loads(result.stdout)
        return response
    except json.JSONDecodeError:
        print(f"⚠️  Could not parse response: {result.stdout}")
        return None

def query_result(submit_id):
    """Query result of a submitted task."""
    result = subprocess.run(
        ["dreamina", "query_result", f"--submit_id={submit_id}"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    return None

def upscale_image(submit_id):
    """Upscale an existing image."""
    result = subprocess.run(
        ["dreamina", "image_upscale", f"--submit_id={submit_id}"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    return None

def image_to_image(prompt, image_path, ratio="16:9", 
                   model_version="5.0", poll_seconds=60):
    """
    Image to image generation (style transfer, variation, etc.)
    """
    cmd = [
        "dreamina", "image2image",
        f"--prompt={prompt}",
        f"--image_path={image_path}",
        f"--ratio={ratio}",
        f"--model_version={model_version}",
        f"--poll={poll_seconds}"
    ]
    
    print(f"🎨 Image-to-image generation...")
    print(f"   Base: {image_path}")
    print(f"   Prompt: {prompt[:60]}...")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    
    print(f"❌ Failed: {result.stderr}")
    return None

def generate_ad_background(style, ratio="16:9", brand_type="automotive"):
    """
    Generate advertisement background based on style and brand type.
    
    Args:
        style: premium, warm, cool, dark, sunset, etc.
        ratio: 16:9, 9:16, 3:4, etc.
        brand_type: automotive, cultural, fragrance, tea, etc.
    """
    # Style-specific prompts
    style_prompts = {
        "premium": "luxury gradient background, deep blue to purple, soft light rays, premium automotive aesthetic, minimalist, high-end commercial photography style, clean, no text",
        "warm": "warm gradient background, orange to pink, energetic, vibrant, soft glow, modern commercial style, clean, no text",
        "cool": "cool gradient background, teal to cyan, eco-friendly, modern tech aesthetic, clean and fresh, no text",
        "dark": "dark premium background, deep navy to black, sophisticated, mysterious, subtle light rays, luxury feel, no text",
        "sunset": "golden sunset gradient, warm orange to red, emotional, aspirational, cinematic lighting, no text",
        "cultural": "traditional Chinese aesthetic, ink wash style, misty mountains, elegant, cultural heritage, serene atmosphere, no text",
        "fragrance": "soft pink and gold gradient, elegant, feminine, luxury cosmetics aesthetic, bokeh lights, dreamy atmosphere, no text",
        "tea": "natural green and beige tones, zen garden aesthetic, bamboo, peaceful, organic textures, traditional tea culture, no text"
    }
    
    # Brand-specific modifiers
    brand_modifiers = {
        "automotive": "automotive advertisement style, showroom quality lighting",
        "cultural": "Chinese cultural heritage, travel destination poster style",
        "fragrance": "perfume advertisement style, luxury beauty aesthetic",
        "tea": "tea ceremony aesthetic, traditional Chinese culture",
        "recruitment": "business professional, opportunity and growth",
        "welfare": "warm, caring, community spirit"
    }
    
    base_prompt = style_prompts.get(style, style_prompts["premium"])
    modifier = brand_modifiers.get(brand_type, "")
    
    full_prompt = f"{base_prompt}, {modifier}".strip(", ")
    
    return generate_image(
        prompt=full_prompt,
        ratio=ratio,
        model_version="5.0",
        resolution_type="2k"
    )

def main():
    parser = argparse.ArgumentParser(description="Dreamina image generation wrapper")
    parser.add_argument("--credit", action="store_true", help="Check credit balance")
    parser.add_argument("--prompt", help="Generation prompt")
    parser.add_argument("--ratio", default="16:9", help="Aspect ratio")
    parser.add_argument("--style", help="Preset style for backgrounds")
    parser.add_argument("--brand", default="automotive", help="Brand type")
    parser.add_argument("--output", "-o", help="Output info JSON path")
    
    args = parser.parse_args()
    
    if args.credit:
        credit = get_credit()
        if credit:
            print(f"💰 Credit Balance:")
            print(f"   VIP: {credit.get('vip_credit', 0)}")
            print(f"   Gift: {credit.get('gift_credit', 0)}")
            print(f"   Total: {credit.get('total_credit', 0)}")
        else:
            print("❌ Failed to get credit info")
        return
    
    if args.style:
        # Generate background with preset style
        result = generate_ad_background(args.style, args.ratio, args.brand)
    elif args.prompt:
        # Generate with custom prompt
        result = generate_image(args.prompt, args.ratio)
    else:
        parser.print_help()
        return
    
    if result:
        print(f"\n✅ Submitted successfully!")
        print(f"   Submit ID: {result.get('submit_id')}")
        print(f"   Status: {result.get('gen_status')}")
        
        if result.get('result_url'):
            print(f"   Result: {result['result_url']}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"   Saved to: {args.output}")

if __name__ == "__main__":
    main()
