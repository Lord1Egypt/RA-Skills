#!/usr/bin/env python3
"""
Daily News English Learning Cards Generator

Fetches latest news via Tavily, generates learning content via DeepSeek,
creates comic illustrations via OpenRouter (Nano Banana 2), and composites
final cards with Pillow. Fully self-contained, no IDE-specific dependencies.

Environment variables required:
    TAVILY_API_KEY      - Tavily Search API key (https://tavily.com)
    DEEPSEEK_API_KEY    - DeepSeek API key (https://platform.deepseek.com)
    OPENROUTER_API_KEY  - OpenRouter API key (https://openrouter.ai)

Optional:
    IMAGE_MODEL         - OpenRouter model (default: google/gemini-2.5-flash-preview-image-generation)
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _load_dotenv():
    """Load .env file from script dir, parent dir, or cwd (no external deps)."""
    candidates = [
        Path(__file__).resolve().parent.parent / ".env",
        Path(__file__).resolve().parent / ".env",
        Path.cwd() / ".env",
    ]
    for env_path in candidates:
        if env_path.is_file():
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key, value = key.strip(), value.strip().strip("'\"")
                    if key and key not in os.environ:
                        os.environ[key] = value
            return


_load_dotenv()


def _ensure_deps():
    required = {
        "tavily": "tavily-python",
        "openai": "openai",
        "PIL": "Pillow",
        "requests": "requests",
    }
    missing = []
    for mod, pkg in required.items():
        try:
            __import__(mod)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"[setup] Installing missing packages: {', '.join(missing)}")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q"] + missing
        )


_ensure_deps()

import argparse
import base64
import io
import json
import logging
import random
import re
import textwrap
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple

import requests
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
from tavily import TavilyClient

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────

CARD_W = 1080
COMIC_H = 936   # top comic area
GRADIENT_OVERLAP = 80
BOTTOM_PADDING = 36  # padding below last content

DEFAULT_CATEGORIES = [random.choice(["politics", "finance", "sports", "entertainment", "technology", "outdoor", "science", "space", "environment", "education", "health", "culture", "animals", "innovation"])]
CATEGORY_LABELS = {
    "politics": "POLITICS",
    "finance": "FINANCE",
    "sports": "SPORTS",
    "entertainment": "ENTERTAINMENT",
    "technology": "TECHNOLOGY",
    "outdoor": "OUTDOOR",
    "science": "SCIENCE",
    "space": "SPACE",
    "environment": "ENVIRONMENT",
    "education": "EDUCATION",
    "health": "HEALTH",
    "culture": "CULTURE",
    "animals": "ANIMALS",
    "innovation": "INNOVATION",
}
CATEGORY_COLORS = {
    "politics": (231, 76, 60),
    "finance": (39, 174, 96),
    "sports": (52, 152, 219),
    "entertainment": (155, 89, 182),
    "technology": (243, 156, 18),
    "outdoor": (46, 139, 87),
    "science": (41, 128, 185),
    "space": (44, 62, 80),
    "environment": (39, 174, 96),
    "education": (230, 126, 34),
    "health": (241, 196, 15),
    "culture": (142, 68, 173),
    "animals": (211, 84, 0),
    "innovation": (22, 160, 133),
}
CATEGORY_CN = {
    "politics": "时政",
    "finance": "财经",
    "sports": "体育",
    "entertainment": "娱乐",
    "technology": "科技",
    "outdoor": "户外",
    "science": "科学发现",
    "space": "太空探索",
    "environment": "环保自然",
    "education": "教育",
    "health": "健康成长",
    "culture": "文化艺术",
    "animals": "动物世界",
    "innovation": "创新发明",
}

DEFAULT_IMAGE_MODEL = "google/gemini-3.1-flash-image-preview"
FONT_CACHE_DIR = Path.home() / ".cache" / "news-cards-fonts"

COMIC_STYLE_PREFIX = (
    "Generate a colorful editorial cartoon illustration with bold outlines, "
    "vibrant colors, comic book style, professional quality. "
    "The image MUST be square (1:1 aspect ratio). "
    "IMPORTANT: You MUST embed the following English vocabulary words as "
    "VISIBLE, READABLE TEXT naturally woven into the scene. "
    "VARIETY IS KEY — use DIFFERENT methods for each word, for example: "
    "one word on a shop sign, another on a character's t-shirt, "
    "one on a computer screen, one on a newspaper headline, "
    "one on a street banner, a license plate, a trophy, a poster on "
    "a wall, a food menu, a name tag, graffiti, a book spine, etc. "
    "Do NOT put all words in speech bubbles — at most 1 word can be "
    "in a speech bubble. Each word must be spelled EXACTLY as given. "
)

DEEPSEEK_SYSTEM_PROMPT = textwrap.dedent("""\
    You are a fun, warm, and encouraging English teacher for 6th-grade students
    (age 11-12). Your goal is to help young learners discover the beauty of
    English through POSITIVE, UPLIFTING, and AGE-APPROPRIATE news stories.

    Given a news headline and content, produce a JSON object with these fields:

    {
      "english_summary": "Simple 1-sentence summary for young learners",
      "chinese_translation": "准确的中文翻译，口语化表达",
      "vocabulary": [
        {
          "word": "victory",
          "phonetic": "/ˈvɪktəri/",
          "chinese": "胜利",
          "pos": "n."
        }
      ],
      "background_en": "2-3 sentence English background explaining the news.",
      "background_cn": "对应的中文背景介绍，2-3句话。",
      "comic_prompt": "Vivid cartoon scene description for this news event."
    }

    ★ CONTENT SAFETY RULES (HIGHEST PRIORITY) ★
    - This card is for CHILDREN. Keep everything cheerful and encouraging.
    - Focus on POSITIVE aspects: achievements, cooperation, progress, hope.
    - NEVER mention: death, killing, injuries, accidents, disasters, violence,
      crime, war, weapons, drugs, abuse, corruption, or any scary content.
    - If the news has negative elements, REFRAME it positively. For example:
      Instead of "4 killed in mine accident" → "Rescue teams work bravely"
      Instead of "War escalates" → "Peace talks continue between nations"
    - The tone should feel like a friendly teacher sharing good news with kids.
    - Choose vocabulary words that are upbeat, useful, and fun to learn.

    STRICT rules (you MUST follow every one):
    - english_summary: ONLY 1 sentence. MUST be under 20 words. Use the
      simplest words possible. Subject-verb-object. No passive voice. No
      subordinate clauses. No words like "while", "through", "potentially".
      The sentence MUST sound positive and uplifting.
      Good: "China's space team successfully launched a new satellite! 🚀"
      Good: "Young athletes from China won gold medals at the tournament!"
      Bad: "4 workers were killed in a mine accident in northern China."
    - chinese_translation: 一句话中文翻译，口语化，像跟小朋友聊天。不超过25个字。
      要阳光、积极，让人读了开心。
    - vocabulary: CRITICAL — ALL 5 words MUST appear in your english_summary
      sentence above. Do NOT pick any word that is not in the sentence.
      Pick exactly 5 words from the sentence, CEFR A2-B1 level. Useful and
      fun words for 12-year-olds. Avoid trivial words like "a", "the", "is",
      "was", "and", "in", "on", "it", "to". Include IPA phonetic.
      Chinese meaning 2-4 characters.
      Choose POSITIVE, ENERGETIC words when possible (e.g. "achieve",
      "brilliant", "discover", "explore", "celebrate").
    - background_en: 2-3 sentences in simple English explaining what happened,
      why it matters, and any key context. Under 60 words total.
      Use simple vocabulary suitable for 12-year-olds.
      Keep the tone warm and educational. NO scary or violent details.
    - background_cn: 对应的中文新闻背景，2-3句，口语化，总共不超过80字。
      保持积极向上的语调，适合青少年阅读。
    - comic_prompt: describe ONE vivid, COLORFUL, CHEERFUL cartoon scene
      (not multiple panels). The scene should be happy and inspiring.
      NO dark themes, NO weapons, NO violence, NO injuries.
      Be specific about characters, objects, actions, and background.
      Characters should be smiling and energetic.
      Suggest natural places where the 5 vocabulary words could appear
      as signs, labels, banners, or floating text in the scene.
    - Return ONLY valid JSON, no markdown fences or extra text.
""")

# ─────────────────────────────────────────────
# Environment & API clients
# ─────────────────────────────────────────────


def _check_env(var: str, service: str, url: str) -> str:
    val = os.environ.get(var)
    if not val:
        log.error(f"Missing {var}. Get your key at {url}")
        sys.exit(1)
    return val


def init_clients():
    tavily_key = _check_env("TAVILY_API_KEY", "Tavily", "https://tavily.com")
    deepseek_key = _check_env(
        "DEEPSEEK_API_KEY", "DeepSeek", "https://platform.deepseek.com"
    )
    openrouter_key = _check_env(
        "OPENROUTER_API_KEY", "OpenRouter", "https://openrouter.ai"
    )

    tavily_client = TavilyClient(api_key=tavily_key)
    deepseek_client = OpenAI(
        api_key=deepseek_key, base_url="https://api.deepseek.com"
    )
    openrouter_client = OpenAI(
        api_key=openrouter_key, base_url="https://openrouter.ai/api/v1"
    )
    image_model = os.environ.get("IMAGE_MODEL", DEFAULT_IMAGE_MODEL)

    return tavily_client, deepseek_client, openrouter_client, image_model


# ─────────────────────────────────────────────
# Module 1: News Fetching (Tavily)
# ─────────────────────────────────────────────

# -- 国内媒体优先（英文版），给予更高优先级 --
DOMESTIC_SOURCES = [
    "xinhuanet.com", "news.cn",            # 新华社
    "chinadaily.com.cn",                    # 中国日报
    "cgtn.com",                             # CGTN (央视国际)
    "globaltimes.cn",                       # 环球时报
    "ecns.cn",                              # 中新社英文
    "china.org.cn",                         # 中国网
    "peoplesdaily.com.cn", "people.com.cn", # 人民日报
    "cctv.com",                             # 央视
    "yicai.com",                            # 第一财经
    "caixin.com",                           # 财新
    "scmp.com",                             # 南华早报
    "sixthtone.com",                        # 澎湃英文
    "shine.cn",                             # 上观新闻英文
    "kankanews.com",                        # 看看新闻
    "thepaper.cn",                          # 澎湃新闻
]

# -- 国际知名媒体（作为补充） --
INTERNATIONAL_SOURCES = [
    "reuters.com", "bbc.com", "bbc.co.uk", "apnews.com",
    "bloomberg.com", "espn.com", "cnn.com", "nytimes.com",
    "theguardian.com", "washingtonpost.com", "techcrunch.com",
    "theverge.com", "variety.com", "cnbc.com",
]

# 合并列表，国内在前
PREFERRED_SOURCES = DOMESTIC_SOURCES + INTERNATIONAL_SOURCES

# -- 各分类对应的国内媒体搜索关键词（偏正能量方向）--
CATEGORY_SEARCH_HINTS = {
    "politics": "China achievement cooperation development site:chinadaily.com.cn OR site:xinhuanet.com OR site:cgtn.com",
    "finance": "China economy growth innovation site:yicai.com OR site:caixin.com OR site:chinadaily.com.cn",
    "sports": "China sports victory championship site:cgtn.com OR site:chinadaily.com.cn OR site:ecns.cn",
    "entertainment": "China entertainment culture festival movie site:chinadaily.com.cn OR site:cgtn.com OR site:globaltimes.cn",
    "technology": "China technology AI breakthrough innovation site:chinadaily.com.cn OR site:cgtn.com OR site:scmp.com",
    "outdoor": "China outdoor hiking camping nature adventure travel site:chinadaily.com.cn OR site:cgtn.com OR site:globaltimes.cn",
    "science": "China science discovery research breakthrough site:chinadaily.com.cn OR site:cgtn.com OR site:ecns.cn",
    "space": "China space exploration rocket satellite launch site:chinadaily.com.cn OR site:cgtn.com OR site:xinhuanet.com",
    "environment": "China environment wildlife conservation green energy climate site:chinadaily.com.cn OR site:cgtn.com OR site:ecns.cn",
    "education": "China education school student youth learning site:chinadaily.com.cn OR site:cgtn.com OR site:ecns.cn",
    "health": "China health nutrition fitness youth wellness site:chinadaily.com.cn OR site:cgtn.com OR site:ecns.cn",
    "culture": "China culture heritage museum art festival tradition site:chinadaily.com.cn OR site:cgtn.com OR site:globaltimes.cn",
    "animals": "China wildlife animal panda endangered species protection site:chinadaily.com.cn OR site:cgtn.com OR site:ecns.cn",
    "innovation": "China innovation invention young inventor robot competition maker site:chinadaily.com.cn OR site:cgtn.com OR site:ecns.cn",
}

# ─────────────────────────────────────────────
# 内容安全风控 (Content Safety Filter)
# ─────────────────────────────────────────────

# 负面内容关键词黑名单 — 命中即跳过该新闻
NEGATIVE_KEYWORDS = [
    # 死亡 / 伤亡
    "killed", "dead", "death", "deaths", "die", "dies", "died",
    "fatality", "fatalities", "fatal", "mortality",
    # 事故 / 灾难
    "accident", "crash", "collision", "explosion", "explode",
    "disaster", "catastrophe", "avalanche", "landslide", "flood",
    "earthquake", "tsunami", "wildfire", "derail", "derailment",
    "mine collapse", "coal mine", "mining accident",
    # 暴力 / 犯罪
    "murder", "homicide", "assault", "rape", "abuse", "torture",
    "kidnap", "trafficking", "shooting", "gunfire", "stabbing",
    "bomb", "bombing", "terrorist", "terrorism", "massacre",
    "execution", "genocide", "violence", "violent",
    # 战争 / 冲突
    "war", "warfare", "airstrike", "missile", "invasion",
    "military strike", "casualties", "troops killed",
    "armed conflict", "drone strike",
    # 疾病 / 疫情
    "pandemic", "epidemic", "plague", "outbreak",
    "death toll", "infection surge",
    # 自杀 / 心理
    "suicide", "self-harm",
    # 毒品 / 违法
    "drug bust", "narcotics", "overdose", "fentanyl",
    "corruption", "bribery", "fraud", "embezzlement", "scandal",
    # 其他负面
    "poverty", "famine", "starvation", "refugee crisis",
    "hostage", "missing persons", "body found",
    "prison", "sentenced to death", "life sentence",
]

# 正能量关键词白名单 — 命中给予加分
POSITIVE_KEYWORDS = [
    # 成就 / 突破
    "achievement", "breakthrough", "milestone", "record-breaking",
    "innovation", "invention", "discovery", "pioneer",
    # 合作 / 友好
    "cooperation", "collaboration", "partnership", "agreement",
    "diplomacy", "peace", "friendship", "alliance", "unity",
    # 发展 / 增长
    "growth", "development", "progress", "improvement", "upgrade",
    "prosperity", "boost", "recovery", "expansion", "thriving",
    # 体育 / 胜利
    "victory", "champion", "championship", "gold medal", "winner",
    "tournament", "competition", "athlete", "sportsmanship",
    "world record", "Olympic",
    # 科技 / 创新
    "AI", "artificial intelligence", "space", "satellite", "rocket",
    "5G", "quantum", "renewable energy", "solar", "green",
    "electric vehicle", "autonomous", "robot",
    # 文化 / 教育
    "culture", "heritage", "festival", "celebration", "art",
    "museum", "education", "scholarship", "student", "university",
    "concert", "film", "movie", "award", "exhibition",
    # 公益 / 温暖
    "volunteer", "charity", "donation", "community",
    "rescue", "hero", "inspire", "inspiring", "heartwarming",
    "kindness", "generosity", "hope", "dream",
    # 健康 / 生活
    "health", "wellness", "fitness", "nutrition",
    "environment", "wildlife", "conservation", "sustainability",
    "beautiful", "scenic", "tourism", "travel",
]


def _is_recent_news(url: str, content: str = "", max_age_days: int = 3) -> bool:
    """检查新闻是否是最近 max_age_days 天内的。
    通过 URL 中的日期模式和内容中的日期来判断。
    如果无法判断日期，返回 True（给予信任）。
    """
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=max_age_days)

    # 从 URL 中提取日期模式
    date_patterns_url = [
        # /2025/04/17/ 或 /2025-04-17/
        r'/(\d{4})[/-](\d{1,2})[/-](\d{1,2})(?:/|\.)',
        # /2025-04/17/ (如 chinadaily URL)
        r'/(\d{4})-(\d{1,2})/(\d{1,2})/',
        # 20250417 in URL
        r'/(\d{4})(\d{2})(\d{2})',
    ]

    for pattern in date_patterns_url:
        match = re.search(pattern, url)
        if match:
            try:
                year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
                article_date = datetime(year, month, day, tzinfo=timezone.utc)
                if article_date < cutoff:
                    log.info(f"[freshness] URL date {year}-{month:02d}-{day:02d} is too old (cutoff: {cutoff.strftime('%Y-%m-%d')}): {url[:80]}")
                    return False
                else:
                    log.debug(f"[freshness] URL date {year}-{month:02d}-{day:02d} is recent ✓")
                    return True
            except (ValueError, OverflowError):
                continue

    # 从内容中提取日期（作为辅助判断）
    content_date_patterns = [
        # April 3, 2026 / Apr 3, 2026
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),?\s+(\d{4})',
        # 2026-04-03
        r'(\d{4})-(\d{1,2})-(\d{1,2})',
    ]

    combined_text = f"{url} {content[:500]}"
    for pattern in content_date_patterns:
        matches = re.findall(pattern, combined_text)
        for m in matches:
            try:
                if len(m) == 2:
                    # Month name pattern: (day, year) — need month from context
                    continue
                elif len(m) == 3:
                    year, month, day = int(m[0]), int(m[1]), int(m[2])
                    article_date = datetime(year, month, day, tzinfo=timezone.utc)
                    if article_date < cutoff:
                        return False
                    else:
                        return True
            except (ValueError, OverflowError):
                continue

    # 无法从 URL/内容中确定日期，给予信任
    log.debug(f"[freshness] Cannot determine date from URL, assuming recent: {url[:80]}")
    return True


def _contains_negative_content(text: str) -> bool:
    """检查文本是否包含负面关键词。"""
    text_lower = text.lower()
    for kw in NEGATIVE_KEYWORDS:
        if kw.lower() in text_lower:
            return True
    return False


def _positive_score(text: str) -> float:
    """计算文本的正能量分数（命中正面关键词越多分越高）。"""
    text_lower = text.lower()
    score = 0.0
    for kw in POSITIVE_KEYWORDS:
        if kw.lower() in text_lower:
            score += 0.1
    return min(score, 1.0)  # 封顶 1.0


def fetch_news(tavily: TavilyClient, categories: list[str]) -> list[dict]:
    today = datetime.now(timezone.utc)
    today_str = today.strftime("%B %d, %Y")
    yesterday_str = (today - timedelta(days=1)).strftime("%B %d, %Y")
    results = []

    for cat in categories:
        # 策略1: 先尝试搜索国内媒体（正能量方向），强调今天/昨天
        domestic_query = CATEGORY_SEARCH_HINTS.get(cat, f"China {cat} news")
        domestic_query = f"{domestic_query} today {today_str}"
        log.info(f"[news] Searching domestic first: {domestic_query}")

        items = _search_with_fallback(tavily, domestic_query)

        # 内容安全 + 日期新鲜度过滤
        safe_items, blocked = _filter_safe_news(items)
        if blocked:
            log.info(f"[safety] Blocked {blocked} items (negative/stale) for {cat}")

        # 从安全结果中筛选国内媒体
        domestic_items = [
            it for it in safe_items
            if any(src in it.get("url", "") for src in DOMESTIC_SOURCES)
        ]

        if domestic_items:
            log.info(f"[news] Found {len(domestic_items)} safe domestic results for {cat}")
            best = _pick_best(domestic_items)
        elif safe_items:
            log.info(f"[news] No domestic results for {cat}, using safe international results")
            best = _pick_best(safe_items)
        else:
            # 策略2: 无安全结果，用正能量专用查询重试，明确要求最新
            positive_query = f"latest {cat} achievement success good news {today_str} OR {yesterday_str}"
            log.info(f"[news] No safe results for {cat}, trying positive query: {positive_query}")
            items = _search_with_fallback(tavily, positive_query)
            safe_items, _ = _filter_safe_news(items)
            if not safe_items:
                log.warning(f"[news] No safe results for {cat}, using placeholder")
                results.append(_placeholder_news(cat))
                continue
            best = _pick_best(safe_items)

        results.append({
            "category": cat,
            "headline": best.get("title", "Untitled"),
            "content": best.get("content", best.get("title", "")),
            "url": best.get("url", ""),
            "source_type": "domestic" if any(
                src in best.get("url", "") for src in DOMESTIC_SOURCES
            ) else "international",
        })
        source_tag = "🇨🇳 domestic" if results[-1]["source_type"] == "domestic" else "🌍 international"
        log.info(f"[news] {cat} [{source_tag}]: {best.get('title', '')[:60]}")
        log.info(f"[news] {cat} URL: {best.get('url', 'N/A')}")

    return results


def _filter_safe_news(items: list) -> tuple[list, int]:
    """过滤掉包含负面内容或日期过旧的新闻，返回安全列表和被拦截数量。"""
    safe = []
    blocked = 0
    for item in items:
        text = f"{item.get('title', '')} {item.get('content', '')}"
        url = item.get("url", "")

        # 日期新鲜度检查
        if not _is_recent_news(url, text, max_age_days=3):
            log.info(f"[freshness] Blocked stale news: {item.get('title', '')[:60]}")
            blocked += 1
            continue

        # 负面内容检查
        if _contains_negative_content(text):
            log.debug(f"[safety] Blocked: {item.get('title', '')[:50]}")
            blocked += 1
        else:
            safe.append(item)
    return safe, blocked


def _search_with_fallback(tavily: TavilyClient, query: str) -> list:
    try:
        resp = tavily.search(
            query=query, topic="news", days=1,
            max_results=8, search_depth="advanced",
        )
        items = resp.get("results", [])
        if items:
            return items
    except Exception as e:
        log.warning(f"[news] Search failed (days=1): {e}")

    try:
        log.info("[news] Retrying with days=2")
        resp = tavily.search(
            query=query, topic="news", days=2,
            max_results=8, search_depth="advanced",
        )
        return resp.get("results", [])
    except Exception as e:
        log.warning(f"[news] Search failed (days=2): {e}")
        return []


def _pick_best(items: list) -> dict:
    """选择最佳新闻条目：国内媒体优先 + 正能量内容优先。"""
    def _score(item):
        s = item.get("score", 0)
        url = item.get("url", "")
        text = f"{item.get('title', '')} {item.get('content', '')}"

        # 国内媒体加分更多 (+0.5)
        if any(src in url for src in DOMESTIC_SOURCES):
            s += 0.5
        # 国际知名媒体也加分但较少 (+0.15)
        elif any(src in url for src in INTERNATIONAL_SOURCES):
            s += 0.15

        # 正能量加分（最多 +1.0）
        s += _positive_score(text)

        return s

    return max(items, key=_score)


def _placeholder_news(cat: str) -> dict:
    return {
        "category": cat,
        "headline": f"No recent {cat} news found",
        "content": f"Unable to find {cat} news from the past 24-48 hours.",
        "url": "",
    }


# ─────────────────────────────────────────────
# Module 2: Content Generation (DeepSeek)
# ─────────────────────────────────────────────


def generate_content(client: OpenAI, news_item: dict) -> dict:
    cat = news_item["category"]
    log.info(f"[llm] Generating content for {cat}: {news_item['headline'][:50]}")

    user_msg = (
        f"Category: {cat}\n"
        f"Headline: {news_item['headline']}\n"
        f"Content: {news_item['content'][:1500]}\n\n"
        f"Remember: This is for children! Keep it positive and uplifting. "
        f"If the news has any negative aspects, REFRAME them positively."
    )

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": DEEPSEEK_SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        raw = resp.choices[0].message.content
        data = json.loads(raw)
        _validate_content(data)

        # ── 最终安全审核 ──
        data = _safety_review(data, client, cat)

        data["category"] = cat
        data["headline"] = news_item["headline"]
        data["source_url"] = news_item["url"]
        return data
    except Exception as e:
        log.error(f"[llm] Failed for {cat}: {e}")
        return _fallback_content(news_item)


def _safety_review(data: dict, client: OpenAI, cat: str) -> dict:
    """对 LLM 生成的内容做最终安全审查，如有负面内容则请求重写。"""
    # 拼接所有文本字段用于检查
    all_text = " ".join([
        data.get("english_summary", ""),
        data.get("chinese_translation", ""),
        data.get("background_en", ""),
        data.get("background_cn", ""),
        data.get("comic_prompt", ""),
    ])

    if not _contains_negative_content(all_text):
        log.info(f"[safety] Content for {cat} passed safety review ✅")
        return data

    # 内容仍有负面元素，请求 LLM 重写
    log.warning(f"[safety] Content for {cat} contains negative elements, requesting rewrite...")

    rewrite_prompt = (
        f"The following content was generated for a children's English learning card, "
        f"but it still contains negative or scary elements. Please REWRITE it to be "
        f"completely positive, cheerful, and suitable for 12-year-old students.\n\n"
        f"Original content:\n{json.dumps(data, ensure_ascii=False, indent=2)}\n\n"
        f"Rules:\n"
        f"- Remove ALL references to death, violence, accidents, disasters, crime\n"
        f"- Focus on positive aspects: achievements, hope, teamwork, progress\n"
        f"- Keep the same JSON structure\n"
        f"- The vocabulary words MUST still appear in the english_summary\n"
        f"- Return ONLY valid JSON"
    )

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": DEEPSEEK_SYSTEM_PROMPT},
                {"role": "user", "content": rewrite_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        raw = resp.choices[0].message.content
        rewritten = json.loads(raw)
        _validate_content(rewritten)
        log.info(f"[safety] Content for {cat} rewritten successfully ✅")
        return rewritten
    except Exception as e:
        log.warning(f"[safety] Rewrite failed for {cat}: {e}, using original with warning")
        return data


def _validate_content(data: dict):
    required = ["english_summary", "chinese_translation", "vocabulary", "comic_prompt",
                 "background_en", "background_cn"]
    for field in required:
        if field not in data or not data[field]:
            raise ValueError(f"Missing or empty field: {field}")
    if len(data["vocabulary"]) < 5:
        raise ValueError(
            f"Need ≥5 vocabulary words, got {len(data['vocabulary'])}"
        )
    for w in data["vocabulary"]:
        for k in ("word", "phonetic", "chinese", "pos"):
            if k not in w:
                raise ValueError(f"Vocabulary word missing field: {k}")


def _fallback_content(news_item: dict) -> dict:
    return {
        "category": news_item["category"],
        "headline": news_item["headline"],
        "english_summary": news_item["headline"],
        "chinese_translation": news_item["headline"],
        "vocabulary": [
            {"word": "news", "phonetic": "/njuːz/", "chinese": "新闻", "pos": "n."},
            {"word": "report", "phonetic": "/rɪˈpɔːrt/", "chinese": "报道", "pos": "n."},
            {"word": "global", "phonetic": "/ˈɡloʊbəl/", "chinese": "全球的", "pos": "adj."},
            {"word": "update", "phonetic": "/ʌpˈdeɪt/", "chinese": "更新", "pos": "v."},
            {"word": "breaking", "phonetic": "/ˈbreɪkɪŋ/", "chinese": "突发的", "pos": "adj."},
        ],
        "background_en": news_item["content"][:200] if news_item.get("content") else "",
        "background_cn": "",
        "comic_prompt": f"A newsroom scene with journalists reporting on {news_item['category']} news.",
        "source_url": news_item["url"],
    }


# ─────────────────────────────────────────────
# Module 3: Comic Generation (OpenRouter)
# ─────────────────────────────────────────────


def generate_comic(
    client: OpenAI, content: dict, model: str, output_dir: Path, date_str: str
) -> Path:
    cat = content["category"]
    words = [w["word"] for w in content["vocabulary"][:5]]
    word_list = ", ".join(words)

    prompt = (
        f"{COMIC_STYLE_PREFIX}"
        f"The 5 words to include are: {word_list}. "
        f"Scene description: {content['comic_prompt']} "
    )

    log.info(f"[img] Generating comic for {cat} with model {model}")

    for attempt in range(3):
        try:
            img_data = _call_openrouter(client, model, prompt)
            if img_data:
                path = output_dir / f"comic_{cat}_{date_str}.png"
                img_data.save(str(path))
                log.info(f"[img] Saved: {path}")
                return path
        except Exception as e:
            wait = 2 ** (attempt + 1)
            log.warning(f"[img] Attempt {attempt + 1} failed for {cat}: {e}")
            if attempt < 2:
                log.info(f"[img] Retrying in {wait}s...")
                time.sleep(wait)

    log.error(f"[img] All retries exhausted for {cat}, using placeholder")
    return _create_placeholder_image(cat, output_dir, date_str)


def _call_openrouter(client: OpenAI, model: str, prompt: str) -> Image.Image | None:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        extra_body={"modalities": ["image", "text"]},
    )

    msg = resp.choices[0].message

    # Case 1: images in model_extra (Gemini via OpenRouter)
    extras = getattr(msg, "model_extra", None) or {}
    images = extras.get("images")
    if images and isinstance(images, list):
        for img_part in images:
            if isinstance(img_part, dict) and img_part.get("type") == "image_url":
                url = img_part["image_url"]["url"]
                return _decode_image_url(url)

    # Case 2: content is a list of parts (multimodal response)
    if isinstance(msg.content, list):
        for part in msg.content:
            if isinstance(part, dict):
                if part.get("type") == "image_url":
                    url = part["image_url"]["url"]
                    return _decode_image_url(url)
                elif part.get("type") == "image":
                    b64 = part.get("data") or part.get("image", "")
                    return _decode_b64(b64)

    # Case 3: content is a string – look for inline base64 or URL
    text = msg.content if isinstance(msg.content, str) else str(msg.content or "")

    b64_match = re.search(
        r"data:image/(?:png|jpeg|webp);base64,([A-Za-z0-9+/=]+)", text
    )
    if b64_match:
        return _decode_b64(b64_match.group(1))

    url_match = re.search(r"(https?://\S+\.(?:png|jpg|jpeg|webp))", text)
    if url_match:
        return _download_image(url_match.group(1))

    raise ValueError("No image found in OpenRouter response")


def _decode_image_url(url: str) -> Image.Image:
    if url.startswith("data:"):
        _, b64 = url.split(",", 1)
        return _decode_b64(b64)
    return _download_image(url)


def _decode_b64(b64: str) -> Image.Image:
    data = base64.b64decode(b64)
    return Image.open(io.BytesIO(data)).convert("RGBA")


def _download_image(url: str) -> Image.Image:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return Image.open(io.BytesIO(resp.content)).convert("RGBA")


def _create_placeholder_image(cat: str, output_dir: Path, date_str: str) -> Path:
    color = CATEGORY_COLORS.get(cat, (128, 128, 128))
    img = Image.new("RGB", (CARD_W, COMIC_H), color)
    draw = ImageDraw.Draw(img)
    label = CATEGORY_LABELS.get(cat, cat.upper())
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        ((CARD_W - tw) // 2, (COMIC_H - th) // 2),
        label, fill="white", font=font,
    )
    path = output_dir / f"comic_{cat}_{date_str}.png"
    img.save(str(path))
    return path


# ─────────────────────────────────────────────
# Module 4: Card Compositing (Pillow)
# ─────────────────────────────────────────────

_font_cache: dict[str, ImageFont.FreeTypeFont] = {}

NOTO_SANS_URL = "https://github.com/google/fonts/raw/main/ofl/notosans/NotoSans%5Bwdth%2Cwght%5D.ttf"
NOTO_SANS_SC_URL = "https://github.com/googlefonts/noto-cjk/releases/download/Sans2.004/08_NotoSansCJKsc.zip"
NOTO_SANS_SC_TTF = "NotoSansCJKsc-Regular.otf"

SYSTEM_FONT_DIRS = [
    "/usr/share/fonts",
    "/usr/local/share/fonts",
    str(Path.home() / ".fonts"),
    str(Path.home() / ".local/share/fonts"),
    "/System/Library/Fonts",
    "/Library/Fonts",
    "C:\\Windows\\Fonts",
]


def _find_system_font(patterns: list[str]) -> str | None:
    for d in SYSTEM_FONT_DIRS:
        p = Path(d)
        if not p.exists():
            continue
        for f in p.rglob("*.[to]tf"):
            name = f.name.lower()
            if any(pat in name for pat in patterns):
                return str(f)
    return None


def _download_font(url: str, filename: str) -> str | None:
    FONT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = FONT_CACHE_DIR / filename
    if cached.exists():
        return str(cached)

    log.info(f"[font] Downloading {filename}...")
    try:
        resp = requests.get(url, timeout=60, allow_redirects=True)
        resp.raise_for_status()

        if url.endswith(".zip"):
            import zipfile
            with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
                for name in zf.namelist():
                    if name.lower().endswith((".otf", ".ttf")) and "regular" in name.lower():
                        with zf.open(name) as src:
                            cached.write_bytes(src.read())
                            return str(cached)
                for name in zf.namelist():
                    if name.lower().endswith((".otf", ".ttf")):
                        with zf.open(name) as src:
                            cached.write_bytes(src.read())
                            return str(cached)
        else:
            cached.write_bytes(resp.content)
            return str(cached)
    except Exception as e:
        log.warning(f"[font] Download failed: {e}")
    return None


def get_font(size: int, bold: bool = False, cjk: bool = False) -> ImageFont.FreeTypeFont:
    key = f"{'cjk' if cjk else 'latin'}_{size}_{'b' if bold else 'r'}"
    if key in _font_cache:
        return _font_cache[key]

    font_path = None

    if cjk:
        font_path = _find_system_font([
            "notosanscjk", "notosanssc", "noto sans cjk", "msyh", "simhei",
            "pingfang", "hiragino", "wqy", "sourcehansans",
        ])
        if not font_path:
            font_path = _download_font(NOTO_SANS_SC_URL, NOTO_SANS_SC_TTF)
    else:
        patterns = (
            ["notosans-bold", "notosans_bold", "arial_bold", "arialbd"]
            if bold
            else ["notosans-regular", "notosans_regular", "notosans[", "arial.ttf", "liberationsans"]
        )
        font_path = _find_system_font(patterns)
        if not font_path:
            font_path = _download_font(NOTO_SANS_URL, "NotoSans.ttf")

    if font_path:
        try:
            font = ImageFont.truetype(font_path, size)
            _font_cache[key] = font
            return font
        except Exception as e:
            log.warning(f"[font] Failed to load {font_path}: {e}")

    log.warning("[font] Using default font")
    font = ImageFont.load_default()
    _font_cache[key] = font
    return font


def composite_card(
    comic_path: Path, content: dict, output_dir: Path, date_str: str
) -> Path:
    cat = content["category"]
    log.info(f"[card] Compositing card for {cat}")

    # Use a tall temporary canvas; we'll crop to actual content height later.
    MAX_H = 2400
    card = Image.new("RGBA", (CARD_W, MAX_H), (255, 255, 255, 255))
    vocab = content.get("vocabulary", [])[:5]
    accent = CATEGORY_COLORS.get(cat, (52, 152, 219))

    # -- Comic area (words already integrated by AI) --
    try:
        comic = Image.open(str(comic_path)).convert("RGBA")
    except Exception:
        comic = Image.new("RGBA", (CARD_W, COMIC_H), accent + (255,))

    comic = _fill_crop(comic, CARD_W, COMIC_H)
    card.paste(comic, (0, 0))

    # -- Gradient transition from comic to panel --
    gradient = Image.new("RGBA", (CARD_W, GRADIENT_OVERLAP), (0, 0, 0, 0))
    for y in range(GRADIENT_OVERLAP):
        alpha = int(240 * (y / GRADIENT_OVERLAP))
        for x in range(CARD_W):
            gradient.putpixel((x, y), (255, 255, 255, alpha))
    card.paste(gradient, (0, COMIC_H - GRADIENT_OVERLAP), gradient)

    draw = ImageDraw.Draw(card)
    y_cur = COMIC_H + 12

    # -- Category badge (playful rounded pill) --
    en_label = CATEGORY_LABELS.get(cat, cat.upper())
    cat_cn = CATEGORY_CN.get(cat, "")
    badge_font = get_font(20, bold=True)
    cjk_badge_font = get_font(18, cjk=True)

    en_part = f"  {en_label} "
    en_bbox = draw.textbbox((0, 0), en_part, font=badge_font)
    en_w = en_bbox[2] - en_bbox[0]
    en_h = en_bbox[3] - en_bbox[1]
    en_top = en_bbox[1]

    cn_part = f" {cat_cn}  " if cat_cn else ""
    cn_w, cn_h, cn_top = 0, 0, 0
    if cn_part:
        cn_bbox = draw.textbbox((0, 0), cn_part, font=cjk_badge_font)
        cn_w = cn_bbox[2] - cn_bbox[0]
        cn_h = cn_bbox[3] - cn_bbox[1]
        cn_top = cn_bbox[1]

    pad_y = 10
    total_w = en_w + cn_w
    pill_h = max(en_h, cn_h) + pad_y * 2
    _draw_rounded_rect(
        draw, (32, y_cur, 32 + total_w, y_cur + pill_h),
        radius=pill_h // 2, fill=accent,
    )
    en_y = y_cur + (pill_h - en_h) // 2 - en_top
    draw.text((32, en_y), en_part, fill="white", font=badge_font)
    if cn_part:
        cn_y = y_cur + (pill_h - cn_h) // 2 - cn_top
        draw.text(
            (32 + en_w, cn_y), cn_part,
            fill=(255, 255, 255, 200), font=cjk_badge_font,
        )

    # Date on right side, vertically aligned with badge
    date_font = get_font(16)
    date_bbox = draw.textbbox((0, 0), date_str, font=date_font)
    date_w = date_bbox[2] - date_bbox[0]
    date_h = date_bbox[3] - date_bbox[1]
    date_top = date_bbox[1]
    date_y = y_cur + (pill_h - date_h) // 2 - date_top
    draw.text(
        (CARD_W - 36 - date_w, date_y), date_str,
        fill=(160, 160, 160), font=date_font,
    )
    y_cur += pill_h + 16

    # -- English summary (dark text, lively) --
    en_font = get_font(24, bold=True)
    en_text = content.get("english_summary", content.get("headline", ""))
    y_cur = _draw_wrapped_text(
        draw, en_text, (36, y_cur), CARD_W - 72,
        font=en_font, fill=(30, 30, 50), line_spacing=8,
    )
    y_cur += 6

    # -- Chinese translation (gray, slightly smaller) --
    cn_font = get_font(20, cjk=True)
    cn_text = content.get("chinese_translation", "")
    if cn_text:
        y_cur = _draw_wrapped_text(
            draw, cn_text, (36, y_cur), CARD_W - 72,
            font=cn_font, fill=(100, 100, 110), line_spacing=5,
        )
    y_cur += 16

    # -- Vocabulary cards row --
    _draw_vocab_cards(draw, card, vocab, y_cur, accent)
    y_cur += 80 + 20  # card_h + spacing

    # -- News background + source link --
    bg_en = content.get("background_en", "")
    bg_cn = content.get("background_cn", "")
    source_url = content.get("source_url", "")
    y_cur = _draw_news_bottom_section(
        draw, y_cur, bg_en, bg_cn, source_url, accent
    )

    # -- Brand logo: 萱媛背单词 (at comic/text boundary) --
    _draw_brand_logo(draw, card, accent)

    # -- Crop to actual content height (remove blank bottom) --
    final_h = y_cur + BOTTOM_PADDING
    card = card.crop((0, 0, CARD_W, final_h))

    # -- Save --
    final = card.convert("RGB")
    out_path = output_dir / f"card_{cat}_{date_str}.png"
    final.save(str(out_path), quality=95)
    log.info(f"[card] Saved: {out_path} ({CARD_W}x{final_h})")
    return out_path


# ── News bottom section (summary + background) ──


def _draw_section_title(
    draw: ImageDraw.ImageDraw, y: int,
    en_label: str, cn_label: str, accent: tuple,
) -> int:
    """Draw a centered bilingual section title and return new y."""
    title_en_font = get_font(14, bold=True)
    title_cn_font = get_font(14, cjk=True)

    en_bb = draw.textbbox((0, 0), en_label, font=title_en_font)
    cn_bb = draw.textbbox((0, 0), cn_label, font=title_cn_font)
    en_w = en_bb[2] - en_bb[0]
    cn_w = cn_bb[2] - cn_bb[0]
    en_h = en_bb[3] - en_bb[1]
    cn_h = cn_bb[3] - cn_bb[1]
    row_h = max(en_h, cn_h)

    tx = (CARD_W - (en_w + cn_w)) // 2
    draw.text((tx, y + (row_h - en_h) // 2 - en_bb[1]), en_label,
              fill=accent, font=title_en_font)
    draw.text((tx + en_w, y + (row_h - cn_h) // 2 - cn_bb[1]), cn_label,
              fill=accent, font=title_cn_font)
    return y + row_h + 10


def _draw_divider(draw: ImageDraw.ImageDraw, y: int, margin_x: int = 36) -> int:
    """Draw a subtle horizontal divider line and return new y."""
    draw.line(
        [(margin_x + 10, y), (CARD_W - margin_x - 10, y)],
        fill=(220, 220, 225), width=1,
    )
    return y + 12


def _draw_news_bottom_section(
    draw: ImageDraw.ImageDraw, y: int,
    bg_en: str, bg_cn: str, source_url: str, accent: tuple,
) -> int:
    """Draw News Background section with source link."""
    margin_x = 36
    max_w = CARD_W - margin_x * 2

    # ── News Background ──
    if bg_en or bg_cn:
        y = _draw_divider(draw, y, margin_x)
        y = _draw_section_title(draw, y, "NEWS BACKGROUND / ", "新闻背景", accent)

        if bg_en:
            en_font = get_font(15)
            y = _draw_wrapped_text(
                draw, bg_en, (margin_x, y), max_w,
                font=en_font, fill=(80, 80, 90), line_spacing=5,
                max_lines=10,
            )
            y += 8

        if bg_cn:
            cn_font = get_font(14, cjk=True)
            y = _draw_wrapped_text(
                draw, bg_cn, (margin_x, y), max_w,
                font=cn_font, fill=(120, 120, 130), line_spacing=5,
                max_lines=10,
            )
            y += 10

    # ── Source Link ──
    if source_url:
        y += 4
        link_font = get_font(12)
        link_label = f"Source: {source_url}"
        y = _draw_wrapped_text(
            draw, link_label, (margin_x, y), max_w,
            font=link_font, fill=(150, 150, 165), line_spacing=4,
            max_lines=2,
        )

    return y


# ── Brand logo ──


def _draw_brand_logo(
    draw: ImageDraw.ImageDraw, card: Image.Image, accent: tuple,
):
    """Draw '萱媛背单词' brand logo at comic/text boundary line."""
    logo_icon = "\u2606"
    logo_text = " 萱媛背单词 "
    full_text = f"{logo_icon}{logo_text}{logo_icon}"

    logo_cjk_font = get_font(22, cjk=True)

    tb = draw.textbbox((0, 0), full_text, font=logo_cjk_font)
    tw = tb[2] - tb[0]
    th = tb[3] - tb[1]
    t_top = tb[1]

    pad_x, pad_y = 18, 8
    pill_w = tw + pad_x * 2
    pill_h = th + pad_y * 2

    logo_x = (CARD_W - pill_w) // 2
    logo_y = COMIC_H - pill_h // 2

    _draw_rounded_rect(
        draw, (logo_x - 2, logo_y - 2, logo_x + pill_w + 2, logo_y + pill_h + 2),
        radius=(pill_h + 4) // 2, fill=(255, 255, 255),
    )
    _draw_rounded_rect(
        draw, (logo_x, logo_y, logo_x + pill_w, logo_y + pill_h),
        radius=pill_h // 2, fill=accent,
    )
    text_x = logo_x + (pill_w - tw) // 2
    text_y = logo_y + (pill_h - th) // 2 - t_top
    draw.text((text_x, text_y), full_text, fill=(255, 255, 255), font=logo_cjk_font)


# ── Word bubbles overlay on comic ──

BUBBLE_POSITIONS = [
    (30, 16),
    (750, 16),
    (30, 770),
    (350, 830),
    (720, 770),
]

BUBBLE_COLORS = [
    (255, 87, 51),   # coral red
    (46, 204, 113),  # emerald
    (52, 152, 219),  # sky blue
    (155, 89, 182),  # amethyst
    (241, 196, 15),  # sunflower
]


def _overlay_word_bubbles(comic: Image.Image, vocab: list, accent: tuple):
    overlay = Image.new("RGBA", comic.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    word_font = get_font(30, bold=True)

    for i, v in enumerate(vocab[:5]):
        word = v.get("word", "")
        label = f" {word} "

        bx, by = BUBBLE_POSITIONS[i % len(BUBBLE_POSITIONS)]
        color = BUBBLE_COLORS[i % len(BUBBLE_COLORS)]

        bbox = draw.textbbox((0, 0), label, font=word_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        t_top = bbox[1]

        bubble_w = tw + 28
        bubble_h = th + 24

        _draw_rounded_rect(
            draw, (bx + 3, by + 3, bx + bubble_w + 3, by + bubble_h + 3),
            radius=16, fill=(0, 0, 0, 60),
        )
        _draw_rounded_rect(
            draw, (bx, by, bx + bubble_w, by + bubble_h),
            radius=16, fill=color + (230,),
        )
        tx = bx + (bubble_w - tw) // 2
        ty = by + (bubble_h - th) // 2 - t_top
        draw.text((tx, ty), label, fill=(255, 255, 255), font=word_font)

    comic.paste(Image.alpha_composite(
        Image.new("RGBA", comic.size, (0, 0, 0, 0)), overlay
    ), (0, 0), overlay)


# ── Vocabulary cards row (bottom panel) ──


def _draw_vocab_cards(
    draw: ImageDraw.ImageDraw, card: Image.Image,
    vocab: list, y: int, accent: tuple
) -> int:
    if not vocab:
        return y

    word_font = get_font(18, bold=True)
    phonetic_font = get_font(13)
    cjk_font = get_font(15, cjk=True)
    pos_font = get_font(12)

    count = min(len(vocab), 5)
    gap = 10
    card_w = (CARD_W - 36 * 2 - gap * (count - 1)) // count
    card_h = 80
    x = 36

    soft_colors = [
        (255, 243, 224),  # warm peach
        (224, 247, 236),  # mint
        (227, 237, 252),  # soft blue
        (243, 229, 252),  # lavender
        (255, 248, 225),  # cream yellow
    ]

    for i, v in enumerate(vocab[:count]):
        bg = soft_colors[i % len(soft_colors)]
        _draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), radius=14, fill=bg)

        word = v.get("word", "")
        phonetic = v.get("phonetic", "")
        chinese = v.get("chinese", "")
        pos = v.get("pos", "")
        cx = x + card_w // 2

        # Measure all three rows to compute total content height
        wp_text = f"{word} {pos}" if pos else word
        wp_bb = draw.textbbox((0, 0), wp_text, font=word_font)
        wp_h = wp_bb[3] - wp_bb[1]

        ph_bb = draw.textbbox((0, 0), phonetic, font=phonetic_font)
        ph_h = ph_bb[3] - ph_bb[1]

        cn_bb = draw.textbbox((0, 0), chinese, font=cjk_font)
        cn_h = cn_bb[3] - cn_bb[1]

        row_gap = 4
        total_content_h = wp_h + ph_h + cn_h + row_gap * 2
        start_y = y + (card_h - total_content_h) // 2

        # Row 1: Word + POS (horizontally + vertically centered)
        wp_w = wp_bb[2] - wp_bb[0]
        row1_x = cx - wp_w // 2
        row1_y = start_y - wp_bb[1]
        draw.text((row1_x, row1_y), word, fill=accent, font=word_font)
        if pos:
            w_only_bb = draw.textbbox((0, 0), word, font=word_font)
            w_only_w = w_only_bb[2] - w_only_bb[0]
            pos_bb = draw.textbbox((0, 0), pos, font=pos_font)
            pos_h = pos_bb[3] - pos_bb[1]
            pos_y = start_y + (wp_h - pos_h) // 2 - pos_bb[1]
            draw.text((row1_x + w_only_w + 4, pos_y), pos, fill=(150, 150, 150), font=pos_font)

        # Row 2: Phonetic (centered)
        ph_w = ph_bb[2] - ph_bb[0]
        row2_y = start_y + wp_h + row_gap - ph_bb[1]
        draw.text((cx - ph_w // 2, row2_y), phonetic, fill=(120, 120, 130), font=phonetic_font)

        # Row 3: Chinese (centered)
        cn_w = cn_bb[2] - cn_bb[0]
        row3_y = start_y + wp_h + ph_h + row_gap * 2 - cn_bb[1]
        draw.text((cx - cn_w // 2, row3_y), chinese, fill=(60, 60, 70), font=cjk_font)

        x += card_w + gap

    return y + card_h


def _fill_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    src_w, src_h = img.size
    # Fit the entire image into the target area (no cropping, add padding if needed)
    src_ratio = src_w / src_h
    tgt_ratio = target_w / target_h

    if abs(src_ratio - tgt_ratio) < 0.15:
        # Close enough ratio — scale to fill and center-crop
        scale = max(target_w / src_w, target_h / src_h)
        new_w, new_h = int(src_w * scale), int(src_h * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 3  # bias toward top to keep main subject
        return img.crop((left, top, left + target_w, top + target_h))
    else:
        # Very different ratio — fit inside and pad with blurred background
        bg = img.copy().resize((target_w, target_h), Image.LANCZOS)
        try:
            from PIL import ImageFilter
            bg = bg.filter(ImageFilter.GaussianBlur(radius=30))
        except Exception:
            pass
        enhancer_layer = Image.new("RGBA", (target_w, target_h), (255, 255, 255, 120))
        bg = Image.alpha_composite(bg.convert("RGBA"), enhancer_layer)

        scale = min(target_w / src_w, target_h / src_h)
        new_w, new_h = int(src_w * scale), int(src_h * scale)
        img_resized = img.resize((new_w, new_h), Image.LANCZOS)
        paste_x = (target_w - new_w) // 2
        paste_y = (target_h - new_h) // 2
        bg.paste(img_resized, (paste_x, paste_y), img_resized if img_resized.mode == "RGBA" else None)
        return bg


def _draw_rounded_rect(draw, bbox, radius, fill):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill)


def _draw_wrapped_text(
    draw: ImageDraw.ImageDraw, text: str, pos: tuple,
    max_width: int, font, fill, line_spacing: int = 4,
    max_lines: int = 3,
) -> int:
    x, y = pos
    lines = _wrap_text(text, font, max_width, draw)
    for line in lines[:max_lines]:
        draw.text((x, y), line, fill=fill, font=font)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + line_spacing
    return y


def _has_cjk(text: str) -> bool:
    return any('\u4e00' <= ch <= '\u9fff' for ch in text)


def _wrap_text(text: str, font, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    if _has_cjk(text):
        return _wrap_text_cjk(text, font, max_width, draw)

    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    if not lines:
        lines = [text]
    return lines


def _wrap_text_cjk(text: str, font, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    if not lines:
        lines = [text]
    return lines


# ─────────────────────────────────────────────
# Main Pipeline
# ─────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Generate daily news English learning cards"
    )
    parser.add_argument(
        "--categories", nargs="+", default=DEFAULT_CATEGORIES,
        help="News categories to cover (default: politics finance sports entertainment technology)",
    )
    parser.add_argument(
        "--output-dir", type=str, default=None,
        help="Output directory (default: output/daily-news-cards/{date})",
    )
    args = parser.parse_args()

    start_time = time.time()
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    # 秒级时间戳用于文件名，避免同一天多次生成互相覆盖
    timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path("output") / "daily-news-cards" / date_str
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Daily News English Cards Generator")
    print(f"  Date: {date_str}")
    print(f"  Timestamp: {timestamp_str}")
    print(f"  Categories: {', '.join(args.categories)}")
    print(f"  Output: {output_dir}")
    print(f"{'='*60}\n")

    # Init clients
    tavily, deepseek, openrouter, image_model = init_clients()

    # Phase 1: Fetch news (国内媒体优先 + 内容安全过滤)
    print(f"\n📰 Phase 1/4: Fetching news (domestic preferred + safety filter)...")
    news_items = fetch_news(tavily, args.categories)
    domestic_count = sum(1 for n in news_items if n.get("source_type") == "domestic")
    intl_count = len(news_items) - domestic_count
    print(f"   Found {len(news_items)} safe news items (🇨🇳 domestic: {domestic_count}, 🌍 international: {intl_count})")
    print(f"   🛡️ Content safety filter: active\n")

    # Phase 2: Generate learning content (正能量引导 + 安全审核)
    print(f"📝 Phase 2/4: Generating learning content via DeepSeek (positive tone)...")
    contents = []
    for item in news_items:
        c = generate_content(deepseek, item)
        contents.append(c)
        print(f"   ✓ {item['category']}: {len(c.get('vocabulary', []))} words")
    print()

    # Phase 3: Generate comic illustrations
    print(f"🎨 Phase 3/4: Generating comics via OpenRouter ({image_model})...")
    comic_paths = []
    for c in contents:
        path = generate_comic(openrouter, c, image_model, output_dir, timestamp_str)
        comic_paths.append(path)
        print(f"   ✓ {c['category']}: {path.name}")
    print()

    # Phase 4: Composite final cards
    print(f"🖼️  Phase 4/4: Compositing final cards...")
    card_paths = []
    for c, cp in zip(contents, comic_paths):
        path = composite_card(cp, c, output_dir, timestamp_str)
        card_paths.append(path)
        print(f"   ✓ {c['category']}: {path.name}")

    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"  ✅ Complete! Generated {len(card_paths)} cards in {elapsed:.1f}s")
    print(f"{'='*60}")
    print(f"\n  Output directory: {output_dir}")
    for p in card_paths:
        print(f"    • {p}")
    print()

    # Save content JSON for reference
    json_path = output_dir / f"content_{timestamp_str}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(contents, f, ensure_ascii=False, indent=2)
    print(f"  Content data: {json_path}\n")


if __name__ == "__main__":
    main()
