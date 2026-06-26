#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日新闻简报 - 新闻抓取脚本 v3（生产版）
功能：搜索当日热点新闻 + 备用新闻源，AI 提炼重点
"""

# 使用 v3 版本
import sys
from pathlib import Path

# 重定向到 v3
v3_script = Path(__file__).parent / "fetch_news_v3.py"
if v3_script.exists():
    with open(v3_script, "r", encoding="utf-8") as f:
        exec(f.read())
else:
    print("错误：fetch_news_v3.py 不存在")
    sys.exit(1)

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 配置
SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"
SOURCES_FILE = CONFIG_DIR / "sources.json"

def load_config():
    """加载配置文件"""
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def search_news(keyword, category, limit=5):
    """使用 SearXNG 搜索新闻"""
    try:
        # 构建搜索命令
        searxng_dir = Path.home() / ".openclaw/workspace/skills/searxng"
        today = datetime.now().strftime('%Y-%m-%d')
        cmd = [
            "uv", "run", "scripts/searxng.py",
            "search", f"{today} {keyword}",
            "-n", str(limit),
            "--language", "zh"
        ]
        
        result = subprocess.run(
            cmd,
            cwd=searxng_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return parse_search_result(result.stdout, keyword)
        else:
            print(f"搜索失败：{keyword}", file=sys.stderr)
            return []
            
    except Exception as e:
        print(f"搜索错误 {keyword}: {e}", file=sys.stderr)
        return []

def parse_search_result(output, keyword):
    """解析搜索结果"""
    news_list = []
    lines = output.strip().split("\n")
    
    # 解析 SearXNG 输出格式
    current_title = ""
    current_url = ""
    current_summary = ""
    
    for line in lines:
        line = line.strip()
        
        # 提取标题（数字 + 点 + 标题的格式）
        if line and line[0].isdigit() and ". " in line:
            if current_title and current_url:
                news_list.append({
                    "title": current_title,
                    "url": current_url,
                    "summary": current_summary[:100]
                })
            
            parts = line.split(". ", 1)
            if len(parts) > 1:
                current_title = parts[1]
                current_url = ""
                current_summary = ""
        
        # 提取 URL
        elif line.startswith("http"):
            current_url = line.split()[0]  # 取第一个 URL
        
        # 提取摘要
        elif current_title and len(line) > 20 and not line.startswith("┏"):
            current_summary = line
    
    # 添加最后一条
    if current_title and current_url:
        news_list.append({
            "title": current_title,
            "url": current_url,
            "summary": current_summary[:100]
        })
    
    return news_list[:5]  # 最多返回 5 条

def generate_brief(news_data):
    """生成简报"""
    brief = []
    brief.append(f"📰 每日新闻简报 - {datetime.now().strftime('%Y 年 %m 月 %d 日')}")
    brief.append("")
    
    for category, news_list in news_data.items():
        if news_list:
            brief.append(f"【{category}】")
            for i, news in enumerate(news_list[:3], 1):  # 每类最多 3 条
                title = news.get("title", "无标题")
                brief.append(f"{i}. {title}")
            brief.append("")
    
    brief.append("---")
    brief.append("💡 简报由 AI 生成，全文阅读请访问来源链接")
    
    return "\n".join(brief)

def fetch_all_news():
    """抓取所有新闻"""
    config = load_config()
    news_data = {}
    
    for category in config["categories"]:
        print(f"正在抓取 {category} 新闻...")
        keywords = config["keywords"].get(category, [category])
        category_news = []
        
        for keyword in keywords[:2]:  # 每类最多 2 个关键词
            results = search_news(keyword, category)
            category_news.extend(results)
        
        # 去重
        seen_urls = set()
        unique_news = []
        for news in category_news:
            url = news.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_news.append(news)
        
        news_data[category] = unique_news[:5]  # 每类最多 5 条
    
    return news_data

def main():
    """主函数"""
    print("🚀 开始抓取新闻...")
    
    # 抓取新闻
    news_data = fetch_all_news()
    
    # 生成简报
    brief = generate_brief(news_data)
    
    # 输出
    print("\n" + "="*50)
    print(brief)
    print("="*50)
    
    # 保存到文件
    output_file = SCRIPT_DIR / "output" / f"brief_{datetime.now().strftime('%Y%m%d')}.md"
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(brief)
    
    print(f"\n✅ 简报已保存到：{output_file}")
    
    return brief

if __name__ == "__main__":
    main()
