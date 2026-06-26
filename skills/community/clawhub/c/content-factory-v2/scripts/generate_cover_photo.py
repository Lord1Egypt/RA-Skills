#!/usr/bin/env python3
"""
WeChat Cover Photo Generator using GLM-Image API
Generates professional cover photos for WeChat Official Account articles
Supports 900x386 pixel WeChat standard size (21:9) with flat vector illustration style
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

import requests

# Try to import PIL for image resizing
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  Warning: PIL/Pillow not installed. Image resizing will be skipped.")
    print("   Install with: pip install Pillow")


def load_env_file(env_path=".env"):
    """Load environment variables from .env file"""
    env_file = Path(env_path)
    if not env_file.exists():
        return False

    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                # Remove quotes
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                os.environ[key] = value
    return True


# Try to load .env file from script directory
script_dir = Path(__file__).parent.parent
env_path = script_dir / ".env"
if env_path.exists():
    load_env_file(env_path)


class GLMImageGenerator:
    """GLM-Image API client for generating cover photos"""

    API_ENDPOINT = "https://open.bigmodel.cn/api/paas/v4/images/generations"
    DEFAULT_MODEL = "glm-image"
    DEFAULT_SIZE = "1280x720"  # Generate at this size, then resize to 900x386 (21:9)
    DEFAULT_QUALITY = "standard"
    WECHAT_SIZE = (900, 386)  # WeChat Official Account cover size (21:9)

    def __init__(self, api_key: str):
        """
        Initialize GLM-Image generator

        Args:
            api_key: GLM API key for authentication
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def generate_image(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        size: str = DEFAULT_SIZE,
        quality: str = DEFAULT_QUALITY,
    ) -> dict:
        """
        Generate image using GLM-Image API

        Args:
            prompt: Text description for image generation
            model: Model to use (glm-image, cogview-4, etc.)
            size: Image size (1280x720, 1024x1024, etc.)
            quality: Image quality (standard, high)

        Returns:
            API response dict with image URL

        Raises:
            requests.RequestException: If API call fails
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
        }

        print(f"🎨 Generating cover photo with GLM-Image API...")
        print(f"   Model: {model}")
        print(f"   Size: {size}")
        print(f"   Quality: {quality}")
        print(f"   Prompt: {prompt[:100]}...")

        try:
            response = requests.post(
                self.API_ENDPOINT,
                headers=self.headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            result = response.json()

            if "data" in result and len(result["data"]) > 0:
                image_url = result["data"][0]["url"]
                print(f"✅ Image generated successfully!")
                print(f"   URL: {image_url}")
                return result
            else:
                raise ValueError("No image data in API response")

        except requests.RequestException as e:
            print(f"❌ API request failed: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"   Response: {e.response.text}")
            raise

    def download_image(self, image_url: str, output_path: str) -> bool:
        """
        Download image from temporary URL to local file

        Args:
            image_url: Temporary image URL from API
            output_path: Local file path to save image

        Returns:
            True if download successful, False otherwise
        """
        try:
            print(f"📥 Downloading image to: {output_path}")
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            # Create output directory if needed
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            # Save image
            with open(output_path, "wb") as f:
                f.write(response.content)

            file_size = os.path.getsize(output_path)
            print(f"✅ Image downloaded successfully!")
            print(f"   Size: {file_size / 1024:.1f} KB")
            print(f"   Path: {output_path}")
            return True

        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False

    def resize_to_wechat(self, input_path: str, output_path: str = None) -> bool:
        """
        Resize image to WeChat Official Account cover size (900x386)

        Args:
            input_path: Path to input image
            output_path: Path to save resized image (optional, defaults to input_path)

        Returns:
            True if resize successful, False otherwise
        """
        if not PIL_AVAILABLE:
            print("⚠️  Skipping resize: PIL/Pillow not installed")
            return False

        try:
            print(f"📐 Resizing image to WeChat size (900x386, 21:9)...")

            # Open image
            img = Image.open(input_path)
            original_size = img.size
            print(f"   Original size: {original_size[0]}x{original_size[1]}")

            # Calculate crop box to maintain aspect ratio
            target_ratio = self.WECHAT_SIZE[0] / self.WECHAT_SIZE[1]  # 900/383 ≈ 2.35
            img_ratio = img.width / img.height

            if img_ratio > target_ratio:
                # Image is wider, crop width
                new_width = int(img.height * target_ratio)
                left = (img.width - new_width) // 2
                crop_box = (left, 0, left + new_width, img.height)
            else:
                # Image is taller, crop height
                new_height = int(img.width / target_ratio)
                top = (img.height - new_height) // 2
                crop_box = (0, top, img.width, top + new_height)

            # Crop and resize
            img_cropped = img.crop(crop_box)
            img_resized = img_cropped.resize(self.WECHAT_SIZE, Image.Resampling.LANCZOS)

            # Save
            if output_path is None:
                output_path = input_path
            img_resized.save(output_path, quality=95, optimize=True)

            file_size = os.path.getsize(output_path)
            print(f"✅ Image resized successfully!")
            print(f"   New size: {self.WECHAT_SIZE[0]}x{self.WECHAT_SIZE[1]}")
            print(f"   File size: {file_size / 1024:.1f} KB")
            print(f"   Path: {output_path}")
            return True

        except Exception as e:
            print(f"❌ Resize failed: {e}")
            return False


def build_cover_prompt(
    title: str,
    theme: str,
    style: str = "flat vector illustration",
    color_scheme: str = "blue gradient",
) -> str:
    """
    Build optimized prompt for WeChat cover photo generation
    Uses flat vector illustration style (平面矢量插画风格)

    Args:
        title: Article title
        theme: Main theme/topic
        style: Visual style description (default: flat vector illustration)
        color_scheme: Color scheme preference

    Returns:
        Optimized prompt string for GLM-Image API
    """
    # Base template for WeChat covers with flat vector illustration style
    prompt = f"""平面矢量插画风格的微信公众号封面图，主题：{theme}。
扁平化设计，几何图形，简洁现代。
{color_scheme}背景，{style}风格。
文章标题：{title}。
900x386像素横版构图，高质量输出。
专业商务风格，适合企业内容传播，吸引眼球。"""

    return prompt.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Generate WeChat cover photo using GLM-Image API (900x386 flat vector style)"
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Article title",
    )
    parser.add_argument(
        "--theme",
        required=True,
        help="Main theme/topic (e.g., 'AI enterprise automation')",
    )
    parser.add_argument(
        "--style",
        default="flat vector illustration",
        help="Visual style (default: flat vector illustration)",
    )
    parser.add_argument(
        "--color-scheme",
        default="blue gradient",
        help="Color scheme (default: blue gradient)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path (e.g., output/2026-01-19-article-cover.png)",
    )
    parser.add_argument(
        "--model",
        default="glm-image",
        choices=["glm-image", "cogview-4-250304", "cogview-4", "cogview-3-flash"],
        help="GLM model to use (default: glm-image)",
    )
    parser.add_argument(
        "--size",
        default="1280x720",
        choices=["1024x1024", "1280x720", "720x1280", "1280x1280", "1568x1056", "1056x1568", "1472x1088", "1088x1472", "1728x960", "960x1728"],
        help="Initial generation size (default: 1280x720, will be resized to 900x386)",
    )
    parser.add_argument(
        "--quality",
        default="standard",
        choices=["standard", "high"],
        help="Image quality (default: standard)",
    )
    parser.add_argument(
        "--api-key",
        help="GLM API key (or set GLM_API_KEY environment variable)",
    )
    parser.add_argument(
        "--custom-prompt",
        help="Use custom prompt instead of auto-generated one",
    )
    parser.add_argument(
        "--no-resize",
        action="store_true",
        help="Skip resizing to 900x386 (keep original size)",
    )

    args = parser.parse_args()

    # Get API key from args or environment
    api_key = args.api_key or os.environ.get("GLM_API_KEY")
    if not api_key:
        print("❌ Error: GLM API key required!")
        print("   Set GLM_API_KEY environment variable or use --api-key argument")
        sys.exit(1)

    # Build or use custom prompt
    if args.custom_prompt:
        prompt = args.custom_prompt
    else:
        prompt = build_cover_prompt(
            title=args.title,
            theme=args.theme,
            style=args.style,
            color_scheme=args.color_scheme,
        )

    # Initialize generator
    generator = GLMImageGenerator(api_key)

    try:
        # Generate image
        result = generator.generate_image(
            prompt=prompt,
            model=args.model,
            size=args.size,
            quality=args.quality,
        )

        # Extract image URL
        image_url = result["data"][0]["url"]

        # Download image
        success = generator.download_image(image_url, args.output)

        if not success:
            print("\n❌ Failed to download image")
            sys.exit(1)

        # Resize to WeChat size (900x386) unless --no-resize flag is set
        if not args.no_resize:
            resize_success = generator.resize_to_wechat(args.output)
            if not resize_success and PIL_AVAILABLE:
                print("⚠️  Warning: Resize failed, but original image was saved")

        print("\n" + "=" * 60)
        print("✅ Cover photo generation completed!")
        print(f"   Output: {args.output}")
        if not args.no_resize and PIL_AVAILABLE:
            print(f"   Size: 900x386 (WeChat standard)")
        print("=" * 60)
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
