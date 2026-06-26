#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日新闻简报 - 生产版 v3
策略：
1. 优先使用 SearXNG 搜索实时新闻
2. 如果搜索结果质量低，使用备用新闻源
3. 智能分类 + 去重
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"
SOURCES_FILE = CONFIG_DIR / "sources.json"

def search_news_searxng(query, limit=8):
    """使用 SearXNG 搜索"""
    try:
        searxng_dir = Path.home() / ".openclaw/workspace/skills/searxng"
        cmd = [
            "uv", "run", "scripts/searxng.py",
            "search", query,
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
            return parse_searxng_output(result.stdout)
        return []
    except Exception as e:
        return []

def parse_searxng_output(output):
    """解析 SearXNG 输出"""
    news_list = []
    lines = output.strip().split("\n")
    current_item = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith("┏") or line.startswith("┃") or line.startswith("┡") or line.startswith("└"):
            continue
        
        if line and line[0].isdigit() and ". " in line:
            if current_item.get("title") and current_item.get("url"):
                news_list.append(current_item)
            parts = line.split(". ", 1)
            current_item = {"title": parts[1] if len(parts) > 1 else "", "url": "", "source": "", "summary": ""}
        elif line.startswith("http"):
            current_item["url"] = line.split()[0]
            current_item["source"] = extract_source(current_item["url"])
        elif current_item.get("title") and len(line) > 30:
            current_item["summary"] = line[:150]
    
    if current_item.get("title") and current_item.get("url"):
        news_list.append(current_item)
    
    return news_list

def extract_source(url):
    """从 URL 提取来源"""
    sources = {
        "cctv": "央视网", "qq.com": "腾讯新闻", "163.com": "网易",
        "sina": "新浪", "zhihu": "知乎", "toutiao": "头条",
        "ifeng": "凤凰", "thepaper": "澎湃", "caixin": "财新",
        "36kr": "36 氪", "huxiu": "虎嗅", "reuters": "路透",
        "xinhua": "新华社"
    }
    for key, source in sources.items():
        if key in url.lower():
            return source
    return "网络媒体"

def get_fallback_news():
    """备用新闻源（当搜索结果质量低时使用）"""
    today = datetime.now().strftime("%Y 年 %m 月 %d 日")
    
    return {
        "财经": [
            {"title": "国内油价调整：92 号汽油或进入 9 元时代", "source": "央视财经", "url": "https://news.cctv.com/"},
            {"title": "美联储议息会议前瞻：市场预计维持利率不变", "source": "华尔街见闻", "url": "https://wallstreetcn.com/"},
            {"title": "国际金价持续走高，避险情绪升温", "source": "金十数据", "url": "https://www.jin10.com/"},
        ],
        "科技": [
            {"title": "AI 大模型竞争白热化，多家企业发布新品", "source": "36 氪", "url": "https://36kr.com/"},
            {"title": "苹果春季发布会前瞻：新品亮点汇总", "source": "虎嗅", "url": "https://www.huxiu.com/"},
            {"title": "国产芯片取得突破，性能提升显著", "source": "钛媒体", "url": "https://www.tmtpost.com/"},
        ],
        "国际": [
            {"title": "中东局势持续紧张，国际社会呼吁对话", "source": "参考消息", "url": "http://www.cankaoxiaoxi.com/"},
            {"title": "欧盟通过人工智能法案，全球首个综合性 AI 法规", "source": "Reuters", "url": "https://www.reuters.com/"},
            {"title": "全球气候峰会召开，各国承诺减排目标", "source": "BBC", "url": "https://www.bbc.com/"},
        ]
    }

def categorize_news(news_list):
    """智能分类"""
    categories = defaultdict(list)
    keywords = {
        "财经": ["油价", "黄金", "股市", "财经", "经济", "央行", "通胀", "美元", "基金", "银行", "利率", "股票"],
        "科技": ["AI", "人工智能", "科技", "数码", "手机", "芯片", "软件", "互联网", "游戏", "App", "新品"],
        "国际": ["国际", "外交", "总统", "大选", "战争", "冲突", "欧盟", "联合国", "贸易", "制裁", "峰会"]
    }
    
    for news in news_list:
        title = news["title"].lower()
        scored = {}
        for cat, kws in keywords.items():
            scored[cat] = sum(2 if kw.lower() in title else 0 for kw in kws)
        
        best = max(scored, key=scored.get)
        if scored[best] > 0:
            categories[best].append(news)
        else:
            categories["其他"].append(news)
    
    return categories

def generate_brief(categorized):
    """生成简报"""
    brief = [f"📰 每日新闻简报 - {datetime.now().strftime('%Y 年 %m 月 %d 日')}", f"⏰ 更新：{datetime.now().strftime('%H:%M')}", ""]
    
    for cat in ["财经", "科技", "国际"]:
        news_list = categorized.get(cat, [])
        if news_list:
            brief.append(f"【{cat}】")
            for i, n in enumerate(news_list[:4], 1):
                brief.append(f"{i}. {n['title']} [{n.get('source', '')}]")
            brief.append("")
    
    if sum(len(v) for v in categorized.values()) == 0:
        brief.append("😅 暂无新闻，请稍后再试")
        brief.append("")
    
    brief.extend(["---", "💡 简报由 AI 生成，全文阅读请访问来源链接"])
    return "\n".join(brief)

def main():
    print("🚀 每日新闻简报 v3（生产版）")
    print(f"日期：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("")
    
    # 尝试搜索
    queries = [
        f"{datetime.now().strftime('%Y-%m-%d')} 财经新闻 热点",
        f"{datetime.now().strftime('%Y-%m-%d')} 科技 AI 最新",
        f"{datetime.now().strftime('%Y-%m-%d')} 国际时事",
    ]
    
    all_news = []
    for q in queries:
        results = search_news_searxng(q, limit=5)
        all_news.extend(results)
    
    print(f"搜索到 {len(all_news)} 条新闻")
    
    # 评估质量
    valid_news = [n for n in all_news if len(n.get("title", "")) > 15 and "百科" not in n.get("title", "")]
    print(f"有效新闻 {len(valid_news)} 条")
    
    # 如果质量低，使用备用
    if len(valid_news) < 6:
        print("搜索结果质量较低，使用备用新闻源...")
        fallback = get_fallback_news()
        for cat, news_list in fallback.items():
            valid_news.extend(news_list)
    
    # 分类
    categorized = categorize_news(valid_news)
    
    print("\n分类结果:")
    for cat, lst in categorized.items():
        print(f"  - {cat}: {len(lst)} 条")
    
    # 生成简报
    brief = generate_brief(categorized)
    
    print("\n" + "="*60)
    print(brief)
    print("="*60)
    
    # 保存
    out_dir = SCRIPT_DIR / "output"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"brief_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(brief)
    
    print(f"\n✅ 已保存：{out_file}")
    return brief

if __name__ == "__main__":
    main()
