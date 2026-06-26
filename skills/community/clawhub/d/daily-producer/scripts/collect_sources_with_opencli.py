#!/usr/bin/env python3
"""
使用 opencli 从 profile.yaml 配置的信息源采集资讯候选池。

读取 profile.yaml 中的 topics（cn/en 关键词）和 sources（platforms + websites），
自动生成并执行 opencli 命令，将结果保存到 output/raw/{date}_index.txt。

用法：
    python3 scripts/collect_sources_with_opencli.py --date 2026-04-04
    python3 scripts/collect_sources_with_opencli.py --date 2026-04-04 --dry-run
    python3 scripts/collect_sources_with_opencli.py --date 2026-04-04 --platform weibo,twitter
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# 每次 opencli 请求之间的间隔秒数（避免平台限流）
REQUEST_DELAY = 3

# 需要代理的平台及代理地址
PROXY_CONFIG = {
    "reddit": "http://xb:xb20260330@123.58.210.235:62520",
}


# ━━ 工具函数 ━━

def resolve_root_dir() -> Path:
    env_root = os.environ.get("DAILY_ROOT") or os.environ.get("AI_DAILY_ROOT")
    candidates = []
    if env_root:
        candidates.append(Path(env_root).expanduser())
    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])
    script_dir = Path(__file__).resolve().parent
    candidates.extend([script_dir, *script_dir.parents])
    seen: set[Path] = set()
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        if (c / "SKILL.md").exists() and (c / "config").is_dir():
            return c
    return script_dir.parent


def load_profile(root: Path) -> dict:
    config_path = root / "config" / "profile.yaml"
    if not config_path.exists():
        print(f"ERROR: {config_path} 不存在", file=sys.stderr)
        sys.exit(1)
    try:
        import yaml
        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        print("ERROR: 需要 pyyaml (pip install pyyaml)", file=sys.stderr)
        sys.exit(1)


def _is_cn(text: str) -> bool:
    return any("\u4e00" <= c <= "\u9fff" for c in text)


def get_keywords(profile: dict, max_total: int = 15) -> tuple[list[str], list[str]]:
    """
    从 profile 的 topics 中提取去重后的 cn/en 关键词列表。
    按优先级分配名额，总数控制在 max_total 以内（cn 和 en 各 max_total 个）。

    分配逻辑：
    - 先按 priority 分组，统计各组 topic 数量
    - high: 每个 topic 分 floor(max_total * 0.8 / high_count) 个
    - medium: 每个 topic 分 floor(max_total * 0.2 / medium_count) 个
    - low: 每个 topic 1 个
    - 剩余名额按 high → medium 顺序补足
    """
    topics = profile.get("topics", [])
    priority_order = {"high": 0, "medium": 1, "low": 2}
    topics_sorted = sorted(
        topics, key=lambda t: priority_order.get(t.get("priority", "medium"), 1)
    )

    # 统计各优先级 topic 数量
    high_topics = [t for t in topics_sorted if t.get("priority") == "high"]
    medium_topics = [t for t in topics_sorted if t.get("priority") == "medium"]
    low_topics = [t for t in topics_sorted if t.get("priority") == "low"]

    # 分配每个 topic 的关键词名额
    per_high = max(1, int(max_total * 0.8 / max(len(high_topics), 1)))
    per_medium = max(1, int(max_total * 0.2 / max(len(medium_topics), 1))) if medium_topics else 0
    per_low = 1

    cn_all, en_all = [], []
    seen_cn, seen_en = set(), set()

    def _add_from_topic(topic, limit):
        kws = topic.get("keywords", {})
        if isinstance(kws, dict):
            cn_list = kws.get("cn", []) or []
            en_list = kws.get("en", []) or []
        else:
            cn_list = [k for k in (kws or []) if _is_cn(k)]
            en_list = [k for k in (kws or []) if not _is_cn(k)]

        added_cn, added_en = 0, 0
        for kw in cn_list:
            if added_cn >= limit:
                break
            if kw not in seen_cn:
                seen_cn.add(kw)
                cn_all.append(kw)
                added_cn += 1
        for kw in en_list:
            if added_en >= limit:
                break
            if kw not in seen_en:
                seen_en.add(kw)
                en_all.append(kw)
                added_en += 1

    for t in high_topics:
        _add_from_topic(t, per_high)
    for t in medium_topics:
        _add_from_topic(t, per_medium)
    for t in low_topics:
        _add_from_topic(t, per_low)

    # 如果还没到 max_total，从 high topics 补足
    if len(cn_all) < max_total:
        for t in high_topics:
            kws = t.get("keywords", {})
            cn_list = kws.get("cn", []) if isinstance(kws, dict) else [k for k in (kws or []) if _is_cn(k)]
            for kw in cn_list:
                if len(cn_all) >= max_total:
                    break
                if kw not in seen_cn:
                    seen_cn.add(kw)
                    cn_all.append(kw)
    if len(en_all) < max_total:
        for t in high_topics:
            kws = t.get("keywords", {})
            en_list = kws.get("en", []) if isinstance(kws, dict) else [k for k in (kws or []) if not _is_cn(k)]
            for kw in en_list:
                if len(en_all) >= max_total:
                    break
                if kw not in seen_en:
                    seen_en.add(kw)
                    en_all.append(kw)

    return cn_all[:max_total], en_all[:max_total]


# ━━ Reddit 直接 API（不走 opencli，走代理）━━

def reddit_search(keyword: str, sort: str = "relevance", time_filter: str = "week", limit: int = 15) -> dict:
    """通过 Reddit JSON API + 代理���索。"""
    import urllib.request
    import urllib.parse

    proxy_url = PROXY_CONFIG.get("reddit", "")
    if not proxy_url:
        return {"success": False, "error": "no proxy configured for reddit", "data": []}

    query = urllib.parse.urlencode({"q": keyword, "sort": sort, "t": time_filter, "limit": limit})
    url = f"https://www.reddit.com/search.json?{query}"

    try:
        proxy_handler = urllib.request.ProxyHandler({"https": proxy_url, "http": proxy_url})
        opener = urllib.request.build_opener(proxy_handler)
        req = urllib.request.Request(url, headers={"User-Agent": "daily-producer/1.0"})
        with opener.open(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())

        items = []
        for post in data.get("data", {}).get("children", []):
            d = post.get("data", {})
            items.append({
                "title": d.get("title", ""),
                "subreddit": d.get("subreddit", ""),
                "author": d.get("author", ""),
                "score": d.get("score", 0),
                "comments": d.get("num_comments", 0),
                "url": f"https://reddit.com{d.get('permalink', '')}",
                "created_utc": d.get("created_utc", 0),
            })

        return {
            "success": True,
            "command": f"reddit search (API+proxy) q={keyword}",
            "data": items,
            "count": len(items),
        }
    except Exception as e:
        return {"success": False, "command": f"reddit search q={keyword}", "error": str(e), "data": []}


def reddit_hot(subreddit: str = "", limit: int = 20) -> dict:
    """通过 Reddit JSON API + 代理获取热门。"""
    import urllib.request

    proxy_url = PROXY_CONFIG.get("reddit", "")
    if not proxy_url:
        return {"success": False, "error": "no proxy configured for reddit", "data": []}

    sub_path = f"r/{subreddit}" if subreddit else "r/all"
    url = f"https://www.reddit.com/{sub_path}/hot.json?limit={limit}"

    try:
        proxy_handler = urllib.request.ProxyHandler({"https": proxy_url, "http": proxy_url})
        opener = urllib.request.build_opener(proxy_handler)
        req = urllib.request.Request(url, headers={"User-Agent": "daily-producer/1.0"})
        with opener.open(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())

        items = []
        for post in data.get("data", {}).get("children", []):
            d = post.get("data", {})
            items.append({
                "title": d.get("title", ""),
                "subreddit": d.get("subreddit", ""),
                "author": d.get("author", ""),
                "score": d.get("score", 0),
                "comments": d.get("num_comments", 0),
                "url": f"https://reddit.com{d.get('permalink', '')}",
                "created_utc": d.get("created_utc", 0),
            })

        return {
            "success": True,
            "command": f"reddit hot (API+proxy) {sub_path}",
            "data": items,
            "count": len(items),
        }
    except Exception as e:
        return {"success": False, "command": f"reddit hot {sub_path}", "error": str(e), "data": []}


# ━━ opencli 执行 ━━

def run_opencli(cmd: str, timeout: int = 30, platform: str = "") -> dict:
    """
    执行 opencli 命令，返回结构化结果。
    cmd 示例: 'weibo hot --limit 30 -f json'
    platform: 平台 opencli 前缀（如 'reddit'），用于判断是否需要代理
    """
    full_cmd = f"opencli {cmd}"
    env = os.environ.copy()
    env["DISPLAY"] = env.get("DISPLAY", ":99")

    # 检查是否需要代理
    proxy_platform = platform or cmd.split()[0] if cmd else ""
    proxy_url = PROXY_CONFIG.get(proxy_platform, "")
    if proxy_url:
        env["HTTP_PROXY"] = proxy_url
        env["HTTPS_PROXY"] = proxy_url
        env["http_proxy"] = proxy_url
        env["https_proxy"] = proxy_url

    try:
        result = subprocess.run(
            full_cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, env=env
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if result.returncode != 0:
            return {
                "success": False,
                "command": full_cmd,
                "error": stderr or stdout,
                "data": []
            }

        # 尝试解析 JSON
        try:
            data = json.loads(stdout)
            if isinstance(data, list):
                return {"success": True, "command": full_cmd, "data": data, "count": len(data)}
            else:
                return {"success": True, "command": full_cmd, "data": [data], "count": 1}
        except json.JSONDecodeError:
            # 非 JSON 输出，按文本返回
            return {"success": True, "command": full_cmd, "data": [], "raw_text": stdout}

    except subprocess.TimeoutExpired:
        return {"success": False, "command": full_cmd, "error": "timeout", "data": []}
    except Exception as e:
        return {"success": False, "command": full_cmd, "error": str(e), "data": []}


def check_opencli() -> bool:
    """检查 opencli 是否可用。"""
    result = run_opencli("doctor", timeout=15)
    if result["success"] and "raw_text" in result:
        return "[OK] Connectivity" in result["raw_text"]
    return False


# ━━ 采集逻辑 ━━

def collect_platform(platform: dict, keywords: list[str], region: str) -> list[dict]:
    """
    对单个平台执行采集。
    platform: profile 中 sources.platforms.cn/global 下的一个平台配置
    keywords: 该平台对应的关键词列表（cn 平台用 cn 词，global 用 en 词）
    region: "cn" 或 "global"
    """
    name = platform.get("name", "")
    opencli_prefix = platform.get("opencli", "")
    commands = platform.get("commands", [])
    results = []

    if not opencli_prefix or not commands:
        return results

    # Reddit：先试 opencli，不通则走 API + 代理
    if opencli_prefix == "reddit":
        # 快速探测 opencli reddit 是否可用
        print(f"  [{name}] 检测 opencli reddit 可用性...", file=sys.stderr)
        probe = run_opencli("reddit hot --limit 1 -f json", platform="reddit")
        use_api = not probe.get("success") or not probe.get("data")

        if use_api:
            print(f"  [{name}] opencli reddit 不可用，切换到 API+代理", file=sys.stderr)
            for cmd_template in commands:
                if "{keyword}" in cmd_template:
                    for kw in keywords:
                        print(f"  [{name}] reddit search (API+proxy) q={kw}", file=sys.stderr)
                        res = reddit_search(kw)
                        res["platform"] = name
                        res["region"] = region
                        res["keyword"] = kw
                        res["fetch_stack"] = "reddit-api-proxy"
                        results.append(res)
                        time.sleep(REQUEST_DELAY)
                elif "hot" in cmd_template:
                    print(f"  [{name}] reddit hot (API+proxy)", file=sys.stderr)
                    res = reddit_hot()
                    res["platform"] = name
                    res["region"] = region
                    res["keyword"] = None
                    res["fetch_stack"] = "reddit-api-proxy"
                    results.append(res)
                    time.sleep(REQUEST_DELAY)
            return results
        else:
            print(f"  [{name}] opencli reddit 可用，走 opencli", file=sys.stderr)
            # 继续走下面的通用 opencli 流程

    for cmd_template in commands:
        if "{keyword}" in cmd_template:
            # 关键词搜索：逐个关键词执行
            for kw in keywords:
                cmd = f'{opencli_prefix} {cmd_template.replace("{keyword}", kw)} -f json'
                print(f"  [{name}] {cmd}", file=sys.stderr)
                res = run_opencli(cmd, platform=opencli_prefix)
                res["platform"] = name
                res["region"] = region
                res["keyword"] = kw
                results.append(res)
                time.sleep(REQUEST_DELAY)
        else:
            # 热搜/热门等不需要关键词的命令
            cmd = f"{opencli_prefix} {cmd_template} -f json"
            print(f"  [{name}] {cmd}", file=sys.stderr)
            res = run_opencli(cmd, platform=opencli_prefix)
            res["platform"] = name
            res["region"] = region
            res["keyword"] = None
            results.append(res)
            time.sleep(REQUEST_DELAY)

    return results


def collect_website(site: dict, keywords: list[str], start_iso: str) -> list[dict]:
    """
    对单个媒体/官网执行采集。
    用 google search "site:域名 关键词 after:日期" + web read 首页。
    """
    name = site.get("name", "")
    url = site.get("url", "")
    results = []

    if not url:
        return results

    # 提取域名
    domain = url.replace("https://", "").replace("http://", "").split("/")[0]
    if domain.startswith("www."):
        domain = domain[4:]

    # 1) web read 首页
    cmd = f'web read --url "{url}"'
    print(f"  [{name}] opencli {cmd}", file=sys.stderr)
    res = run_opencli(cmd, timeout=30)
    res["platform"] = name
    res["region"] = "website"
    res["keyword"] = None
    results.append(res)
    time.sleep(REQUEST_DELAY)

    # 2) google site: 搜索（取前 3 个关键词）
    for kw in keywords[:3]:
        cmd = f'google search "site:{domain} {kw} after:{start_iso}" -f json'
        print(f"  [{name}] opencli {cmd}", file=sys.stderr)
        res = run_opencli(cmd, timeout=30)
        res["platform"] = name
        res["region"] = "website"
        res["keyword"] = kw
        results.append(res)
        time.sleep(REQUEST_DELAY)

    return results


# ━━ 结果格式化 ━━

def format_raw_output(all_results: list[dict], date_str: str, max_results: int = 0) -> str:
    """将采集结果格式化为 raw index 文本。max_results: 每次搜索最多输出的条目数，0=不限。"""
    lines = [
        f"# 日报候选池采集结果 — {date_str}",
        f"# 采集时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"# 总命令数: {len(all_results)}",
        f"# 成功: {sum(1 for r in all_results if r.get('success'))}",
        f"# 失败: {sum(1 for r in all_results if not r.get('success'))}",
        "",
    ]

    # 统计（按截断后的实际输出数量）
    total_items = 0
    for res in all_results:
        data = res.get("data", [])
        if max_results > 0:
            data = data[:max_results]
        total_items += len(data)
    lines.append(f"# 总候选条目: {total_items}")
    lines.append("")
    lines.append("=" * 70)
    lines.append("")

    for res in all_results:
        platform = res.get("platform", "unknown")
        region = res.get("region", "")
        keyword = res.get("keyword", "")
        command = res.get("command", "")
        success = res.get("success", False)

        lines.append(f"--- [{platform}] ({region}) ---")
        lines.append(f"command: {command}")
        lines.append(f"keyword: {keyword or '(none)'}")
        lines.append(f"status: {'success' if success else 'FAILED'}")
        lines.append(f"fetch_stack: opencli")

        if not success:
            lines.append(f"error: {res.get('error', 'unknown')}")
            lines.append("")
            continue

        data = res.get("data", [])
        if max_results > 0:
            data = data[:max_results]
        lines.append(f"count: {len(data)}")
        lines.append("")

        for i, item in enumerate(data):
            if isinstance(item, dict):
                # 提取常见字段
                title = (item.get("title") or item.get("word") or item.get("name", ""))
                text = item.get("text", "")
                url = item.get("url", "")
                author = (item.get("author") or item.get("channel", ""))
                subreddit = item.get("subreddit", "")

                # 时间字段：各平台名称不同，全部尝试
                time_field = (
                    item.get("created_at") or       # Twitter
                    item.get("time") or             # 微博
                    item.get("published_at") or     # 小红书
                    item.get("published") or        # YouTube / arXiv
                    item.get("date") or             # 36氪 / Google news / Product Hunt
                    item.get("pub_date") or         # RSS
                    ""
                )
                # Reddit API 的 created_utc (Unix 时间戳)
                created_utc = item.get("created_utc")
                if not time_field and created_utc:
                    try:
                        time_field = datetime.utcfromtimestamp(float(created_utc)).strftime("%Y-%m-%d %H:%M")
                    except (ValueError, TypeError, OSError):
                        time_field = str(created_utc)

                # 热度信号：取第一个非空的
                hot = (
                    item.get("hot_value") or        # 微博热搜
                    item.get("likes") or            # Twitter / 小红书
                    item.get("views") or            # Twitter / YouTube
                    item.get("score") or            # B站 / Reddit / HN
                    item.get("play") or             # B站
                    item.get("heat") or             # 知乎
                    item.get("votes") or            # 知乎 search
                    item.get("comments") or         # Reddit / HN
                    item.get("danmaku") or          # B站
                    item.get("replies") or          # V2EX
                    item.get("traffic") or          # Google trends
                    ""
                )

                # 额外字段
                duration = item.get("duration", "")     # YouTube
                tagline = item.get("tagline", "")       # Product Hunt
                snippet = item.get("snippet", "")       # Google search
                summary = item.get("summary", "")       # 36氪

                # 有 title 就用 title，没有就用 text（如 Twitter 推文）
                display = title or text
                lines.append(f"  [{i+1}] {display}")
                # 如果 title 和 text 都有且不同，text 作为正文单独输出
                if title and text and title != text:
                    lines.append(f"      text: {text}")
                if tagline:
                    lines.append(f"      tagline: {tagline}")
                if snippet:
                    lines.append(f"      snippet: {snippet}")
                if summary:
                    lines.append(f"      summary: {summary}")
                if author:
                    lines.append(f"      author: {author}")
                if subreddit:
                    lines.append(f"      subreddit: r/{subreddit}")
                if time_field:
                    lines.append(f"      time: {time_field}")
                if duration:
                    lines.append(f"      duration: {duration}")
                if hot:
                    lines.append(f"      hot: {hot}")
                if url:
                    lines.append(f"      url: {url}")
                lines.append("")
            else:
                lines.append(f"  [{i+1}] {str(item)[:200]}")
                lines.append("")

        # raw_text（非 JSON 输出）
        raw_text = res.get("raw_text", "")
        if raw_text and not data:
            # 截取前 500 字符
            lines.append(f"  raw_text: {raw_text[:500]}")
            lines.append("")

        lines.append("")

    return "\n".join(lines)


# ━━ 主流程 ━━

def main() -> None:
    parser = argparse.ArgumentParser(description="使用 opencli 采集资讯候选池")
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="目标日期 (默认今天)",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=3,
        help="时间窗口天数 (默认 3)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只输出要执行的命令，不实际执行",
    )
    parser.add_argument(
        "--platform",
        default="",
        help="只采集指定平台 (逗号分隔, 如 weibo,twitter)",
    )
    parser.add_argument(
        "--skip-websites",
        action="store_true",
        help="跳过媒体/官网采集",
    )
    parser.add_argument(
        "--max-keywords",
        type=int,
        default=15,
        help="每个平台最多搜索的关键词数 (默认 15)",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=0,
        help="每次搜索最多保留的结果数, 0=不限 (默认 0, 使用平台默认 limit)",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="不保存结果到文件",
    )
    args = parser.parse_args()

    root = resolve_root_dir()
    profile = load_profile(root)

    # 计算时间范围
    end = datetime.strptime(args.date, "%Y-%m-%d")
    start = end - timedelta(days=args.window - 1)
    start_iso = start.strftime("%Y-%m-%d")

    # 提取关键词
    cn_keywords, en_keywords = get_keywords(profile, max_total=args.max_keywords)
    print(f"关键词: cn={len(cn_keywords)} 个, en={len(en_keywords)} 个", file=sys.stderr)

    # 过滤平台
    filter_platforms = set()
    if args.platform:
        filter_platforms = set(args.platform.split(","))

    sources = profile.get("sources", {})

    # ━━ 1. 检查 opencli ━━
    if not args.dry_run:
        print("\n[检查] opencli doctor...", file=sys.stderr)
        if not check_opencli():
            print("ERROR: opencli 不可用，请检查 Chrome 和 Browser Bridge", file=sys.stderr)
            sys.exit(1)
        print("[检查] opencli 连接正常\n", file=sys.stderr)

    # ━━ 2. 生成采集任务 ━━
    tasks = []

    # 国内平台 + cn 关键词
    for platform in sources.get("platforms", {}).get("cn", []):
        if filter_platforms and platform.get("opencli") not in filter_platforms:
            continue
        tasks.append(("platform", platform, cn_keywords, "cn"))

    # 国外平台 + en 关键词
    for platform in sources.get("platforms", {}).get("global", []):
        if filter_platforms and platform.get("opencli") not in filter_platforms:
            continue
        tasks.append(("platform", platform, en_keywords, "global"))

    # 媒体/官网
    if not args.skip_websites:
        for site in sources.get("websites", {}).get("cn", []):
            tasks.append(("website", site, cn_keywords, "cn"))
        for site in sources.get("websites", {}).get("global", []):
            tasks.append(("website", site, en_keywords, "global"))

    # ━━ 3. dry-run 模式 ━━
    if args.dry_run:
        print(f"\n# 采集任务预览 — {args.date}（窗口 {args.window} 天）")
        print(f"# 平台: {len([t for t in tasks if t[0]=='platform'])} 个")
        print(f"# 网站: {len([t for t in tasks if t[0]=='website'])} 个\n")

        for task_type, source, keywords, region in tasks:
            name = source.get("name", "")
            if task_type == "platform":
                opencli_prefix = source.get("opencli", "")
                for cmd_template in source.get("commands", []):
                    if "{keyword}" in cmd_template:
                        for kw in keywords[:3]:
                            cmd = cmd_template.replace("{keyword}", kw)
                            print(f"opencli {opencli_prefix} {cmd} -f json")
                        print(f"  ... 共 {len(keywords)} 个关键词")
                    else:
                        print(f"opencli {opencli_prefix} {cmd_template} -f json")
            else:
                url = source.get("url", "")
                domain = url.replace("https://", "").replace("http://", "").split("/")[0]
                if domain.startswith("www."):
                    domain = domain[4:]
                print(f"opencli web read --url \"{url}\"")
                for kw in keywords[:3]:
                    print(f"opencli google search \"site:{domain} {kw} after:{start_iso}\" -f json")
            print()
        return

    # ━━ 4. 执行采集 ━━
    all_results = []

    for task_type, source, keywords, region in tasks:
        name = source.get("name", "")
        print(f"\n{'='*50}", file=sys.stderr)
        print(f"采集: {name} ({region})", file=sys.stderr)
        print(f"{'='*50}", file=sys.stderr)

        if task_type == "platform":
            results = collect_platform(source, keywords, region)
        else:
            results = collect_website(source, keywords, start_iso)

        all_results.extend(results)

        # 实时统计
        ok = sum(1 for r in results if r.get("success"))
        items = sum(len(r.get("data", [])) for r in results)
        print(f"  => {ok}/{len(results)} 成功, {items} 条结果", file=sys.stderr)

    # ━━ 5. 保存结果 ━━
    raw_text = format_raw_output(all_results, args.date, max_results=args.max_results)
    print(raw_text)

    if not args.no_save:
        raw_dir = root / "output" / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        save_path = raw_dir / f"{args.date}_index.txt"
        save_path.write_text(raw_text, encoding="utf-8")
        print(f"\n# 已保存到 {save_path}", file=sys.stderr)

    # ━━ 6. 输出摘要 ━━
    total_ok = sum(1 for r in all_results if r.get("success"))
    total_items = sum(len(r.get("data", [])) for r in all_results)
    total_fail = len(all_results) - total_ok

    print(f"\n{'='*50}", file=sys.stderr)
    print(f"采集完成", file=sys.stderr)
    print(f"  总命令: {len(all_results)}", file=sys.stderr)
    print(f"  成功: {total_ok}", file=sys.stderr)
    print(f"  失败: {total_fail}", file=sys.stderr)
    print(f"  总候选: {total_items} 条", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)

    # 按平台统计
    platform_stats: dict[str, dict] = {}
    for r in all_results:
        pname = r.get("platform", "unknown")
        if pname not in platform_stats:
            platform_stats[pname] = {"ok": 0, "fail": 0, "items": 0}
        if r.get("success"):
            platform_stats[pname]["ok"] += 1
        else:
            platform_stats[pname]["fail"] += 1
        platform_stats[pname]["items"] += len(r.get("data", []))

    print(f"\n  按平台:", file=sys.stderr)
    for pname, stats in platform_stats.items():
        status = "✅" if stats["fail"] == 0 else "⚠️"
        print(f"    {status} {pname}: {stats['items']} 条 ({stats['ok']} 成功, {stats['fail']} 失败)", file=sys.stderr)


if __name__ == "__main__":
    main()
