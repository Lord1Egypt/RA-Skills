#!/usr/bin/env python3
"""
生成简洁的下载页面（参考其他龙虾机器人的方案）
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            max-width: 700px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #333; margin-bottom: 5px; font-size: 24px; }}
        .file-info {{
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #007AFF;
        }}
        .file-info p {{ margin: 8px 0; color: #444; font-size: 15px; }}
        .file-info strong {{ color: #333; }}
        .download-btn {{
            display: inline-block;
            background: #007AFF;
            color: white;
            padding: 15px 40px;
            text-decoration: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            margin: 15px 0;
            border: none;
            cursor: pointer;
        }}
        .download-btn:hover {{
            background: #0056CC;
        }}
        .status {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 20px;
            padding: 10px 15px;
            background: #E8F8E8;
            border-radius: 6px;
            color: #2E7D32;
            font-weight: 500;
        }}
        .status-dot {{
            width: 10px;
            height: 10px;
            background: #4CAF50;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        .file-list {{
            margin-top: 25px;
        }}
        .file-item {{
            background: #fafafa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
            border-left: 3px solid #007AFF;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .file-item a {{
            color: #007AFF;
            text-decoration: none;
            font-weight: 500;
        }}
        .file-item a:hover {{ text-decoration: underline; }}
        .file-size {{ color: #888; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📄 {title}</h1>
        {description_html}
        
        {content}
        
        <div class="status">
            <span class="status-dot"></span>
            服务状态：运行中
        </div>
    </div>
</body>
</html>
"""

def get_file_size(file_path):
    """获取文件大小，返回可读格式"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def get_upload_time(file_path):
    """获取文件修改时间"""
    mtime = os.path.getmtime(file_path)
    dt = datetime.fromtimestamp(mtime)
    return dt.strftime("%Y年%m月%d日")

def main():
    parser = argparse.ArgumentParser(description="生成简洁的下载页面")
    parser.add_argument("path", help="文件或目录路径")
    parser.add_argument("--title", default="文件下载", help="页面标题")
    parser.add_argument("--description", default="", help="页面描述")
    parser.add_argument("--output", help="输出 HTML 文件路径")
    
    args = parser.parse_args()
    
    # 确定输出路径
    if args.output:
        output_path = args.output
    elif os.path.isdir(args.path):
        output_path = os.path.join(args.path, "index.html")
    else:
        output_path = os.path.join(os.path.dirname(args.path), "index.html")
    
    # 生成内容
    if os.path.isfile(args.path):
        # 单个文件
        filename = os.path.basename(args.path)
        file_size = get_file_size(args.path)
        upload_time = get_upload_time(args.path)
        
        description_html = f'<p style="color: #666; margin-top: 0;">{args.description}</p>' if args.description else ''
        
        content = f'''
        <div class="file-info">
            <p><strong>文件名：</strong>{filename}</p>
            <p><strong>大小：</strong>{file_size}</p>
            <p><strong>上传时间：</strong>{upload_time}</p>
        </div>
        <a href="{filename}" class="download-btn" download>⬇️ 点击下载文件</a>
        '''
        
    elif os.path.isdir(args.path):
        # 目录
        description_html = f'<p style="color: #666; margin-top: 0;">{args.description}</p>' if args.description else ''
        
        # 列出目录中的文件
        file_items = []
        for item in sorted(os.listdir(args.path)):
            item_path = os.path.join(args.path, item)
            if os.path.isfile(item_path) and not item.startswith('.') and item != 'index.html':
                size = get_file_size(item_path)
                file_items.append(f'''
                <div class="file-item">
                    <a href="{item}" download>{item}</a>
                    <span class="file-size">({size})</span>
                </div>
                ''')
        
        if file_items:
            content = f'''
            <div class="file-list">
                <h3 style="color: #333; margin-bottom: 15px;">📁 文件列表：</h3>
                {"".join(file_items)}
            </div>
            '''
        else:
            content = '<p style="color: #888;">目录中没有可下载的文件</p>'
    
    else:
        print(f"❌ 错误：路径不存在: {args.path}")
        sys.exit(1)
    
    # 生成 HTML
    html = HTML_TEMPLATE.format(
        title=args.title,
        description_html=description_html,
        content=content
    )
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 下载页面已生成: {output_path}")
    print(f"📄 标题: {args.title}")
    if args.description:
        print(f"📝 描述: {args.description}")

if __name__ == "__main__":
    main()
