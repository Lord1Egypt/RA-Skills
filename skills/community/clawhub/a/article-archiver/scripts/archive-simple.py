#!/usr/bin/env python3
"""
长文章归档到飞书 - 简化版
使用已验证的方法：直接调用 feishu_doc 工具
"""
import json
import os
import subprocess
import sys
import time

# 飞书配置
FEISHU_CONFIG = {
    'space_id': '7527734827164909572',
    'parent_node_token': 'NqZvwBqMTiTEtkkMsRoc76rznce'
}

def create_wiki_node(space_id, parent_token, title):
    """创建飞书 wiki 节点"""
    # 转义标题中的特殊字符
    title_escaped = title.replace('"', '\\"')
    
    # 分两步：先获取 token，再创建节点
    # 步骤 1: 获取 access token
    token_cmd = '''curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \\
  -H "Content-Type: application/json" \\
  -d '{"app_id":"cli_a90ecd03bc399bcb","app_secret":"gdEsio0WzDtHEhHFeLS55wBseDpExVtg"}' | jq -r '.tenant_access_token'
'''
    
    result = subprocess.run(token_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to get token: {result.stderr}")
    
    token = result.stdout.strip()
    
    # 步骤 2: 创建节点
    create_cmd = f'''curl -s -X POST "https://open.feishu.cn/open-apis/wiki/v2/spaces/{space_id}/nodes" \\
  -H "Authorization: Bearer {token}" \\
  -H "Content-Type: application/json" \\
  -d '{{"obj_type":"docx","parent_node_token":"{parent_token}","node_type":"origin","title":"{title_escaped}"}}'
'''
    
    result = subprocess.run(create_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to create node: {result.stderr}")
    
    data = json.loads(result.stdout)
    if data.get('code') != 0:
        raise Exception(f"API error: {data.get('msg')}")
    
    return data['data']['node']['obj_token'], data['data']['node']['node_token']

def parse_content_segments(content):
    """解析文章内容，识别文本段和图片位置"""
    lines = content.split('\n')
    segments = []
    current_text = []
    image_index = 1
    
    for line in lines:
        # 检测图片标记
        if '![图像]' in line or '](/mkdir700/article/' in line or '](/lumoswhy/article/' in line or '](/fkysly/article/' in line:
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
    if len(sys.argv) < 3:
        print("Usage: python3 archive-simple.py <article_json_file> <image_dir> [url]")
        sys.exit(1)
    
    article_file = sys.argv[1]
    image_dir = sys.argv[2]
    url = sys.argv[3] if len(sys.argv) > 3 else 'N/A'
    
    # 读取文章数据
    print(f"📖 Reading article from {article_file}...")
    with open(article_file, 'r', encoding='utf-8') as f:
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
    
    # 创建文档
    print(f"\n📝 Creating document: {title}")
    doc_token, node_token = create_wiki_node(
        FEISHU_CONFIG['space_id'],
        FEISHU_CONFIG['parent_node_token'],
        title
    )
    print(f"Document created: {doc_token}")
    print(f"URL: https://qingzhao.feishu.cn/wiki/{node_token}")
    
    # 保存文档信息供后续使用
    doc_info = {
        'doc_token': doc_token,
        'node_token': node_token,
        'url': f'https://qingzhao.feishu.cn/wiki/{node_token}',
        'title': title,
        'segments': len(segments),
        'images': len(image_segments)
    }
    
    with open('/tmp/current_doc.json', 'w') as f:
        json.dump(doc_info, f, indent=2)
    
    print(f"\n✅ Document created! Now use feishu_doc tool to write content.")
    print(f"📎 Document info saved to /tmp/current_doc.json")
    print(f"\nNext steps:")
    print(f"1. Use feishu_doc write to add metadata")
    print(f"2. Use feishu_doc append to add content segments")
    print(f"3. Use feishu_doc upload_image to add images")
    print(f"\nTotal segments to process: {len(segments)}")

if __name__ == '__main__':
    main()
