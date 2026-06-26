#!/usr/bin/env python3
"""
抓取新闻详情页，提取关键信息
"""

import asyncio
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from curl_cffi import requests as curl_requests


# 利空关键词 - 电池行业相关
NEGATIVE_KEYWORDS = [
    "锂电池着火", "电池起火", "电池爆炸", "电池召回", "电池自燃",
    "电动汽车起火", "储能电站火灾", "电池工厂爆炸", "停车场电动车起火",
    "fire", "explosion", "recall", "battery fire incident", "EV fire",
    "взрыв батареи", "пожар аккумулятор"
]

# 利好关键词 - 政策补贴
POSITIVE_KEYWORDS = [
    "补贴", "奖励", "支持", "激励", "优惠", "批准", "减税", "免税",
    "subsidy", "incentive", "tax credit", "grant", "funding", "approval",
    "субсидия", "поддержка", "финансирование"
]

# 政策法规关键词
POLICY_KEYWORDS = [
    "法案", "法规", "政策", "可拆卸", "回收", "标准", "要求", "强制",
    "act", "law", "regulation", "mandate", "requirement",
    "закон", "политика", "регулирование"
]


def extract_article_date(html: str) -> Optional[str]:
    """从HTML中提取文章日期"""
    patterns = [
        r'<span[^>]*class="[^"]*date[^"]*"[^>]*>([^<]+)</span>',
        r'<time[^>]*datetime="([^"]*)"',
        r'(\d{4}[-/]\d{2}[-/]\d{2})',
        r'(\d{4}年\d{1,2}月\d{1,2}日)',
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    return None


def extract_article_content(html: str) -> str:
    """提取文章正文"""
    # 移除脚本和样式
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    # 移除标签获取纯文本
    text = re.sub(r'<[^>]+>', ' ', html)
    # 清理空白
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:1500]  # 限制长度


def classify_sentiment(title: str, content: str) -> str:
    """分类情感：利好/利空/中性"""
    text = (title + " " + content).lower()

    neg_count = sum(1 for kw in NEGATIVE_KEYWORDS if kw.lower() in text)
    pos_count = sum(1 for kw in POSITIVE_KEYWORDS if kw.lower() in text)
    pol_count = sum(1 for kw in POLICY_KEYWORDS if kw.lower() in text)

    if neg_count > 0:
        return "利空"
    elif pos_count > 0 or pol_count > 0:
        return "利好"
    return "中性"


def classify_type(title: str, content: str) -> str:
    """分类新闻类型"""
    text = (title + " " + content).lower()

    if any(kw in text for kw in ["补贴", "subsidy", "incentive", "funding", "grant", "tax credit"]):
        return "政策补贴"
    elif any(kw in text for kw in ["法案", "law", "regulation", "mandate", "standard", "法规"]):
        return "法规"
    elif any(kw in text for kw in ["着火", "fire", "爆炸", "explosion", "起火", "взрыв"]):
        return "重大事件"
    elif any(kw in text for kw in ["产能", "production", "扩产", "investment", "factory", "plant"]):
        return "行业动态"
    return "行业动态"


def fetch_detail(news_item: Dict) -> Dict:
    """抓取单条新闻详情"""
    url = news_item.get("url", "")
    if not url or not url.startswith("http"):
        return {**news_item, "content": "", "date": None, "sentiment": "中性", "type": "行业动态"}

    try:
        resp = curl_requests.get(url, timeout=8, impersonate="chrome")
        content = extract_article_content(resp.text)
        date = extract_article_date(resp.text)

        sentiment = classify_sentiment(news_item["title"], content)
        news_type = classify_type(news_item["title"], content)

        return {
            **news_item,
            "content": content,
            "date": date,
            "sentiment": sentiment,
            "type": news_type
        }
    except Exception as e:
        return {
            **news_item,
            "content": "",
            "date": None,
            "sentiment": "中性",
            "type": "行业动态"
        }


async def fetch_batch(news_list: List[Dict], batch_size: int = 5) -> List[Dict]:
    """批量抓取"""
    results = []
    for i in range(0, len(news_list), batch_size):
        batch = news_list[i:i+batch_size]
        tasks = [asyncio.to_thread(fetch_detail, item) for item in batch]
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
        print(f"  Processed {min(i+batch_size, len(news_list))}/{len(news_list)}")
        await asyncio.sleep(0.5)
    return results


async def main():
    """主函数"""
    today = datetime.now().strftime("%Y%m%d")
    input_file = Path(__file__).parent.parent / "data" / f"news_raw_{today}.json"

    if not input_file.exists():
        print(f"Raw data not found: {input_file}")
        return

    with open(input_file, encoding="utf-8") as f:
        news_list = json.load(f)

    print(f"Fetching details for {len(news_list)} news...")

    enriched_news = await fetch_batch(news_list)

    # 按情感分组统计
    sentiment_stats = {"利好": 0, "利空": 0, "中性": 0}
    for news in enriched_news:
        sentiment_stats[news["sentiment"]] += 1

    output_file = Path(__file__).parent.parent / "data" / f"news_parsed_{today}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(enriched_news, f, ensure_ascii=False, indent=2)

    print(f"\n[DONE] Good: {sentiment_stats['利好']} | Bad: {sentiment_stats['利空']} | Neutral: {sentiment_stats['中性']}")
    return enriched_news


if __name__ == "__main__":
    asyncio.run(main())
