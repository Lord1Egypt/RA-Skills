#!/usr/bin/env python3
"""
Generate premium gradient backgrounds for car advertisements.
Uses DALL-E or similar image generation API.
"""

import argparse
import json
import sys
from pathlib import Path

# Color palette presets (Li Auto inspired)
COLOR_PALETTES = {
    "premium": {
        "primary": "#1a237e",
        "secondary": "#7c4dff",
        "name": "Deep blue to purple",
        "description": "Luxury, premium, sophisticated"
    },
    "warm": {
        "primary": "#ff6b35",
        "secondary": "#f7931e",
        "name": "Orange to pink",
        "description": "Energetic, sporty, youthful"
    },
    "cool": {
        "primary": "#00897b",
        "secondary": "#00bcd4",
        "name": "Teal to cyan",
        "description": "Tech, modern, clean"
    },
    "dark": {
        "primary": "#0d1b2a",
        "secondary": "#1b263b",
        "name": "Deep dark",
        "description": "Mysterious, premium, night"
    },
    "sunset": {
        "primary": "#ff512f",
        "secondary": "#dd2476",
        "name": "Sunset gradient",
        "description": "Warm, emotional, aspirational"
    }
}

def build_prompt(palette_key, style_hints=""):
    """Build image generation prompt for background."""
    palette = COLOR_PALETTES.get(palette_key, COLOR_PALETTES["premium"])
    
    base_prompt = f"""Premium gradient background for luxury car advertisement.
    Smooth gradient from {palette['primary']} to {palette['secondary']}.
    Subtle light rays and atmospheric effects.
    Clean, minimalist, high-end commercial photography style.
    No text, no objects, no car, no person.
    Abstract luxury automotive aesthetic.
    {style_hints}
    8K quality, professional lighting, cinematic."""
    
    return " ".join(base_prompt.split())

def generate_background(palette, output_path, size="1024x1536"):
    """
    Generate background using available image generation API.
    Falls back to creating a colored gradient with PIL if no API available.
    """
    try:
        # Try DALL-E first
        return generate_with_dalle(palette, output_path, size)
    except Exception as e:
        print(f"DALL-E failed: {e}, falling back to PIL gradient")
        return generate_with_pil(palette, output_path, size)

def generate_with_dalle(palette, output_path, size):
    """Generate using DALL-E API (requires OPENAI_API_KEY)."""
    import openai
    
    prompt = build_prompt(palette)
    
    client = openai.OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1
    )
    
    # Download and save image
    import requests
    image_url = response.data[0].url
    img_data = requests.get(image_url).content
    
    Path(output_path).write_bytes(img_data)
    return output_path

def generate_with_pil(palette, output_path, size):
    """Generate gradient using PIL (no API required)."""
    from PIL import Image, ImageDraw
    
    width, height = map(int, size.split('x'))
    palette_info = COLOR_PALETTES.get(palette, COLOR_PALETTES["premium"])
    
    # Parse hex colors
    c1 = tuple(int(palette_info["primary"][i:i+2], 16) for i in (1, 3, 5))
    c2 = tuple(int(palette_info["secondary"][i:i+2], 16) for i in (1, 3, 5))
    
    # Create gradient
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        # Linear interpolation
        ratio = y / height
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    img.save(output_path)
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Generate ad backgrounds")
    parser.add_argument("palette", choices=list(COLOR_PALETTES.keys()),
                       help="Color palette preset")
    parser.add_argument("--output", "-o", required=True,
                       help="Output file path")
    parser.add_argument("--size", default="1024x1536",
                       help="Image size (WxH)")
    parser.add_argument("--list-palettes", action="store_true",
                       help="List available palettes")
    
    args = parser.parse_args()
    
    if args.list_palettes:
        print("Available color palettes:")
        for key, info in COLOR_PALETTES.items():
            print(f"  {key}: {info['name']} - {info['description']}")
        return
    
    output_path = generate_background(args.palette, args.output, args.size)
    print(f"Generated background: {output_path}")

if __name__ == "__main__":
    main()
