#!/usr/bin/env python3
"""
早报脚本 - 每天 8:30 执行
抓取 RSS 信源 → LLM 筛选 → 推送到 Telegram（闪电Bot）

信源：
- blogwatcher管理：36氪、量子位、Product Hunt、RadarAI
- 直接抓取：Hugging Face Blog、人人都是产品经理

筛选方向：
1. AI工具平台动态：头部大厂进展；竞品更新/暴雷；OpenRouter top apps榜单变化
2. AI Agent新进展、普通人用AI转型或变现案例
3. 资本市场动荡：AI大厂动态；裁员/融资/暴雷/政策
4. 内容运营/流量变现新机会
"""

import subprocess
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import os
import re
from datetime import datetime, timezone, timedelta

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
CLAWDCHAT_API_KEY = os.environ.get("CLAWDCHAT_API_KEY", "")
API_HUB_BASE = os.environ.get("API_HUB_BASE_URL", os.environ.get("API_HUB_BASE", "https://api.mulerun.com"))
API_HUB_KEY = os.environ.get("API_HUB_KEY", "")
MAX_ITEMS = 10

# 直接抓取的信源（不走blogwatcher）
DIRECT_FEEDS = [
    ("Hugging Face Blog", "https://huggingface.co/blog/feed.xml"),
    ("人人都是产品经理", "https://www.woshipm.com/feed"),
]

def call_clawdchat_tool(server, tool, args=None):
    """调用虾聊工具网关，每次消耗1积分（上限10/天）"""
    payload = json.dumps({
        "server": server,
        "tool": tool,
        "arguments": args or {}
    }, ensure_ascii=True).encode("ascii")
    req = urllib.request.Request(
        "https://clawdchat.cn/api/v1/tools/call",
        data=payload,
        headers={
            "Authorization": f"Bearer {CLAWDCHAT_API_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=20).read())
        if r.get("success"):
            return r.get("data", {})
        else:
            print(f"[WARN] {server}.{tool}: {r.get('error','')}")
            return None
    except Exception as e:
        print(f"[WARN] clawdchat tool {server}.{tool} 失败: {e}")
        return None


def get_clawdchat_articles():
    """
    调用虾聊工具网关补充早报信源（5次/天，合计5积分）
    - trends-hub.get-36kr-trending   36氪科技热榜
    - trends-hub.get-infoq-news      InfoQ AI/技术资讯
    - trends-hub.get-zhihu-trending  知乎热榜
    - reddit.get_subreddit_hot_posts r/LocalLLaMA
    - twitter-scraper.twitter_get_tweets @xuezhiqian123
    """
    articles = []

    # 1. 36氪热榜
    d = call_clawdchat_tool("trends-hub", "get-36kr-trending", {"type": "hot"})
    if d:
        items = d if isinstance(d, list) else d.get("items", d.get("data", []))
        for item in (items[:8] if isinstance(items, list) else []):
            title = item.get("title") or item.get("name", "")
            link = item.get("url") or item.get("link", "")
            if title:
                articles.append({"title": title, "link": link, "source": "36氪"})

    # 2. InfoQ技术资讯
    d = call_clawdchat_tool("trends-hub", "get-infoq-news", {"region": "cn"})
    if d:
        items = d if isinstance(d, list) else d.get("items", d.get("data", []))
        for item in (items[:8] if isinstance(items, list) else []):
            title = item.get("title") or item.get("name", "")
            link = item.get("url") or item.get("link", "")
            if title:
                articles.append({"title": title, "link": link, "source": "InfoQ"})

    # 3. 知乎热榜
    d = call_clawdchat_tool("trends-hub", "get-zhihu-trending", {"limit": 10})
    if d:
        items = d if isinstance(d, list) else d.get("items", d.get("data", []))
        for item in (items[:8] if isinstance(items, list) else []):
            title = item.get("title") or item.get("name") or item.get("question", {}).get("title", "")
            link = item.get("url") or item.get("link", "")
            if title:
                articles.append({"title": title, "link": link, "source": "知乎热榜"})

    # 4. Reddit r/LocalLLaMA 热帖
    d = call_clawdchat_tool("reddit", "get_subreddit_hot_posts",
                            {"subreddit_name": "LocalLLaMA", "limit": 8})
    if d:
        posts = d if isinstance(d, list) else d.get("posts", d.get("data", []))
        for p in (posts[:8] if isinstance(posts, list) else []):
            title = p.get("title", "")
            link = p.get("url") or p.get("permalink", "")
            if title:
                articles.append({"title": f"[r/LocalLLaMA] {title}", "link": link, "source": "Reddit"})

    # 5. Twitter @xuezhiqian123（中文财经AI视角）
    d = call_clawdchat_tool("twitter-scraper", "twitter_get_tweets",
                            {"username": "xuezhiqian123", "limit": 5})
    if d:
        tweets = d if isinstance(d, list) else d.get("tweets", d.get("data", []))
        for t in (tweets[:5] if isinstance(tweets, list) else []):
            text = t.get("text") or t.get("content", "")
            link = t.get("url") or t.get("link", "")
            if text and len(text) > 20:
                articles.append({"title": text[:100], "link": link, "source": "Twitter/@xuezhiqian123"})

    print(f"clawdchat tools: {len(articles)} 条")
    return articles


def fetch_rss(url, name):
    """抓取RSS，返回文章列表 [{title, link, pub_date}]"""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; RSS/1.0)",
        })
        resp = urllib.request.urlopen(req, timeout=15)
        content = resp.read().decode("utf-8", errors="replace")
        root = ET.fromstring(content)
        
        articles = []
        # RSS 2.0
        for item in root.findall(".//item"):
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            pub = item.findtext("pubDate", "").strip()
            if title and link:
                articles.append({"title": title, "link": link, "pub": pub, "source": name})
        
        # Atom
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            title = entry.findtext("atom:title", namespaces=ns, default="").strip()
            link_el = entry.find("atom:link", ns)
            link = link_el.get("href", "") if link_el is not None else ""
            pub = entry.findtext("atom:published", namespaces=ns, default="").strip()
            if title and link:
                articles.append({"title": title, "link": link, "pub": pub, "source": name})
        
        return articles[:20]
    except Exception as e:
        print(f"[WARN] {name} 抓取失败: {e}")
        return []


def get_openrouter_top_apps():
    """读取由 cron agent 预先抓取并存储的 OpenRouter top apps 数据"""
    cache_path = os.path.expanduser("~/.openclaw/workspace/data/openrouter-top-apps.json")
    try:
        if not os.path.exists(cache_path):
            print("[INFO] OpenRouter top apps: 缓存文件不存在，跳过")
            return []

        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        apps = data.get("apps", [])
        if not apps:
            return []

        articles = []
        for item in apps[:20]:
            rank = item.get("rank", "?")
            name = item.get("name", "")
            trend = item.get("trend", "")
            tokens = item.get("tokens", "")
            trend_str = f" {trend}" if trend else ""
            tokens_str = f"，{tokens}" if tokens else ""
            articles.append({
                "source": "OpenRouter TopApps",
                "title": f"#{rank} {name}{trend_str}{tokens_str} — OpenRouter App 榜单",
                "url": "https://openrouter.ai/apps",
                "published": data.get("fetched_at", datetime.now(timezone.utc).isoformat()),
            })
        print(f"OpenRouter top apps: {len(articles)} 条（来自缓存）")
        return articles
    except Exception as e:
        print(f"[WARN] OpenRouter top apps 读取失败: {e}")
        return []


def get_blogwatcher_articles():
    """从 blogwatcher 获取最新未读文章"""
    try:
        # 先 scan
        subprocess.run(["blogwatcher", "scan"], capture_output=True, timeout=60)
        # 获取文章（默认显示未读）
        result = subprocess.run(
            ["blogwatcher", "articles"],
            capture_output=True, text=True, timeout=10
        )
        articles = []
        current = {}
        for line in result.stdout.split("\n"):
            # 格式: "  [141] [new] 标题 — 来源网站"
            #        "       Blog: RadarAI"
            #        "       URL: https://..."
            stripped = line.strip()
            m = re.match(r'\[(\d+)\]\s+\[new\]\s+(.+)', stripped)
            if m:
                if current.get("title") and current.get("link"):
                    articles.append(current.copy())
                current = {"title": m.group(2).strip(), "id": m.group(1)}
            elif stripped.startswith("Blog:"):
                current["source"] = stripped[5:].strip()
            elif stripped.startswith("URL:"):
                current["link"] = stripped[4:].strip()
        if current.get("title") and current.get("link"):
            articles.append(current.copy())
        return articles[:60]
    except Exception as e:
        print(f"[WARN] blogwatcher 失败: {e}")
        return []


def llm_filter(articles):
    """用 LLM 从文章列表中选出对宝哥最有用的 ≤10 条，附一句话判断"""
    if not articles:
        return []

    titles_text = "\n".join(
        f"{i+1}. [{a['source']}] {a['title']}"
        for i, a in enumerate(articles[:60])
    )

    prompt = f"""你是我的信息助理。从以下文章标题中，筛选出对我最有价值的**不超过10条**，并附一句话说明价值。

我的关注方向（优先级从高到低）：
1. AI工具平台动态：X/Google/Meta/Anthropic/OpenAI等国际头部大厂进展；OpenClaw竞品更新/暴雷/停服；OpenRouter top apps榜单新入榜或排名大变动的App（重点关注有评测类内容的）
2. AI Agent 新进展、普通人用AI实现转型或变现的案例
3. 资本市场动荡：国内外AI大厂股价/融资/裁员/暴雷；腾讯系/阿里系/字节系港股美股最新动态；政策收紧或利好
4. 内容运营/流量变现：小红书/微信公众号新打法；腾讯广告投流操作；闲鱼/独立变现新机会

⚡ 特别标注：以下为 OpenClaw 直接竞品，任何相关新闻优先入选并在 reason 里注明「竞品」：
Hermes Agent、Cline、Roo Code、Agent Zero、Gobii

❌ 一律不选（过滤掉）：
- 纯技术/底层基础设施新闻（格式标准加入某基金会、库版本更新、学术论文）
- 不涉及市场影响的工程类公告

✅ 优先选（即使不在上述方向内）：
- 有商业影响的产品发布、用户规模数据、竞品动态
- 第三方机构/大厂（NVIDIA、IBM、Google等）在HuggingFace Blog发布的研究或产品内容

❌ 额外过滤（补充）：
- HuggingFace 官方发布的关于自身平台/生态的报告（如「State of Open Source on HF」「Liberate your OpenClaw」等HF自我宣传内容）
- 标题含「OpenClaw」但来源是 HuggingFace Blog 的条目——这是HF自家生态工具，不是竞品动态

其余不相关内容**一律不选**。

文章列表：
{titles_text}

请直接输出JSON数组（不要markdown代码块），格式：
[{{"index": 1, "reason": "一句话说明价值"}}, ...]
只输出你选的条目，按价值从高到低排序，最多10条。"""

    try:
        payload = json.dumps({
            "model": "mule-computer-default",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }).encode()

        req = urllib.request.Request(
            f"{API_HUB_BASE}/v1/messages",
            data=payload,
            headers={
                "x-api-key": API_HUB_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
                "User-Agent": "OpenClaw/1.0 (morning-brief)",
            },
            method="POST"
        )
        resp = urllib.request.urlopen(req, timeout=60)
        result = json.loads(resp.read())
        text = result["content"][0]["text"].strip()
        
        # 清理可能的markdown和控制字符
        text = re.sub(r"```json\s*|\s*```", "", text).strip()
        # 修复特殊字符导致的JSON解析问题
        text = re.sub(r'[\x00-\x1f\x7f]', ' ', text)
        selected = json.loads(text)
        
        output = []
        for item in selected:
            idx = item["index"] - 1
            if 0 <= idx < len(articles):
                a = articles[idx].copy()
                a["reason"] = item.get("reason", "")
                output.append(a)
        return output
    except Exception as e:
        print(f"[WARN] LLM 筛选失败: {e}")
        # 降级：直接返回前10条
        return articles[:10]


def send_telegram(text):
    """发送 Telegram 消息"""
    payload = json.dumps({
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    resp = urllib.request.urlopen(req, timeout=15)
    result = json.loads(resp.read())
    return result.get("ok", False)


def mark_all_read():
    """标记所有文章为已读"""
    try:
        subprocess.run(["blogwatcher", "read-all"], capture_output=True, timeout=10)
    except Exception:
        pass  # blogwatcher 未安装时静默跳过


def main():
    now = datetime.now(tz=timezone(timedelta(hours=8)))
    date_str = now.strftime("%Y-%m-%d %a")
    
    print(f"[{now.strftime('%H:%M:%S')}] 开始抓取...")
    
    # 收集文章
    all_articles = []
    
    # blogwatcher 信源
    bw_articles = get_blogwatcher_articles()
    all_articles.extend(bw_articles)
    print(f"blogwatcher: {len(bw_articles)} 篇")

    # 虾聊工具网关（trends-hub / twitter-scraper / reddit）
    cc_articles = get_clawdchat_articles()
    all_articles.extend(cc_articles)

    # OpenRouter top apps 榜单（仅作参考快照，不注入文章列表）
    get_openrouter_top_apps()  # 静默执行，仅更新缓存

    # 直接抓取信源
    for name, url in DIRECT_FEEDS:
        articles = fetch_rss(url, name)
        all_articles.extend(articles)
        print(f"{name}: {len(articles)} 篇")
    
    if not all_articles:
        send_telegram(f"⚡ *{date_str} 早报*\n\n今日无新内容，信源可能暂时不可达。")
        return
    
    print(f"总计 {len(all_articles)} 篇，送 LLM 筛选...")
    
    # LLM 筛选
    selected = llm_filter(all_articles)
    
    if not selected:
        send_telegram(f"⚡ *{date_str} 早报*\n\n今日无值得关注的内容。")
        mark_all_read()
        return
    
    # 组装消息
    lines = [f"⚡ *{date_str} 早报*\n"]
    for i, a in enumerate(selected, 1):
        title = a["title"].replace("*", "").replace("[", "").replace("]", "")
        link = a.get("link", "")
        reason = a.get("reason", "")
        source = a.get("source", "")
        lines.append(f"{i}. [{title}]({link})")
        if reason:
            lines.append(f"   _{reason}_ `{source}`")
    
    lines.append(f"\n_共 {len(selected)} 条 · {now.strftime('%H:%M')} 更新_")
    message = "\n".join(lines)
    
    # Telegram 单条消息最大4096字，超出则截断
    if len(message) > 4000:
        message = message[:3950] + "\n..._（内容已截断）_"
    
    ok = send_telegram(message)
    print(f"发送{'成功' if ok else '失败'}")
    
    # 标记已读
    mark_all_read()
    print("完成")


if __name__ == "__main__":
    main()
