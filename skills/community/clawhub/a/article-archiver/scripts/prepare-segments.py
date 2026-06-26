#!/usr/bin/env python3
"""
批量处理文章段落 - 写入内容和上传图片
"""
import json
import os
import sys
import time

def load_segments(article_file):
    """加载并解析文章段落"""
    with open(article_file, 'r', encoding='utf-8') as f:
        article = json.load(f)
    
    content = article.get('content', '')
    lines = content.split('\n')
    segments = []
    current_text = []
    image_index = 1
    
    for line in lines:
        if '![图像]' in line or '](/mkdir700/article/' in line or '](/lumoswhy/article/' in line or '](/fkysly/article/' in line:
            if current_text:
                text = '\n'.join(current_text).strip()
                if text:
                    segments.append({'type': 'text', 'content': text})
                current_text = []
            segments.append({'type': 'image', 'index': image_index})
            image_index += 1
        else:
            current_text.append(line)
    
    if current_text:
        text = '\n'.join(current_text).strip()
        if text:
            segments.append({'type': 'text', 'content': text})
    
    return segments

def save_segment_files(segments, output_dir):
    """保存段落到独立文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    manifest = []
    for i, segment in enumerate(segments):
        if segment['type'] == 'text':
            filename = f"segment_{i:03d}_text.md"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(segment['content'])
            manifest.append({'index': i, 'type': 'text', 'file': filepath})
        else:
            manifest.append({'index': i, 'type': 'image', 'image_index': segment['index']})
    
    # 保存清单
    with open(os.path.join(output_dir, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=2)
    
    return manifest

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 prepare-segments.py <article_json> <output_dir>")
        sys.exit(1)
    
    article_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    print(f"📖 Loading article from {article_file}...")
    segments = load_segments(article_file)
    
    print(f"🔍 Found {len(segments)} segments")
    text_count = len([s for s in segments if s['type'] == 'text'])
    image_count = len([s for s in segments if s['type'] == 'image'])
    print(f"   - {text_count} text segments")
    print(f"   - {image_count} image segments")
    
    print(f"\n💾 Saving segments to {output_dir}...")
    manifest = save_segment_files(segments, output_dir)
    
    print(f"✅ Saved {len(manifest)} segments")
    print(f"📋 Manifest: {output_dir}/manifest.json")
