"""新闻处理：外部 API 合并 / 信源归一 / 摘要压缩 / 语言判定 / 重要度评分。

C0 内容归一化的核心实现。所有函数仅做归一/排序/标记，不篡改新闻事实。
"""
import re
from datetime import datetime

from aiweekly.utils import _parse_date_arg, _parse_iso_datetime

# ============ 内容编辑归一化（C0：摘要 / 信源 / 重要度）============
# 目标：把 RSS 原始搬运水平提升为「编辑视角」——摘要压缩为事实句、信源归一短名、
#       并基于「来源权威度 × 时效 × 类别权重」给出重要度评分与🔥必读标记。
# 这些只用于排序/标记，绝不篡改新闻事实（标题、原文链接、发布时间保持不变）。

SUMMARY_MAX = 120        # 超过此长度触发归一化
SUMMARY_TARGET = 110     # 归一化后目标长度
MUSTREAD_TOP_N = 8       # 评分最高的前 N 条标记为必读

# 从 aiweekly.const 重新导出，供上游模块按需 import 统一常量（P2-1 / P2-5）
from aiweekly.const import (  # noqa: F401  # pylint: disable=unused-import
    NEWS_MAX_ITEMS,
    NEWS_SUMMARY_MAX_CHARS,
    LEADERBOARD_MAX_MODELS,
    LEADERBOARD_STALE_DAYS,
    HTML_MAX_SIZE_BYTES,
    SUMMARY_TARGET_CHARS as SUMMARY_TARGET_CONST,
)

# 信源短名映射（键为 RSS feed 原始标题，值为页面展示短名）
SOURCE_ALIASES = {
    "量子位": "量子位", "QbitAI": "量子位", "量子位 QbitAI": "量子位",
    "机器之心": "机器之心", "机器之心 Machine Intelligence": "机器之心",
    "极客公园": "极客公园", "GeekPark": "极客公园",
    "智东西": "智东西",
    "钛媒体：引领未来商业与生活新知": "钛媒体", "钛媒体": "钛媒体", "钛媒体 APP": "钛媒体",
    "InfoQ - 促进软件开发领域知识与创新的传播": "InfoQ", "InfoQ 中国": "InfoQ", "InfoQ": "InfoQ",
    "36氪": "36氪", "36Kr": "36氪",
    "AI News & Artificial Intelligence | TechCrunch": "TechCrunch", "TechCrunch": "TechCrunch",
    "Techmeme": "Techmeme",
    "MIT Technology Review": "MIT Tech Review", "MIT Technology Review 中文": "MIT Tech Review",
    "MIT News - Artificial intelligence": "MIT News", "MIT News - Artificial Intelligence": "MIT News",
    "VentureBeat": "VentureBeat", "Hugging Face Blog": "Hugging Face", "Hugging Face - Blog": "Hugging Face", "Google AI Blog": "Google AI",
    "The Verge": "The Verge", "Ars Technica": "Ars Technica", "Wired": "Wired",
    "网易科技": "网易科技", "新浪科技": "新浪科技", "澎湃新闻": "澎湃新闻",
    "第一财经": "第一财经", "财新": "财新", "界面新闻": "界面新闻",
    "雷锋网": "雷锋网", "新智元": "新智元",
}

# 信源权威度权重（0~1，S/A 级头部源更高；聚合类/社媒略低）
SOURCE_AUTHORITY = {
    "MIT Tech Review": 1.0, "TechCrunch": 0.95, "MIT News": 0.9,
    "量子位": 0.95, "36氪": 0.9, "智东西": 0.9, "极客公园": 0.9,
    "InfoQ": 0.88, "机器之心": 0.92, "钛媒体": 0.85,
    "Techmeme": 0.7, "VentureBeat": 0.85, "Hugging Face": 0.85,
    "Google AI": 0.85, "The Verge": 0.8, "Ars Technica": 0.82,
    "Wired": 0.82, "第一财经": 0.8, "财新": 0.85, "界面新闻": 0.78,
    "澎湃新闻": 0.8, "新浪科技": 0.75, "网易科技": 0.75, "雷锋网": 0.75,
    "新智元": 0.8,
}
DEFAULT_SOURCE_AUTHORITY = 0.6   # 未命中别名的源给中等默认权重，避免 0 分

# 类别权重：模型/论文/产品更高，行业八卦略低
CATEGORY_WEIGHT = {
    "ai-models": 1.0, "paper": 1.0, "ai-products": 0.85,
    "tip": 0.8, "industry": 0.7,
}
DEFAULT_CATEGORY_WEIGHT = 0.6

# 已知开源模型开发方（用于推断 open_source 字段）
OPEN_SOURCE_PROVIDERS = {
    "DeepSeek", "Meta", "Mistral", "Alibaba", "Alibaba Cloud", "01.AI",
    "Zhipu", "Cohere", "EleutherAI", "Stability AI", "Hugging Face",
    "Nomic", "Qwen", "Yi", "GLM", "Microsoft",
}

# CJK 字符范围，用于判定报道语言（含中文→zh，否则→en）
_CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")
# 连续英文单词（≥2 字母），用于语言判定时区分「英文为主的中英混排」
_LATIN_RE = re.compile(r"[A-Za-z]{2,}")


def merge_external_news(base_items: list, external_items: list) -> list:
    """将用户自备的外部 API 新闻合并进 RSS 新闻，按 url/title 去重。

    Args:
        base_items: RSS 抓取的新闻列表
        external_items: 用户自备外部 API 导出（如 AI HOT）的新闻列表
    返回去重后的合并列表（RSS 优先，外部补充）。
    """
    seen = set()
    merged = []
    for it in base_items + external_items:
        key = (it.get("url") or "").strip().lower() or (it.get("title") or "").strip().lower()
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        merged.append(it)
    return merged


def format_news_items(api_data: dict, truncate: bool = True) -> list:
    """将 API 数据格式化为 JS 数组需要的格式（含信源/摘要归一化）。

    Args:
        api_data: 抓取或外部 API 返回的 news 数据（{"items": [...]}）
        truncate: 是否对超长摘要做截断归一（默认 True，服务于新闻卡片显示兜底）。
            设为 False 时保留完整清洗后摘要，供「本周看点」等需完整呈现的场景使用。
    返回: 归一化后的新闻列表（NewsItem 形态：含 lang / score / cn_summary 等编辑字段）。
    """
    items = []
    for item in api_data.get("items", []):
        items.append({
            "title": item.get("title", ""),
            "summary": _normalize_summary(item.get("summary", ""), truncate=truncate),
            "url": item.get("url") or item.get("permalink", ""),
            "source": _normalize_source(item.get("source", "")),
            "publishedAt": item.get("publishedAt", ""),
            "category": item.get("category", ""),
            "lang": _detect_lang(item.get("title", ""), item.get("summary", "")),
            "score": item.get("score", 0),
            "cn_summary": item.get("cn_summary", "") or "",
            "cn_title": item.get("cn_title", "") or "",
        })
    return items


def _normalize_source(raw: str) -> str:
    """把 RSS feed 原始标题归一为页面展示短名。"""
    if not raw:
        return ""
    raw = raw.strip()
    return SOURCE_ALIASES.get(raw, raw)


def _detect_lang(title: str, summary: str) -> str:
    """基于标题+摘要判定报道语言：zh / en。

    默认：含中文字符即判中文，对纯中文/中文源（量子位、36氪、TechCrunch 中文转载等）
    与纯英文源自然分流，供页面「语言」筛选；不依赖 RSS 源名映射，鲁棒。

    增强（P1#5）：纠正「英文为主的中英混排」误判——如 "OpenAI 发布 GPT-5"，
    旧逻辑因含个别汉字直接判中文、导致这类英文报道既不进「语言=英文」筛选、
    也不触发中文总结。现改为：汉字极少（<8）且含 ≥2 个英文词时判英文。
    正常中文报道摘要汉字数远大于 8，不会误伤。
    """
    text = f"{title or ''} {summary or ''}"
    if not _CJK_RE.search(text):
        return "en"
    han = len(_CJK_RE.findall(text))
    latin = len(_LATIN_RE.findall(text))
    if han < 8 and latin >= 2:
        return "en"
    return "zh"


def _normalize_summary(raw: str, max_len: int = SUMMARY_MAX,
                       target: int = SUMMARY_TARGET,
                       truncate: bool = True) -> str:
    """把 RSS 原始 summary 做噪声归一（署名/源站名/空白）。

    - 始终做噪声清洗（作者/编辑署名行、开头重复源站名、空白换行归一）；
    - truncate=True（默认，历史行为）：超长（>max_len）时按句压缩为 ≤target 字
      的事实句摘要并加省略号。主要服务于新闻卡片——卡片本身已有 CSS line-clamp
      作显示兜底，此截断是数据层冗余保险。
    - truncate=False：只清洗、不截断，返回完整摘要。用于「本周看点」的 analysis
      字段——用户明确要求看点信息完整呈现，不应被中途掐断。

    不编造、不改动事实，仅做噪声清洗与（可选）长度归一。
    """
    if not raw:
        return ""
    text = re.sub(r"\s+", " ", raw).strip()
    # 去除 RSS 署名行噪声：作者 | 王涵 编辑 | 云鹏 编译 | 茄子 等
    # 注意用 \S+（遇空格即止），避免贪婪跨吞下一条署名与正文开头
    text = re.sub(r"(?:作者|编辑|责编|来源|出品|编译)\s*[\|｜:：]\s*\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    # 去除开头重复的源站名（如「智东西 智东西8月…」→「智东西8月…」）
    for alias in SOURCE_ALIASES.values():
        if text.startswith(alias) and len(text) > len(alias) and text[len(alias)] in " ，,、。：:":
            text = text[len(alias):].strip()
            break
    # 清掉署名/源站名剥离后可能残留的行首标点或空格
    text = re.sub(r"^[\s，,、；;：:.。]+", "", text)
    # 看点或相似场景要求保留全文时，清洗后即返回，不进入截断分支。
    if not truncate:
        return text
    if len(text) <= max_len:
        return text
    parts = re.split(r"(?<=[。！？!?])", text)
    out = ""
    for p in parts:
        if not p.strip():
            continue
        if len(out) + len(p) <= target:
            out += p
        else:
            if not out:
                out = p[:target]
            break
    out = out.strip()
    if len(out) < len(text):
        out = out.rstrip("，,、；;：:）).。！？!?") + "…"
    return out


def _is_open_source(provider: str) -> bool:
    """根据开发方名称推断是否开源。"""
    return any(p.lower() in provider.lower() for p in OPEN_SOURCE_PROVIDERS)


def _score_news(items: list, report_date: str = None, top_n: int = MUSTREAD_TOP_N,
                pin_terms: list = None) -> list:
    """基于「来源权威度 × 时效 × 类别权重」计算重要度评分，并标记 Top-N 为必读。

    评分仅用于排序与🔥必读标记，绝不篡改标题/链接/时间等事实字段。
    返回原列表（就地写入 score / mustRead）。

    pin_terms: 编辑钉选词列表（子串匹配标题）。命中的条目强制必读（mustRead=True、
    pinned=True），避免重大事件被拆成多条、各自分数稀释而漏出 Top-N。
    """
    if not items:
        return items
    rd = _parse_date_arg(report_date) if report_date else None
    if rd is None:
        rd = datetime.now()

    scores = []
    for it in items:
        src = _normalize_source(it.get("source", ""))
        auth = SOURCE_AUTHORITY.get(src, DEFAULT_SOURCE_AUTHORITY)
        cat = CATEGORY_WEIGHT.get(it.get("category", ""), DEFAULT_CATEGORY_WEIGHT)
        rec = 0.5
        pub = it.get("publishedAt", "")
        if pub:
            pd = _parse_iso_datetime(pub)
            if pd is not None:
                if pd.tzinfo is not None:
                    pd = pd.replace(tzinfo=None)
                age_days = (rd - pd).total_seconds() / 86400.0
                if age_days < 0:
                    age_days = 0
                rec = max(0.2, 1.0 - age_days * 0.1)  # 24h 内=1.0，7天=0.4，更久→0.2
        s = auth * 0.5 + cat * 0.3 + rec * 0.2
        it["score"] = round(s, 3)
        scores.append(s)

    order = sorted(range(len(items)), key=lambda i: scores[i], reverse=True)
    for rank, idx in enumerate(order):
        items[idx]["mustRead"] = (rank < top_n)
    # 编辑钉选：命中 pin_terms 的条目强制必读，重大事件不被算法稀释漏出 Top-N
    pts = [t.strip() for t in (pin_terms or []) if t and t.strip()]
    if pts:
        for it in items:
            t = (it.get("title", "") or "")
            if any(p.lower() in t.lower() for p in pts):
                it["mustRead"] = True
                it["pinned"] = True
    return items


def get_default_ranking() -> list:
    """保留兼容占位：返回空列表，避免脑补虚构模型名（已不再默认启用）。"""
    return []


__all__ = [
    "SUMMARY_MAX", "SUMMARY_TARGET", "MUSTREAD_TOP_N", "LEADERBOARD_STALE_DAYS",
    "SOURCE_ALIASES", "SOURCE_AUTHORITY", "CATEGORY_WEIGHT",
    "DEFAULT_SOURCE_AUTHORITY", "DEFAULT_CATEGORY_WEIGHT", "OPEN_SOURCE_PROVIDERS",
    "merge_external_news", "format_news_items",
    "_normalize_source", "_detect_lang", "_normalize_summary",
    "_is_open_source", "_score_news", "get_default_ranking",
]