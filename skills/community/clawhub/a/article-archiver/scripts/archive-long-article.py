#!/usr/bin/env python3
"""
长文章归档到飞书 - 完整版
处理长文章（600+ 行）和多图片（20+ 张）
"""
import json
import os
import re
import subprocess
import sys
import time

# 飞书配置
FEISHU_CONFIG = {
    'space_id': '7527734827164909572',
    'parent_node_token': 'NqZvwBqMTiTEtkkMsRoc76rznce',
    'app_id': 'cli_a90ecd03bc399bcb',
    'app_secret': 'gdEsio0WzDtHEhHFeLS55wBseDpExVtg'
}

def run_cmd(cmd):
    """执行命令并返回输出"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def get_access_token():
    """获取飞书 access token"""
    cmd = f'''curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \\
      -H "Content-Type: application/json" \\
      -d '{{"app_id":"{FEISHU_CONFIG['app_id']}","app_secret":"{FEISHU_CONFIG['app_secret']}"}}'
    '''
    code, stdout, stderr = run_cmd(cmd)
    if code != 0:
        raise Exception(f"Failed to get token: {stderr}")
    
    data = json.loads(stdout)
    if data.get('code') != 0:
        raise Exception(f"API error: {data.get('msg')}")
    
    return data['tenant_access_token']

def create_document(token, title):
    """创建飞书文档"""
    cmd = f'''curl -s -X POST "https://open.feishu.cn/open-apis/wiki/v2/spaces/{FEISHU_CONFIG['space_id']}/nodes" \\
      -H "Authorization: Bearer {token}" \\
      -H "Content-Type: application/json" \\
      -d '{{"obj_type":"docx","parent_node_token":"{FEISHU_CONFIG['parent_node_token']}","node_type":"origin","title":"{title}"}}'
    '''
    code, stdout, stderr = run_cmd(cmd)
    if code != 0:
        raise Exception(f"Failed to create document: {stderr}")
    
    data = json.loads(stdout)
    if data.get('code') != 0:
        raise Exception(f"API error: {data.get('msg')}")
    
    return data['data']['node']['obj_token'], data['data']['node']['node_token']

def write_content(doc_token, content):
    """写入内容到飞书文档"""
    # 转义特殊字符
    content_escaped = content.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('$', '\\$')
    cmd = f'openclaw feishu-doc write --doc-token "{doc_token}" --content "{content_escaped}"'
    code, stdout, stderr = run_cmd(cmd)
    return code == 0

def append_content(doc_token, content):
    """追加内容到飞书文档"""
    # 转义特殊字符
    content_escaped = content.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('$', '\\$')
    cmd = f'openclaw feishu-doc append --doc-token "{doc_token}" --content "{content_escaped}"'
    code, stdout, stderr = run_cmd(cmd)
    return code == 0

def upload_image(doc_token, image_path):
    """上传图片到飞书文档"""
    cmd = f'openclaw feishu-doc upload-image --doc-token "{doc_token}" --file-path "{image_path}"'
    code, stdout, stderr = run_cmd(cmd)
    return code == 0

def parse_content_segments(content):
    """解析文章内容，识别文本段和图片位置"""
    lines = content.split('\n')
    segments = []
    current_text = []
    image_index = 1
    
    for line in lines:
        # 检测图片标记
        if '![图像]' in line or '](/mkdir700/article/' in line or '](/lumoswhy/article/' in line:
            # 保存当前文本段
            if current_text:
                text = '\n'.join(current_text).strip()
                if text:
                    segments.append({'type': 'text', 'content': text})
                current_text = []
            
            # 添加图片段
            segments.append({'type': 'image', 'index': image_index})
            image_index += 1
        else:
            current_text.append(line)
    
    # 保存最后一段文本
    if current_text:
        text = '\n'.join(current_text).strip()
        if text:
            segments.append({'type': 'text', 'content': text})
    
    return segments

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 archive-long-article.py <article_json_file> <image_dir>")
        sys.exit(1)
    
    article_file = sys.argv[1]
    image_dir = sys.argv[2] if len(sys.argv) > 2 else '/tmp/mkdir_images'
    
    # 读取文章数据
    print(f"📖 Reading article from {article_file}...")
    with open(article_file, 'r') as f:
        article = json.load(f)
    
    title = article.get('title', 'Untitled')
    author = article.get('author', '') or article.get('username', '') or 'Unknown'
    content = article.get('content', '')
    
    print(f"Title: {title}")
    print(f"Author: {author}")
    print(f"Content: {len(content)} chars, {len(content.split(chr(10)))} lines")
    
    # 解析内容段落
    print("\n🔍 Parsing content structure...")
    segments = parse_content_segments(content)
    text_segments = [s for s in segments if s['type'] == 'text']
    image_segments = [s for s in segments if s['type'] == 'image']
    
    print(f"Parsed: {len(segments)} segments ({len(text_segments)} text, {len(image_segments)} images)")
    
    # 获取 access token
    print("\n🔑 Getting access token...")
    token = get_access_token()
    
    # 创建文档
    print(f"\n📝 Creating document: {title}")
    doc_token, node_token = create_document(token, title)
    print(f"Document created: {doc_token}")
    print(f"URL: https://qingzhao.feishu.cn/wiki/{node_token}")
    
    # 写入元数据
    print("\n✍️  Writing metadata...")
    metadata = f'''> **原始链接**：{sys.argv[3] if len(sys.argv) > 3 else 'N/A'}
> 
> **归档时间**：{time.strftime('%Y-%m-%d %H:%M:%S')}
> 
> **来源**：x.com (Twitter Article)
> 
> **作者**：{author}

---

'''
    
    if not write_content(doc_token, metadata):
        print("❌ Failed to write metadata")
        sys.exit(1)
    
    # 逐段写入内容和图片
    print(f"\n📄 Writing {len(segments)} segments...")
    for i, segment in enumerate(segments):
        if segment['type'] == 'text':
            print(f"[{i+1}/{len(segments)}] Writing text ({len(segment['content'])} chars)...")
            if not append_content(doc_token, segment['content']):
                print(f"⚠️  Failed to append text segment {i+1}")
        
        elif segment['type'] == 'image':
            image_path = os.path.join(image_dir, f"img{segment['index']}.jpg")
            if os.path.exists(image_path):
                print(f"[{i+1}/{len(segments)}] Uploading image {segment['index']}...")
                if not upload_image(doc_token, image_path):
                    print(f"⚠️  Failed to upload image {segment['index']}")
            else:
                print(f"[{i+1}/{len(segments)}] ⚠️  Image not found: {image_path}")
        
        # 短暂延迟，避免 API 限流
        time.sleep(0.2)
    
    print(f"\n✅ Article archived successfully!")
    print(f"📎 Document URL: https://qingzhao.feishu.cn/wiki/{node_token}")

if __name__ == '__main__':
    main()
