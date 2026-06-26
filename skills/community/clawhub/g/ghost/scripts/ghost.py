#!/usr/bin/env python3
"""
Ghost CMS Admin API Client
支持：发布、更新、删除文章
"""

import json
import sys
import os
import re
from datetime import datetime, timedelta
import requests
import jwt

# Ghost API 配置
def get_config(config_path):
    """
    获取配置 - 唯一方式：自定义配置文件路径（项目隔离）
    
    Args:
        config_path: Path to JSON configuration file (e.g., "../../projects/fuye/ghost-admin.config.json")
    
    Returns:
        Config dict with api_url and admin_api_key
    """
    if not config_path:
        raise ValueError("❌ 必须提供 config_path 参数。Ghost API 调用唯一方式：自定义配置文件路径")
    
    target_file = os.path.expanduser(config_path)
    
    if not os.path.exists(target_file):
        raise FileNotFoundError(f"❌ 配置文件不存在: {target_file}")
    
    try:
        with open(target_file, 'r') as f:
            file_config = json.load(f)
            config = {
                'api_url': file_config.get('api_url', ''),
                'admin_api_key': file_config.get('admin_api_key', '')
            }
            if not config['api_url'] or not config['admin_api_key']:
                raise ValueError(f"❌ 配置文件 {target_file} 缺少 api_url 或 admin_api_key 字段")
            return config
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ 配置文件 {target_file} JSON 格式错误: {e}")
    except Exception as e:
        raise RuntimeError(f"❌ 加载配置文件 {target_file} 失败: {e}")

def generate_token(api_key):
    """生成 Ghost Admin API JWT Token"""
    if not api_key or ':' not in api_key:
        return None
    
    key_id, secret = api_key.split(':', 1)
    
    # Ghost 使用 HS256 算法
    token = jwt.encode(
        {
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=5),
            'aud': '/admin/'
        },
        bytes.fromhex(secret),
        algorithm='HS256',
        headers={'kid': key_id}
    )
    return token

def get_headers(api_key, content_type='application/json'):
    """获取请求头"""
    token = generate_token(api_key)
    headers = {
        'Authorization': f'Ghost {token}'
    }
    if content_type:
        headers['Content-Type'] = content_type
    return headers

def upload_image(config, image_path):
    """上传本地图片到 Ghost 获取 URL"""
    if not image_path:
        return None
        
    if not os.path.exists(image_path):
        print(f"❌ 本地图片文件不存在: {image_path}")
        return None
    
    # 规范化 URL
    api_url = config['api_url'].rstrip('/')
    url = f"{api_url}/images/upload/"
    
    try:
        # 自动判断 MIME 类型
        ext = os.path.splitext(image_path)[1].lower()
        mime_type = 'image/jpeg'
        if ext == '.png': mime_type = 'image/png'
        elif ext == '.gif': mime_type = 'image/gif'
        elif ext == '.webp': mime_type = 'image/webp'
        
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, mime_type)}
            headers = get_headers(config['admin_api_key'], None)
            
            print(f"⏳ 正在上传本地图片 {image_path} ({mime_type})...")
            response = requests.post(url, files=files, headers=headers)
            
            if response.status_code != 201:
                print(f"❌ 上传失败 (HTTP {response.status_code}): {response.text}")
                return None

            data = response.json()
            image_url = data.get('url') or data.get('images', [{}])[0].get('url')
            
            if image_url:
                print(f"✅ 图片上传成功: {image_url}")
                return image_url
            else:
                return None
    except Exception as e:
        print(f"❌ 上传过程出错: {e}")
        return None

def slugify(text):
    """生成 slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    return text[:100]

def download_image(url):
    """下载远程图片到临时文件"""
    try:
        print(f"⏳ 正在从远程下载图片: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # 提取扩展名
        import urllib.parse
        path = urllib.parse.urlparse(url).path
        ext = os.path.splitext(path)[1] or '.jpg'
        if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            ext = '.jpg'
            
        temp_path = f"temp_download_{int(datetime.now().timestamp())}{ext}"
        with open(temp_path, 'wb') as f:
            f.write(response.content)
        return temp_path
    except Exception as e:
        print(f"❌ 下载远程图片失败: {e}")
        return None

def create_post(config, title, content, status='draft', tags=None, excerpt=None, feature_image=None):
    """创建新文章 (自动检测并转换 Markdown)"""
    
    # 如果 feature_image 是远程 URL，尝试先下载并上传到 Ghost (确保稳定性)
    if feature_image and feature_image.startswith('http') and 'fu-ye.com' not in feature_image:
        print(f"📸 检测到外部图片 URL，正在尝试本地化上传...")
        local_path = download_image(feature_image)
        if local_path:
            ghost_image_url = upload_image(config, local_path)
            if ghost_image_url:
                feature_image = ghost_image_url
            # 清理临时文件
            try: os.remove(local_path)
            except: pass

    # 自动转换逻辑：如果内容包含 Markdown 特征（如 ## 或 **）且不包含大量的 <html> 标签
    if ('##' in content or '**' in content or '- ' in content) and '<p>' not in content:
        print("📝 检测到 Markdown 格式，正在自动转换为 HTML...")
        import re
        html = content
        # 基础 MD -> HTML 转换 (由于环境可能没安装 markdown 库，用正则做可靠转换)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        # 处理段落：将双换行符替换为 P标签包装
        paragraphs = html.split('\n\n')
        html = ''.join([f'<p>{p.strip()}</p>' for p in paragraphs if p.strip()])
        # 简单的列表清理
        html = html.replace('</li><p><li>', '</li><li>').replace('<li>', '<ul><li>').replace('</li>', '</li></ul>')
        content = html

    # 规范化 API URL (确保不出现双斜杠)
    api_url = config['api_url'].rstrip('/')
    url = f"{api_url}/posts/?source=html"
    
    post_data = {
        'posts': [{
            'title': title,
            'html': content,
            'slug': slugify(title),
            'status': status,  # draft 或 published
            'excerpt': excerpt or ''
        }]
    }
    
    if tags:
        post_data['posts'][0]['tags'] = [{'name': tag} for tag in tags]
    
    if feature_image:
        post_data['posts'][0]['feature_image'] = feature_image
    
    headers = get_headers(config['admin_api_key'])
    
    try:
        response = requests.post(url, json=post_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        post = data['posts'][0]
        print(f"✅ 文章创建成功")
        print(f"   ID: {post['id']}")
        print(f"   标题: {post['title']}")
        print(f"   URL: {post.get('url', 'N/A')}")
        print(f"   状态: {post['status']}")
        return post
    except requests.exceptions.RequestException as e:
        print(f"❌ 创建失败: {e}")
        if hasattr(e.response, 'text'):
            print(f"   错误详情: {e.response.text}")
        return None

def update_post(config, post_id, **kwargs):
    """更新文章"""
    api_url = config['api_url'].rstrip('/')
    url = f"{api_url}/posts/{post_id}/?source=html" # Added ?source=html for content fetching
    
    headers = get_headers(config['admin_api_key'])
    
    try:
        # 先获取文章，拿到 updated_at
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        existing_post = response.json()['posts'][0]
        
        update_data = {'posts': [{}]}
        update_data['posts'][0]['updated_at'] = existing_post['updated_at'] # 加上 updated_at
    
        if 'title' in kwargs:
            update_data['posts'][0]['title'] = kwargs['title']
        if 'content' in kwargs:
            # 如果是 Markdown，也进行转换
            new_content = kwargs['content']
            if ('##' in new_content or '**' in new_content or '- ' in new_content) and '<p>' not in new_content:
                print("📝 检测到 Markdown 格式，正在自动转换为 HTML...")
                html = new_content
                html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
                html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
                html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
                html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
                html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
                paragraphs = html.split('\n\n')
                html = ''.join([f'<p>{p.strip()}</p>' for p in paragraphs if p.strip()])
                html = html.replace('</li><p><li>', '</li><li>').replace('<li>', '</li><li>') # Simplified list
                update_data['posts'][0]['html'] = html
            else:
                update_data['posts'][0]['html'] = new_content
        if 'status' in kwargs:
            update_data['posts'][0]['status'] = kwargs['status']
        if 'excerpt' in kwargs:
            update_data['posts'][0]['excerpt'] = kwargs['excerpt']
        if 'tags' in kwargs:
            update_data['posts'][0]['tags'] = [{'name': tag} for tag in kwargs['tags']]
        if 'feature_image' in kwargs:
            update_data['posts'][0]['feature_image'] = kwargs['feature_image']
        
        # PUT 请求需要带上 ID
        url = f"{api_url}/posts/{post_id}/?source=html"
        response = requests.put(url, json=update_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        post = data['posts'][0]
        print(f"✅ 文章更新成功")
        print(f"   ID: {post['id']}")
        print(f"   标题: {post['title']}")
        print(f"   状态: {post['status']}")
        print(f"   URL: {post.get('url', 'N/A')}")
        return post
    except requests.exceptions.RequestException as e:
        print(f"❌ 更新失败: {e}")
        if hasattr(e.response, 'text'):
            print(f"   错误详情: {e.response.text}")
        return None

def delete_post(config, post_id):
    """删除文章"""
    url = f"{config['api_url']}/posts/{post_id}/"
    
    headers = get_headers(config['admin_api_key'])
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        print(f"✅ 文章删除成功")
        print(f"   ID: {post_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ 删除失败: {e}")
        if hasattr(e.response, 'text'):
            print(f"   错误详情: {e.response.text}")
        return False

def list_posts(config, limit=10):
    """列出文章"""
    url = f"{config['api_url']}/posts/?limit={limit}"
    
    headers = get_headers(config['admin_api_key'])
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        posts = data['posts']
        print(f"📄 最近 {len(posts)} 篇文章:")
        print("-" * 60)
        for post in posts:
            status = "🟢" if post['status'] == 'published' else "🟡"
            print(f"{status} [{post['id']}] {post['title']}")
            print(f"   状态: {post['status']} | 更新: {post['updated_at'][:10]}")
            print(f"   URL: {post.get('url', 'N/A')}")
            print()
        return posts
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取失败: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print(f"  {sys.argv[0]} <command> [args] --config path/to/config.json")
        print("")
        print("命令:")
        print("  create <title> <content> [--status published|draft] [--tags tag1,tag2] [--feature-image url] --config <path>")
        print("  upload <image_path> --config <path>")
        print("  update <post_id> [--title ...] [--content ...] [--status ...] [--tags ...] --config <path>")
        print("  delete <post_id> --config <path>")
        print("  list [limit] --config <path>")
        print("")
        print("唯一方式 - 自定义配置文件路径（项目隔离）:")
        print("  --config ../../projects/fuye/ghost-admin.config.json")
        sys.exit(1)

    # 提取 --config 参数（唯一方式）
    def pop_arg(flag):
        if flag in sys.argv:
            idx = sys.argv.index(flag)
            if idx + 1 < len(sys.argv):
                val = sys.argv[idx + 1]
                sys.argv.pop(idx + 1)
                sys.argv.pop(idx)
                return val
        return None

    config_path = pop_arg('--config')
    
    # 移除其他已废弃的参数（为了兼容性，只提示错误）
    deprecated_args = ['--site', '--api-url', '--api-key']
    for arg in deprecated_args:
        if arg in sys.argv:
            print(f"❌ 错误: 参数 {arg} 已废弃。Ghost API 调用唯一方式：--config 配置文件路径")
            sys.exit(1)
    
    if not config_path:
        print("❌ 错误: 必须提供 --config 参数指定配置文件路径")
        print("Ghost API 调用唯一方式：自定义配置文件路径（项目隔离）")
        print("示例: --config ../../projects/fuye/ghost-admin.config.json")
        sys.exit(1)
    
    try:
        config = get_config(config_path)
    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"{e}")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'create':
        if len(sys.argv) < 4:
            print("❌ 错误: 创建文章需要标题和内容")
            sys.exit(1)
        
        title = sys.argv[2]
        content = sys.argv[3]
        status = 'draft'
        tags = None
        feature_image = None
        
        # 解析额外参数
        i = 4
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == '--status' and i + 1 < len(sys.argv):
                status = sys.argv[i + 1]
                i += 2
            elif arg == '--tags' and i + 1 < len(sys.argv):
                tags = sys.argv[i + 1].split(',')
                i += 2
            elif arg == '--feature-image' and i + 1 < len(sys.argv):
                feature_image = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        
        create_post(config, title, content, status, tags, feature_image=feature_image)
    
    elif command == 'upload':
        if len(sys.argv) < 3:
            print("❌ 错误: 上传图片需要文件路径")
            sys.exit(1)
        
        image_path = sys.argv[2]
        upload_image(config, image_path)

    elif command == 'update':
        if len(sys.argv) < 3:
            print("❌ 错误: 更新文章需要 post_id")
            sys.exit(1)
        
        post_id = sys.argv[2]
        kwargs = {}
        
        # 解析参数
        i = 3
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == '--title' and i + 1 < len(sys.argv):
                kwargs['title'] = sys.argv[i + 1]
                i += 2
            elif arg == '--content' and i + 1 < len(sys.argv):
                kwargs['content'] = sys.argv[i + 1]
                i += 2
            elif arg == '--status' and i + 1 < len(sys.argv):
                kwargs['status'] = sys.argv[i + 1]
                i += 2
            elif arg == '--tags' and i + 1 < len(sys.argv):
                kwargs['tags'] = sys.argv[i + 1].split(',')
                i += 2
            else:
                i += 1
        
        update_post(config, post_id, **kwargs)
    
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("❌ 错误: 删除文章需要 post_id")
            sys.exit(1)
        
        post_id = sys.argv[2]
        delete_post(config, post_id)
    
    elif command == 'list':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        list_posts(config, limit)
    
    else:
        print(f"❌ 未知命令: {command}")
        print("支持的命令: create, upload, update, delete, list")

if __name__ == '__main__':
    main()
