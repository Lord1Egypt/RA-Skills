#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create and upload default cover image for WeChat Official Account

This script creates a simple cover image with text and uploads it to WeChat.
The media_id can then be used for article publishing.

Usage:
    python create_default_cover.py
"""

import json
import logging
import os
import sys
from pathlib import Path

try:
    import requests
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install requests pillow")
    sys.exit(1)

# WeChat Official Account Credentials
APPID = "wxf9400829e3405317"
APPSECRET = "a6800143c01df2e73121c631cac4ec32"

# API Endpoints
TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
UPLOAD_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_access_token(appid, appsecret):
    """Get access token from WeChat API"""
    params = {
        'grant_type': 'client_credential',
        'appid': appid,
        'secret': appsecret
    }

    try:
        response = requests.get(TOKEN_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'access_token' in data:
            logger.info("✓ Access token obtained")
            return data['access_token']
        else:
            logger.error(f"Failed to get token: {data.get('errmsg', 'Unknown error')}")
            return None
    except Exception as e:
        logger.error(f"Error getting token: {e}")
        return None


def create_cover_image(output_path, title_text):
    """
    Create a simple cover image with text

    Args:
        output_path: Path to save the image
        title_text: Text to display on the cover
    """
    # WeChat cover image size: 900x386 pixels
    width, height = 900, 383

    # Create image with gradient background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Create gradient background (blue to purple)
    for y in range(height):
        r = int(52 + (155 - 52) * y / height)
        g = int(152 + (89 - 152) * y / height)
        b = int(219 + (182 - 219) * y / height)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))

    # Try to use a Chinese font, fallback to default
    font_size = 48
    try:
        # Try common Chinese fonts on Windows
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",  # Microsoft YaHei
            "C:/Windows/Fonts/simhei.ttf",  # SimHei
            "C:/Windows/Fonts/simsun.ttc",  # SimSun
        ]
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
                break

        if not font:
            logger.warning("Chinese font not found, using default")
            font = ImageFont.load_default()
    except Exception as e:
        logger.warning(f"Error loading font: {e}, using default")
        font = ImageFont.load_default()

    # Split title into multiple lines if too long
    max_chars_per_line = 20
    lines = []
    current_line = ""

    for char in title_text:
        if len(current_line) >= max_chars_per_line:
            lines.append(current_line)
            current_line = char
        else:
            current_line += char

    if current_line:
        lines.append(current_line)

    # Draw text centered
    y_offset = (height - len(lines) * (font_size + 10)) // 2

    for line in lines:
        # Get text bounding box
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (width - text_width) // 2
        y = y_offset

        # Draw text shadow
        draw.text((x + 2, y + 2), line, font=font, fill=(0, 0, 0, 128))
        # Draw text
        draw.text((x, y), line, font=font, fill='white')

        y_offset += font_size + 10

    # Add subtitle
    subtitle = "AI内容生产工厂"
    subtitle_font_size = 32
    try:
        subtitle_font = ImageFont.truetype(font_paths[0], subtitle_font_size) if os.path.exists(font_paths[0]) else font
    except:
        subtitle_font = font

    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    x = (width - subtitle_width) // 2
    y = height - 80

    draw.text((x + 2, y + 2), subtitle, font=subtitle_font, fill=(0, 0, 0, 128))
    draw.text((x, y), subtitle, font=subtitle_font, fill='white')

    # Save image
    img.save(output_path, 'JPEG', quality=95)
    logger.info(f"✓ Cover image created: {output_path}")

    return output_path


def upload_cover_image(access_token, image_path):
    """
    Upload cover image to WeChat as permanent material

    Args:
        access_token: WeChat access token
        image_path: Path to image file

    Returns:
        media_id if successful, None otherwise
    """
    url = f"{UPLOAD_URL}?access_token={access_token}&type=image"

    try:
        with open(image_path, 'rb') as f:
            files = {'media': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(url, files=files, timeout=30)
            response.raise_for_status()
            data = response.json()

            if 'media_id' in data:
                media_id = data['media_id']
                logger.info(f"✓ Image uploaded successfully")
                logger.info(f"✓ Media ID: {media_id}")
                return media_id
            else:
                logger.error(f"Upload failed: {data.get('errmsg', 'Unknown error')}")
                return None

    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        return None


def save_media_id(media_id, config_path):
    """Save media_id to config file"""
    config = {
        'default_cover_media_id': media_id,
        'created_at': str(Path(config_path).stat().st_mtime if Path(config_path).exists() else 'new')
    }

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    logger.info(f"✓ Media ID saved to: {config_path}")


def main():
    """Main entry point"""
    # Paths
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent / "assets"
    output_dir.mkdir(exist_ok=True)

    image_path = output_dir / "default_cover.jpg"
    config_path = script_dir / "wechat_config.py"

    # Cover text
    title_text = "Claude Skill打造内容生成分发工厂"

    print("\n" + "=" * 60)
    print("Creating and uploading default cover image...")
    print("=" * 60 + "\n")

    # Step 1: Create cover image
    logger.info("Step 1: Creating cover image...")
    create_cover_image(image_path, title_text)

    # Step 2: Get access token
    logger.info("\nStep 2: Getting access token...")
    access_token = get_access_token(APPID, APPSECRET)
    if not access_token:
        print("\n✗ Failed to get access token")
        sys.exit(1)

    # Step 3: Upload image
    logger.info("\nStep 3: Uploading image to WeChat...")
    media_id = upload_cover_image(access_token, image_path)
    if not media_id:
        print("\n✗ Failed to upload image")
        sys.exit(1)

    # Step 4: Save media_id to config
    logger.info("\nStep 4: Saving media_id to config...")

    # Update wechat_config.py
    config_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat Publishing Configuration
Auto-generated by create_default_cover.py
"""

# Default cover image media_id
DEFAULT_COVER_MEDIA_ID = "{media_id}"

# WeChat Official Account Credentials
APPID = "{APPID}"
APPSECRET = "{APPSECRET}"
'''

    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)

    logger.info(f"✓ Configuration saved to: {config_path}")

    print("\n" + "=" * 60)
    print("✓ SUCCESS!")
    print(f"Cover image: {image_path}")
    print(f"Media ID: {media_id}")
    print(f"Config file: {config_path}")
    print("=" * 60 + "\n")

    return media_id


if __name__ == '__main__':
    main()
