#!/usr/bin/env python3
"""
创造者情报 V5 - 工程师视角终极版
严禁VC话术，只关注底层技术实现
"""

import json
import os
import sys
from datetime import datetime
import feedparser
import re
import requests

CONFIG_DIR = os.path.expanduser("~/.openclaw/creator-intel")
HISTORY_FILE = os.path.join(CONFIG_DIR, "history.json")
TAVILY_API_KEY = "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"

# V5 工程师视角搜索关键词（去商业化，重技术）
ENGINEER_QUERIES = [
    # 开源项目与GitHub霸榜
    "GitHub trending robotics open source 2026",
    "open source surgical robot hardware design",
    "brain computer interface BCI open source project",
    "humanoid robot open source hardware GitHub",
    
    # 硬核技术原理解析
    "MoE mixture of experts architecture medical AI",
    "sparse attention mechanism robotics",
    "flow matching diffusion model technical",
    "neural radiance field NeRF medical imaging",
    
    # 极客硬件与创新交互
    "ESP32 medical device prototype Kickstarter",
    "Raspberry Pi 5 robotics project",
    "e-ink display wearable health monitoring",
    "flexible electronics brain implant material",
    
    # 算法与架构突破
    "transformer alternative architecture 2026",
    "edge AI inference optimization robotics",
    "neuromorphic computing chip medical",
]

# 国内技术向RSS
CN_TECH_SOURCES = [
    {"name": "机器之心", "url": "https://www.jiqizhixin.com/rss", "cat": "tech"},
    {"name": "量子位", "url": "https://www.qbitai.com/feed", "cat": "tech"},
    {"name": "开源中国", "url": "https://www.oschina.net/news/rss", "cat": "opensource"},
]

# V5 黑名单（商业化噪音）
BLACKLIST = [
    r'融资.*亿', r'估值.*亿', r'商业化.*落地', r'规模化.*部署',
    r'拓展.*市场', r'战略.*发布', r'生态.*布局', r'赛道.*龙头',
    r'领跑.*行业', r'颠覆.*传统', r'革命性.*突破', r'重磅.*发布',
    r'iPhone', r'Samsung', r'消费.*电子', r'春晚', r'超级碗',
]

# V5 白名单（技术信号）
WHITELIST = [
    r'开源', r'GitHub', r'架构', r'算法', r'模型.*参数', 
    r'MoE', r'稀疏注意力', r'流匹配', r'扩散.*模型',
    r'手术机器人', r'脑机接口', r'BCI', r'灵巧手',
    r'ESP32', r'树莓派', r'Raspberry', r'NVMe', r'PCIe',
    r'边缘.*推理', r'实时.*推理', r'神经网络', r'芯片.*架构',
]

def tavily_search(query, max_results=3):
    """Tavily API 搜索技术向内容"""
    try:
        url = "https://api.tavily.com/search"
        headers = {"Content-Type": "application/json"}
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "advanced",
            "include_answer": False,
            "max_results": max_results,
            "include_domains": [
                "github.com", "arxiv.org", "hackaday.com", "kickstarter.com",
                "ieee.org", "spectrum.ieee.org", "embedded.com", "raspberrypi.com"
            ]
        }
        
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        data = resp.json()
        
        results = []
        for item in data.get("results", []):
            title = item.get("title", "")
            url = item.get("url", "")
            content = item.get("content", "")
            
            # V5 过滤：降权纯商业化内容
            if any(re.search(p, title + content, re.I) for p in BLACKLIST):
                if not any(re.search(p, title + content, re.I) for p in WHITELIST):
                    continue
            
            results.append({
                "title": title,
                "url": url,
                "content": content,
                "source": "tavily"
            })
        
        return results
    except Exception as e:
        print(f"Tavily 搜索失败: {e}")
        return []

def clean_title(title):
    """清洗标题"""
    patterns = [
        r'\|.*36氪.*', r'\|.*机器之心.*', r'\|.*量子位.*',
        r'重磅.*', r'深度.*', r'独家.*', r'首发.*',
        r'GitHub - ', r'GitHub: ', r'Kickstarter - ',
    ]
    for p in patterns:
        title = re.sub(p, '', title)
    return title.strip()

def rewrite_engineer_title(original):
    """V5 工程师视角重写标题"""
    title = clean_title(original)
    
    # 提取核心技术实体
    tech_entities = [
        (r'(MoE|Mixture of Experts)', 'MoE架构'),
        (r'(sparse attention|稀疏注意力)', '稀疏注意力'),
        (r'(flow matching|流匹配)', '流匹配'),
        (r'(diffusion|扩散模型)', '扩散模型'),
        (r'(transformer|Transformer)', 'Transformer'),
        (r'(ESP32|esp32)', 'ESP32'),
        (r'(Raspberry Pi|raspberry)', '树莓派'),
        (r'(NVMe|nvme)', 'NVMe'),
        (r'(PCIe|pcie)', 'PCIe'),
        (r'(GitHub|github)', 'GitHub'),
        (r'(surgical robot|手术机器人)', '手术机器人'),
        (r'(BCI|brain.?computer|脑机)', '脑机接口'),
        (r'(humanoid|人形机器人)', '人形机器人'),
        (r'(flexible electronics|柔性电子)', '柔性电子'),
        (r'(neuromorphic|神经形态)', '神经形态芯片'),
    ]
    
    core_tech = ""
    for pattern, name in tech_entities:
        if re.search(pattern, title, re.I):
            core_tech = name
            break
    
    # 提取动作
    actions = [
        (r'(开源|open.?source)', '开源'),
        (r'(发布|release|launch)', '发布'),
        (r'(实现|achieve|reach)', '实现'),
        (r'(采用|adopt|use)', '采用'),
        (r'(优化|optimize|improve)', '优化'),
    ]
    
    action = ""
    for pattern, name in actions:
        if re.search(pattern, title, re.I):
            action = name
            break
    
    # 提取性能参数
    perf_match = re.search(r'(\d+[\d\s]*(?:tokens?/s|Hz|GB|MB/s|fps|ms|参数|B|M))', title, re.I)
    perf = perf_match.group(1) if perf_match else ""
    
    # 组合：技术 + 动作 + 性能
    parts = [p for p in [core_tech, action, perf] if p]
    if len(parts) >= 2:
        rewritten = f"{parts[0]}{parts[1]}" + (f"达{parts[2]}" if len(parts) > 2 else "")
    elif len(parts) == 1:
        rewritten = parts[0] + "技术突破"
    else:
        rewritten = title[:18] + "…" if len(title) > 18 else title
    
    # 控制长度
    if len(rewritten) > 22:
        rewritten = rewritten[:20] + "…"
    
    return rewritten

def extract_tech_summary(content):
    """V5 提取硬核技术摘要（至少2个技术名词/参数）"""
    text = content or ""
    
    # 找架构/算法描述
    arch_patterns = [
        r'(?:采用|使用|基于|通过)([^，。]{8,40})(?:架构|算法|机制|技术)',
        r'((?:MoE|sparse attention|flow matching|diffusion|transformer)[^，。]{5,30})',
        r'((?:PCIe|NVMe|ESP32|ARM|RISC-V)[^，。]{5,25})',
    ]
    
    tech_detail = ""
    for pattern in arch_patterns:
        match = re.search(pattern, text, re.I)
        if match:
            tech_detail = match.group(1) if match.lastindex else match.group(0)
            break
    
    # 找性能参数
    perf_patterns = [
        r'(\d+[\d\s]*(?:tokens?/s|Hz|GB/s|MB/s|fps|ms|微秒|纳秒))',
        r'(\d+[\d\s]*(?:亿|万|B|M|参数))',
        r'(延迟|速度|吞吐量|带宽)(?:降低|提升|达到)([^，。]{3,15})',
    ]
    
    perf_detail = ""
    for pattern in perf_patterns:
        match = re.search(pattern, text, re.I)
        if match:
            perf_detail = match.group(0)
            break
    
    # 找解决的问题/应用场景
    problem_patterns = [
        r'(?:解决了|攻克了|针对)([^，。]{8,30})(?:问题|痛点|瓶颈)',
        r'(?:支持|实现)([^，。]{5,25})(?:功能|能力|操作)',
    ]
    
    problem_detail = ""
    for pattern in problem_patterns:
        match = re.search(pattern, text, re.I)
        if match:
            problem_detail = match.group(1) if match.lastindex else match.group(0)
            break
    
    # 组合摘要（必须包含至少2个技术元素）
    summary_parts = []
    if tech_detail:
        summary_parts.append(tech_detail)
    if perf_detail:
        summary_parts.append(f"关键性能：{perf_detail}")
    if problem_detail and len(summary_parts) < 2:
        summary_parts.append(f"应用场景：{problem_detail}")
    
    if len(summary_parts) >= 2:
        summary = "；".join(summary_parts[:2])
    elif len(summary_parts) == 1:
        # 补充技术细节
        summary = summary_parts[0] + "，实现底层架构突破"
    else:
        # 备选：提取前80字
        summary = text[:70] + "…" if len(text) > 70 else text
    
    return summary[:75] + "…" if len(summary) > 75 else summary

def fetch_cn_tech_news(source, history):
    """抓取国内技术向RSS"""
    try:
        feed = feedparser.parse(source["url"])
        news_list = []
        
        for entry in feed.entries[:5]:
            url = entry.get('link', '')
            title = entry.get('title', '')
            
            if not url or not title or url in history.get("sent_urls", []):
                continue
            
            # V5 过滤商业化噪音
            if any(re.search(p, title, re.I) for p in BLACKLIST):
                if not any(re.search(p, title, re.I) for p in WHITELIST):
                    continue
            
            content = entry.get('description', '') or entry.get('summary', '')
            
            # 重写标题
            new_title = rewrite_engineer_title(title)
            
            # 提取技术摘要
            summary = extract_tech_summary(content)
            if not summary or len(summary) < 15:
                continue
            
            news_list.append({
                "title": new_title,
                "summary": summary,
                "url": url,
                "region": "cn",
                "source": "rss"
            })
        
        return news_list
    except:
        return []

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data.setdefault("sent_urls", [])
            return data
    return {"sent_urls": []}

def save_history(history):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def generate_intel():
    """V5 工程师视角生成情报"""
    history = load_history()
    
    # 1. Tavily 搜索国际技术向内容（优先）
    global_news = []
    for query in ENGINEER_QUERIES[:4]:  # 搜索4个关键词
        results = tavily_search(query, max_results=2)
        for item in results:
            # 重写标题
            new_title = rewrite_engineer_title(item["title"])
            # 提取技术摘要
            summary = extract_tech_summary(item["content"])
            
            global_news.append({
                "title": new_title,
                "summary": summary,
                "url": item["url"],
                "region": "global"
            })
    
    # 2. 国内技术RSS
    cn_news = []
    for source in CN_TECH_SOURCES:
        news = fetch_cn_tech_news(source, history)
        cn_news.extend(news)
    
    # 合并并去重
    all_news = global_news + cn_news
    seen_urls = set()
    unique_news = []
    for n in all_news:
        if n["url"] not in seen_urls and n["url"] not in history.get("sent_urls", []):
            unique_news.append(n)
            seen_urls.add(n["url"])
    
    # V5 优先技术向内容（国际优先）
    selected = unique_news[:6]
    
    if len(selected) < 3:
        return "[警告] 未获取到足够的硬核技术情报"
    
    # V5 严格格式输出
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"[{today}] 创造者情报 🌍", ""]
    
    for news in selected:
        # Emoji
        t = news["title"].lower()
        if any(kw in t for kw in ["github", "开源", "open source"]):
            emoji = "📦"
        elif any(kw in t for kw in ["架构", "算法", "model", "transformer", "diffusion"]):
            emoji = "⚛️"
        elif any(kw in t for kw in ["esp32", "raspberry", "树莓派", "nvme", "pcie"]):
            emoji = "🛠️"
        elif any(kw in t for kw in ["手术机器人", "surgical", "机器人"]):
            emoji = "🔬"
        elif any(kw in t for kw in ["脑机", "bci", "brain"]):
            emoji = "🧠"
        else:
            emoji = "💡"
        
        # V5 格式
        lines.append(f"> {emoji} {news['title']}")
        lines.append(f"> 摘要：{news['summary']}")
        lines.append("")
        lines.append("")
        
        history["sent_urls"].append(news["url"])
    
    save_history(history)
    return "\n".join(lines)

if __name__ == "__main__":
    intel = generate_intel()
    print(intel)
