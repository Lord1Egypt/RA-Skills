#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日新闻简报 - 搜索优化版 v2
改进：
1. 使用日期范围的搜索词
2. 多关键词交叉验证
3. 结果去重和排序
4. 智能分类
"""

import json
import subprocess
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# 配置
SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"
SOURCES_FILE = CONFIG_DIR / "sources.json"

def load_config():
    """加载配置文件"""
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def search_news_searxng(query, limit=10):
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
        print(f"搜索错误：{e}", file=sys.stderr)
        return []

def parse_searxng_output(output):
    """解析 SearXNG 输出"""
    news_list = []
    lines = output.strip().split("\n")
    
    current_item = {}
    
    for line in lines:
        line = line.strip()
        
        # 跳过表格线
        if line.startswith("┏") or line.startswith("┃") or line.startswith("┡") or line.startswith("└"):
            continue
        
        # 新条目开始（数字 + 点）
        if line and line[0].isdigit() and ". " in line:
            # 保存前一个条目
            if current_item.get("title") and current_item.get("url"):
                news_list.append(current_item)
            
            # 开始新条目
            parts = line.split(". ", 1)
            current_item = {
                "title": parts[1] if len(parts) > 1 else "",
                "url": "",
                "source": "",
                "summary": ""
            }
        
        # URL 行
        elif line.startswith("http"):
            url = line.split()[0]
            current_item["url"] = url
            current_item["source"] = extract_source_from_url(url)
        
        # 摘要行
        elif current_item.get("title") and len(line) > 30:
            current_item["summary"] = line[:150]
    
    # 添加最后一个条目
    if current_item.get("title") and current_item.get("url"):
        news_list.append(current_item)
    
    return news_list

def extract_source_from_url(url):
    """从 URL 提取来源"""
    url_lower = url.lower()
    
    source_map = {
        "cctv": "央视网",
        "qq.com": "腾讯新闻",
        "163.com": "网易新闻",
        "sina.com": "新浪新闻",
        "zhihu": "知乎",
        "baidu": "百度",
        "toutiao": "今日头条",
        "ifeng": "凤凰网",
        "thepaper": "澎湃新闻",
        "caixin": "财新",
        "36kr": "36 氪",
        "huxiu": "虎嗅",
        "reuters": "路透社",
        "bbc": "BBC",
        "xinhuanet": "新华网"
    }
    
    for key, source in source_map.items():
        if key in url_lower:
            return source
    
    return "网络媒体"

def build_search_queries():
    """构建优化的搜索查询"""
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    
    # 优化：使用更具体的关键词，排除百科类内容
    queries = {
        "财经": [
            f"{today_str} 油价调整 最新消息 -百科 -百度知道",
            f"今日黄金价格 实时行情 {today_str}",
            f"美股 股市行情 {today_str} 最新",
        ],
        "科技": [
            f"AI 大模型 最新发布 {today_str} -百科",
            f"科技数码 新品发布 {today_str}",
            f"人工智能 技术突破 {today_str}",
        ],
        "国际": [
            f"国际时事 热点新闻 {today_str} -百科",
            f"外交 国际贸易 {today_str}",
            f"海外新闻 全球 {today_str}",
        ]
    }
    
    return queries

def deduplicate_news(news_list, threshold=0.9):
    """去重新闻（基于标题相似度）"""
    seen = []
    unique = []
    
    for news in news_list:
        title = news["title"].lower()
        
        # 检查是否与已有新闻相似
        is_duplicate = False
        for seen_title in seen:
            similarity = calculate_similarity(title, seen_title)
            if similarity > threshold:
                is_duplicate = True
                break
        
        if not is_duplicate:
            seen.append(title)
            unique.append(news)
    
    return unique

def calculate_similarity(s1, s2):
    """简单计算字符串相似度"""
    # 使用 Jaccard 相似度
    set1 = set(s1)
    set2 = set(s2)
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0

def categorize_news(news_list):
    """智能分类新闻"""
    categories = defaultdict(list)
    
    # 关键词权重
    finance_keywords = {
        "油价": 3, "黄金": 3, "股市": 3, "财经": 2, "经济": 2,
        "央行": 3, "通胀": 3, "美元": 2, "人民币": 2, "基金": 2,
        "银行": 2, "利率": 3, "股票": 3, "交易": 2, "市场": 1
    }
    
    tech_keywords = {
        "AI": 3, "人工智能": 3, "科技": 2, "数码": 2, "手机": 2,
        "电脑": 2, "芯片": 3, "软件": 2, "互联网": 2, "游戏": 2,
        "App": 2, "系统": 1, "发布": 1, "新品": 2, "技术": 1
    }
    
    intl_keywords = {
        "国际": 3, "外交": 3, "总统": 3, "大选": 3, "战争": 3,
        "冲突": 3, "欧盟": 2, "联合国": 2, "贸易": 2, "制裁": 3,
        "峰会": 2, "访问": 1, "谈判": 2
    }
    
    for news in news_list:
        title = news["title"].lower()
        
        # 计算各类别得分
        scores = {"财经": 0, "科技": 0, "国际": 0}
        
        for keyword, weight in finance_keywords.items():
            if keyword.lower() in title:
                scores["财经"] += weight
        
        for keyword, weight in tech_keywords.items():
            if keyword.lower() in title:
                scores["科技"] += weight
        
        for keyword, weight in intl_keywords.items():
            if keyword.lower() in title:
                scores["国际"] += weight
        
        # 分配到最高分类别
        max_category = max(scores, key=scores.get)
        if scores[max_category] > 0:
            categories[max_category].append(news)
        else:
            categories["其他"].append(news)
    
    return categories

def filter_quality_news(news_list):
    """过滤低质量新闻"""
    filtered = []
    
    # 排除词
    exclude_patterns = [
        "广告", "推广", "赞助", "营销",
        "点击查看答案", "展开全文", "阅读全文",
        "____", "___", "...",  # 排除格式不良
        "百度百科", "百度知道", "问答",  # 排除百科和问答
    ]
    
    # 排除的 URL 模式
    exclude_urls = [
        "baike.baidu.com",
        "zhidao.baidu.com",
    ]
    
    for news in news_list:
        title = news["title"]
        url = news.get("url", "")
        
        # 检查排除词
        if any(pattern in title for pattern in exclude_patterns):
            continue
        
        # 检查排除 URL
        if any(exclude in url for exclude in exclude_urls):
            continue
        
        # 检查 URL 有效性
        if not url or not url.startswith("http"):
            continue
        
        # 检查标题长度
        if len(title) < 10 or len(title) > 100:
            continue
        
        filtered.append(news)
    
    return filtered

def generate_brief(categorized_news):
    """生成简报"""
    brief = []
    brief.append(f"📰 每日新闻简报 - {datetime.now().strftime('%Y 年 %m 月 %d 日')}")
    brief.append(f"⏰ 更新时间：{datetime.now().strftime('%H:%M')}")
    brief.append("")
    
    for category in ["财经", "科技", "国际"]:
        news_list = categorized_news.get(category, [])
        if news_list:
            brief.append(f"【{category}】")
            for i, news in enumerate(news_list[:4], 1):  # 每类最多 4 条
                title = news["title"]
                source = news.get("source", "")
                brief.append(f"{i}. {title} [{source}]")
            brief.append("")
    
    # 如果没有足够新闻
    total_news = sum(len(v) for v in categorized_news.values())
    if total_news == 0:
        brief.append("😅 今日暂无足够新闻，请稍后再试")
        brief.append("")
    
    brief.append("---")
    brief.append("💡 简报由 AI 生成，全文阅读请访问来源链接")
    
    return "\n".join(brief)

def main():
    """主函数"""
    print("🚀 开始抓取新闻（优化版）...")
    print(f"搜索日期：{datetime.now().strftime('%Y-%m-%d')}")
    print("")
    
    # 构建搜索查询
    queries = build_search_queries()
    
    # 抓取新闻
    all_news = []
    for category, category_queries in queries.items():
        print(f"正在搜索 {category} 新闻...")
        for query in category_queries[:2]:  # 每类 2 个查询
            results = search_news_searxng(query, limit=8)
            print(f"  - '{query}': {len(results)} 条结果")
            all_news.extend(results)
    
    print(f"\n共抓取 {len(all_news)} 条原始新闻")
    
    # 过滤低质量
    filtered_news = filter_quality_news(all_news)
    print(f"过滤后剩余 {len(filtered_news)} 条")
    
    # 去重
    unique_news = deduplicate_news(filtered_news)
    print(f"去重后剩余 {len(unique_news)} 条")
    
    # 分类
    categorized = categorize_news(unique_news)
    
    print("\n分类结果:")
    for cat, news_list in categorized.items():
        print(f"  - {cat}: {len(news_list)} 条")
    
    # 生成简报
    brief = generate_brief(categorized)
    
    # 输出
    print("\n" + "="*60)
    print(brief)
    print("="*60)
    
    # 保存
    output_dir = SCRIPT_DIR / "output"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"brief_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(brief)
    
    # 同时保存原始数据
    data_file = output_dir / f"raw_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total": len(all_news),
            "filtered": len(filtered_news),
            "unique": len(unique_news),
            "categories": {k: len(v) for k, v in categorized.items()},
            "news": unique_news
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 简报已保存到：{output_file}")
    print(f"📊 原始数据已保存到：{data_file}")
    
    return brief

if __name__ == "__main__":
    main()
