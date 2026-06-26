#!/usr/bin/env python3
"""
🎯 Competitor Radar — 竞品动态雷达
用法:
  python3 radar.py                    # 扫描过去7天（使用默认 config.yaml）
  python3 radar.py --days 14          # 扫描过去14天
  python3 radar.py --output report.md # 保存报告
  python3 radar.py --config my.yaml   # 自定义配置文件
"""
import sys, os, re, json, argparse, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

SKILL_DIR = Path(__file__).parent

# ── LLM ──────────────────────────────────────────────────────────────────────

def llm_call(prompt: str, max_tokens: int = 600) -> str:
    url = "http://127.0.0.1:18790/anthropic/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "sk-RPBUoe2SH7KigJ0SZn6IPDirZtJ2fUaWSukEx1FwxjhWFx0G",
        "anthropic-version": "2023-06-01",
    }
    data = json.dumps({
        "model": "ppio/pa/claude-sonnet-4-6",
        "max_tokens": max_tokens,
        "system": "你是一个竞品分析助理，用简洁中文回答，不要废话。",
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["content"][0]["text"]


# ── YAML 解析（极简，不依赖 pyyaml）────────────────────────────────────────

def parse_simple_yaml(text: str) -> dict:
    """极简 YAML 解析，支持本配置文件的格式"""
    result = {"competitors": []}
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "competitors:":
            continue
        if stripped.startswith("- name:"):
            if current:
                result["competitors"].append(current)
            current = {"name": stripped.split(":", 1)[1].strip().strip('"')}
        elif current and ":" in stripped:
            k, v = stripped.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"')
            if k == "keywords":
                continue  # 跳过，下面单独处理
            current[k] = v
        elif current and stripped.startswith("- ") and "keywords" not in stripped:
            pass  # keyword list items — handled below
    if current:
        result["competitors"].append(current)
    # 重新解析 keywords
    comp_idx = -1
    in_kw = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- name:"):
            comp_idx += 1
            in_kw = False
            if "keywords" not in result["competitors"][comp_idx]:
                result["competitors"][comp_idx]["keywords"] = []
        elif stripped == "keywords:":
            in_kw = True
        elif in_kw and stripped.startswith("- ") and comp_idx >= 0:
            kw = stripped[2:].strip().strip('"')
            result["competitors"][comp_idx].setdefault("keywords", []).append(kw)
        elif ":" in stripped and not stripped.startswith("- "):
            in_kw = False
    return result


# ── 数据源抓取 ────────────────────────────────────────────────────────────────

def fetch_url(url: str, timeout: int = 8) -> str | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 CompetitorRadar/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def parse_rss(xml_text: str, since: datetime) -> list:
    items = []
    try:
        root = ET.fromstring(xml_text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        # RSS 2.0
        for item in root.findall(".//item"):
            title_el = item.find("title")
            link_el  = item.find("link")
            date_el  = item.find("pubDate")
            title = title_el.text if title_el is not None else ""
            link  = link_el.text  if link_el  is not None else ""
            pub   = date_el.text  if date_el  is not None else ""
            items.append({"title": title, "link": link, "date": pub, "source": "blog_rss"})
        # Atom
        for entry in root.findall(".//atom:entry", ns):
            title_el = entry.find("atom:title", ns)
            link_el  = entry.find("atom:link", ns)
            date_el  = entry.find("atom:updated", ns)
            title = title_el.text if title_el is not None else ""
            link  = link_el.get("href", "") if link_el is not None else ""
            pub   = date_el.text if date_el is not None else ""
            items.append({"title": title, "link": link, "date": pub, "source": "blog_rss"})
    except Exception:
        pass
    return items[:10]  # 最多10条


def fetch_github_releases(org: str, since: datetime) -> list:
    url = f"https://api.github.com/orgs/{org}/repos?per_page=10&sort=pushed"
    text = fetch_url(url)
    if not text:
        return []
    items = []
    try:
        repos = json.loads(text)
        for repo in repos[:5]:
            rname = repo.get("name", "")
            rel_url = f"https://api.github.com/repos/{org}/{rname}/releases?per_page=3"
            rel_text = fetch_url(rel_url)
            if rel_text:
                releases = json.loads(rel_text)
                for r in releases:
                    items.append({
                        "title": f"[{rname}] {r.get('name') or r.get('tag_name', '')}",
                        "link":  r.get("html_url", ""),
                        "date":  r.get("published_at", ""),
                        "source": "github_release",
                    })
    except Exception:
        pass
    return items[:8]


def fetch_hn_mentions(keywords: list) -> list:
    items = []
    for kw in keywords[:2]:
        url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(kw)}&tags=story&hitsPerPage=5"
        text = fetch_url(url)
        if text:
            try:
                data = json.loads(text)
                for hit in data.get("hits", []):
                    items.append({
                        "title":  hit.get("title", ""),
                        "link":   hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                        "date":   hit.get("created_at", ""),
                        "source": "hackernews",
                    })
            except Exception:
                pass
    return items[:6]


import urllib.parse


# ── AI 评分 ───────────────────────────────────────────────────────────────────

def score_items(comp_name: str, items: list) -> list:
    if not items:
        return []
    titles_text = "\n".join([f"{i+1}. [{it['source']}] {it['title']}" for i, it in enumerate(items)])
    prompt = f"""以下是关于 {comp_name} 的最新动态，请给每条打分（1-5分，5=非常重要的产品/战略动态，1=无关紧要）。
只返回 JSON 数组，格式: [{{"idx":1,"score":4,"reason":"一句话理由"}}]

{titles_text}"""
    try:
        resp = llm_call(prompt, max_tokens=400)
        # 提取 JSON
        m = re.search(r'\[.*\]', resp, re.DOTALL)
        if m:
            scores = json.loads(m.group(0))
            score_map = {s["idx"]: s for s in scores}
            for i, it in enumerate(items):
                s = score_map.get(i+1, {})
                it["score"] = s.get("score", 3)
                it["reason"] = s.get("reason", "")
    except Exception:
        for it in items:
            it.setdefault("score", 3)
            it.setdefault("reason", "")
    return items


# ── 报告生成 ──────────────────────────────────────────────────────────────────

def build_report(results: dict, days: int) -> str:
    now = datetime.now(timezone(timedelta(hours=8)))
    lines = [
        f"# 🎯 竞品雷达报告 {now.strftime('%Y-%m-%d')}",
        f"",
        f"## 摘要",
    ]
    total = sum(len(v) for v in results.values())
    important = sum(1 for items in results.values() for it in items if it.get("score", 0) >= 4)
    lines.append(f"过去 **{days} 天**监控了 **{len(results)} 个竞品**，共收集 **{total} 条动态**，其中重要动态 **{important} 条**。")
    lines.append("")
    lines.append("---")

    for comp_name, items in results.items():
        lines.append(f"\n## {comp_name}\n")
        high   = [it for it in items if it.get("score", 0) >= 4]
        mid    = [it for it in items if it.get("score", 0) == 3]
        low    = [it for it in items if it.get("score", 0) <= 2]

        if high:
            lines.append("### 🔴 重要动态")
            for it in high:
                title = it["title"] or "(无标题)"
                link  = it["link"]
                src   = it["source"]
                reason = it.get("reason", "")
                if link:
                    lines.append(f"- **[{title}]({link})** — 来源: {src}")
                else:
                    lines.append(f"- **{title}** — 来源: {src}")
                if reason:
                    lines.append(f"  > {reason}")
        if mid:
            lines.append("\n### 🟡 值得关注")
            for it in mid:
                title = it["title"] or "(无标题)"
                link  = it["link"]
                src   = it["source"]
                if link:
                    lines.append(f"- [{title}]({link}) · {src}")
                else:
                    lines.append(f"- {title} · {src}")
        if low:
            lines.append("\n### ⚪ 一般")
            for it in low:
                title = it["title"] or "(无标题)"
                lines.append(f"- {title}")
        if not items:
            lines.append("_本周期内暂无数据（可能网络受限）_")

    lines.append(f"\n---\n*生成时间：{now.strftime('%Y-%m-%d %H:%M')} GMT+8 | 数据周期：最近 {days} 天*")
    return "\n".join(lines)


# ── 主程序 ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="🎯 Competitor Radar — 竞品动态雷达")
    parser.add_argument("--days",   type=int, default=7,  help="监控天数（默认7）")
    parser.add_argument("--output", default="",           help="输出报告路径")
    parser.add_argument("--config", default=str(SKILL_DIR / "config.yaml"), help="配置文件路径")
    parser.add_argument("--no-ai",  action="store_true",  help="跳过 AI 评分（更快）")
    args = parser.parse_args()

    # 读取配置
    config_text = Path(args.config).read_text()
    config = parse_simple_yaml(config_text)
    competitors = config.get("competitors", [])
    since = datetime.now(timezone.utc) - timedelta(days=args.days)

    print(f"🎯 竞品雷达启动，监控 {len(competitors)} 个竞品，过去 {args.days} 天...")

    results = {}
    for comp in competitors:
        name = comp.get("name", "Unknown")
        print(f"  📡 正在抓取 {name} ...", end="", flush=True)
        items = []

        # RSS
        if comp.get("blog_rss"):
            text = fetch_url(comp["blog_rss"])
            if text:
                items.extend(parse_rss(text, since))

        # GitHub releases
        if comp.get("github_org"):
            items.extend(fetch_github_releases(comp["github_org"], since))

        # HackerNews
        if comp.get("keywords"):
            items.extend(fetch_hn_mentions(comp["keywords"]))

        # 去重（按标题）
        seen, unique = set(), []
        for it in items:
            key = it.get("title", "")[:60]
            if key not in seen and key:
                seen.add(key)
                unique.append(it)

        # AI 评分
        if not args.no_ai and unique:
            unique = score_items(name, unique)
        else:
            for it in unique:
                it.setdefault("score", 3)
                it.setdefault("reason", "")

        unique.sort(key=lambda x: x.get("score", 0), reverse=True)
        results[name] = unique
        print(f" {len(unique)} 条")

    report = build_report(results, args.days)

    if args.output:
        Path(args.output).write_text(report)
        print(f"\n✅ 报告已保存：{args.output}")
    else:
        print("\n" + "="*60)
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
