#!/usr/bin/env python3
"""
微信公众号文章抓取 - 使用文章标题命名文件
"""

import sys

# 检查依赖
try:
    import requests
except ImportError:
    print("❌ 缺少依赖: requests")
    print("请安装: pip install requests")
    sys.exit(1)

import re
import html
import os
import hashlib
from urllib.parse import unquote
from datetime import datetime

def check_workspace():
    """检查并创建工作目录"""
    workspace = '/root/.openclaw/workspace'
    if not os.path.exists(workspace):
        os.makedirs(workspace, exist_ok=True)
        print(f"✅ 创建工作目录: {workspace}")
    return workspace

def extract_keywords(title):
    """从标题提取英文关键词"""
    # 提取英文单词（包括技术名词、品牌名等）
    english_words = re.findall(r'[A-Za-z][A-Za-z0-9_]+', title)
    
    # 如果找到英文单词，用前2-3个
    if english_words:
        keywords = '_'.join(english_words[:3])
        return keywords
    
    # 如果没有英文，提取数字
    numbers = re.findall(r'\d+', title)
    if numbers:
        return '_'.join(numbers[:2])
    
    # 兜底：用日期
    return datetime.now().strftime('%m%d')

def generate_filename(title, url):
    """生成文件名：日期_关键词.html"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    keywords = extract_keywords(title)
    
    if keywords:
        return f"{date_str}_{keywords}.html"
    else:
        # 用URL短码兜底
        url_hash = url.split('/')[-1][:8]
        return f"{date_str}_{url_hash}.html"

# 检查工作目录
workspace = check_workspace()

# 获取URL
url = sys.argv[1] if len(sys.argv) > 1 else ''

if not url:
    print("❌ 请提供微信文章URL")
    print("用法: python3 fetch.py <URL>")
    sys.exit(1)

if not url.startswith('https://mp.weixin.qq.com/'):
    print(f"⚠️  警告: URL看起来不是微信公众号链接")
    print(f"   预期: https://mp.weixin.qq.com/s/xxxxx")
    print(f"   实际: {url}")
    response = input("是否继续? (y/N): ")
    if response.lower() != 'y':
        sys.exit(0)

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://mp.weixin.qq.com/',
}

try:
    print(f"正在抓取: {url}")
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = 'utf-8'
    html_content = response.text
    
    # 提取标题 - 尝试多种方式
    title = None
    
    # 方式1: msg_title变量
    title_match = re.search(r'var msg_title = [\'"](.+?)[\'"];', html_content)
    if title_match:
        title = html.unescape(title_match.group(1))
    
    # 方式2: activity-name
    if not title:
        title_match = re.search(r'id="activity-name"[^>]*>\s*([^<]+)', html_content)
        if title_match:
            title = title_match.group(1).strip()
    
    # 方式3: og:title
    if not title:
        title_match = re.search(r'property="og:title" content="([^"]+)"', html_content)
        if title_match:
            title = title_match.group(1)
    
    # 方式4: 从URL提取
    if not title:
        url_hash = url.split('/')[-1][:8]
        title = f"微信文章_{url_hash}"
    
    # 生成文件名
    output_file = f'/root/.openclaw/workspace/{generate_filename(title, url)}'
    
    print(f"文章标题: {title}")
    print(f"文件名: {generate_filename(title, url)}")
    
    # 提取 js_content
    content_match = re.search(r'id="js_content"[^\u003e]*\u003e([\s\S]*?)\u003c/div\u003e\s*\u003c/div\u003e', html_content)
    original_html = content_match.group(1) if content_match else ''
    
    # 创建图片目录
    img_dir = '/root/.openclaw/workspace/images'
    os.makedirs(img_dir, exist_ok=True)
    
    # 提取并下载图片
    img_pattern = r'<img[^\u003e]+data-src=["\']([^"\']+)["\'][^\u003e]*\u003e'
    img_urls = re.findall(img_pattern, original_html)
    
    print(f"找到 {len(img_urls)} 张图片")
    
    downloaded = 0
    for img_url in img_urls:
        try:
            url_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
            ext = '.jpg'
            local_path = f'{img_dir}/{url_hash}{ext}'
            
            if not os.path.exists(local_path):
                img_headers = headers.copy()
                img_headers['Referer'] = url
                
                img_response = requests.get(img_url, headers=img_headers, timeout=30)
                
                if img_response.status_code == 200 and len(img_response.content) > 100:
                    with open(local_path, 'wb') as f:
                        f.write(img_response.content)
            
            downloaded += 1
            original_html = original_html.replace(img_url, f'images/{url_hash}{ext}')
        except:
            pass
    
    print(f"成功处理 {downloaded}/{len(img_urls)} 张图片")
    
    # 将 data-src 改为 src
    original_html = original_html.replace('data-src=', 'src=')
    
    # 处理视频 - 下载封面+链接方案
    cover_dir = '/root/.openclaw/workspace/video_covers'
    os.makedirs(cover_dir, exist_ok=True)
    
    # 提取视频信息
    video_pattern = r'<iframe[^\u003e]*class=["\'][^"\']*video_iframe[^"\']*["\'][^\u003e]*(?:data-src|src)=["\']([^"\']+)["\'][^\u003e]*(?:data-cover|cover)=["\']([^"\']+)["\'][^\u003e]*\u003e'
    videos = re.findall(video_pattern, original_html)
    
    print(f"找到 {len(videos)} 个视频")
    
    # 下载视频封面
    for i, (video_src, cover_url) in enumerate(videos):
        try:
            cover_url = unquote(cover_url)
            cover_base = generate_filename(title, url).replace('.html', '')
            local_cover = f'{cover_dir}/{cover_base}_cover_{i+1}.jpg'
            
            if not os.path.exists(local_cover):
                resp = requests.get(cover_url, headers=headers, timeout=30)
                if resp.status_code == 200 and len(resp.content) > 100:
                    with open(local_cover, 'wb') as f:
                        f.write(resp.content)
            
            print(f"✓ 视频封面 {i+1} 已下载")
        except Exception as e:
            print(f"✗ 视频封面 {i+1} 失败: {e}")
    
    # 替换视频为封面+链接
    def replace_video(match):
        video_src = match.group(1)
        cover_url = unquote(match.group(2))
        # 使用本地封面路径
        cover_base = generate_filename(title, url).replace('.html', '')
        cover_filename = f'{cover_base}_cover_{replace_video.counter}.jpg'
        replace_video.counter += 1
        
        return f'''<div class="video-wrapper" style="margin:20px 0;position:relative;">
            <a href="{url}" target="_blank" style="display:block;position:relative;">
                <img src="video_covers/{cover_filename}" style="width:100%;border-radius:8px;display:block;" onerror="this.style.display='none'">
                <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:80px;height:80px;background:rgba(0,0,0,0.7);border-radius:50%;display:flex;align-items:center;justify-content:center;">
                    <svg width="30" height="30" viewBox="0 0 24 24" fill="white">
                        <polygon points="8,5 8,19 19,12"/>
                    </svg>
                </div>
                <div style="position:absolute;bottom:10px;left:10px;color:white;font-size:14px;background:rgba(0,0,0,0.6);padding:6px 12px;border-radius:4px;">▶ 点击播放视频</div>
            </a>
        </div>'''
    
    replace_video.counter = 1
    original_html = re.sub(video_pattern, replace_video, original_html)
    
    # 处理 videosnap（视频号）
    snap_pattern = r'<mp-common-videosnap[^\u003e]*data-url=["\']([^"\']+)["\'][^\u003e]*data-headimgurl=["\']([^"\']+)["\'][^\u003e]*data-desc=["\']([^"\']+)["\'][^\u003e]*\u003e'
    def replace_snap(match):
        cover = match.group(2)
        desc = match.group(3)
        return f'''<div class="videosnap-wrapper" style="margin:20px 0;padding:16px;background:#f8f9fa;border-radius:8px;border:1px solid #e1e4e8;">
            <div style="display:flex;align-items:center;gap:12px;">
                <img src="{cover}" style="width:60px;height:60px;border-radius:50%;object-fit:cover;" onerror="this.style.display='none'">
                <div style="flex:1;">
                    <p style="margin:0;font-weight:600;color:#333;">{html.escape(desc[:50])}</p>
                    <p style="margin:4px 0 0 0;font-size:12px;color:#666;">💡 视频号内容需在原文中查看</p>
                </div>
            </div>
        </div>'''
    original_html = re.sub(snap_pattern, replace_snap, original_html)
    
    # 构建完整HTML
    full_html = f"""\u003c!DOCTYPE html>
\u003chtml lang="zh-CN">
\u003chead>
    \u003cmeta charset="UTF-8"\u003e
    \u003cmeta name="viewport" content="width=device-width, initial-scale=1.0"\u003e
    \u003ctitle\u003e{html.escape(title)}\u003c/title\u003e
    \u003cstyle\u003e
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
        }}
        
        /* 视频封面样式 */
        .video-wrapper {{
            margin: 20px 0;
            position: relative;
        }}
        .video-wrapper a {{
            display: block;
            position: relative;
            text-decoration: none;
        }}
        .video-wrapper img {{
            width: 100%;
            border-radius: 8px;
            display: block;
            margin: 0;
        }}
        
        /* 代码块样式 */
        .code-snippet__fix {{
            background: #f6f8fa;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            margin: 16px 0;
            overflow: hidden;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 14px;
            line-height: 1.6;
        }}
        .code-snippet__js {{
            display: flex;
            background: #f6f8fa;
        }}
        .code-snippet__line-index {{
            list-style: none;
            margin: 0;
            padding: 16px 12px;
            background: #f0f1f2;
            border-right: 1px solid #e1e4e8;
            color: #6e7781;
            text-align: right;
            user-select: none;
            min-width: 40px;
        }}
        .code-snippet__line-index li {{
            padding: 2px 0;
            font-size: 12px;
            line-height: 1.6;
        }}
        .code-snippet__js pre {{
            margin: 0;
            padding: 16px;
            overflow-x: auto;
            flex: 1;
            background: transparent;
        }}
        .code-snippet__js code {{
            font-family: inherit;
            font-size: 14px;
            line-height: 1.6;
            color: #24292f;
            background: transparent;
            padding: 0;
        }}
        .code-snippet__selector-tag {{ color: #22863a; font-weight: 600; }}
        .code-snippet__attribute {{ color: #6f42c1; }}
        .code-snippet__built_in {{ color: #005cc5; }}
        
        code {{
            background: rgba(175, 184, 193, 0.2);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 85%;
            color: #24292f;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 14px;
        }}
        th, td {{
            border: 1px solid #d0d7de;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background: #f6f8fa;
            font-weight: 600;
            color: #24292f;
        }}
        tr:nth-child(even) {{ background: #f9fafb; }}
        tr:hover {{ background: #f3f4f6; }}
        
        blockquote {{
            border-left: 4px solid #42b883;
            background: #f0fdf4;
            padding: 16px 20px;
            margin: 16px 0;
            border-radius: 0 8px 8px 0;
        }}
        blockquote p {{ margin: 0; color: #2c3e50; }}
        
        ol, ul {{ margin: 16px 0; padding-left: 24px; }}
        li {{ margin: 8px 0; }}
        
        a {{ color: #0969da; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    \u003c/style\u003e
\u003c/head\u003e
\u003cbody\u003e
    \u003cdiv class="container">
        \u003ch1 style="font-size: 24px; margin-bottom: 20px;"\u003e{html.escape(title)}\u003c/h1\u003e
        \u003cdiv class="rich_media_content"\u003e
            {original_html}
        \u003c/div\u003e
    \u003c/div\u003e
\u003c/body\u003e
\u003c/html>"""
    
    # 保存
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"\n✅ 文章已保存: {output_file}")
    print(f"文件大小: {len(full_html)} 字符")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    print(traceback.format_exc())
