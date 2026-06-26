#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日新闻简报 - 新闻抓取脚本 v2
功能：直接抓取新闻网站 + web_search 补充
"""

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

def fetch_headlines():
    """直接获取当日新闻标题（模拟）"""
    # 实际应该用 requests + BeautifulSoup 抓取
    # 这里先用 web_search 替代
    try:
        searxng_dir = Path.home() / ".openclaw/workspace/skills/searxng"
        today = datetime.now().strftime('%Y 年 %m 月 %d 日')
        
        # 搜索当日新闻
        cmd = [
            "uv", "run", "scripts/searxng.py",
            "search", f"{today} 最新消息 热点新闻",
            "-n", "15",
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
            return parse_headlines(result.stdout)
        return []
        
    except Exception as e:
        print(f"搜索错误：{e}", file=sys.stderr)
        return []

def parse_headlines(output):
    """解析新闻标题"""
    news_list = []
    lines = output.strip().split("\n")
    
    current_title = ""
    current_url = ""
    current_source = ""
    
    for line in lines:
        line = line.strip()
        
        # 提取标题
        if line and line[0].isdigit() and ". " in line:
            if current_title and current_url:
                news_list.append({
                    "title": current_title,
                    "url": current_url,
                    "source": current_source
                })
            
            parts = line.split(". ", 1)
            if len(parts) > 1:
                current_title = parts[1]
                current_url = ""
                current_source = ""
        
        # 提取 URL 和来源
        elif line.startswith("http"):
            current_url = line.split()[0]
            # 从 URL 提取来源
            if "cctv" in current_url:
                current_source = "央视网"
            elif "qq.com" in current_url:
                current_source = "腾讯新闻"
            elif "163.com" in current_url:
                current_source = "网易新闻"
            elif "sina" in current_url:
                current_source = "新浪"
            elif "zhihu" in current_url:
                current_source = "知乎"
            elif "baidu" in current_url:
                current_source = "百度"
            else:
                current_source = "网络"
    
    # 添加最后一条
    if current_title and current_url:
        news_list.append({
            "title": current_title,
            "url": current_url,
            "source": current_source
        })
    
    return news_list[:15]

def categorize_news(news_list):
    """简单分类新闻"""
    categories = {
        "财经": [],
        "科技": [],
        "国际": [],
        "其他": []
    }
    
    finance_keywords = ["油价", "黄金", "股市", "财经", "经济", "央行", "通胀", "美元", "人民币"]
    tech_keywords = ["AI", "科技", "数码", "手机", "电脑", "芯片", "软件", "互联网", "游戏"]
    intl_keywords = ["国际", "外交", "总统", "大选", "战争", "冲突", "欧盟", "联合国"]
    
    for news in news_list:
        title = news["title"].lower()
        
        if any(k.lower() in title for k in finance_keywords):
            categories["财经"].append(news)
        elif any(k.lower() in title for k in tech_keywords):
            categories["科技"].append(news)
        elif any(k.lower() in title for k in intl_keywords):
            categories["国际"].append(news)
        else:
            categories["其他"].append(news)
    
    return categories

def generate_brief(categorized_news):
    """生成简报"""
    brief = []
    brief.append(f"📰 每日新闻简报 - {datetime.now().strftime('%Y 年 %m 月 %d 日')}")
    brief.append("")
    
    for category in ["财经", "科技", "国际"]:
        news_list = categorized_news.get(category, [])
        if news_list:
            brief.append(f"【{category}】")
            for i, news in enumerate(news_list[:3], 1):  # 每类最多 3 条
                title = news["title"]
                source = news.get("source", "")
                brief.append(f"{i}. {title} [{source}]")
            brief.append("")
    
    # 如果没有足够新闻，显示其他
    other_news = categorized_news.get("其他", [])
    if other_news and len(brief) < 10:
        brief.append("【其他热点】")
        for i, news in enumerate(other_news[:3], 1):
            brief.append(f"{i}. {news['title']}")
        brief.append("")
    
    brief.append("---")
    brief.append("💡 简报由 AI 生成，全文阅读请访问来源链接")
    
    return "\n".join(brief)

def main():
    """主函数"""
    print("🚀 开始抓取新闻...")
    
    # 抓取新闻
    all_news = fetch_headlines()
    print(f"抓取到 {len(all_news)} 条新闻")
    
    # 分类
    categorized = categorize_news(all_news)
    
    # 生成简报
    brief = generate_brief(categorized)
    
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
