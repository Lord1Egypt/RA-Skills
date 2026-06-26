#!/usr/bin/env python3
"""
AI Agent 企业落地案例 — RSS 抓取器 + LLM 智能过滤

用法:
  python3 rss-crawler.py                    # 抓取所有 RSS 源
  python3 rss-crawler.py --dry-run          # 只抓取不过滤
  python3 rss-crawler.py --source openai    # 只抓指定源
"""

import feedparser
import json
import hashlib
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# === 配置 ===
SKILL_DIR = Path(__file__).parent
SKILL_ROOT = SKILL_DIR.parent
DATA_DIR = SKILL_ROOT / "data"
STATE_FILE = DATA_DIR / "rss-state.json"
OUTPUT_DIR = DATA_DIR / "candidates"

RSS_FEEDS = {
    "openai": {
        "url": "https://openai.com/blog/rss.xml",
        "type": "rss",
        "lang": "en",
        "filter_keywords": ["enterprise", "customer", "business", "production", "deployment", "case study", "api", "agent"]
    },
    "microsoft-ai": {
        "url": "https://blogs.microsoft.com/ai/feed",
        "type": "rss",
        "lang": "en",
        "filter_keywords": ["enterprise", "customer", "copilot", "production", "deployment", "agent", "case"]
    },
    "aws-ml": {
        "url": "https://aws.amazon.com/blogs/machine-learning/feed/",
        "type": "rss",
        "lang": "en",
        "filter_keywords": ["enterprise", "customer", "production", "deployment", "agent", "case study", "industry"]
    },
    "hn-frontpage": {
        "url": "https://hnrss.org/frontpage",
        "type": "rss",
        "lang": "en",
        "filter_keywords": ["enterprise AI", "AI agent", "AI production", "AI deployment", "LLM production"]
    },
    "hn-enterprise-ai": {
        "url": "https://hnrss.org/newest?q=enterprise+AI+agent",
        "type": "rss",
        "lang": "en",
        "filter_keywords": []
    },
    "hn-ai-production": {
        "url": "https://hnrss.org/newest?q=AI+production+deployment",
        "type": "rss",
        "lang": "en",
        "filter_keywords": []
    },
    "devto-aigents": {
        "url": "https://dev.to/feed/tag/aigents",
        "type": "rss",
        "lang": "en",
        "filter_keywords": ["enterprise", "production", "deployment", "business", "case"]
    },
    # 机器之心：RSS 已失效（返回 JS 渲染 HTML），改为浏览器源
    # "jiqizhixin": {
    #     "url": "https://www.jiqizhixin.com/rss",
    #     "type": "rss",
    #     "lang": "zh",
    #     "filter_keywords": ["企业", "落地", "部署", "应用", "案例", "智能体", "Agent"],
    #     "parser": "lenient"
    # },
    "36kr": {
        "url": "https://www.36kr.com/feed",
        "type": "rss",
        "lang": "zh",
        "filter_keywords": ["AI智能体", "AI Agent", "大模型落地", "AI应用", "企业AI", "AI转型", "智能体落地"]
    },
    # === 2026-05-01 新增：影响力渠道 ===
    "techmeme": {
        "url": "https://www.techmeme.com/feed.xml",
        "type": "rss",
        "lang": "en",
        "filter_keywords": ["AI", "agent", "enterprise", "LLM", "startup", "deployment", "model"]
    },
    "product-hunt": {
        "url": "https://www.producthunt.com/feed",
        "type": "rss",
        "lang": "en",
        "filter_keywords": ["AI", "agent", "LLM", "enterprise", "automation", "productivity"]
    },
    "hn-show-hn": {
        "url": "https://hnrss.org/show",
        "type": "rss",
        "lang": "en",
        "filter_keywords": ["AI", "agent", "LLM", "enterprise", "deployment", "production"]
    },
    "hn-ask-hn": {
        "url": "https://hnrss.org/ask",
        "type": "rss",
        "lang": "en",
        "filter_keywords": ["AI", "agent", "LLM", "enterprise", "deployment", "production", "architecture"]
    }
}

# Web-fetch 源（无 RSS，需浏览器或 web_fetch 抓取）
# ⚠️ 大部分咨询/厂商站封了 web_fetch，需要浏览器自动化
# 建议：手动定期浏览，或配置 Brave Search API 后用搜索发现
WEB_FETCH_SOURCES = {
    "anthropic-customers": {
        "url": "https://claude.com/customers",
        "lang": "en",
        "method": "browser",  # JS渲染，需浏览器
        "notes": "Anthropic客户案例，高质量"
    },
    "google-cloud-ai": {
        "url": "https://cloud.google.com/blog/ai",
        "lang": "en",
        "method": "browser"
    },
    "mckinsey-ai": {
        "url": "https://www.mckinsey.com/capabilities/quantumblack/our-insights",
        "lang": "en",
        "method": "browser",  # 403封web_fetch
        "notes": "需Cookie或浏览器"
    },
    "bcg-ai": {
        "url": "https://www.bcg.com/capabilities/technology-artificial-intelligence",
        "lang": "en",
        "method": "browser"
    },
    "hbr-ai": {
        "url": "https://hbr.org/topic/subject/ai-machine-learning",
        "lang": "en",
        "method": "browser"
    },
    "infoq-ai": {
        "url": "https://www.infoq.cn/article/ai",
        "lang": "zh",
        "method": "browser"  # 451
    },
    "qbitai": {
        "url": "https://www.qbitai.com",
        "lang": "zh",
        "method": "browser"  # 403
    },
    "jiqizhixin": {
        "url": "https://www.jiqizhixin.com/articles",
        "lang": "zh",
        "method": "browser",  # RSS 已失效，返回JS渲染HTML
        "notes": "机器之心，高质量AI新闻"
    }
}


def load_state():
    """加载已处理条目的状态"""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"processed": {}, "last_run": None}


def save_state(state):
    """保存状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["last_run"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def entry_id(entry):
    """生成条目唯一 ID"""
    key = entry.get("id", "") or entry.get("link", "") or entry.get("title", "")
    return hashlib.md5(key.encode()).hexdigest()[:12]


def keyword_match(text, keywords, lang):
    """关键词匹配（简单过滤，LLM 精筛在后续步骤）"""
    if not keywords:
        return True  # HN 搜索源已预过滤
    text_lower = text.lower()
    if lang == "zh":
        return any(kw in text for kw in keywords)
    return any(kw.lower() in text_lower for kw in keywords)


def fetch_rss(source_name, source_config, state, max_age_days=7):
    """抓取单个 RSS 源"""
    url = source_config["url"]
    lang = source_config["lang"]
    keywords = source_config.get("filter_keywords", [])
    
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f"  ❌ 抓取失败: {e}")
        return []
    
    if feed.bozo and not feed.entries:
        # 宽松模式：有些源格式不规范但有内容
        if source_config.get("parser") == "lenient":
            try:
                feed = feedparser.parse(url, resolve_relative_uris=False, sanitize_html=False)
                if not feed.entries:
                    print(f"  ❌ 解析失败: {feed.bozo_exception}")
                    return []
            except:
                print(f"  ❌ 解析失败: {feed.bozo_exception}")
                return []
        else:
            print(f"  ❌ 解析失败: {feed.bozo_exception}")
            return []
    
    results = []
    cutoff = datetime.now() - timedelta(days=max_age_days)
    
    for entry in feed.entries[:20]:  # 每源最多 20 条
        eid = entry_id(entry)
        
        # 跳过已处理的
        if eid in state["processed"]:
            continue
        
        # 解析发布时间
        published = None
        for field in ["published_parsed", "updated_parsed"]:
            tp = entry.get(field)
            if tp:
                try:
                    published = datetime(*tp[:6])
                    break
                except:
                    pass
        
        if published and published < cutoff:
            continue
        
        # 标题+摘要拼接
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        if len(summary) > 500:
            summary = summary[:500] + "..."
        text = f"{title}\n{summary}"
        
        # 关键词过滤
        if not keyword_match(text, keywords, lang):
            state["processed"][eid] = {"skipped": True, "date": datetime.now().isoformat()}
            continue
        
        results.append({
            "id": eid,
            "source": source_name,
            "title": title,
            "link": entry.get("link", ""),
            "summary": summary,
            "published": published.isoformat() if published else None,
            "lang": lang
        })
    
    return results


def main():
    parser = argparse.ArgumentParser(description="AI Agent 企业落地案例 RSS 抓取器")
    parser.add_argument("--dry-run", action="store_true", help="只抓取不过滤/不保存")
    parser.add_argument("--source", help="只抓指定源（如 openai, 36kr）")
    parser.add_argument("--max-age", type=int, default=7, help="最大天数（默认7）")
    args = parser.parse_args()
    
    state = load_state()
    all_candidates = []
    
    # 选择源
    sources = RSS_FEEDS
    if args.source:
        if args.source in sources:
            sources = {args.source: sources[args.source]}
        else:
            print(f"未知源: {args.source}")
            print(f"可用源: {', '.join(RSS_FEEDS.keys())}")
            sys.exit(1)
    
    # 抓取 RSS
    for name, config in sources.items():
        print(f"📡 抓取 [{name}] {config['url']}")
        results = fetch_rss(name, config, state, args.max_age)
        print(f"   → {len(results)} 条候选")
        all_candidates.extend(results)
    
    print(f"\n📊 总计: {len(all_candidates)} 条新候选")
    
    if not all_candidates:
        print("没有新的候选条目")
        if not args.dry_run:
            save_state(state)
        return
    
    # 保存候选
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = OUTPUT_DIR / f"{today}_candidates.json"
    
    # 如果今天已有文件，合并
    existing = []
    if output_file.exists():
        existing = json.loads(output_file.read_text())
        existing_ids = {e["id"] for e in existing}
        all_candidates = [c for c in all_candidates if c["id"] not in existing_ids]
    
    combined = existing + all_candidates
    
    if not args.dry_run:
        output_file.write_text(json.dumps(combined, ensure_ascii=False, indent=2))
        save_state(state)
        print(f"💾 保存到: {output_file}")
        print(f"   今日总计: {len(combined)} 条候选")
    else:
        print("\n[DRY RUN] 候选条目预览:")
        for c in all_candidates[:10]:
            print(f"  [{c['source']}] {c['title'][:60]}...")
    
    # 输出摘要
    print(f"\n📋 按源统计:")
    by_source = {}
    for c in combined:
        by_source.setdefault(c["source"], []).append(c)
    for src, items in sorted(by_source.items()):
        print(f"  {src}: {len(items)} 条")


if __name__ == "__main__":
    main()
