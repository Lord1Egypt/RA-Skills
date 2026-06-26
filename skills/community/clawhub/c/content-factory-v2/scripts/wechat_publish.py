#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat Official Account Auto-Publishing Script

This script publishes HTML articles to WeChat Official Account for preview.
It handles authentication, cover image upload, draft creation, and preview link generation.

Usage:
    python wechat_publish.py --html "path/to/article.html" --cover "path/to/cover.png"

Requirements:
    pip install requests beautifulsoup4
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install requests beautifulsoup4")
    sys.exit(1)


# Load environment variables from .env file
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

# Get credentials from environment variables or config file
try:
    from wechat_config import DEFAULT_COVER_MEDIA_ID, APPID, APPSECRET
    print("ℹ️  Using credentials from wechat_config.py (deprecated, please migrate to .env)")
except ImportError:
    # Get from environment variables (no hardcoded fallback)
    APPID = os.environ.get('WECHAT_APP_ID')
    APPSECRET = os.environ.get('WECHAT_APP_SECRET')
    DEFAULT_COVER_MEDIA_ID = None

    # Validate credentials
    if not APPID or not APPSECRET:
        print("\n❌ Error: WeChat credentials not configured!")
        print("\n📝 Please set up your credentials:")
        print("   1. Copy .env.example to .env")
        print("   2. Edit .env and add your WeChat credentials:")
        print("      WECHAT_APP_ID=your-app-id")
        print("      WECHAT_APP_SECRET=your-app-secret")
        print("\n   Or set environment variables:")
        print("      $env:WECHAT_APP_ID='your-app-id'")
        print("      $env:WECHAT_APP_SECRET='your-app-secret'")
        print("\n   Get credentials from: https://mp.weixin.qq.com/")
        sys.exit(1)

# Proxy configuration (Tencent Cloud SCF with fixed egress IP)
# When set, all WeChat API calls route through the proxy to avoid IP whitelist issues.
WECHAT_PROXY_URL = os.environ.get('WECHAT_PROXY_URL', '')  # e.g. https://service-xxxxx-xxxxx.gz.apigw.tencentcs.com
WECHAT_PROXY_TOKEN = os.environ.get('WECHAT_PROXY_TOKEN', '')

# API Endpoints - use proxy if configured, otherwise direct
if WECHAT_PROXY_URL:
    _base = WECHAT_PROXY_URL.rstrip('/')
    TOKEN_URL = f"{_base}/token"
    UPLOAD_IMG_URL = f"{_base}/uploadimg"
    UPLOAD_MATERIAL_URL = f"{_base}/add_material"
    DRAFT_ADD_URL = f"{_base}/draft/add"
    PREVIEW_URL = f"{_base}/freepublish"
else:
    TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
    UPLOAD_IMG_URL = "https://api.weixin.qq.com/cgi-bin/media/uploadimg"
    UPLOAD_MATERIAL_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    DRAFT_ADD_URL = "https://api.weixin.qq.com/cgi-bin/draft/add"
    PREVIEW_URL = "https://api.weixin.qq.com/cgi-bin/freepublish/submit"

# Configure logging
LOG_DIR = Path(r"D:\AI\contents\CCoutput")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "publish_errors.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class WeChatPublisher:
    """WeChat Official Account Publisher"""

    def __init__(self, appid, appsecret):
        self.appid = appid
        self.appsecret = appsecret
        self.access_token = None
        self.token_expires_at = 0
        self._proxy_headers = {}
        if WECHAT_PROXY_URL and WECHAT_PROXY_TOKEN:
            self._proxy_headers = {'X-Proxy-Token': WECHAT_PROXY_TOKEN}
            logger.info(f"Using WeChat API proxy: {WECHAT_PROXY_URL}")

    def get_access_token(self):
        """
        Get access token from WeChat API.
        Tokens are cached for 2 hours (7200 seconds).
        """
        # Check if cached token is still valid
        if self.access_token and time.time() < self.token_expires_at:
            logger.info("Using cached access token")
            return self.access_token

        # Request new token
        params = {
            'grant_type': 'client_credential',
            'appid': self.appid,
            'secret': self.appsecret
        }

        try:
            response = requests.get(TOKEN_URL, params=params, headers=self._proxy_headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'access_token' in data:
                self.access_token = data['access_token']
                # Token expires in 7200 seconds, cache for 7000 to be safe
                self.token_expires_at = time.time() + 7000
                logger.info("Access token obtained successfully")
                return self.access_token
            else:
                error_msg = data.get('errmsg', 'Unknown error')
                logger.error(f"Failed to get access token: {error_msg}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error getting access token: {e}")
            return None

    def upload_cover_image(self, image_path):
        """
        Upload cover image to WeChat and get media_id.

        Args:
            image_path: Path to cover image file (jpg, png)

        Returns:
            media_id if successful, None otherwise
        """
        if not self.access_token:
            logger.error("No access token available")
            return None

        image_path = Path(image_path)
        if not image_path.exists():
            logger.error(f"Cover image not found: {image_path}")
            return None

        # Check file size (WeChat limit: 2MB for cover images)
        file_size = image_path.stat().st_size
        if file_size > 2 * 1024 * 1024:
            logger.error(f"Cover image too large: {file_size / 1024 / 1024:.2f}MB (max 2MB)")
            return None

        url = f"{UPLOAD_MATERIAL_URL}?access_token={self.access_token}&type=thumb"

        try:
            with open(image_path, 'rb') as f:
                files = {'media': (image_path.name, f, 'image/png')}
                response = requests.post(url, files=files, headers=self._proxy_headers, timeout=60)
                response.raise_for_status()
                data = response.json()

                if 'media_id' in data:
                    media_id = data['media_id']
                    logger.info(f"Cover image uploaded successfully: {media_id}")
                    return media_id
                else:
                    error_msg = data.get('errmsg', 'Unknown error')
                    logger.error(f"Failed to upload cover image: {error_msg}")
                    return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error uploading cover image: {e}")
            return None

    def upload_content_image(self, image_path):
        """
        Upload content image to WeChat and get URL.
        Uses uploadimg API which returns a permanent URL for article content.

        Args:
            image_path: Path to image file (jpg, png)

        Returns:
            image URL if successful, None otherwise
        """
        if not self.access_token:
            logger.error("No access token available")
            return None

        image_path = Path(image_path)
        if not image_path.exists():
            logger.error(f"Content image not found: {image_path}")
            return None

        # Check file size (WeChat limit: 10MB for content images)
        file_size = image_path.stat().st_size
        if file_size > 10 * 1024 * 1024:
            logger.error(f"Content image too large: {file_size / 1024 / 1024:.2f}MB (max 10MB)")
            return None

        url = f"{UPLOAD_IMG_URL}?access_token={self.access_token}"

        try:
            with open(image_path, 'rb') as f:
                files = {'media': (image_path.name, f, 'image/png')}
                response = requests.post(url, files=files, headers=self._proxy_headers, timeout=60)
                response.raise_for_status()
                data = response.json()

                if 'url' in data:
                    image_url = data['url']
                    logger.info(f"Content image uploaded: {image_path.name} -> {image_url}")
                    return image_url
                else:
                    error_msg = data.get('errmsg', 'Unknown error')
                    logger.error(f"Failed to upload content image: {error_msg}")
                    return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error uploading content image: {e}")
            return None

    def extract_html_content(self, html_path):
        """
        Extract title and content from HTML file.
        Upload all images referenced in the HTML and replace with WeChat URLs.
        Convert HTML to WeChat-compatible format.

        Args:
            html_path: Path to HTML file

        Returns:
            dict with 'title', 'content', 'digest' keys
        """
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract title
            title_tag = soup.find('h1')
            title = title_tag.get_text().strip() if title_tag else "Untitled Article"

            # WeChat title limit: Maximum 64 characters
            max_title_length = 64
            if len(title) > max_title_length:
                title = title[:max_title_length]
                logger.warning(f"Title truncated to {max_title_length} characters")

            # Extract first paragraph as digest
            first_p = soup.find('p')
            digest = first_p.get_text().strip()[:120] if first_p else title[:120]

            # Get body content
            body = soup.find('body')
            if not body:
                body = soup

            # Remove script and style tags
            for tag in body.find_all(['script', 'style']):
                tag.decompose()

            # Upload all images and replace src with WeChat URLs
            html_dir = Path(html_path).parent
            img_tags = body.find_all('img')

            logger.info(f"Found {len(img_tags)} images in HTML")

            for img in img_tags:
                src = img.get('src')
                if not src:
                    continue

                # Skip if already a full URL
                if src.startswith('http://') or src.startswith('https://'):
                    continue

                # Resolve relative path
                img_path = html_dir / src
                if not img_path.exists():
                    logger.warning(f"Image not found: {img_path}")
                    continue

                # Upload image to WeChat
                wechat_url = self.upload_content_image(img_path)
                if wechat_url:
                    img['src'] = wechat_url
                    # Remove class attribute as WeChat doesn't support custom classes
                    if img.get('class'):
                        del img['class']
                    # Add inline styles for image display
                    img['style'] = 'max-width: 100%; height: auto; display: block; margin: 20px auto;'
                    logger.info(f"Replaced {src} with {wechat_url}")
                else:
                    logger.warning(f"Failed to upload image: {src}")

            # Convert to WeChat-compatible HTML
            # WeChat supports limited inline styles, so we need to convert CSS classes to inline styles

            # Process headings
            for h2 in body.find_all('h2'):
                h2['style'] = 'font-size: 24px; margin-top: 40px; color: #1a5490; border-left: 4px solid #2980b9; padding-left: 14px; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);'
                if h2.get('class'):
                    del h2['class']

            for h3 in body.find_all('h3'):
                h3['style'] = 'font-size: 19px; margin-top: 30px; color: #2c5282;'
                if h3.get('class'):
                    del h3['class']

            for h4 in body.find_all('h4'):
                h4['style'] = 'font-size: 16px; margin-top: 20px; color: #34495e;'
                if h4.get('class'):
                    del h4['class']

            # Process paragraphs - preserve ALL existing inline styles
            # Only apply default style to paragraphs that have no existing style
            for p in body.find_all('p'):
                existing = p.get('style', '')
                if not existing:
                    p['style'] = 'margin: 10px 0; line-height: 1.8; color: #333;'
                # If paragraph already has custom style (border-left, background, etc.), preserve it
                if p.get('class'):
                    del p['class']

            # Process blockquotes - preserve existing styles, use olive green for custom ones
            for blockquote in body.find_all('blockquote'):
                existing = blockquote.get('style', '')
                if '556b2f' in existing or 'border-left' in existing:
                    # Preserve custom border-left style
                    if blockquote.get('class'):
                        del blockquote['class']
                else:
                    blockquote['style'] = 'border-left: 4px solid #556b2f; padding: 16px 20px; color: #34495e; margin: 28px 0; background: #ebf5fb; border-radius: 4px;'
                    if blockquote.get('class'):
                        del blockquote['class']

            # Process strong tags - preserve existing styles, only add default if plain
            for strong in body.find_all('strong'):
                existing = strong.get('style', '')
                if not existing:
                    strong['style'] = 'color: #556b2f; font-weight: 600;'

            # Process lists
            for ul in body.find_all('ul'):
                ul['style'] = 'margin-left: 22px; line-height: 1.8;'
                if ul.get('class'):
                    del ul['class']

            for ol in body.find_all('ol'):
                ol['style'] = 'margin-left: 22px; line-height: 1.8;'
                if ol.get('class'):
                    del ol['class']

            for li in body.find_all('li'):
                li['style'] = 'margin: 8px 0;'
                if li.get('class'):
                    del li['class']

            # Remove blank lines between list items for WeChat compatibility
            # WeChat adds extra bullets for whitespace between <li> elements
            for list_tag in body.find_all(['ul', 'ol']):
                # Remove all NavigableString (text/whitespace) nodes between li elements
                for child in list(list_tag.children):
                    if child.name != 'li' and isinstance(child, str) and child.strip() == '':
                        child.extract()

            # Process spans with classes
            for span in body.find_all('span'):
                classes = span.get('class', [])
                if 'key-number' in classes:
                    span['style'] = 'color: #2980b9; font-weight: 700; font-size: 1.1em;'
                elif 'highlight-blue' in classes or 'highlight' in classes:
                    span['style'] = 'color: #2980b9; background: linear-gradient(180deg, transparent 60%, #d6eaf8 60%); padding: 2px 4px; font-weight: 600;'
                elif 'underline-dotted' in classes:
                    span['style'] = 'border-bottom: 2px dotted #3498db; padding-bottom: 2px;'
                if span.get('class'):
                    del span['class']

            # Process divs with classes
            for div in body.find_all('div'):
                classes = div.get('class', [])
                if 'data-box' in classes:
                    div['style'] = 'background: #ebf5fb; border-left: 4px solid #2980b9; padding: 16px 20px; margin: 20px 0; border-radius: 4px;'
                if div.get('class'):
                    del div['class']

            # Process figure and figcaption
            for figure in body.find_all('figure'):
                figure['style'] = 'margin: 40px 0;'
                if figure.get('class'):
                    del figure['class']

            for figcaption in body.find_all('figcaption'):
                figcaption['style'] = 'text-align: center; font-size: 14px; color: #7f8c8d; margin-top: 12px; font-style: italic;'
                if figcaption.get('class'):
                    del figcaption['class']

            # Process links
            for a in body.find_all('a'):
                a['style'] = 'color: #2980b9; text-decoration: none;'
                if a.get('class'):
                    del a['class']

            # Remove h1 from body (title is separate)
            for h1 in body.find_all('h1'):
                h1.decompose()

            content = str(body)

            logger.info(f"Extracted and converted content from HTML: {title}")

            return {
                'title': title,
                'content': content,
                'digest': digest
            }

        except Exception as e:
            logger.error(f"Error extracting HTML content: {e}")
            return None

    def create_draft(self, article_data, cover_media_id=None):
        """
        Create draft article in WeChat Official Account.

        Args:
            article_data: dict with 'title', 'content', 'digest'
            cover_media_id: Optional cover image media_id

        Returns:
            media_id if successful, None otherwise
        """
        if not self.access_token:
            logger.error("No access token available")
            return None

        url = f"{DRAFT_ADD_URL}?access_token={self.access_token}"

        # Build article payload
        article = {
            "title": article_data['title'],
            "author": "黎镭",
            "digest": article_data['digest'],
            "content": article_data['content'],
            "content_source_url": "",
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }

        # Add cover image if provided
        if cover_media_id:
            article["thumb_media_id"] = cover_media_id
            logger.info(f"Using cover image: {cover_media_id}")
        elif DEFAULT_COVER_MEDIA_ID:
            article["thumb_media_id"] = DEFAULT_COVER_MEDIA_ID
            logger.info(f"Using default cover image: {DEFAULT_COVER_MEDIA_ID}")
        else:
            logger.warning("No cover image provided")

        payload = {
            "articles": [article]
        }

        try:
            # Manually serialize JSON with ensure_ascii=False to preserve Chinese characters
            json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            headers.update(self._proxy_headers)
            response = requests.post(url, data=json_data, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            if 'media_id' in data:
                media_id = data['media_id']
                logger.info(f"Draft article created with media_id: {media_id}")
                return media_id
            else:
                error_msg = data.get('errmsg', 'Unknown error')
                logger.error(f"Failed to create draft: {error_msg}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error creating draft: {e}")
            return None

    def publish_preview(self, media_id):
        """
        Submit draft for preview.

        Note: WeChat API may require additional verification for actual publishing.
        This creates a preview that can be reviewed before publishing.

        Args:
            media_id: Media ID from draft creation

        Returns:
            Preview URL if successful, None otherwise
        """
        if not self.access_token:
            logger.error("No access token available")
            return None

        url = f"{PREVIEW_URL}?access_token={self.access_token}"

        payload = {
            "media_id": media_id
        }

        try:
            response = requests.post(url, json=payload, headers=self._proxy_headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get('errcode') == 0 or 'publish_id' in data:
                # Generate preview URL (actual URL format may vary)
                preview_url = f"https://mp.weixin.qq.com/s?__biz={self.appid}&mid={media_id}"
                logger.info(f"Preview submitted successfully")
                logger.info(f"Preview URL: {preview_url}")
                return preview_url
            else:
                error_msg = data.get('errmsg', 'Unknown error')
                logger.warning(f"Preview submission: {error_msg}")
                # Even if preview fails, draft is created and can be manually published
                logger.info(f"Draft created with media_id: {media_id}")
                logger.info("Please login to WeChat Official Account backend to publish manually:")
                logger.info("https://mp.weixin.qq.com/")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error publishing preview: {e}")
            logger.info(f"Draft created with media_id: {media_id}")
            logger.info("Please login to WeChat Official Account backend to publish manually")
            return None

    def publish_article(self, html_path, cover_path=None):
        """
        Main method to publish article from HTML file.

        Args:
            html_path: Path to HTML file
            cover_path: Optional path to cover image

        Returns:
            dict with 'success', 'preview_url', 'media_id' keys
        """
        logger.info(f"Starting publication for: {html_path}")

        # Step 1: Get access token
        if not self.get_access_token():
            return {
                'success': False,
                'error': 'Failed to obtain access token',
                'manual_url': 'https://mp.weixin.qq.com/'
            }

        # Step 2: Upload cover image if provided
        cover_media_id = None
        if cover_path:
            logger.info(f"Uploading cover image: {cover_path}")
            cover_media_id = self.upload_cover_image(cover_path)
            if not cover_media_id:
                logger.warning("Cover image upload failed, continuing without cover")

        # Step 3: Extract content
        article_data = self.extract_html_content(html_path)
        if not article_data:
            return {
                'success': False,
                'error': 'Failed to extract HTML content'
            }

        # Step 4: Create draft
        media_id = self.create_draft(article_data, cover_media_id)
        if not media_id:
            return {
                'success': False,
                'error': 'Failed to create draft',
                'manual_url': 'https://mp.weixin.qq.com/'
            }

        # Step 5: Publish preview
        preview_url = self.publish_preview(media_id)

        return {
            'success': True,
            'media_id': media_id,
            'preview_url': preview_url,
            'title': article_data['title'],
            'manual_url': 'https://mp.weixin.qq.com/'
        }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Publish HTML article to WeChat Official Account'
    )
    parser.add_argument(
        '--html',
        required=True,
        help='Path to HTML file to publish'
    )
    parser.add_argument(
        '--cover',
        help='Path to cover image (PNG/JPG, max 2MB)'
    )

    args = parser.parse_args()
    html_path = Path(args.html)
    cover_path = Path(args.cover) if args.cover else None

    # Validate HTML file exists
    if not html_path.exists():
        logger.error(f"HTML file not found: {html_path}")
        sys.exit(1)

    # Validate cover image if provided
    if cover_path and not cover_path.exists():
        logger.error(f"Cover image not found: {cover_path}")
        sys.exit(1)

    # Create publisher and publish
    publisher = WeChatPublisher(APPID, APPSECRET)
    result = publisher.publish_article(html_path, cover_path)

    # Print results
    print("\n" + "=" * 60)
    if result['success']:
        print("PUBLICATION SUCCESSFUL")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"Media ID: {result['media_id']}")
        if result.get('preview_url'):
            print(f"Preview URL: {result['preview_url']}")
        else:
            print(f"Manual Publishing Required:")
            print(f"Login at: {result['manual_url']}")
    else:
        print("PUBLICATION FAILED")
        print(f"Error: {result.get('error', 'Unknown error')}")
        if result.get('manual_url'):
            print(f"Please publish manually at: {result['manual_url']}")
    print("=" * 60)

    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()
