# -*- coding: utf-8 -*-
import os
import sys
import re
import time
import json
import logging
import argparse
import requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
WECHAT_API_URL = "https://api.weixin.qq.com"

class WeChatUploader:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.expires_at = 0

    def get_access_token(self):
        """Fetch or return cached access token"""
        current_time = time.time()
        if self.access_token and current_time < self.expires_at:
            return self.access_token

        url = f"{WECHAT_API_URL}/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        try:
            response = requests.get(url)
            data = response.json()
            if "access_token" in data:
                self.access_token = data["access_token"]
                self.expires_at = current_time + data["expires_in"] - 60  # Buffer time
                logger.info("Successfully obtained WeChat access token")
                # print(f"DEBUG: Token obtained successfully.")
                return self.access_token
            else:
                logger.error(f"Failed to get access token: {data}")
                print(f"❌ Failed to get access token: {data}")
                # raise Exception(f"WeChat API Error: {data}")
                return None
        except Exception as e:
            logger.error(f"Error fetching access token: {e}")
            print(f"❌ Error fetching access token: {e}")
            raise

    def upload_image(self, image_path_or_url):
        """Upload image to WeChat permanent material and return media_id and url"""
        token = self.get_access_token()
        if not token: return None, None
        
        # url = f"{WECHAT_API_URL}/cgi-bin/material/add_material?access_token={token}&type=image"
        # Since we are creating drafts, maybe try temporary media upload? Or just permanent image
        # Using permanent image upload as draft needs media_id
        url = f"{WECHAT_API_URL}/cgi-bin/media/uploadimg?access_token={token}" # For inside article images
        
        # Handle remote URL
        temp_file = None
        if image_path_or_url.startswith(('http://', 'https://')):
            try:
                # logger.info(f"Downloading image from URL: {image_path_or_url}")
                headers = {'User-Agent': 'Mozilla/5.0'}
                img_resp = requests.get(image_path_or_url, headers=headers, stream=True)
                img_resp.raise_for_status()
                
                # Create a temporary file
                filename = os.path.basename(image_path_or_url.split('?')[0])
                if not filename: filename = "temp_image.jpg"
                # Force jpg extension if missing, WeChat needs it
                if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    filename += ".jpg"
                
                temp_file = filename
                with open(temp_file, 'wb') as f:
                    for chunk in img_resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                image_path = temp_file
            except Exception as e:
                logger.error(f"Failed to download image: {e}")
                print(f"❌ Image download error: {e}")
                return None, None
        else:
            image_path = image_path_or_url

        # Check if file exists
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return None, None

        # Upload to WeChat
        try:
            # logger.info(f"Uploading image to WeChat: {image_path}")
            with open(image_path, 'rb') as f:
                files = {'media': (os.path.basename(image_path), f)}
                r = requests.post(url, files=files)
                res = r.json()
                
            if 'url' in res:
                return None, res['url'] # uploadimg only returns url, media_id is for thumb
            else:
                logger.error(f"Failed to upload image: {res}")
                return None, None
        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            return None, None
        finally:
            # Clean up temp file
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
                
    def upload_cover_image(self, image_path_or_url):
         """Upload cover image (thumb) which requires media_id"""
         token = self.get_access_token()
         if not token: return None
         
         # For cover image, use permanent material add
         url = f"{WECHAT_API_URL}/cgi-bin/material/add_material?access_token={token}&type=image"
         
         temp_file = None
         if image_path_or_url.startswith(('http://', 'https://')):
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                img_resp = requests.get(image_path_or_url, headers=headers, stream=True)
                img_resp.raise_for_status()
                filename = "cover_temp.jpg"
                with open(filename, 'wb') as f:
                    for chunk in img_resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                image_path = filename
                temp_file = filename
            except Exception as e:
                print(f"❌ Cover download error: {e}")
                return None
         else:
             image_path = image_path_or_url

         try:
            with open(image_path, 'rb') as f:
                files = {'media': (os.path.basename(image_path), f)}
                r = requests.post(url, files=files)
                res = r.json()
            if 'media_id' in res:
                return res['media_id']
            else:
                logger.error(f"Cover upload failed: {res}")
                print(f"❌ Cover upload failed: {res}")
                return None
         except Exception as e:
             print(f"❌ Cover upload failed: {e}")
             return None
         finally:
             if temp_file and os.path.exists(temp_file):
                 os.remove(temp_file)

    def simple_markdown_to_html(self, content):
        """Convert simple markdown to WeChat-compatible HTML"""
        html = content
        
        # Remove metadata block if present (e.g. at start of file)
        # Assuming metadata block like Jekyll front matter
        if html.startswith('---'):
            try:
                parts = html.split('---', 2)
                if len(parts) >= 3:
                     html = parts[2]
            except:
                pass

        # Bold
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        
        # Images: ![alt](url) -> <img src="url" alt="alt" />
        # Note: We will handle image replacement separately before calling this, 
        # but this handles any remaining ones or standard format
        # html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" />', html)
        
        # Headers - Convert only # to h1/h2 to avoid styling issues, standard p tags
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        lines = html.split('\n')
        new_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                new_lines.append('<br/>') 
                continue
            
            # If line is an image tag (created by us), don't wrap in p
            if line.startswith('<img'):
                new_lines.append(line)
            elif line.startswith('<h'):
                new_lines.append(line)
            else:
                new_lines.append(f'<p>{line}</p>')
        
        return '\n'.join(new_lines)

    def create_draft(self, title, content, thumb_media_id):
        """Create a draft in WeChat"""
        token = self.get_access_token()
        if not token: return
        
        url = f"{WECHAT_API_URL}/cgi-bin/draft/add?access_token={token}"
        
        article = {
            "title": title,
            "author": "Liuu",
            "digest": "", # Optional: summary
            "content": content,
            "content_source_url": "",
            "thumb_media_id": thumb_media_id,
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }
        
        payload = {"articles": [article]}
        
        try:
            logger.info("Creating draft...")
            # Ensure proper JSON encoding with utf-8
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            response = requests.post(url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), headers=headers)
            res = response.json()
            
            if 'media_id' in res:
                logger.info(f"Successfully created draft! Media ID: {res['media_id']}")
                print(f"\n✅ **上传成功！**")
                print(f"📂 草稿ID: {res['media_id']}")
                print("👉 请在微信公众号后台/订阅号助手App查看草稿箱。")
            else:
                logger.error(f"Failed to create draft: {res}")
                print(f"❌ Failed to create draft: {res}")
        except Exception as e:
            logger.error(f"Error creating draft: {e}")
            print(f"❌ Error creating draft: {e}")

    def run_manual(self, title, raw_content):
         # 1. Look for images in content
         images = re.findall(r'!\[(.*?)\]\((.*?)\)', raw_content)
         
         thumb_media_id = None
         processed_content = raw_content
         
         # 2. Upload images found in content
         for i, (alt, url) in enumerate(images):
             logger.info(f"Processing image {i+1}: {url}")
             # Add cover logic: first image as cover
             if i == 0:
                 thumb_media_id = self.upload_cover_image(url)
             
             # Upload for article body (returns URL)
             _, wechat_url = self.upload_image(url)
             if wechat_url:
                 # Replace markdown image with HTML img tag
                 processed_content = processed_content.replace(f'![{alt}]({url})', f'<img src="{wechat_url}" alt="{alt}" />')
         
         # If no images, use a default fallback or warn
         if not thumb_media_id:
             print("⚠️ No images found in content. Using a default cover is recommended strictly.")
             # Fallback to a placeholder if you have one, or fail. WeChat requires thumb_media_id.
             # For now, let's try to upload a default "Sincere" style cover if none exists
             # placeholder_url = "https://via.placeholder.com/900x383.png?text=Cover"
             # thumb_media_id = self.upload_cover_image(placeholder_url)
             print("❌ Error: WeChat requires a cover image (thumb_media_id). Please include at least one image in markdown.")
             return

         # 3. Format to HTML
         html_content = self.simple_markdown_to_html(processed_content)
         
         # 4. Create Draft
         self.create_draft(title, html_content, thumb_media_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manual WeChat Article Uploader')
    parser.add_argument('--title', help='Article Title')
    parser.add_argument('--content', help='Article Content')
    parser.add_argument('file', nargs='?', help='Path to markdown file (optional)')
    args = parser.parse_args()

    # Load credentials
    # 1. Environment variables
    app_id = os.environ.get('WECHAT_APP_ID')
    app_secret = os.environ.get('WECHAT_APP_SECRET')
    
    # 2. Try credentials file if env vars missing
    if not app_id or not app_secret:
        cred_path = os.path.expanduser("~/.openclaw/credentials/wechat.env")
        if os.path.exists(cred_path):
             with open(cred_path, 'r') as f:
                for line in f:
                    if line.startswith('WECHAT_APP_ID='):
                        app_id = line.split('=')[1].strip().strip('"').strip("'")
                    elif line.startswith('WECHAT_APP_SECRET='):
                        app_secret = line.split('=')[1].strip().strip('"').strip("'")

    if not app_id or not app_secret:
        print("❌ Error: WECHAT_APP_ID and WECHAT_APP_SECRET not found.")
        print("   Please set them in environment variables or ~/.openclaw/credentials/wechat.env")
        sys.exit(1)

    uploader = WeChatUploader(app_id, app_secret)

    if args.title and args.content:
        uploader.run_manual(args.title, args.content)
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
            # Try to extract title
            title_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else "New Article"
            uploader.run_manual(title, content)
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    else:
        print("❌ Error: Provide either --title/--content or a file path.")
