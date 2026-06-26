#!/usr/bin/env python3
import json, re, subprocess, sys, urllib.request
from datetime import datetime, timezone, timedelta

SKILL_DIR = "/Applications/QClaw.app/Contents/Resources/openclaw/config/skills/design-daily-news-1.0.0"

KEEP_KW = [
    "AI", "GPT", "Claude", "Gemini", "OpenAI", "DeepSeek",
    "GPU", "UI", "UX", "Figma", "Adobe", "Cursor", "Midjourney", "OpenClaw",
    "人工智能", "芯片", "设计", "产品", "交互", "科技", "技术", "创新", "趋势",
    "Agent", "模型", "智能", "腾讯", "阿里", "百度", "龙虾", "大模型", "机器人",
    "开源", "MiniMax", "Manus", "字节", "小米", "华为", "苹果", "谷歌", "微软"
]

FILTER_KW = [
    "白酒", "营销", "广告", "SU7", "电动车评测", "明星", "综艺",
    "体育", "足球", "篮球", "娱乐", "八卦", "房产", "理财", "基金"
]

MAX_TOTAL = 15


def extract_inline_url(content):
    match = re.search(r'\[\[(?:来源|全文|官网):?(https?://[^\]]+)\]\]', content)
    if match:
        url = match.group(1).strip()
        clean = re.sub(r'\[\[(?:来源|全文|官网):?https?://[^\]]+\]\]', '', content).strip()
        return clean, url
    return content, ""


def fetch_uisdc():
    try:
        result = subprocess.run(
            ["bash", f"{SKILL_DIR}/scripts/fetch_uisdc.sh"],
            capture_output=True, text=True, timeout=30
        )
        raw = result.stdout.strip()
        if not raw:
            return []
        try:
            data = json.loads(raw)
        except Exception:
            raw = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', raw)
            data = json.loads(raw)
        if not data:
            return []
        latest = data[0]
        news = []
        for item in latest.get("dubao", []):
            title = item.get("title", "").replace("\u300b","").replace("\u300a","").replace("\u3011","").replace("\u3010","").strip()
            raw_content = item.get("content", "").strip()
            raw_url = item.get("url", "").strip()
            content, inline_url = extract_inline_url(raw_content)
            url = raw_url or inline_url
            if title:
                news.append({"title": title, "content": content, "url": url, "source": "优设读报"})
        return news
    except Exception as e:
        print(f"[优设读报] 失败: {e}", file=sys.stderr)
        return []


def fetch_36kr():
    try:
        result = subprocess.run(
            ["bash", f"{SKILL_DIR}/scripts/fetch_36kr.sh"],
            capture_output=True, text=True, timeout=30
        )
        raw = result.stdout.strip()
        if not raw:
            return []
        data = json.loads(raw)
        news = []
        for item in data.get("articles", []):
            title = item.get("title", "").strip()
            summary = item.get("summary", "").strip()
            url = item.get("url", "").strip()
            if not title:
                continue
            if any(kw in title or kw in summary for kw in FILTER_KW):
                continue
            if any(kw in title or kw in summary for kw in KEEP_KW):
                news.append({"title": title, "content": summary, "url": url, "source": "36氪"})
        return news
    except Exception as e:
        print(f"[36氪] 失败: {e}", file=sys.stderr)
        return []


def fetch_huxiu():
    try:
        req = urllib.request.Request(
            "https://www.huxiu.com",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept-Language": "zh-CN,zh;q=0.9"
            }
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        articles = []
        match = re.search(r'<script[^>]*data-nuxt-data[^>]*>(.*?)</script>', html, re.DOTALL)
        if match:
            try:
                raw_data = json.loads(match.group(1))
                titles, urls = [], []
                if isinstance(raw_data, list):
                    for item in raw_data:
                        if isinstance(item, str) and 10 < len(item) < 200:
                            if any(c in item for c in ["\uff1f","\uff01","\uff1a","\u4e28"]) or ("\u7684" in item and len(item) > 15):
                                titles.append(item)
                        elif isinstance(item, str) and item.startswith("/article/"):
                            urls.append("https://www.huxiu.com" + item)
                for i, t in enumerate(titles[:20]):
                    articles.append({"title": t, "url": urls[i] if i < len(urls) else "", "summary": ""})
            except Exception:
                pass
        news = []
        for item in articles:
            title = item.get("title", "").strip()
            summary = item.get("summary", "").strip()
            url = item.get("url", "").strip()
            if not title:
                continue
            if any(kw in title or kw in summary for kw in FILTER_KW):
                continue
            if any(kw in title or kw in summary for kw in KEEP_KW):
                news.append({"title": title, "content": summary, "url": url, "source": "虎嗅"})
        return news
    except Exception as e:
        print(f"[虎嗅] 失败: {e}", file=sys.stderr)
        return []


def format_item(idx, item, show_source_tag=False):
    """
    格式：序号. [标题](url) - 摘要
    有链接用 markdown 超链接格式，没链接纯文本
    """
    title = item["title"]
    if show_source_tag:
        title = f"{title} [{item['source']}]"
    content = item["content"]
    url = item["url"]

    if url:
        line = f"{idx}. [{title}]({url})"
    else:
        line = f"{idx}. {title}"

    if content:
        line += f" - {content}"

    return line


def build_report():
    tz = timezone(timedelta(hours=8))
    today = datetime.now(tz).strftime("%Y-%m-%d")

    uisdc_news = fetch_uisdc()
    remaining = max(0, MAX_TOTAL - len(uisdc_news))
    extra_news = []

    if remaining > 0:
        kr_news = fetch_36kr()
        hx_news = fetch_huxiu()
        combined = []
        for i in range(max(len(kr_news), len(hx_news))):
            if i < len(kr_news):
                combined.append(kr_news[i])
            if i < len(hx_news):
                combined.append(hx_news[i])
        extra_news = combined[:remaining]

    lines = [f"📰 设计日报 - {today}", ""]

    idx = 1
    if uisdc_news:
        lines.append("🎨 优设读报")
        lines.append("")
        for item in uisdc_news:
            lines.append(format_item(idx, item, show_source_tag=False))
            lines.append("")
            idx += 1

    if extra_news:
        lines.append("📡 科技资讯精选")
        lines.append("")
        for item in extra_news:
            lines.append(format_item(idx, item, show_source_tag=True))
            lines.append("")
            idx += 1

    total = len(uisdc_news) + len(extra_news)
    lines.append("---")
    lines.append(f"共 {total} 条 | 优设读报 {len(uisdc_news)} 条 + 科技精选 {len(extra_news)} 条")
    return "\n".join(lines)


if __name__ == "__main__":
    print(build_report())
