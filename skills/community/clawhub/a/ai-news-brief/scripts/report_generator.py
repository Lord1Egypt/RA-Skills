#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成模块
功能：生成 HTML/Markdown 格式的资讯报告
"""

import sys
import io
import os
import json
from datetime import datetime, timedelta

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "user_config")
CONFIG_FILE = os.path.join(USER_CONFIG_DIR, "report_config.json")
DEFAULT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "report_config.json.default")
DATA_DIR = os.path.join(SCRIPT_DIR, "data")


def load_report_config():
    """加载报告配置（优先用户配置）"""
    # 优先读取用户配置目录
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] 读取用户配置失败: {e}")
    
    # 读取默认配置
    if os.path.exists(DEFAULT_CONFIG_FILE):
        try:
            with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                print("[INFO] 使用默认报告配置，请复制到 user_config 目录进行自定义")
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] 无法加载默认配置: {e}")
            return None
    
    return {"config": {"enabled": False}}


def generate_html_report(articles, date_range):
    """生成HTML报告"""
    config = load_report_config()
    settings = config.get('config', {}).get('report_settings', {})
    
    title_prefix = settings.get('title_prefix', 'AI资讯简报')
    max_articles = settings.get('max_articles', 20)
    include_summary = settings.get('include_summary', True)
    include_key_points = settings.get('include_key_points', True)
    include_credibility = settings.get('include_credibility', True)
    
    articles = articles[:max_articles]
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title_prefix}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        h1 {{ color: #1a73e8; border-bottom: 3px solid #1a73e8; padding-bottom: 15px; margin-bottom: 30px; }}
        h2 {{ color: #5f6368; margin-top: 30px; border-left: 4px solid #1a73e8; padding-left: 10px; }}
        .info {{ background: #e8f5e9; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
        .article {{ background: white; border-radius: 8px; padding: 20px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .article:hover {{ box-shadow: 0 4px 8px rgba(0,0,0,0.15); }}
        .title {{ font-size: 18px; font-weight: bold; color: #1a73e8; margin-bottom: 10px; }}
        .title a {{ color: inherit; text-decoration: none; }}
        .title a:hover {{ text-decoration: underline; }}
        .meta {{ font-size: 13px; color: #666; margin-bottom: 10px; }}
        .source {{ background: #e3f2fd; padding: 2px 8px; border-radius: 4px; margin-right: 10px; }}
        .credibility {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }}
        .cred-A {{ background: #34a853; color: white; }}
        .cred-B {{ background: #fbbc04; color: #333; }}
        .cred-C {{ background: #ea4335; color: white; }}
        .cred-D {{ background: #9e9e9e; color: white; }}
        .summary {{ color: #444; margin: 10px 0; line-height: 1.7; }}
        .key-points {{ background: #e8f0fe; padding: 12px; border-radius: 6px; margin-top: 10px; }}
        .key-points-title {{ font-weight: bold; color: #1a73e8; font-size: 13px; margin-bottom: 8px; }}
        .key-points ul {{ margin: 0; padding-left: 20px; }}
        .key-points li {{ color: #333; font-size: 13px; margin: 5px 0; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 12px; }}
        .hot-tag {{ background: #ea4335; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px; margin-left: 8px; }}
    </style>
</head>
<body>
    <h1>🤖 {title_prefix}</h1>
    
    <div class="info">
        <strong>📅 日期范围</strong>: {date_range}<br>
        <strong>📊 资讯数量</strong>: {len(articles)} 条<br>
        <strong>⏰ 生成时间</strong>: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    
    <h2>🔥 热门资讯 TOP {len(articles)}</h2>
"""
    
    # 添加热点标签
    hot_keywords = ['GPU', 'Nvidia', 'AMD', '大模型', 'GPT', 'AI', '芯片', '算力']
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', '无标题')
        url = article.get('url', '#')
        source = article.get('source', '未知来源')
        summary = article.get('summary', '暂无摘要')
        key_points = article.get('key_points', [])
        credibility = article.get('credibility', {})
        hot_score = article.get('hot_score', 0)
        
        level = credibility.get('level', 'D')
        
        # 检查是否是热点
        is_hot = any(kw.lower() in title.lower() for kw in hot_keywords)
        
        html += f"""
    <div class="article">
        <div class="title">
            {f'<span class="hot-tag">🔥 {hot_score}</span>' if hot_score > 20 else ''}
            <a href="{url}" target="_blank">{i}. {title}</a>
        </div>
        <div class="meta">
            <span class="source">{source}</span>
            <span class="credibility cred-{level}">可信度 {level}</span>
        </div>
"""
        
        if include_summary and summary:
            html += f'        <div class="summary">{summary[:300]}...</div>\n'
        
        if include_key_points and key_points:
            html += f"""        <div class="key-points">
            <div class="key-points-title">📌 关键点</div>
            <ul>
"""
            for kp in key_points[:3]:
                html += f'                <li>{kp[:100]}</li>\n'
            html += """            </ul>
        </div>
"""
        
        html += """    </div>
"""
    
    html += f"""
    <div class="footer">
        <p>🤖 由 AI 资讯简报自动生成</p>
        <p>📧 此报告由系统自动生成，请勿回复</p>
    </div>
</body>
</html>
"""
    
    return html


def generate_markdown_report(articles, date_range):
    """生成Markdown报告"""
    title_prefix = "AI资讯简报"
    
    md = f"""# 🤖 {title_prefix}

> 📅 日期范围: {date_range}  
> 📊 资讯数量: {len(articles)} 条  
> ⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 🔥 热门资讯 TOP {len(articles)}

"""
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', '无标题')
        url = article.get('url', '#')
        source = article.get('source', '未知来源')
        summary = article.get('summary', '暂无摘要')
        key_points = article.get('key_points', [])
        credibility = article.get('credibility', {})
        
        level = credibility.get('level', 'D')
        
        md += f"""### {i}. {title}

- **来源**: {source} | **可信度**: {level}
- **链接**: {url}

"""
        
        if summary:
            md += f">{summary[:200]}...\n\n"
        
        if key_points:
            md += "**关键点**:\n"
            for kp in key_points[:2]:
                md += f"- {kp[:80]}\n"
            md += "\n"
        
        md += "---\n\n"
    
    return md


def save_report(articles, date_range, output_format='html'):
    """保存报告到文件"""
    config = load_report_config()
    output_dir = config.get('config', {}).get('output_dir', './reports')
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成日期前缀
    date_prefix = datetime.now().strftime("%Y%m%d")
    
    if output_format == 'html':
        content = generate_html_report(articles, date_range)
        filename = f"ai_news_{date_prefix}.html"
    else:
        content = generate_markdown_report(articles, date_range)
        filename = f"ai_news_{date_prefix}.md"
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


def test_report():
    """测试报告生成"""
    # 模拟数据
    test_articles = [
        {
            'title': 'NVIDIA发布RTX 5090显卡，性能提升50%',
            'url': 'https://example.com/1',
            'source': '36kr',
            'summary': 'NVIDIA发布了最新的RTX 5090显卡...',
            'key_points': ['性能提升50%', '价格不变'],
            'credibility': {'level': 'B'},
            'hot_score': 85
        },
        {
            'title': 'OpenAI发布GPT-5',
            'url': 'https://example.com/2',
            'source': '量子位',
            'summary': 'GPT-5在多个基准测试中超越人类...',
            'key_points': ['超越人类基准', '多模态能力增强'],
            'credibility': {'level': 'A'},
            'hot_score': 95
        }
    ]
    
    print("生成HTML报告...")
    html_path = save_report(test_articles, "2026-04-06", "html")
    print(f"✅ HTML报告: {html_path}")
    
    print("\n生成Markdown报告...")
    md_path = save_report(test_articles, "2026-04-06", "markdown")
    print(f"✅ Markdown报告: {md_path}")


if __name__ == "__main__":
    test_report()