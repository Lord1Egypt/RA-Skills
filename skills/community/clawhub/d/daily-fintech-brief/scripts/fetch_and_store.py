#!/usr/bin/env python3
"""
数据抓取 + 本地存储 + 自动清理
- 从数据源抓取信息
- 按天存储原始数据 (保留7天)
- 可被其他脚本调用，返回 JSON 给下一步
"""
import os
import sys
import json
import datetime
import urllib.request
import re
import glob
import shutil

# ===== 复用现有爬虫逻辑 =====
SOURCES = [
    {"title": "The Batch", "url": "https://www.deeplearning.ai/the-batch/rss/", "type": "rss"},
    {"title": "Ben's Bites", "url": "https://www.bensbites.co/rss", "type": "rss"},
    {"title": "Banking Dive", "url": "https://www.bankingdive.com/feeds/news/", "type": "rss"},
    {"title": "中国金融电脑-科技资讯", "url": "https://www.fcc.com.cn/art/kjzx/", "type": "html_list", "base_url": "https://www.fcc.com.cn"},
    {"title": "中国电子银行网-数字银行", "url": "https://www.cebnet.com.cn/szyh/", "type": "html_list", "base_url": "https://www.cebnet.com.cn"},
    {"title": "中国电子银行网-金融AI", "url": "https://www.cebnet.com.cn/financialai/", "type": "html_list", "base_url": "https://www.cebnet.com.cn"},
    {"title": "移动支付网-首页", "url": "https://www.mpaypass.com.cn/", "type": "html_list", "base_url": "https://www.mpaypass.com.cn"},
    {"title": "移动支付网-金科专栏", "url": "https://www.mpaypass.com.cn/authordefault.asp?id=80115", "type": "html_list", "base_url": "https://www.mpaypass.com.cn"}
]

FILTER_KEYWORDS = r"(银行|智能|风控|大模型|分布式|数字化|金融科技|AI|算法|深度学习|核心系统|架构)"

DATA_RETENTION_DAYS = 7

def fetch_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            charset = r.headers.get_content_charset() or 'utf-8'
            return r.read().decode(charset, errors='ignore')
    except Exception as e:
        print(f"[WARN] fetch_html failed: {url} -> {e}", file=sys.stderr)
        return ""

def extract_pure_text(html_content):
    text = re.sub(r'<script[^>]*>([\s\S]*?)</script>', '', html_content)
    text = re.sub(r'<style[^>]*>([\s\S]*?)</style>', '', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:2500]

def crawl_sources():
    """抓取所有数据源，返回原始数据列表"""
    final_payload = []

    for src in SOURCES:
        html = fetch_html(src["url"])
        if not html:
            continue

        links_to_crawl = []

        if src["type"] == "rss":
            items = re.findall(r'<item>([\s\S]*?)</item>', html)[:5]
            for item in items:
                title = (re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', item) or re.findall(r'<title>(.*?)</title>', item) or [""])[0]
                desc = (re.findall(r'<description><!\[CDATA\[(.*?)\]\]></description>', item) or re.findall(r'<description>(.*?)</description>', item) or [""])[0]
                if re.search(FILTER_KEYWORDS, title + desc, re.I):
                    final_payload.append({
                        "source": src["title"],
                        "title": title,
                        "content": extract_pure_text(desc),
                        "url": src["url"]
                    })

        elif src["type"] == "html_list":
            raw_links = re.findall(r'href=["\']([^"\']+\.html[^"\']*)["\'][^>]*>([\s\S]*?)</a>', html)
            seen_urls = set()

            for url, anchor_text in raw_links:
                clean_title = extract_pure_text(anchor_text)
                if len(clean_title) < 6 or not re.search(FILTER_KEYWORDS, clean_title):
                    continue

                full_url = url if url.startswith("http") else src["base_url"] + ("/" + url if not url.startswith("/") else url)
                if full_url in seen_urls:
                    continue
                seen_urls.add(full_url)

                links_to_crawl.append({"title": clean_title, "url": full_url})

            for item in links_to_crawl[:3]:
                detail_html = fetch_html(item["url"])
                if detail_html:
                    body_match = re.search(r'(<article[\s\S]*?</article>|<div[^>]+(?:content|article|body|text)[\s\S]*?>[\s\S]*?</div>)', detail_html)
                    target_html = body_match.group(1) if body_match else detail_html
                    pure_text = extract_pure_text(target_html)

                    final_payload.append({
                        "source": src["title"],
                        "title": item["title"],
                        "content": pure_text,
                        "url": item["url"]
                    })

    return final_payload

def get_data_dir():
    base = os.path.expanduser("~/.openclaw/workspace/skills/daily-fintech-brief")
    return os.path.join(base, "data", "raw")

def get_report_dir():
    base = os.path.expanduser("~/.openclaw/workspace/skills/daily-fintech-brief")
    return os.path.join(base, "output", "reports")

def cleanup_old_data(data_dir, retention_days):
    """清理超过保留天数的旧数据"""
    if not os.path.isdir(data_dir):
        return

    today = datetime.date.today()
    cutoff = today - datetime.timedelta(days=retention_days)

    for f in glob.glob(os.path.join(data_dir, "*.json")):
        basename = os.path.basename(f)
        try:
            date_str = basename.replace(".json", "")
            file_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            if file_date < cutoff:
                os.remove(f)
                print(f"[CLEANUP] Removed old data: {basename}", file=sys.stderr)
        except ValueError:
            continue

def save_raw_data(articles):
    """保存当日原始数据"""
    today = datetime.date.today().isoformat()
    data_dir = get_data_dir()
    os.makedirs(data_dir, exist_ok=True)

    file_path = os.path.join(data_dir, f"{today}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({
            "date": today,
            "articles": articles
        }, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Raw data saved: {file_path}", file=sys.stderr)
    return file_path

def load_today_raw_data():
    """加载当日原始数据（供后续步骤使用）"""
    today = datetime.date.today().isoformat()
    data_dir = get_data_dir()
    file_path = os.path.join(data_dir, f"{today}.json")

    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    return None

def save_report(content, date_str=None):
    """保存总结报告"""
    if date_str is None:
        date_str = datetime.date.today().isoformat()

    report_dir = get_report_dir()
    os.makedirs(report_dir, exist_ok=True)

    file_path = os.path.join(report_dir, f"{date_str}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path

def check_today_report_exists():
    """检查今日报告是否已存在"""
    today = datetime.date.today().isoformat()
    report_dir = get_report_dir()
    report_path = os.path.join(report_dir, f"{today}.md")
    return report_path if os.path.isfile(report_path) else None

def get_yesterday_data():
    """获取昨日的原始数据"""
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    data_dir = get_data_dir()
    file_path = os.path.join(data_dir, f"{yesterday}.json")

    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def check_today_report_exists():
    """检查今日报告是否已存在"""
    today = datetime.date.today().isoformat()
    report_dir = get_report_dir()
    report_path = os.path.join(report_dir, f"{today}.md")
    return report_path if os.path.isfile(report_path) else None

def main():
    today = datetime.date.today().isoformat()

    # 1. 检查今日报告是否已存在
    existing_report = check_today_report_exists()
    if existing_report:
        with open(existing_report, "r", encoding="utf-8") as f:
            report_content = f.read()
        result = {
            "status": "already_exists",
            "date": today,
            "message": "今日报告已存在，直接返回",
            "report_path": existing_report,
            "report_content": report_content
        }
        print(json.dumps(result, ensure_ascii=False))
        return

    # 2. 尝试使用昨日原始数据生成报告
    yesterday_data = get_yesterday_data()
    if yesterday_data:
        articles = yesterday_data.get("articles", [])
        result = {
            "status": "success_from_cache",
            "date": today,
            "data_source_date": (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
            "article_count": len(articles),
            "articles": articles
        }
        print(json.dumps(result, ensure_ascii=False))
        return

    # 3. 没有昨日数据，执行爬取
    articles = crawl_sources()

    # 保存原始数据
    save_raw_data(articles)

    # 清理旧数据
    cleanup_old_data(get_data_dir(), DATA_RETENTION_DAYS)

    # 输出 JSON 给下游
    result = {
        "status": "success",
        "date": today,
        "article_count": len(articles),
        "articles": articles
    }

    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()