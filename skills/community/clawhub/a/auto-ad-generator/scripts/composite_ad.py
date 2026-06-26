#!/usr/bin/env python3
"""
Composite car advertisement - layer car, background, text, logo.
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import json

# Typography presets
FONT_PRESETS = {
    "luxury": {
        "headline_font": "fonts/NotoSansSC-Bold.otf",
        "subtitle_font": "fonts/NotoSansSC-Light.otf",
        "headline_size": 80,
        "subtitle_size": 36,
        "slogan_size": 48
    },
    "sporty": {
        "headline_font": "fonts/NotoSansSC-Bold.otf",
        "subtitle_font": "fonts/NotoSansSC-Regular.otf",
        "headline_size": 90,
        "subtitle_size": 32,
        "slogan_size": 42
    },
    "minimal": {
        "headline_font": "fonts/NotoSansSC-Light.otf",
        "subtitle_font": "fonts/NotoSansSC-Thin.otf",
        "headline_size": 72,
        "subtitle_size": 28,
        "slogan_size": 36
    }
}

def load_image(path, size=None):
    """Load and optionally resize image."""
    img = Image.open(path).convert("RGBA")
    if size:
        img = img.resize(size, Image.Resampling.LANCZOS)
    return img

def create_drop_shadow(img, offset=(10, 10), blur_radius=20, shadow_color=(0, 0, 0, 128)):
    """Add drop shadow to image."""
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    
    # Create shadow layer
    alpha = img.split()[-1]
    shadow_layer = Image.new('RGBA', img.size, shadow_color)
    shadow_layer.putalpha(alpha)
    
    # Blur
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))
    
    return shadow_layer

def composite_layers(background_path, car_path, output_path, 
                     car_position="center", car_scale=0.7,
                     logo_path=None, celebrity_path=None):
    """
    Composite the advertisement layers.
    
    Layout (1080x1920):
    - Background: full canvas
    - Car: centered, 70% scale
    - Celebrity: optional, overlapping car or side
    - Logo: bottom corner
    """
    # Load background
    canvas = Image.open(background_path).convert("RGBA")
    target_size = (1080, 1920)
    canvas = canvas.resize(target_size, Image.Resampling.LANCZOS)
    
    # Load car
    car = Image.open(car_path).convert("RGBA")
    
    # Scale car to fit
    car_width = int(target_size[0] * car_scale)
    car_height = int(car.height * (car_width / car.width))
    car = car.resize((car_width, car_height), Image.Resampling.LANCZOS)
    
    # Calculate position
    if car_position == "center":
        x = (target_size[0] - car_width) // 2
        y = (target_size[1] - car_height) // 2 + 100  # Slightly lower
    elif car_position == "center-bottom":
        x = (target_size[0] - car_width) // 2
        y = target_size[1] - car_height - 100
    
    # Add shadow to car
    shadow = create_drop_shadow(car, offset=(15, 15), blur_radius=30)
    canvas.paste(shadow, (x + 15, y + 15), shadow)
    
    # Paste car
    canvas.paste(car, (x, y), car)
    
    # Add celebrity if provided
    if celebrity_path:
        celebrity = Image.open(celebrity_path).convert("RGBA")
        # Scale and position celebrity
        cel_height = int(target_size[1] * 0.6)
        cel_width = int(celebrity.width * (cel_height / celebrity.height))
        celebrity = celebrity.resize((cel_width, cel_height), Image.Resampling.LANCZOS)
        
        cel_x = target_size[0] - cel_width - 50
        cel_y = target_size[1] - cel_height - 50
        canvas.paste(celebrity, (cel_x, cel_y), celebrity)
    
    # Add logo if provided
    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")
        logo_width = 150
        logo_height = int(logo.height * (logo_width / logo.width))
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
        
        logo_x = 50
        logo_y = target_size[1] - logo_height - 50
        canvas.paste(logo, (logo_x, logo_y), logo)
    
    # Save
    canvas.convert("RGB").save(output_path, quality=95)
    return output_path

def add_text_layers(image_path, output_path, text_config, style="luxury"):
    """
    Add typography to the advertisement.
    
    text_config: {
        "headline": "理想i6",
        "subtitle": "新形态纯电五座SUV",
        "slogan": "理想，就是活成自己喜欢的样子"
    }
    """
    img = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    
    preset = FONT_PRESETS.get(style, FONT_PRESETS["luxury"])
    width, height = img.size
    
    # Load fonts (fallback to default if custom not available)
    try:
        headline_font = ImageFont.truetype(preset["headline_font"], preset["headline_size"])
        subtitle_font = ImageFont.truetype(preset["subtitle_font"], preset["subtitle_size"])
        slogan_font = ImageFont.truetype(preset["headline_font"], preset["slogan_size"])
    except:
        headline_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        slogan_font = ImageFont.load_default()
    
    # Draw headline (top area)
    headline = text_config.get("headline", "")
    if headline:
        # Add text with shadow
        bbox = draw.textbbox((0, 0), headline, font=headline_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = 150
        
        # Shadow
        draw.text((x + 3, y + 3), headline, font=headline_font, fill=(0, 0, 0, 100))
        # Main text
        draw.text((x, y), headline, font=headline_font, fill=(255, 255, 255, 255))
    
    # Draw subtitle
    subtitle = text_config.get("subtitle", "")
    if subtitle:
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = 150 + preset["headline_size"] + 20
        
        draw.text((x + 2, y + 2), subtitle, font=subtitle_font, fill=(0, 0, 0, 80))
        draw.text((x, y), subtitle, font=subtitle_font, fill=(255, 255, 255, 230))
    
    # Draw slogan (bottom area)
    slogan = text_config.get("slogan", "")
    if slogan:
        bbox = draw.textbbox((0, 0), slogan, font=slogan_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height - 250
        
        draw.text((x + 2, y + 2), slogan, font=slogan_font, fill=(0, 0, 0, 80))
        draw.text((x, y), slogan, font=slogan_font, fill=(255, 255, 255, 255))
    
    img.convert("RGB").save(output_path, quality=95)
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Composite car advertisement")
    parser.add_argument("--background", "-b", required=True, help="Background image")
    parser.add_argument("--car", "-c", required=True, help="Car image (transparent PNG)")
    parser.add_argument("--output", "-o", required=True, help="Output path")
    parser.add_argument("--logo", help="Logo image")
    parser.add_argument("--celebrity", help="Celebrity image")
    parser.add_argument("--car-scale", type=float, default=0.7, help="Car scale (0-1)")
    parser.add_argument("--text-config", help="JSON file with text content")
    parser.add_argument("--style", choices=["luxury", "sporty", "minimal"], 
                       default="luxury", help="Typography style")
    
    args = parser.parse_args()
    
    # Composite layers
    temp_output = args.output + ".temp.png"
    composite_layers(
        args.background, 
        args.car, 
        temp_output,
        car_scale=args.car_scale,
        logo_path=args.logo,
        celebrity_path=args.celebrity
    )
    
    # Add text if config provided
    if args.text_config:
        with open(args.text_config) as f:
            text_config = json.load(f)
        add_text_layers(temp_output, args.output, text_config, args.style)
        Path(temp_output).unlink()
    else:
        Path(temp_output).rename(args.output)
    
    print(f"Generated ad: {args.output}")

if __name__ == "__main__":
    main()
