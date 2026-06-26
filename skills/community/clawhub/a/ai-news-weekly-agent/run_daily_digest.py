#!/usr/bin/env python3
import argparse
import datetime as dt
import html
import json
import os
import pathlib
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import timedelta
from email.utils import parsedate_to_datetime


DEFAULT_SOURCES_FILE = "sources.json"
DEFAULT_OUTPUT_DIR = "daily_docs"
USER_AGENT = "ai-digest-agent/0.1 (+local-script)"
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
OPENCLAW_LEADERBOARD_URL = "https://topclawhubskills.com/"
DEFAULT_ALLOWED_LLM_HOSTS = {
    "ark.cn-beijing.volces.com",
    "api.openai.com",
    "openrouter.ai",
}
ALLOWED_WEBHOOK_SUFFIXES = (
    ".feishu.cn",
    ".larksuite.com",
    ".dingtalk.com",
)


def now_local() -> dt.datetime:
    return dt.datetime.now().astimezone()


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_dotenv(path: pathlib.Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def fetch_text(url: str, timeout: int = 15, allow_insecure_fallback: bool = False) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    def _read_with_context(context: ssl.SSLContext) -> str:
        with urllib.request.urlopen(req, timeout=timeout, context=context) as resp:
            return resp.read().decode("utf-8", errors="ignore")

    try:
        return _read_with_context(ssl.create_default_context())
    except ssl.SSLCertVerificationError:
        if not allow_insecure_fallback:
            raise
        return _read_with_context(ssl._create_unverified_context())
    except urllib.error.URLError as ex:
        if not allow_insecure_fallback:
            raise
        if isinstance(ex.reason, ssl.SSLCertVerificationError):
            return _read_with_context(ssl._create_unverified_context())
        raise


def parse_human_number(text: str) -> float:
    value = (text or "").strip().upper().replace(",", "")
    if not value:
        return 0.0
    m = re.match(r"^([0-9]+(?:\.[0-9]+)?)([KM]?)$", value)
    if not m:
        return 0.0
    num = float(m.group(1))
    unit = m.group(2)
    if unit == "K":
        return num * 1000
    if unit == "M":
        return num * 1000000
    return num


def strip_tags(raw: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw or "")).strip()


def fetch_openclaw_stars_top(
    top_n: int = 3, focus_skill: str = "", allow_insecure_fallback: bool = False
) -> tuple[list[dict], dict | None, str]:
    html_text = fetch_text(
        OPENCLAW_LEADERBOARD_URL,
        timeout=25,
        allow_insecure_fallback=allow_insecure_fallback,
    )
    panel_match = re.search(
        r'<div class="panel" id="panel-stars".*?<tbody>(.*?)</tbody>',
        html_text,
        flags=re.S,
    )
    if not panel_match:
        raise ValueError("cannot find OpenClaw stars panel")
    tbody = panel_match.group(1)
    rows = re.findall(r"<tr.*?>(.*?)</tr>", tbody, flags=re.S)
    items = []
    for row in rows:
        tds = re.findall(r"<td.*?>(.*?)</td>", row, flags=re.S)
        if len(tds) < 5:
            continue
        rank_text = strip_tags(tds[0])
        rank = int(rank_text) if rank_text.isdigit() else 0
        skill_anchor_match = re.search(r'(<a[^>]*class="skill-name"[^>]*>.*?</a>)', tds[1], flags=re.S)
        author_match = re.search(r'href="([^"]+)"[^>]*>(.*?)</a>', tds[2], flags=re.S)
        summary_match = re.search(r'<div class="skill-summary">(.*?)</div>', tds[1], flags=re.S)
        skill_anchor = skill_anchor_match.group(1) if skill_anchor_match else ""
        skill_name = strip_tags(skill_anchor)
        skill_url_match = re.search(r'href="([^"]+)"', skill_anchor)
        skill_url = (skill_url_match.group(1) if skill_url_match else "").strip()
        author = strip_tags(author_match.group(2) if author_match else "")
        author_url = (author_match.group(1) if author_match else "").strip()
        summary = strip_tags(summary_match.group(1) if summary_match else "")
        stars_text = strip_tags(tds[3])
        downloads_text = strip_tags(tds[4])
        items.append(
            {
                "rank": rank,
                "skill_name": skill_name,
                "skill_url": skill_url,
                "author": author,
                "author_url": author_url,
                "stars_text": stars_text,
                "stars_num": parse_human_number(stars_text),
                "downloads_text": downloads_text,
                "summary": summary,
            }
        )
    items = [x for x in items if x["rank"] > 0 and x["skill_name"]]
    items.sort(key=lambda x: (-x["stars_num"], x["rank"]))

    focus_result = None
    if focus_skill:
        q = focus_skill.lower().strip()
        for row in items:
            if q in row["skill_name"].lower():
                focus_result = row
                break

    asof_match = re.search(r"As of ([^<]+)</div>", html_text, flags=re.S)
    asof_text = strip_tags(asof_match.group(1)) if asof_match else "最新可用快照"
    return items[: max(1, top_n)], focus_result, asof_text


def text_of(elem: ET.Element, tag: str) -> str:
    child = elem.find(tag)
    return child.text.strip() if child is not None and child.text else ""


def parse_rss(xml_text: str) -> list[dict]:
    items = []
    root = ET.fromstring(xml_text)

    channel = root.find("channel")
    if channel is not None:
        for node in channel.findall("item"):
            title = strip_html(text_of(node, "title"))
            link = text_of(node, "link")
            desc = strip_html(text_of(node, "description"))
            pub_date = text_of(node, "pubDate")
            if title and link:
                items.append(
                    {"title": title, "link": link, "summary": desc, "published": pub_date}
                )

    if items:
        return items

    ns = {
        "atom": "http://www.w3.org/2005/Atom",
    }
    for node in root.findall("atom:entry", ns):
        title = strip_html(text_of(node, "{http://www.w3.org/2005/Atom}title"))
        link = ""
        link_elem = node.find("{http://www.w3.org/2005/Atom}link")
        if link_elem is not None:
            link = link_elem.attrib.get("href", "")
        summary = text_of(node, "{http://www.w3.org/2005/Atom}summary")
        if not summary:
            summary = text_of(node, "{http://www.w3.org/2005/Atom}content")
        published = text_of(node, "{http://www.w3.org/2005/Atom}updated")
        if title and link:
            items.append(
                {
                    "title": strip_html(title),
                    "link": link.strip(),
                    "summary": strip_html(summary),
                    "published": published,
                }
            )
    return items


def dedupe_items(items: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for it in items:
        key = (it.get("link") or "").strip() or (it.get("title") or "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out


def load_sources(path: pathlib.Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("sources.json must be an array")
    return data


def collect_news(
    sources: list[dict], per_source: int, allow_insecure_fallback: bool, window_hours: int
) -> tuple[list[dict], list[str]]:
    all_items = []
    errors = []
    now_dt = now_local()
    cutoff = now_dt - timedelta(hours=max(1, window_hours))

    def parse_published_dt(raw: str) -> dt.datetime | None:
        text = (raw or "").strip()
        if not text:
            return None
        try:
            d = parsedate_to_datetime(text)
            if d is None:
                return None
            if d.tzinfo is None:
                d = d.replace(tzinfo=now_dt.tzinfo)
            return d.astimezone(now_dt.tzinfo)
        except Exception:
            pass
        try:
            # Handles common Atom format like 2026-03-23T08:30:00Z
            norm = text.replace("Z", "+00:00")
            d2 = dt.datetime.fromisoformat(norm)
            if d2.tzinfo is None:
                d2 = d2.replace(tzinfo=now_dt.tzinfo)
            return d2.astimezone(now_dt.tzinfo)
        except Exception:
            return None

    for src in sources:
        name = src.get("name", "unknown")
        rss = src.get("rss_url", "").strip()
        category = src.get("category", "其他")
        if not rss:
            errors.append(f"{name}: rss_url empty")
            continue
        try:
            xml_text = fetch_text(rss, allow_insecure_fallback=allow_insecure_fallback)
            entries = parse_rss(xml_text)[:per_source]
            for e in entries:
                pub_dt = parse_published_dt(e.get("published", ""))
                # Keep only news published in the recent window.
                if pub_dt is None or pub_dt < cutoff or pub_dt > now_dt + timedelta(minutes=10):
                    continue
                all_items.append(
                    {
                        "source": name,
                        "category": category,
                        "title": e["title"],
                        "link": e["link"],
                        "summary": e.get("summary", ""),
                        "published": e.get("published", ""),
                    }
                )
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ET.ParseError) as ex:
            errors.append(f"{name}: {type(ex).__name__} {ex}")
        except Exception as ex:  # noqa: BLE001
            errors.append(f"{name}: {type(ex).__name__} {ex}")
    return dedupe_items(all_items), errors


def parse_published_dt_for_sort(raw: str) -> dt.datetime:
    text = (raw or "").strip()
    if not text:
        return dt.datetime.fromtimestamp(0, tz=now_local().tzinfo)
    try:
        d = parsedate_to_datetime(text)
        if d is None:
            raise ValueError("empty datetime")
        if d.tzinfo is None:
            d = d.replace(tzinfo=now_local().tzinfo)
        return d.astimezone(now_local().tzinfo)
    except Exception:
        pass
    try:
        norm = text.replace("Z", "+00:00")
        d2 = dt.datetime.fromisoformat(norm)
        if d2.tzinfo is None:
            d2 = d2.replace(tzinfo=now_local().tzinfo)
        return d2.astimezone(now_local().tzinfo)
    except Exception:
        return dt.datetime.fromtimestamp(0, tz=now_local().tzinfo)


def balance_items(
    items: list[dict],
    max_paper_ratio: float,
    min_official_items: int,
) -> list[dict]:
    if not items:
        return items
    safe_ratio = min(1.0, max(0.0, max_paper_ratio))
    papers = [x for x in items if x.get("category") == "论文研究"]
    non_papers = [x for x in items if x.get("category") != "论文研究"]
    papers.sort(key=lambda x: parse_published_dt_for_sort(x.get("published", "")), reverse=True)
    non_papers.sort(key=lambda x: parse_published_dt_for_sort(x.get("published", "")), reverse=True)

    # Ensure official releases are prioritized in non-paper set.
    official = [x for x in non_papers if x.get("category") == "官方发布"]
    others = [x for x in non_papers if x.get("category") != "官方发布"]
    non_papers_sorted = official + others

    if not papers or safe_ratio >= 1.0:
        return non_papers_sorted + papers

    total_target = len(items)
    max_papers = int(total_target * safe_ratio)
    max_papers = max(0, max_papers)
    keep_papers = papers[:max_papers]
    kept = non_papers_sorted + keep_papers

    # Keep at least some official news if available.
    if min_official_items > 0:
        official_kept = [x for x in kept if x.get("category") == "官方发布"]
        if len(official_kept) < min_official_items and official:
            need = min_official_items - len(official_kept)
            add = official[:need]
            for x in add:
                if x not in kept:
                    kept.insert(0, x)

    return dedupe_items(kept)


def cap_papers_by_ratio(items: list[dict], max_paper_ratio: float) -> list[dict]:
    if not items:
        return items
    safe_ratio = min(1.0, max(0.0, max_paper_ratio))
    papers = [x for x in items if x.get("category") == "论文研究"]
    news = [x for x in items if x.get("category") != "论文研究"]
    if not papers:
        return items
    if not news and safe_ratio < 1.0:
        # If only papers are available, keep a few to avoid empty report.
        return papers[: max(1, min(5, len(papers)))]

    # papers <= ratio * total => papers <= ratio/(1-ratio) * news
    max_papers = int((safe_ratio / (1.0 - safe_ratio)) * len(news)) if safe_ratio < 1.0 else len(papers)
    max_papers = max(0, min(len(papers), max_papers))
    papers_sorted = sorted(
        papers,
        key=lambda x: parse_published_dt_for_sort(x.get("published", "")),
        reverse=True,
    )
    return dedupe_items(news + papers_sorted[:max_papers])


def category_order_key(name: str) -> tuple[int, str]:
    preferred = {
        "官方发布": 0,
        "国内厂商动态": 1,
        "开源与工具": 2,
        "论文研究": 3,
        "行业资讯": 4,
        "社区讨论": 5,
        "其他": 99,
    }
    return (preferred.get(name, 90), name)


def call_chat_completion(
    api_key: str,
    model: str,
    messages: list[dict],
    base_url: str,
    timeout: int = 90,
) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
    }
    req = urllib.request.Request(
        base_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as resp:
        body = resp.read().decode("utf-8", errors="ignore")
    data = json.loads(body)
    try:
        return data["choices"][0]["message"]["content"]
    except Exception as ex:  # noqa: BLE001
        raise ValueError(f"invalid chat completion response: {ex}") from ex


def normalize_chat_completions_url(raw_url: str) -> str:
    url = (raw_url or "").strip()
    if not url:
        return ""
    if url.endswith("/v1"):
        return url + "/chat/completions"
    if url.endswith("/chat/completions"):
        return url
    return url.rstrip("/") + "/chat/completions"


def validate_https_url(url: str, field_name: str) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme.lower() != "https" or not parsed.netloc:
        raise ValueError(f"{field_name} must be a valid https URL")
    return parsed


def allowed_llm_hosts_from_env() -> set[str]:
    raw = os.getenv("LLM_ALLOWED_HOSTS", "")
    extra = {x.strip().lower() for x in raw.split(",") if x.strip()}
    return {h.lower() for h in DEFAULT_ALLOWED_LLM_HOSTS} | extra


def resolve_llm_runtime(args: argparse.Namespace) -> tuple[str, str, str]:
    # Backward-compatible API key resolution: Ark first, then common OpenAI-style env names.
    api_key = (
        args.ark_api_key
        or os.getenv("ARK_API_KEY", "")
        or os.getenv("OPENAI_API_KEY", "")
        or os.getenv("api_key", "")
        or os.getenv("API_KEY", "")
        or ""
    ).strip()

    ark_model_or_ep = (
        args.ark_endpoint_id
        or os.getenv("ARK_ENDPOINT_ID", "")
        or args.ark_model
        or os.getenv("ARK_MODEL", "")
        or ""
    ).strip()
    openai_model = (os.getenv("OPENAI_MODEL", "") or os.getenv("MODEL", "")).strip()
    model = ark_model_or_ep or openai_model or "Doubao-Seed-1.6-lite"

    provider = (args.llm_provider or "auto").strip().lower()
    if provider not in {"auto", "ark", "openai-compatible"}:
        provider = "auto"

    # Auto mode: if Ark-specific vars exist, keep Ark behavior; otherwise use OpenAI-compatible.
    has_ark_hint = bool(
        args.ark_endpoint_id or os.getenv("ARK_ENDPOINT_ID") or os.getenv("ARK_MODEL")
    )
    if provider == "auto":
        provider = "ark" if has_ark_hint else "openai-compatible"

    if provider == "ark":
        base_url = (os.getenv("ARK_BASE_URL", "") or ARK_BASE_URL).strip()
    else:
        base_url = (
            args.llm_base_url
            or os.getenv("OPENAI_BASE_URL", "")
            or os.getenv("LLM_BASE_URL", "")
            or ""
        ).strip()
        if not base_url:
            raise ValueError(
                "openai-compatible mode requires OPENAI_BASE_URL (or --llm-base-url)"
            )
        base_url = normalize_chat_completions_url(base_url)

    base_url = normalize_chat_completions_url(base_url)
    parsed = validate_https_url(base_url, "LLM base URL")
    host = (parsed.hostname or "").lower()
    if not args.allow_custom_llm_endpoint and host not in allowed_llm_hosts_from_env():
        raise ValueError(
            f"LLM endpoint host '{host}' is not in allowlist. "
            "Use --allow-custom-llm-endpoint or set LLM_ALLOWED_HOSTS."
        )

    return provider, base_url, api_key


def fetch_article_excerpt(url: str, allow_insecure_fallback: bool = False) -> str:
    if not url:
        return ""
    # Avoid non-HTML pages such as PDF downloads.
    if url.lower().endswith(".pdf"):
        return ""
    try:
        page = fetch_text(url, timeout=12, allow_insecure_fallback=allow_insecure_fallback)
    except Exception:
        return ""
    page = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", page)
    page = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", page)
    text = strip_tags(page)
    if len(text) < 120:
        return ""
    return text[:1600]


def enrich_items_with_llm(
    items: list[dict],
    api_key: str,
    model: str,
    base_url: str,
    allow_insecure_fallback: bool,
) -> tuple[str, list[str], list[str]]:
    if not items:
        return "今日暂无可分析资讯。", [], []

    rows = []
    for idx, it in enumerate(items, 1):
        excerpt = fetch_article_excerpt(
            it.get("link", ""), allow_insecure_fallback=allow_insecure_fallback
        )
        rows.append(
            {
                "idx": idx,
                "category": it.get("category", "其他"),
                "source": it.get("source", ""),
                "title": it.get("title", ""),
                "summary": (it.get("summary", "") or "")[:220],
                "link": it.get("link", ""),
                "published": it.get("published", ""),
                "content_excerpt": excerpt[:700],
            }
        )

    system_prompt = (
        "你是AI行业资讯编辑。请根据给定资讯，输出中文JSON，不要输出JSON以外内容。"
        "要求客观准确、信息密度高。"
    )
    user_prompt = {
        "task": "生成周报顶部小结和逐条中文解读",
        "rules": {
            "overview": "3-4句，概括本周动态、主线与重要变化",
            "per_item": "每条生成title_cn和detail。title_cn要中文；detail不少于200字，优先依据content_excerpt与summary，分2-3个自然段阐述：发生了什么、细节信息、为什么值得关注。不要英文。",
            "style": "中文、自然、信息密度高，不要空话",
        },
        "format": {
            "overview": "string",
            "items": [{"idx": 1, "title_cn": "string", "detail": "string"}],
        },
        "news": rows,
    }

    content = call_chat_completion(
        api_key=api_key,
        model=model,
        base_url=base_url,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=False)},
        ],
    )
    parsed = json.loads(content)
    overview = parsed.get("overview", "").strip() or "今日资讯以产品发布与研究进展为主。"
    details = [""] * len(items)
    titles_cn = [""] * len(items)
    for row in parsed.get("items", []):
        idx = row.get("idx")
        detail = (row.get("detail") or "").strip()
        title_cn = (row.get("title_cn") or "").strip()
        if isinstance(idx, int) and 1 <= idx <= len(items):
            details[idx - 1] = detail
            titles_cn[idx - 1] = title_cn
    return overview, details, titles_cn


def build_fallback_detail(item: dict) -> str:
    category = item.get("category", "其他")
    source = item.get("source", "未知信源")
    summary = (item.get("summary") or "").strip()
    title = item.get("title", "")

    if summary:
        base = summary if len(summary) <= 260 else summary[:257] + "..."
    else:
        base = f"标题显示该动态与“{category}”方向相关。"

    return (
        f"这是一条来自{source}的{category}动态，发布时间建议结合原文确认。"
        f"从公开信息看，核心内容是：{base}\n\n"
        "从应用价值看，这类更新通常会影响三个层面：一是能力边界是否变化（例如推理、工具调用、稳定性）；"
        "二是使用成本是否变化（部署门槛、效率、维护复杂度）；三是流程是否变化（是否需要调整你的采集、分析、推送策略）。\n\n"
        "建议把它纳入后续跟踪清单，并在下一次周报中对比同类动态，判断它是一次性新闻，还是可能持续演进的长期趋势。"
    )


def build_openclaw_purpose_text(skill_name: str, summary: str) -> str:
    text = (summary or "").strip()
    lower = text.lower()
    if "continuous improvement" in lower or "self-improving" in lower:
        return (
            "这个技能用于把代理在执行任务时的失败案例、修正过程和成功经验沉淀成可复用记忆，"
            "让后续同类任务少走弯路。它适合长期使用的个人工作流，价值在于持续降低重复错误率，"
            "并逐步提升任务完成质量与稳定性。"
        )
    if "google workspace" in lower or "gmail" in lower or "calendar" in lower:
        return (
            "这个技能把邮件、日历、文档、表格、网盘等 Google Workspace 操作统一成可调用能力，"
            "适合做跨工具的自动化处理。它的价值是减少手动切换和重复操作，"
            "把日程整理、信息检索、文档协作串成一条完整流程。"
        )
    if "web search" in lower or "tavily" in lower or "search" in lower:
        return (
            "这个技能用于执行面向 AI 代理的网页检索，重点是返回结构化、相关性更高的结果，"
            "方便后续摘要、比对和事实校验。它适合资讯追踪与研究场景，"
            "价值在于提高检索效率并降低无效信息噪声。"
        )
    return (
        f"这个技能主要用于 {skill_name} 相关能力扩展，帮助代理在特定场景下执行更稳定、可复用的操作。"
        "在日常使用中，建议重点评估它对你的任务链路是否能带来效率提升、错误率下降和更强的自动化闭环。"
    )


def render_markdown(
    date_label: str,
    items: list[dict],
    errors: list[str],
    llm_overview: str = "",
    llm_details: list[str] | None = None,
    llm_titles_cn: list[str] | None = None,
    openclaw_top: list[dict] | None = None,
    openclaw_focus: dict | None = None,
    openclaw_asof: str = "",
) -> str:
    if llm_details is None:
        llm_details = []
    if llm_titles_cn is None:
        llm_titles_cn = []
    categories = Counter(it.get("category", "其他") for it in items)
    top_categories = sorted(categories.items(), key=lambda x: (-x[1], category_order_key(x[0])))

    lines = [
        f"# AI 资讯周报 - {date_label}",
        "",
        "## 小结",
    ]
    if items:
        overview_text = llm_overview.strip()
        lines.extend(
            [
                f"- 研判小结：{overview_text or '今日主要增量集中在模型发布、工具链演进与论文更新。'}",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "- 今天没有抓取到有效资讯，建议检查网络或信源地址可用性。",
                "",
            ]
        )

    lines.extend(["## 正文", ""])

    if openclaw_top:
        lines.extend(["### OpenClaw 技能热榜（按 Star）", ""])
        lines.append(
            f"以下为最近一周区间内可获取的最新榜单快照（更新时间：{openclaw_asof or '未知'}）。"
        )
        lines.append("")
        for i, row in enumerate(openclaw_top, 1):
            purpose = build_openclaw_purpose_text(row["skill_name"], row.get("summary", ""))
            lines.extend(
                [
                    f"#### 热榜第{i}名：{row['skill_name']}",
                    f"该技能由 {row['author']} 发布，当前 Stars 约为 {row['stars_text']}。"
                    f"主要用途：{purpose}",
                    "",
                ]
            )
        if openclaw_focus:
            lines.append(
                f"你关注的技能「{openclaw_focus['skill_name']}」当前排名第 {openclaw_focus['rank']}，"
                f"发布者为 {openclaw_focus['author']}，Stars 约 {openclaw_focus['stars_text']}。"
            )
            lines.append("")

    if not items:
        lines.extend(["- 今日无可用条目（可检查网络或信源地址）", ""])
    else:
        grouped = defaultdict(list)
        for it in items:
            grouped[it.get("category", "其他")].append(it)

        idx = 1
        for cat_name in sorted(grouped.keys(), key=category_order_key):
            lines.append(f"### {cat_name}")
            lines.append("")
            for it in grouped[cat_name]:
                detail = ""
                if idx - 1 < len(llm_details):
                    detail = llm_details[idx - 1].strip()
                title_cn = ""
                if idx - 1 < len(llm_titles_cn):
                    title_cn = llm_titles_cn[idx - 1].strip()
                if not title_cn:
                    title_cn = f"第{idx}条资讯"
                lines.extend(
                    [
                        f"#### {idx}. {title_cn}",
                        f"发布日期：{it.get('published', '未知')}",
                        f"{detail or build_fallback_detail(it)}",
                        "",
                    ]
                )
                idx += 1

    if openclaw_top:
        lines.extend(["## OpenClaw 链接", ""])
        lines.append(f"- 榜单来源页：{OPENCLAW_LEADERBOARD_URL}")
        for i, row in enumerate(openclaw_top, 1):
            lines.append(f"- 热榜第{i}名 {row['skill_name']}：{row['skill_url']}")
            if row.get("author_url"):
                lines.append(f"- 热榜第{i}名发布者 {row['author']}：{row['author_url']}")
        if openclaw_focus:
            lines.append(
                f"- 关注技能 {openclaw_focus['skill_name']}：{openclaw_focus['skill_url']}"
            )
        lines.append("")

    lines.extend(["## 信源与原文链接", ""])
    for i, it in enumerate(items, 1):
        lines.append(
            f"- [{i}] {it.get('source', '未知信源')}（发布日期：{it.get('published', '未知')}）：{it.get('link', '')}"
        )
    lines.append("")

    lines.extend(
        [
            "## 生成信息",
            f"- 生成时间：{now_local().strftime('%Y-%m-%d %H:%M:%S %z')}",
            f"- 总条目：{len(items)}",
            f"- 信源数：{len(set(i['source'] for i in items)) if items else 0}",
            f"- 分类数：{len(categories)}",
            "",
        ]
    )

    lines.extend(["## 抓取异常", ""])
    if errors:
        lines.extend([f"- {err}" for err in errors])
    else:
        lines.append("- 无")
    lines.append("")
    return "\n".join(lines)


def write_doc(output_dir: pathlib.Path, content: str) -> pathlib.Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = f"ai_weekly_{now_local().strftime('%Y%m%d')}.md"
    out_path = output_dir / name
    out_path.write_text(content, encoding="utf-8")
    return out_path


def post_webhook(url: str, text: str) -> tuple[bool, str]:
    try:
        parsed = validate_https_url(url, "webhook URL")
    except ValueError as ex:
        return False, str(ex)
    host = (parsed.hostname or "").lower()
    if not (host.endswith(ALLOWED_WEBHOOK_SUFFIXES) or host in {"feishu.cn", "larksuite.com", "dingtalk.com"}):
        return False, "Unsupported webhook host (expect Feishu/Lark or DingTalk official domains)"

    if host.endswith(".feishu.cn") or host.endswith(".larksuite.com") or host == "feishu.cn" or host == "larksuite.com":
        payload = {"msg_type": "text", "content": {"text": text}}
    elif host.endswith(".dingtalk.com") or host == "dingtalk.com":
        payload = {"msgtype": "text", "text": {"content": text}}
    else:
        return False, "Unsupported webhook host (expect feishu/lark or dingtalk)"

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            return True, body[:500]
    except Exception as ex:  # noqa: BLE001
        return False, f"{type(ex).__name__}: {ex}"


def main() -> int:
    load_dotenv(pathlib.Path(".env").resolve())

    parser = argparse.ArgumentParser(description="Generate AI weekly digest markdown")
    parser.add_argument("--sources", default=DEFAULT_SOURCES_FILE, help="Path to sources json")
    parser.add_argument("--out", default=DEFAULT_OUTPUT_DIR, help="Output docs directory")
    parser.add_argument("--limit", type=int, default=5, help="Max items per source")
    parser.add_argument(
        "--webhook-url",
        default=os.getenv("DIGEST_WEBHOOK_URL", ""),
        help="Optional Feishu/DingTalk webhook URL",
    )
    parser.add_argument(
        "--send",
        action="store_true",
        help="Send message to webhook after generating markdown",
    )
    parser.add_argument(
        "--allow-insecure-ssl",
        action="store_true",
        help="Allow insecure SSL fallback (not recommended)",
    )
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Use LLM to generate Chinese overview/details",
    )
    parser.add_argument(
        "--llm-provider",
        default="auto",
        choices=["auto", "ark", "openai-compatible"],
        help="LLM provider mode",
    )
    parser.add_argument(
        "--llm-base-url",
        default=os.getenv("OPENAI_BASE_URL", ""),
        help="OpenAI-compatible chat completions URL",
    )
    parser.add_argument(
        "--allow-custom-llm-endpoint",
        action="store_true",
        help="Allow non-allowlisted LLM endpoint host (use with caution)",
    )
    parser.add_argument(
        "--ark-model",
        default=os.getenv("ARK_MODEL", "Doubao-Seed-1.6-lite"),
        help="Ark model name (legacy arg, still supported)",
    )
    parser.add_argument(
        "--ark-endpoint-id",
        default=os.getenv("ARK_ENDPOINT_ID", ""),
        help="Ark endpoint ID (ep-xxx), higher priority than --ark-model",
    )
    parser.add_argument(
        "--ark-api-key",
        default="",
        help="Ark API key (legacy arg, higher priority than env)",
    )
    parser.add_argument(
        "--window-hours",
        type=int,
        default=168,
        help="Only keep news published in the last N hours (default: 168h = 1 week)",
    )
    parser.add_argument(
        "--focus-skill",
        default="",
        help="Optional: skill name keyword to show its ranking",
    )
    parser.add_argument(
        "--official-window-hours",
        type=int,
        default=168,
        help="Fallback hours window for official-release sources",
    )
    parser.add_argument(
        "--max-paper-ratio",
        type=float,
        default=0.2,
        help="Maximum ratio for paper news in final report",
    )
    parser.add_argument(
        "--min-official-items",
        type=int,
        default=3,
        help="Try to keep at least this many official-release items",
    )
    args = parser.parse_args()

    sources_path = pathlib.Path(args.sources).resolve()
    out_dir = pathlib.Path(args.out).resolve()

    if not sources_path.exists():
        print(f"[ERROR] sources file not found: {sources_path}")
        return 1

    try:
        sources = load_sources(sources_path)
    except Exception as ex:  # noqa: BLE001
        print(f"[ERROR] load sources failed: {ex}")
        return 1

    items, errors = collect_news(
        sources,
        max(1, args.limit),
        allow_insecure_fallback=args.allow_insecure_ssl,
        window_hours=args.window_hours,
    )

    # If official releases are too few in base window, fetch official sources with a wider window.
    official_count = len([x for x in items if x.get("category") == "官方发布"])
    if official_count < max(0, args.min_official_items):
        official_sources = [s for s in sources if s.get("category") == "官方发布"]
        if official_sources:
            more_items, more_errors = collect_news(
                official_sources,
                max(1, args.limit),
                allow_insecure_fallback=args.allow_insecure_ssl,
                window_hours=max(args.window_hours, args.official_window_hours),
            )
            items = dedupe_items(items + more_items)
            # Keep only unique extra errors to avoid noisy duplicates.
            for err in more_errors:
                if err not in errors:
                    errors.append(err)

    items = balance_items(
        items,
        max_paper_ratio=args.max_paper_ratio,
        min_official_items=max(0, args.min_official_items),
    )
    items = cap_papers_by_ratio(items, max_paper_ratio=args.max_paper_ratio)

    llm_overview = ""
    llm_details: list[str] = []
    llm_titles_cn: list[str] = []
    openclaw_top: list[dict] = []
    openclaw_focus: dict | None = None
    openclaw_asof = ""

    try:
        openclaw_top, openclaw_focus, openclaw_asof = fetch_openclaw_stars_top(
            top_n=3,
            focus_skill=args.focus_skill,
            allow_insecure_fallback=args.allow_insecure_ssl,
        )
    except Exception as ex:  # noqa: BLE001
        errors.append(f"OpenClaw热榜: {type(ex).__name__} {ex}")

    if args.use_llm:
        try:
            provider, base_url, api_key = resolve_llm_runtime(args)
            if not api_key:
                errors.append("LLM: 未检测到可用 API Key（ARK_API_KEY 或 OPENAI_API_KEY）")
            else:
                model = (
                    args.ark_endpoint_id
                    or os.getenv("ARK_ENDPOINT_ID", "")
                    or args.ark_model
                    or os.getenv("ARK_MODEL", "")
                    or os.getenv("OPENAI_MODEL", "")
                    or os.getenv("MODEL", "")
                    or "Doubao-Seed-1.6-lite"
                )
                llm_overview, llm_details, llm_titles_cn = enrich_items_with_llm(
                    items,
                    api_key,
                    model,
                    base_url=base_url,
                    allow_insecure_fallback=args.allow_insecure_ssl,
                )
                print(f"[INFO] llm_provider={provider}, llm_model={model}")
        except Exception as ex:  # noqa: BLE001
            hint = ""
            msg = f"{type(ex).__name__} {ex}"
            if "404" in msg:
                hint = "（Ark 模式可能需要 ARK_ENDPOINT_ID=ep-xxx，而不是模型展示名）"
            errors.append(f"LLM: {msg}{hint}")

    date_label = now_local().strftime("%Y-%m-%d")
    md = render_markdown(
        date_label,
        items,
        errors,
        llm_overview=llm_overview,
        llm_details=llm_details,
        llm_titles_cn=llm_titles_cn,
        openclaw_top=openclaw_top,
        openclaw_focus=openclaw_focus,
        openclaw_asof=openclaw_asof,
    )
    doc_path = write_doc(out_dir, md)

    print(f"[OK] markdown generated: {doc_path}")
    print(f"[INFO] items={len(items)}, errors={len(errors)}")

    if args.send:
        if not args.webhook_url:
            print("[WARN] --send is set but webhook url is empty, skip sending")
            return 0
        msg = f"AI 日报已生成：{doc_path.name}\n路径：{doc_path}\n条目数：{len(items)}"
        success, resp = post_webhook(args.webhook_url, msg)
        if success:
            print(f"[OK] webhook sent: {resp}")
        else:
            print(f"[WARN] webhook failed: {resp}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
