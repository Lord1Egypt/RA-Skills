#!/usr/bin/env python3
"""
Amber-Hunter v1.2.41
Huper琥珀本地感知引擎

兼容 huper v1.0.0（DID 身份层）
P1-2: Multi-Embedding | P1-3: Recall Cooldown | P2-2: Pattern Detection | P2-3: Cross-device Sync
v1.2.41: RAG 升级 — BGE-M3 embedding + BM25 + Cross-Encoder Reranker + HyDE + Multi-Hop
v1.2.38: Knowledge Compiler — wiki markdown + wikilinks concept pages, auto-compile daemon
v1.2.34: /ingest deduplication — content_hash exact dedup + semantic similarity soft dedup
"""
from __future__ import annotations

import os, sys, json, time, secrets, sqlite3, hashlib, base64, gc, threading, logging, traceback
from pathlib import Path
from typing import Optional

HOME = Path.home()  # moved from line ~811 to fix forward-reference NameError

# ── 核心模块 ────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
from core.crypto import derive_key, encrypt_content, decrypt_content, generate_salt, derive_capsule_key
from core.keychain import (
    get_master_password, set_master_password,
    get_api_token, get_huper_url,
    ensure_config_dir, CONFIG_PATH,
    get_os, is_headless,
)
from core.db import (init_db, insert_capsule, get_capsule, list_capsules, count_capsules, mark_synced,
    get_unsynced_capsules, get_config, set_config,
    queue_insert, queue_list_pending, queue_get, queue_set_status, queue_update,
    insert_memory_hit, update_capsule_hit,
    save_tag_feedback, get_tag_feedback,
    _get_conn)
from core.vector import index_capsule, search_vectors, delete_vector, get_vector_stats
from core.embedding import find_snippets
from core.db import record_recall_session_genes, get_genes_for_capsule, find_capsule_by_content_hash, find_similar_capsules
from core.wal import write_wal_entry, read_wal_entries, get_wal_stats, wal_gc, _detect_signal_type
from core.session import get_current_session_key, build_session_summary, get_recent_files, read_session_messages
from core.models import CapsuleIn, CapsuleUpdate
from core.llm import get_llm, LLM_AVAILABLE as LLM_READY, load_llm_config, save_llm_config, LLMConfig

# ── FastAPI ─────────────────────────────────────────────
import uvicorn
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware as StarletteCORSMiddleware
from starlette.responses import Response

# ── 语义模型缓存（模块级，只加载一次）────────────────────
_EMBED_MODEL = None
_SEMANTIC_AVAILABLE = None  # 缓存语义搜索可用性检查结果
_MODEL_LOADING = False      # 是否正在加载中
_MODEL_LOAD_ERROR = None    # 加载失败原因
_MODEL_LOAD_LOCK = threading.Lock()  # 防止并发重复加载


# ── 通用辅助函数 ─────────────────────────────────────────
def _extract_bearer_token(request, authorization: str = None) -> str:
    """
    从请求中提取 Bearer token。
    优先级：query_param.token > Authorization header
    返回格式化的 'Bearer xxx' 字符串。
    """
    raw_token = request.query_params.get("token") if request else None
    if not raw_token:
        raw_token = authorization
    else:
        raw_token = f"Bearer {raw_token}"
    return raw_token


# ── MFS 路径推断 v1.2.11 ─────────────────────────────────
# 分级路径索引：按 category_path 组织胶囊，支持路径前缀搜索

_MFS_PATH_KEYWORDS = {
    "projects/amber-hunter": ["amber-hunter", "skill", "openclaw", "mcp", "amber hunter"],
    "projects/huper": ["huper", "琥珀", "huper.org", "网站", "部署", "nginx"],
    "projects/wake-fog": ["wake-fog", "品牌", "品牌项目"],
    "knowledge/python": ["python", "pip", "venv", "import", "pip install", "conda"],
    "knowledge/devops": ["ssh", "linux", "docker", "systemctl", "nginx", "vps", "部署"],
    "knowledge/llm": ["gpt", "claude", "gemini", "模型", "token", "prompt", "llm", "openai"],
    "knowledge/macos": ["macos", "homebrew", "brew", "osx"],
    "reflections/daily": ["今天", "复盘", "总结", "日报", "每日", "daily"],
    "reflections/weekly": ["本周", "周总结", "weekly", "周报"],
    "context/vps-sessions": ["ssh", "root@", "vps", "sshpass", "服务器"],
    "context/error-debugs": ["错误", "bug", "error", "调试", "修复", "exception", "failed"],
    "people/leo": ["leo", "chen", "安克"],
    "creative/writing": ["写作", "文章", "blog", "post"],
}

def _infer_category_path(memo: str, content: str = "", tags: str = "") -> str:
    """
    根据胶囊内容自动推断 category_path。
    返回最匹配的路径，默认为 'general/default'。
    """
    full_text = f"{memo} {content} {tags}".lower()

    best_match = "general/default"
    best_score = 0

    for path, keywords in _MFS_PATH_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in full_text)
        if score > best_score:
            best_score = score
            best_match = path

    return best_match


def backfill_category_paths(dry_run: bool = True) -> dict:
    """
    一次性脚本：遍历所有胶囊，填充 category_path。
    返回归类统计。
    dry_run=True 时只报告不实际写入。
    """
    from core.db import _get_conn

    conn = _get_conn()
    c = conn.cursor()

    # 只更新 general/default 的胶囊（有明确分类的不动）
    rows = c.execute(
        "SELECT id, memo, content, tags, category_path FROM capsules WHERE category_path = 'general/default'"
    ).fetchall()

    stats = {"total": len(rows), "updated": 0, "by_path": {}}
    for row in rows:
        cap_id, memo, content, tags, old_path = row
        new_path = _infer_category_path(memo or "", content or "", tags or "")

        if new_path != "general/default":
            if not dry_run:
                c.execute(
                    "UPDATE capsules SET category_path = ? WHERE id = ?",
                    (new_path, cap_id)
                )
            stats["updated"] += 1
            stats["by_path"][new_path] = stats["by_path"].get(new_path, 0) + 1

    if not dry_run:
        conn.commit()

    return stats


# ── 本地轻量标签生成（无需网络/ML，关键词匹配）────────────────────────
# ── v0.8.9: 可扩展 Topic 分类系统 ─────────────────────────

# 默认 16 个 topic（用户可在 config.json 里自定义扩展）
DEFAULT_TOPICS = [
    {
        "name": "工作",
        "emoji": "💼",
        "keywords": ["项目", "客户", "周报", "deadline", "需求", "任务", "汇报", "职场", "上班", "老板"],
    },
    {
        "name": "技术",
        "emoji": "⚙️",
        "keywords": ["代码", "bug", "api", "部署", "服务器", "python", "数据库", "架构", "接口", "调试"],
    },
    {
        "name": "学习",
        "emoji": "📚",
        "keywords": ["课程", "教程", "学习", "读书", "研究", "论文", "理解", "概念", "知识点"],
    },
    {
        "name": "创意",
        "emoji": "💡",
        "keywords": ["灵感", "创意", "idea", "想法", "创新", "方案", "思路", "设计", "构思"],
    },
    {
        "name": "偏好",
        "emoji": "❤️",
        "keywords": ["我喜欢", "我一般", "我比较", "i prefer", "i like", "i usually",
                     "我不喜欢", "我偏向", "我的习惯", "我宁愿"],
    },
    {
        "name": "健康",
        "emoji": "🏃",
        "keywords": ["健康", "运动", "锻炼", "睡眠", "减肥", "身体", "医生", "体检", "饮食"],
    },
    {
        "name": "财务",
        "emoji": "💰",
        "keywords": ["钱", "投资", "理财", "收入", "支出", "预算", "存款", "股票", "工资", "报销"],
    },
    {
        "name": "生活",
        "emoji": "🌿",
        "keywords": ["做饭", "吃饭", "天气", "周末", "购物", "家务", "日用品", "生活琐事"],
    },
    {
        "name": "人际",
        "emoji": "🤝",
        "keywords": ["朋友", "同事", "合作", "沟通", "社交", "关系", "聚会", "人情"],
    },
    {
        "name": "家庭",
        "emoji": "🏠",
        "keywords": ["家", "父母", "孩子", "宝宝", "伴侣", "亲人", "结婚", "装修", "育儿"],
    },
    {
        "name": "旅行",
        "emoji": "✈️",
        "keywords": ["旅行", "旅游", "出行", "机票", "酒店", "行程", "签证", "景点", "度假"],
    },
    {
        "name": "娱乐",
        "emoji": "🎬",
        "keywords": ["电影", "音乐", "游戏", "剧", "综艺", "小说", "追剧", "演唱会"],
    },
    {
        "name": "灵感",
        "emoji": "✨",
        "keywords": ["突然想到", "灵感", "一闪", "冒出来", "game changer", "有意思",
                     "没想到", "原来如此", "竟然", " breakthrough"],
    },
    {
        "name": "决策",
        "emoji": "🎯",
        "keywords": ["决定", "确定", "选择", "方案定了", "decided", "going with",
                     "最终方案", "采用", "放弃", "取舍"],
    },
    {
        "name": "情绪",
        "emoji": "🌧️",
        "keywords": ["开心", "高兴", "沮丧", "焦虑", "兴奋", "压力大", "累", "疲惫",
                     "期待", "失望", "感动"],
    },
    {
        "name": "项目",
        "emoji": "📦",
        "keywords": ["项目", "里程碑", "迭代", "上线", "发布", "验收", "需求评审", "PRD"],
    },
]

# 敏感类 topic（必须有明确信号词才打，不能只用关键词命中）
EXPLICIT_ONLY_TOPICS = {"偏好", "情绪", "决策"}


def _get_topics_from_config() -> list[dict]:
    """从 config.json 读取用户自定义 topics，缺失时返回默认 topics."""
    try:
        cfg_path = HOME / ".amber-hunter" / "config.json"
        if cfg_path.exists():
            import json as _json
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = _json.load(f)
            custom = cfg.get("topics", [])
            if custom and isinstance(custom, list) and len(custom) > 0:
                return custom
    except Exception:
        pass
    return DEFAULT_TOPICS


def _get_embed_model(blocking: bool = True):
    """
    P1-2: 获取 EmbedProvider 实例，委托给 core.embedding 模块。
    保留原接口兼容 classify_topics 等内部调用。

    Args:
        blocking: True=同步等待加载完成；False=若正在加载则立即返回 None（不阻塞）
    Returns:
        EmbedProvider 实例或 None
    """
    global _SEMANTIC_AVAILABLE, _EMBED_MODEL
    from core.embedding import get_cached_embed, reset_embed_provider
    try:
        provider = get_cached_embed()
        # MiniLMProvider 在首次 encode 时才真正加载模型；强制触发加载并更新全局状态
        provider.encode(["amber-hunter-init-signal"])
        _EMBED_MODEL = provider._model
        _SEMANTIC_AVAILABLE = True
        return provider
    except Exception as e:
        _MODEL_LOAD_ERROR = str(e)
        _SEMANTIC_AVAILABLE = False
        return None


def _preload_embed_model():
    """后台线程预加载语义模型，不阻塞主线程。"""
    def _background_load():
        try:
            global _EMBED_MODEL
            from core.embedding import get_cached_embed
            provider = get_cached_embed()
            # Force SentenceTransformer lazy-load by encoding a dummy string
            provider.encode(["amber-hunter-wakeup-signal"])
            # Mark model as loaded
            _EMBED_MODEL = provider._model
        except Exception:
            pass
    t = threading.Thread(target=_background_load, daemon=True, name="amber-embed-preload")
    t.start()


def _cosine_sim(a: list, b: list) -> float:
    """计算两个向量的 cosine similarity."""
    import math
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _classify_llm(text: str) -> str:
    """LLM-powered topic classification (v1.2.0).

    Uses MiniMax with extended thinking. May need retry with higher tokens
    if thinking consumes all allocated output tokens.
    """
    if not LLM_READY:
        return ""
    try:
        llm = get_llm()
        if not llm.config.api_key:
            return ""
        prompt = (
            "You are a topic classifier. Given a text in Chinese or English, return 1-3 comma-separated topic tags.\n"
            "Valid tags: 工作,技术,学习,创意,偏好,健康,财务,生活,旅行,家庭,社交,娱乐,灵感,决策,情绪\n"
            "Return ONLY the comma-separated tags on a single line, no explanation.\n"
            "If the text is ambiguous or too short, respond with a single hyphen (-).\n\n"
            f"Text: {text[:500]}\nTags:"
        )
        # Try with 200 tokens first; if no text block appears, retry with 400
        for max_t in (200, 400):
            result = llm.complete(prompt, max_tokens=max_t)
            if result.startswith("[ERROR"):
                return ""
            first_line = result.strip().split("\n")[0].strip()
            if first_line and first_line != "-":
                tags = [t.strip() for t in first_line.split(",") if t.strip()]
                seen = set()
                cleaned = []
                for t in tags:
                    if t and len(t) <= 6 and " " not in t and t not in seen:
                        seen.add(t)
                        cleaned.append(t)
                if cleaned:
                    return ",".join(cleaned[:3])
        return ""
    except Exception:
        return ""


def classify_topics(text: str, existing_tags: str = "") -> str:
    """
    v0.8.9: 可扩展 topic 分类。

    策略：
    1. 关键词匹配（所有用户可用）
    2. 向量模型精调（有模型时）：text vs topic vectors，cosine similarity

    敏感类（偏好/情绪/决策）：必须命中显式关键词，不走向量
    其他类：关键词命中 ≥ 1 → 进入候选；向量 top1 > 0.35 → 加入结果
    最多返回 3 个 topic。
    """
    if not text:
        return existing_tags or ""


# ── v1.2.8: LLM structured memory extraction (Proactive V4) ───────────

_MEMORY_EXTRACT_SYSTEM = """You are a memory analyst. Your task is to extract important, non-obvious facts from a conversation transcript.

Extract memories that are:
- FACT: verifiable information (project names, decisions made, numbers, schedules)
- DECISION: explicit choices or commitments made
- PREFERENCE: expressed likes/dislikes/habits
- ERROR: mistakes, bugs, or failures mentioned
- INSIGHT: non-obvious observations or lessons learned

Rules:
- Only extract memories with importance >= 0.6 (on a 0.0–1.0 scale)
- Return at most 10 memories, sorted by importance descending
- importance = affected_scope × frequency × time_relevance (0.0–1.0)
- tags = max 4 keywords; entities = names/projects/locations found
- Return STRICT JSON only — no markdown, no explanation, no thinking
- If no valuable memories exist, return []"""

_MEMORY_EXTRACT_USER = """Extract structured memories from this conversation:

{conversation}

Existing tags in this user's memory (avoid duplicates, prefer more specific):
{existing_tags}

Return exactly this JSON format:
{{
  "memories": [
    {{
      "type": "fact|decision|preference|error|insight",
      "summary": "one-sentence description of this memory",
      "importance": 0.0-1.0,
      "tags": ["tag1", "tag2"],
      "entities": ["entity1"],
      "expires_at": null
    }}
  ]
}}"""


def _get_existing_tag_context(limit: int = 20) -> str:
    """获取现有标签样本 + 用户修正历史，用于引导 LLM 生成不同标签"""
    db_path = Path.home() / ".amber-hunter" / "hunter.db"
    all_tags = set()

    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        c = conn.cursor()
        rows = c.execute(
            "SELECT tags FROM capsules ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        conn.close()
        for (tags,) in rows:
            for t in (tags or "").split(","):
                t = t.strip()
                if t and not t.startswith("#"):
                    all_tags.add(t.lower())

    # 加入用户修正反馈（用户改过的标签 → 优先用修正后的）
    import json as _json
    feedback_tags = set()
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        c = conn.cursor()
        fb_rows = c.execute(
            "SELECT value FROM config WHERE key LIKE 'tag_feedback:%'"
        ).fetchall()
        conn.close()
        for (val,) in fb_rows:
            try:
                corrections = _json.loads(val)
                for corr in corrections:
                    feedback_tags.add(corr)
            except Exception:
                pass

    combined = all_tags | feedback_tags
    return ", ".join(sorted(combined)) if combined else "（无）"


_TAG_RULES_CACHE: dict | None = None
_TAG_RULES_TTL: float = 0
_TAG_RULES_CACHE_TTL_SEC = 300  # 5 分钟缓存


def _normalize_tag(tag: str) -> str:
    """标签归一化：小写化空格 trim，同义词映射 + 用户校正规则"""
    tag = tag.strip().lower()
    SYNONYMS = {
        "py": "python", "js": "javascript",
        "ml": "ai", "llm": "ai",
        "kecheng": "course", "shu": "book", "book": "book",
        "react": "react", "vue": "vue", "angular": "angular",
        "postgres": "postgresql", "postgres": "postgresql",
        "pg": "postgresql",
    }
    # G1: 应用用户校正规则（缓存 5 分钟）
    global _TAG_RULES_CACHE, _TAG_RULES_TTL
    now = time.time()
    if _TAG_RULES_CACHE is None or (now - _TAG_RULES_TTL) > _TAG_RULES_CACHE_TTL_SEC:
        try:
            from core.db import get_tag_corrections as _gtc
            _TAG_RULES_CACHE = _gtc()
            _TAG_RULES_TTL = now
        except Exception:
            _TAG_RULES_CACHE = {}
    if _TAG_RULES_CACHE and tag in _TAG_RULES_CACHE:
        return _TAG_RULES_CACHE[tag]
    return SYNONYMS.get(tag, tag)


def _parse_hierarchical_tag(tag: str) -> tuple[str, str]:
    """返回 (prefix, value)，如 'project:huper' -> ('project', 'huper')"""
    if ":" in tag:
        parts = tag.split(":", 1)
        return parts[0].strip(), parts[1].strip()
    return "", tag


def _normalize_tags(tags_str: str) -> str:
    """对逗号分隔的标签字符串做归一化处理"""
    if not tags_str:
        return tags_str
    parts = []
    for t in tags_str.split(","):
        t = t.strip()
        if not t:
            continue
        # 去掉 # 前缀（如果有）
        if t.startswith("#"):
            t = t[1:]
        normalized = _normalize_tag(t)
        if normalized:
            parts.append(normalized)
    return ",".join(parts)


def _llm_extract_memories(text: str) -> list[dict]:
    """
    v1.2.8: Use LLM to extract structured memories from raw conversation text.

    Returns a list of memory dicts with keys: type, summary, importance, tags, entities, expires_at.
    Only memories with importance >= 0.6 are returned.
    """
    if not text or not LLM_READY:
        return []
    if len(text.strip()) < 50:
        return []

    try:
        llm = get_llm()
        if not llm.config.api_key:
            return []

        existing_tags = _get_existing_tag_context()
        user_prompt = _MEMORY_EXTRACT_USER.format(conversation=text[:6000], existing_tags=existing_tags)
        raw = llm.acomplete(user_prompt, system=_MEMORY_EXTRACT_SYSTEM,
                             max_tokens=1024, temperature=0.3)
        if raw.startswith("[ERROR"):
            return []

        # Parse JSON response
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            cleaned = "\n".join(lines[1:] if lines[0].startswith("```") else lines)
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
        import json as _json
        data = _json.loads(cleaned)
        memories = data.get("memories", [])

        # Filter: only importance >= 0.6
        filtered = [m for m in memories if isinstance(m, dict) and m.get("importance", 0) >= 0.6]
        # Normalize tags in each memory (dedup + lowercase + synonym)
        for m in filtered:
            raw_tags = m.get("tags", [])
            if isinstance(raw_tags, list):
                normalized = [_normalize_tag(t) for t in raw_tags]
                # Remove duplicates while preserving order
                seen = set()
                unique = []
                for t in normalized:
                    if t and t not in seen:
                        seen.add(t)
                        unique.append(t)
                m["tags"] = unique[:4]  # max 4 tags
        # Sort by importance desc, keep top 10
        filtered.sort(key=lambda x: x.get("importance", 0), reverse=True)
        return filtered[:10]

    except Exception as e:
        import sys
        print(f"[_llm_extract_memories] failed: {e}", file=sys.stderr)
        return []


# ── Knowledge Compiler v1.2.38 ─────────────────────────────────────────────

_WIKI_COMPILER_SYSTEM = """You are a memory analyst building a personal wiki for a second-brain system.
Given capsules from the same topic, generate a structured concept page in markdown.
IMPORTANT: You MUST include a "## Related Capsules" section with wikilinks to EVERY source capsule ID.
Wikilink format: [[capsule_id:short_label]] — one per capsule, no exceptions."""

_WIKI_COMPILER_USER = """path: {path}

source capsules (id | memo):
{capsules_text}

Generate a concise concept page in markdown. Output MUST end with a "### Related" section."""


# ── Legacy Insight prompts (v1.2.17, kept for queue/categorization use) ──────
_INSIGHT_SYSTEM = """You are a memory analyst. Given a collection of memory capsules from the same category, generate a concise structured summary."""

_INSIGHT_USER = """请将以下同路径的记忆胶囊压缩成一段有组织的摘要：

{capsules}

要求：
- 保留核心事实、关键洞察和决策
- 去除重复信息
- 100字以内
- 纯文本，不要列表
- 用连贯的段落叙述"""


def _slug_to_title(path: str) -> str:
    """dev/python → Python"""
    parts = path.split("/")
    last = parts[-1] if parts else path
    return last.replace("-", " ").replace("_", " ").title()


def _generate_wiki_insight(path: str, capsule_ids: list[str], memos: list[str], hotness: float) -> dict | None:
    """
    编译同 path 胶囊为带 wikilinks 的 concept page（v1.2.38）。
    同时生成 wiki_content（markdown）和兼容 summary（纯文本首段）。
    失败返回 None。
    """
    if not memos or not capsule_ids:
        return None
    try:
        llm = get_llm()
        topic_title = _slug_to_title(path)
        capsules_text = "\n".join(f"[{cid}] {m[:200]}" for cid, m in zip(capsule_ids, memos))
        prompt = _WIKI_COMPILER_USER.format(
            path=path,
            topic_title=topic_title,
            capsules_text=capsules_text[:2500],
        )
        wiki_content = llm.complete(
            prompt,
            system=_WIKI_COMPILER_SYSTEM.format(topic_title=topic_title),
            max_tokens=1000,
            temperature=0.2,
        )
        if not wiki_content or wiki_content.startswith("[ERROR"):
            return None

        wiki_content = wiki_content.strip()

        # Post-process: 移除 LLM 输出的 "### Related" 尾巴（如果被截断则整段丢弃）
        lines = wiki_content.rsplit("\n", 1)
        if len(lines) > 1 and "related" in lines[-1].lower():
            wiki_content = lines[0].rstrip()

        # 事后插入完整的 Related Capsules wikilinks（LLM 不稳定，代码补全更可靠）
        short_label = topic_title.lower().replace(" ", "-")[:20]
        wikilinks = " ".join(f"[[{cid}:{short_label}]]" for cid in capsule_ids)
        wiki_content = wiki_content.rstrip() + f"\n\n### Related Capsules\n{wikilinks}"

        # 提取纯文本 summary（取非标题行，兼容旧格式）
        body_lines = wiki_content.split("\n")
        summary_parts = [
            l.lstrip("#* -").strip()
            for l in body_lines
            if l.strip() and not l.strip().startswith("#") and "related capsules" not in l.lower()
        ]
        summary = " ".join(summary_parts)[:200]

        import secrets as _secrets
        concept_slug = path.replace("/", "-")

        return {
            "id": _secrets.token_hex(6),
            "capsule_ids": json.dumps(capsule_ids),
            "summary": summary,
            "path": path,
            "concept_slug": concept_slug,
            "wiki_content": wiki_content,
            "hotness_score": hotness,
            "created_at": time.time(),
            "updated_at": time.time(),
        }
    except Exception as e:
        print(f"[_generate_wiki_insight] failed: {e}", file=sys.stderr)
        return None


def _generate_insight(path: str, capsule_ids: list[str], memos: list[str], hotness: float) -> dict | None:
    """
    压缩同路径胶囊为 insight 字典（v1.2.17 旧版，纯文本 summary）。
    失败返回 None。
    """
    if not memos:
        return None
    try:
        llm = get_llm()
        capsules_text = "\n---\n".join(f"[{i+1}] {m}" for i, m in enumerate(memos))
        prompt = _INSIGHT_USER.format(capsules=capsules_text[:3000])
        summary = llm.complete(prompt, system=_INSIGHT_SYSTEM, max_tokens=256, temperature=0.2)
        if summary.startswith("[ERROR"):
            return None
        import secrets as _secrets
        return {
            "id": _secrets.token_hex(6),
            "capsule_ids": json.dumps(capsule_ids),
            "summary": summary.strip(),
            "path": path,
            "hotness_score": hotness,
            "created_at": time.time(),
            "updated_at": time.time(),
        }
    except Exception as e:
        print(f"[_generate_insight] failed: {e}", file=sys.stderr)
        return None


    topics = _get_topics_from_config()
    text_lower = text.lower()
    candidate_topics = []
    topic_scores = {}

    # ── Step 1: 关键词匹配 ────────────────────────────
    for topic in topics:
        name = topic["name"]
        kws = topic.get("keywords", [])
        hit_count = sum(1 for kw in kws if kw.lower() in text_lower)

        # 敏感类：必须显式命中关键词
        if name in EXPLICIT_ONLY_TOPICS:
            if hit_count > 0:
                candidate_topics.append(name)
                topic_scores[name] = 1.0
            continue

        if hit_count > 0:
            candidate_topics.append(name)
            topic_scores[name] = min(hit_count / 2.0, 1.0)  # 归一化 0~1

    # ── Step 2: 向量模型精调（有模型时）───────────────
    model = _get_embed_model()
    if model and text.strip():
        try:
            text_vec = model.encode(text[:1000])  # 截断避免太长
            for topic in topics:
                name = topic["name"]
                # 跳过敏感类（已在上一步处理）
                if name in EXPLICIT_ONLY_TOPICS:
                    continue
                # 用 keywords 作为 topic 向量的代理
                kws = topic.get("keywords", [])
                if not kws:
                    continue
                kw_text = " ".join(kws[:8])  # 最多8个关键词
                topic_vec = model.encode(kw_text)
                sim = _cosine_sim(text_vec.tolist(), topic_vec.tolist())
                if sim > 0.35 and name not in topic_scores:
                    candidate_topics.append(name)
                    topic_scores[name] = sim
                elif sim > topic_scores.get(name, 0):
                    topic_scores[name] = sim
        except Exception:
            pass

    # ── Step 3: 合并已有标签，取 top 3 ─────────────────
    existing = [t.strip() for t in existing_tags.split(",") if t.strip()] if existing_tags else []
    result = list(dict.fromkeys(existing))

    # 按 score 排序，取 top 3（不含已有的）
    for name in sorted(candidate_topics, key=lambda n: topic_scores.get(n, 0), reverse=True)[:3]:
        if name not in result:
            result.append(name)

    return ",".join(result) if result else existing_tags or ""


# 兼容旧名称
_auto_tag_local = classify_topics


# ── DID 胶囊密钥派生（v1.2.22 D2）────────────────────────
DID_CONFIG_PATH = Path.home() / ".amber-hunter" / "did.json"


def _get_did_encryption_key(capsule_id: str) -> tuple:
    """
    获取胶囊加密密钥。
    优先使用 DID 设备私钥派生；无 DID 身份则回退到 PBKDF2。
    返回 (aes_key, key_source, salt_or_None)
    """
    if DID_CONFIG_PATH.exists():
        try:
            cfg = json.loads(DID_CONFIG_PATH.read_text())
            device_priv = cfg.get("device_priv")
            if device_priv:
                aes_key, _ = derive_capsule_key(device_priv, capsule_id)
                return aes_key, "did", None  # DID 密钥不需要 salt
        except Exception:
            pass

    # fallback: PBKDF2
    master_pw = get_master_password()
    if not master_pw:
        raise HTTPException(
            status_code=401,
            detail="未设置 master_password，请先在 huper.org/dashboard 配置"
        )
    salt = generate_salt()
    key = derive_key(master_pw, salt)
    return key, "pbkdf2", salt


def _decrypt_with_did(ciphertext_b64: str, nonce_b64: str, capsule_id: str):
    """尝试使用 DID 设备私钥解密。成功返回明文，失败返回 None。"""
    if not DID_CONFIG_PATH.exists():
        return None
    try:
        cfg = json.loads(DID_CONFIG_PATH.read_text())
        device_priv = cfg.get("device_priv")
        if not device_priv:
            return None
        aes_key, _ = derive_capsule_key(device_priv, capsule_id)
        ct = base64.b64decode(ciphertext_b64)
        nonce = base64.b64decode(nonce_b64)
        plaintext = decrypt_content(ct, aes_key, nonce)
        return plaintext.decode("utf-8") if plaintext else None
    except Exception:
        return None


from pydantic import BaseModel

ensure_config_dir()  # HOME now defined at top of file (line 18)

# ── FastAPI App ────────────────────────────────────────
app = FastAPI(title="Amber Hunter", version="1.2.41")

# CORS：仅允许 huper.org（生产）和 localhost（开发）
# 使用 Starlette CORS middleware（更稳定）
app.add_middleware(
    StarletteCORSMiddleware,
    allow_origins=["https://huper.org", "http://localhost:18998", "http://127.0.0.1:18998"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# ── Private Network Access middleware ──────────────────
# Chrome 要求 HTTPS 页面访问 localhost 时，服务端必须在 OPTIONS 预检及实际响应中
# 返回 Access-Control-Allow-Private-Network: true，否则请求被浏览器直接拦截。
@app.middleware("http")
async def private_network_access_middleware(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response

# ── 认证 ────────────────────────────────────────────────
def verify_token(authorization: str = Header(None)) -> bool:
    """验证本地 API token，防同一机器上其他进程滥用"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization[7:]
    stored = get_api_token()
    if not stored or token != stored:
        raise HTTPException(status_code=401, detail="Invalid API token")
    return True

# ── 通用 CORS 响应头 ──────────────────────────────────
ALLOWED_ORIGINS = [
    "https://huper.org",
    "http://localhost:18998",
    "http://127.0.0.1:18998",
]

def add_cors_headers(request: Request):
    """手动给 Response 添加 CORS origin 头（private-network 由 middleware 处理）"""
    origin = request.headers.get("origin", "")
    h = {}
    if origin in ALLOWED_ORIGINS:
        h["access-control-allow-origin"] = origin
        h["access-control-allow-credentials"] = "true"
    return h

# ── Topic 分类接口（无认证，供 amber-proactive 调用）─────
@app.get("/classify")
def api_classify(request: Request, text: str = ""):
    """对一段文本进行 topic 分类，返回逗号分隔的标签字符串.

    策略：
    1. 关键词匹配（所有用户可用，无网络依赖）
    2. LLM 分类（关键词匹配为空时触发，需要配置 LLM API key）
    """
    headers = add_cors_headers(request)
    if not text or len(text.strip()) < 5:
        return JSONResponse({"topics": ""}, headers=headers)
    topics = classify_topics(text)
    # Fallback to LLM if keyword matching returned little
    if not topics or len(topics.split(",")) < 2:
        topics_llm = _classify_llm(text)
        if topics_llm:
            # Merge without duplicates
            existing = set(t.strip() for t in topics.split(",") if t.strip()) if topics else set()
            new_tags = [t for t in topics_llm.split(",") if t.strip() and t.strip() not in existing]
            all_tags = list(existing) + new_tags
            topics = ",".join(all_tags[:5])
    return JSONResponse({"topics": topics}, headers=headers)


# ── v1.2.8: Proactive V4 — LLM structured memory extraction ─────────
class ExtractIn(BaseModel):
    text: str
    source: str = "unknown"


@app.post("/extract")
async def extract_memories(request: Request, body: ExtractIn, authorization: str = Header(None)):
    """
    LLM-powered structured memory extraction from raw conversation text (Proactive V4).

    Body: {"text": "...", "source": "session_id or description"}
    Returns: {"memories": [{"type": "...", "summary": "...", "importance": 0.0-1.0, "tags": [], "entities": []}]}

    认证：Bearer Token
    """
    headers = add_cors_headers(request)
    if authorization:
        verify_token(authorization)
    if not body.text or len(body.text.strip()) < 50:
        return JSONResponse({"memories": []}, headers=headers)

    memories = _llm_extract_memories(body.text)
    return JSONResponse({"source": body.source, "memories": memories, "count": len(memories)}, headers=headers)


# ── Session 读取（无认证，供前端读取）──────────────────
@app.get("/session/summary")
def session_summary(request: Request):
    headers = add_cors_headers(request)
    session_key = get_current_session_key()
    if not session_key:
        return JSONResponse({"session_key": None, "summary": "未找到活跃 session", "messages": []}, headers=headers)
    return JSONResponse(build_session_summary(session_key), headers=headers)

@app.get("/session/files")
def session_files(request: Request):
    headers = add_cors_headers(request)
    files = get_recent_files(limit=10)
    return JSONResponse({
        "files": files,
        "workspace": str(HOME / ".openclaw" / "workspace")
    }, headers=headers)

# ── B3: 场景预加载记忆 v1.2.18 ────────────────────────────────
@app.get("/session/preload")
def get_session_preload(request: Request, session_id: str = ""):
    """
    返回指定 session 的预加载记忆（供 Agent heartbeat 读取）。
    session_id='' 时返回最新的预加载文件。
    """
    h = add_cors_headers(request)
    preload_dir = HOME / ".amber-hunter" / "preload"
    if not preload_dir.exists():
        return JSONResponse({"scene": "none", "category_path": "", "memories": []}, headers=h)

    if session_id:
        preload_file = preload_dir / f"{session_id}_preload.json"
        if not preload_file.exists():
            return JSONResponse({"scene": "none", "category_path": "", "memories": []}, headers=h)
        try:
            data = json.loads(preload_file.read_text())
        except (ValueError, OSError):
            return JSONResponse({"scene": "none", "category_path": "", "memories": []}, headers=h)
        return JSONResponse(data, headers=h)
    else:
        files = sorted(preload_dir.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
        if not files:
            return JSONResponse({"scene": "none", "category_path": "", "memories": []}, headers=h)
        try:
            data = json.loads(files[0].read_text())
        except (ValueError, OSError):
            return JSONResponse({"scene": "none", "category_path": "", "memories": []}, headers=h)
        return JSONResponse(data, headers=h)

@app.api_route("/freeze", methods=["GET", "POST", "OPTIONS"])
def trigger_freeze(request: Request, authorization: str = Header(None)):
    """触发 freeze：返回预填数据（需认证）
    
    认证方式（按优先级）：
    1. Query param: ?token=xxx（解决浏览器混合内容限制）
    2. Header: Authorization: Bearer xxx
    """
    # 处理 CORS preflight
    if request.method == "OPTIONS":
        h = add_cors_headers(request)
        h["access-control-allow-methods"] = "GET, POST, OPTIONS"
        h["access-control-allow-headers"] = "Authorization, Content-Type"
        return JSONResponse({}, headers=h)

    # 优先从 query param 读取 token（兼容混合内容场景）
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    session_key = get_current_session_key()
    session_data = build_session_summary(session_key) if session_key else {}
    files = get_recent_files(limit=5)
    prefill = session_data.get("last_topic", "") or ""
    if files:
        file_names = "; ".join([f"{f['path']}" for f in files])
        prefill = f"{prefill}\n\n相关文件：{file_names}" if prefill else file_names

    h = add_cors_headers(request)
    # 如果用户开启了 auto_sync，freeze 时自动触发后台同步
    _spawn_sync_if_enabled()
    return JSONResponse({
        "session_key": session_key,
        "prefill": prefill[:500],
        "summary": session_data.get("summary", ""),
        "preferences": session_data.get("preferences", []),
        "files": files[:5],
        "timestamp": time.time(),
    }, headers=h)

# ── 胶囊 CRUD（需认证）──────────────────────────────────
@app.get("/memories")
def get_memories(limit: int = 20, request: Request = None):
    """
    本地记忆快照——无需账号，仅限 localhost 访问。
    让新用户装完立刻看到价值，注册 huper.org 后可跨设备同步。
    """
    if request and request.client and request.client.host not in ("127.0.0.1", "::1"):
        raise HTTPException(status_code=403, detail="仅限本地访问 / localhost only")
    capsules = list_capsules(limit=max(1, min(limit, 100)))
    h = add_cors_headers(request) if request else {}
    items = []
    for c in capsules:
        items.append({
            "id":          c["id"],
            "memo":        c["memo"],
            "tags":        c["tags"],
            "category":    c.get("category") or "",
            "source_type": c.get("source_type") or "manual",
            "source":      c.get("window_title") or c.get("session_id") or "unknown",
            "created_at":  c["created_at"],
            "synced":      bool(c["synced"]),
            "encrypted":   bool(c.get("salt")),
        })
    return JSONResponse({
        "total":    len(items),
        "memories": items,
        "hint":     (
            "这是你的本地记忆快照，数据已加密存储在本机。"
            "注册 huper.org 账号后可跨设备同步，并通过 AI 主动召回相关记忆。"
        ),
    }, headers=h)


@app.get("/capsules")
def list_capsules_handler(
    authorization: str = Header(None),
    request: Request = None,
    limit: int = 50,
    category_path: str = "",
):
    """
    列出胶囊列表（支持分页和路径过滤）。
    - limit: 返回数量（默认50，最大300）
    - category_path: MFS路径过滤，支持前缀匹配
    """
    verify_token(authorization)
    limit = max(1, min(limit, 300))
    capsules = list_capsules(limit=limit, category_path=category_path)
    total = count_capsules()
    h = add_cors_headers(request) if request else {}
    return JSONResponse({
        "total":          total,
        "returned":      len(capsules),
        "category_path": category_path,
        "capsules": [
            {
                "id":                    c["id"],
                "memo":                  c["memo"],
                "content":               c.get("content") or "",
                "tags":                  c["tags"],
                "category":              c.get("category") or "",
                "category_path":         c.get("category_path") or "general/default",
                "source_type":           c.get("source_type") or "manual",
                "session_id":            c["session_id"],
                "window_title":          c["window_title"],
                "created_at":            c["created_at"],
                "synced":                bool(c["synced"]),
                "has_encrypted_content": bool(c.get("salt")),
            }
            for c in capsules
        ]
    }, headers=h)

def _auto_tag_local(content: str, existing_tags: str) -> str:
    """
    基于内容关键词规则自动打标签（轻量，无 LLM 调用开销）。
    已有的标签不会被覆盖，只在检测到明确信号时追加。
    """
    import re
    text = (content or "").lower()

    # 检测信号 → 标签映射
    TAG_RULES = [
        # 技术栈
        (["python", "pytorch", "torch"], "python"),
        (["javascript", "js", "node", "npm", "react", "vue"], "javascript"),
        (["rust", "cargo", "wasm"], "rust"),
        (["golang", " go "], "golang"),
        (["docker", "kubernetes", "k8s", "container"], "devops"),
        (["git", "github", "commit", "branch"], "git"),
        (["api", "rest", "graphql", "endpoint", "http"], "api"),
        (["database", "sql", "postgres", "mysql", "sqlite", "mongodb"], "database"),
        (["linux", "unix", "shell", "bash", "zsh"], "linux"),
        (["aws", "gcp", "azure", "cloud"], "cloud"),
        (["machine learning", "ml", "ai", "neural", "model training"], "ml-ai"),
        (["bug", "error", "crash", "exception", "fix"], "debug"),
        (["design", "ui", "ux", "figma", "css", "html"], "design"),
        (["business", "startup", "product", "revenue", "用户"], "business"),
        (["learn", "course", "tutorial", "读书", "学习"], "learning"),
        (["meeting", "decision", "decided", "agreed"], "decision"),
        (["preference", "prefer", "like", "倾向"], "preference"),
        (["proactive", "capture", "amber", "memory"], "huper"),
    ]

    new_tags = set()
    for keywords, tag in TAG_RULES:
        for kw in keywords:
            if kw in text:
                new_tags.add(tag)
                break

    # 合并已有标签
    existing = set(t.strip() for t in (existing_tags or "").split(",") if t.strip())
    merged = existing | new_tags
    return ",".join(sorted(merged))


@app.post("/capsules")
def create_capsule(capsule: CapsuleIn, authorization: str = Header(None), request: Request = None):
    verify_token(authorization)

    capsule_id = secrets.token_hex(8)
    now = time.time()

    if capsule.content:
        # ── 加密 content（DID 优先，PBKDF2 回退）───────
        aes_key, key_source, salt = _get_did_encryption_key(capsule_id)
        ciphertext, nonce = encrypt_content(capsule.content.encode("utf-8"), aes_key)
        import hashlib, base64
        content_hash = hashlib.sha256(ciphertext).hexdigest()
        salt_b64   = base64.b64encode(salt).decode() if salt else None
        nonce_b64  = base64.b64encode(nonce).decode()
        ct_b64     = base64.b64encode(ciphertext).decode()
    else:
        salt_b64 = nonce_b64 = ct_b64 = content_hash = None
        key_source = "pbkdf2"
        ct_b64 = capsule.content  # 空内容存空字符串

    # 本地自动打标签（E2E 架构：标签在本地生成，加密后上传，服务端不处理内容）
    final_tags = _auto_tag_local(capsule.content or "", capsule.tags or "")

    insert_capsule(
        capsule_id=capsule_id,
        memo=capsule.memo,
        content=ct_b64,
        tags=final_tags,
        session_id=capsule.session_id,
        window_title=capsule.window_title,
        url=capsule.url,
        created_at=now,
        salt=salt_b64,
        nonce=nonce_b64,
        encrypted_len=len(ct_b64) if ct_b64 else 0,
        content_hash=content_hash,
        source_type=getattr(capsule, 'source_type', 'manual'),
        category=getattr(capsule, 'category', '') or _infer_category(capsule.memo or ""),
        key_source=key_source,
    )

    # ── P0-1: 写入 LanceDB 向量索引 ────────────────────
    if capsule.memo:
        try:
            index_capsule(capsule_id, capsule.memo, now)
        except Exception as e:
            logging.warning(f"[create_capsule] vector index failed: {e}")

    h = add_cors_headers(request) if request else {}
    return JSONResponse({"id": capsule_id, "created_at": now, "synced": False}, headers=h)

@app.get("/capsules/{capsule_id}")
def get_capsule_handler(capsule_id: str, authorization: str = Header(None), request: Request = None):
    verify_token(authorization)
    record = get_capsule(capsule_id)
    if not record:
        raise HTTPException(status_code=404, detail="胶囊不存在")

    master_pw = get_master_password()
    content = record["content"] or ""

    if record.get("salt") and record.get("nonce") and content:
        import base64
        key_source = record.get("key_source", "pbkdf2")
        try:
            # D2: 优先 DID 解密
            if key_source == "did":
                plaintext = _decrypt_with_did(content, record["nonce"], capsule_id)
                if plaintext:
                    content = plaintext
                else:
                    content = "[解密失败：DID 密钥不匹配]"
            else:
                # PBKDF2 回退
                salt = base64.b64decode(record["salt"])
                nonce = base64.b64decode(record["nonce"])
                ciphertext = base64.b64decode(content)
                key = derive_key(master_pw, salt)
                plaintext = decrypt_content(ciphertext, key, nonce)
                content = plaintext.decode("utf-8") if plaintext else "[解密失败：密钥错误]"
        except Exception as e:
            content = f"[解密失败：{e}]"

    h = add_cors_headers(request) if request else {}
    return JSONResponse({
        "id": record["id"],
        "memo": record["memo"],
        "content": content,
        "tags": record["tags"],
        "session_id": record["session_id"],
        "window_title": record["window_title"],
        "url": record.get("url"),
        "created_at": record["created_at"],
        "synced": bool(record["synced"]),
    }, headers=h)

@app.delete("/capsules/{capsule_id}")
def delete_capsule(capsule_id: str, authorization: str = Header(None), request: Request = None):
    verify_token(authorization)
    from core.db import get_capsule
    if not get_capsule(capsule_id):
        raise HTTPException(status_code=404, detail="胶囊不存在")
    import sqlite3
    conn = sqlite3.connect(str(HOME / ".amber-hunter" / "hunter.db"))
    c = conn.cursor()
    c.execute("DELETE FROM capsules WHERE id=?", (capsule_id,))
    conn.commit()
    conn.close()
    # P0-1: 删除 LanceDB 向量
    try:
        delete_vector(capsule_id)
    except Exception:
        pass
    h = add_cors_headers(request) if request else {}
    return JSONResponse({"status": "ok"}, headers=h)


@app.patch("/capsules/{capsule_id}")
def update_capsule(
    capsule_id: str,
    body: CapsuleUpdate,
    authorization: str = Header(None),
    request: Request = None,
):
    """更新胶囊的 memo / tags / category（部分更新）"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    from core.db import get_capsule
    existing = get_capsule(capsule_id)
    if not existing:
        raise HTTPException(status_code=404, detail="胶囊不存在")

    # 只更新提供的字段
    updates = []
    values = []
    if body.memo is not None:
        updates.append("memo = ?")
        values.append(body.memo)
    if body.tags is not None:
        updates.append("tags = ?")
        values.append(body.tags)
    if body.category is not None:
        updates.append("category = ?")
        values.append(body.category)
    if body.category_path is not None:
        updates.append("category_path = ?")
        values.append(body.category_path)

    if updates:
        updates.append("synced = 0")       # P0-1: 本地修改后必须重新同步
        updates.append("updated_at = ?")   # P0-2: 记录更新时间
        values.append(time.time())
        values.append(capsule_id)
        conn = _get_conn()
        conn.execute(f"UPDATE capsules SET {', '.join(updates)} WHERE id = ?", values)
        conn.commit()

    h = add_cors_headers(request) if request else {}
    return JSONResponse({"status": "ok"}, headers=h)


# ── 主动回忆（需认证）──────────────────────────────────
@app.get("/recall")
def recall_memories(
    request: Request,
    q: str = "",
    limit: int = 3,
    mode: str = "auto",
    rerank: bool = False,  # deprecated, use rerank_engine
    rerank_engine: str = "auto",
    category_path: str = "",
    use_insights: bool = True,
    citation: int = 0,  # v1.2.32: 1=返回 snippet 片段而非完整 content
    hyde: bool = False,  # v1.2.41: 是否启用 HyDE
    multi_hop: bool = False,  # v1.2.41: 是否启用多跳检索
    authorization: str = Header(None),
    # 注意：12 个参数已接近上限。未来重构建议将检索选项
    # 捆绑为 RecallOptions(citation=0, hyde=False, ...) dataclass
):
    """
    AI 在回复前调用此端点，用返回的记忆补充上下文。

    参数：
      q: 搜索查询（用户当前消息）
      limit: 返回记忆数量（默认 3）
      mode: keyword | semantic | auto/hybrid（默认 auto）
      rerank: (deprecated) 是否用 LLM 重排序，等价于 rerank_engine="llm"
      rerank_engine: auto | model | llm | none（默认 auto：模型优先，失败降级 LLM）
      category_path: MFS路径过滤（如 "projects/huper"），支持前缀匹配
      citation: 1=返回 embedding 裁剪的片段（snippets）而非完整 content
      hyde: 是否启用 HyDE（假设性答案增强检索）v1.2.41
      multi_hop: 是否启用多跳检索 v1.2.41

    v1.2.3: hybrid 模式对全量胶囊做语义+关键词联合评分
    v1.2.32: citation=1 返回 snippet；指数时间衰减（半衰期）；gene co-occurrence 图谱
    v1.2.35: rerank_engine 支持本地模型自动降级
    v1.2.41: BM25 关键词检索；BGE-M3 embedding；Cross-Encoder Reranker；HyDE；Multi-Hop
    """
    import time as _time
    rerank_time_ms = 0.0
    hyde_time_ms = 0.0
    retrieval_hops = 1
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    if not q or len(q.strip()) < 2:
        return JSONResponse({"memories": [], "query": q, "mode": mode, "count": 0},
                            headers=add_cors_headers(request))

    q_lower = q.lower().strip()

    # ── Insight 缓存查询 v1.2.17 ─────────────────────────────
    # 如果 use_insights=True 且指定了 category_path（且非默认路径），优先返回 insight 摘要
    if use_insights and category_path and category_path != "general/default":
        conn = _get_conn()
        c = conn.cursor()
        row = c.execute(
            "SELECT id, capsule_ids, summary, path, hotness_score FROM insights "
            "WHERE path=? ORDER BY hotness_score DESC LIMIT 1",
            (category_path,)
        ).fetchone()
        if row:
            import json as _json
            capsule_ids = _json.loads(row[1]) if row[1] else []
            return JSONResponse({
                "type":          "insight",
                "summary":       row[2],
                "source_ids":    capsule_ids,
                "path":          row[3],
                "hotness_score": row[4],
                "count":         len(capsule_ids),
            }, headers=add_cors_headers(request))
        del conn, c

    # ── 读取所有胶囊（含 category_path）────────────────
    conn = _get_conn()
    c = conn.cursor()

    # category_path 前缀过滤（支持路径路由）
    if category_path:
        # 例如 category_path="projects" 时匹配 "projects/huper" 和 "projects/amber-hunter"
        rows = c.execute(
            "SELECT id,memo,content,tags,session_id,window_title,url,created_at,salt,nonce,synced,source_type,category,category_path "
            "FROM capsules WHERE category_path LIKE ? || '%' ORDER BY created_at DESC LIMIT 300",
            (category_path,)
        ).fetchall()
    else:
        rows = c.execute(
            "SELECT id,memo,content,tags,session_id,window_title,url,created_at,salt,nonce,synced,source_type,category,category_path "
            "FROM capsules ORDER BY created_at DESC LIMIT 300"
        ).fetchall()
    # 注意：不断开连接，由连接池管理

    keys = ["id","memo","content","tags","session_id","window_title","url",
            "created_at","salt","nonce","synced","source_type","category","category_path"]
    capsules_raw = [dict(zip(keys, r)) for r in rows]

    # ── v1.2.10+: keyword模式两阶段：先用memo+tags预筛，避免全量解密 ──
    # 第一阶段：只靠未加密的memo+tags评分，不解密任何content
    def _kw_score_memo_tags(cap) -> float:
        score = 0
        qw = q_lower.split()
        memo = (cap.get("memo") or "").lower()
        tags = (cap.get("tags") or "").lower()
        for w in qw:
            score += memo.count(w) * 3
            score += tags.count(w) * 2
        if q_lower in memo: score += 10
        return float(score)

    # keyword模式：只取memo+tags评分最高的50条再解密，避免全量AES解密
    PRE_DECRYPT_LIMIT = 50
    if mode == "keyword":
        # 第一阶段：全部300条只评分不解密
        scored = [(_kw_score_memo_tags(c), c) for c in capsules_raw]
        scored.sort(key=lambda x: x[0], reverse=True)
        # 取top N或所有有分数的
        top_candidates = [c for _, c in scored[:PRE_DECRYPT_LIMIT]]
        # 解密content只对候选者
        master_pw = get_master_password()
        parsed = []
        for cap in top_candidates:
            content = cap.get("content") or ""
            if cap.get("salt") and cap.get("nonce") and content and master_pw:
                try:
                    import base64 as _b64
                    salt = _b64.b64decode(cap["salt"])
                    nonce = _b64.b64decode(cap["nonce"])
                    ciphertext = _b64.b64decode(content)
                    key = derive_key(master_pw, salt)
                    plaintext = decrypt_content(ciphertext, key, nonce)
                    content = plaintext.decode("utf-8") if plaintext else ""
                except Exception as e:
                    import sys
                    print(f"[recall] decrypt failed for {cap.get('id','?')}: {e}", file=sys.stderr)
                    content = ""
            cap["_text"] = f"{cap.get('memo','')}\n{content}"
            cap["_plain_content"] = content
            parsed.append(cap)
        capsules_raw = []  # 释放内存
    else:
        # semantic/hybrid模式：全量解密（语义编码需要完整_text）
        master_pw = get_master_password()
        parsed = []
        for cap in capsules_raw:
            content = cap.get("content") or ""
            if cap.get("salt") and cap.get("nonce") and content and master_pw:
                try:
                    import base64 as _b64
                    salt = _b64.b64decode(cap["salt"])
                    nonce = _b64.b64decode(cap["nonce"])
                    ciphertext = _b64.b64decode(content)
                    key = derive_key(master_pw, salt)
                    plaintext = decrypt_content(ciphertext, key, nonce)
                    content = plaintext.decode("utf-8") if plaintext else ""
                except Exception as e:
                    import sys
                    print(f"[recall] decrypt failed for {cap.get('id','?')}: {e}", file=sys.stderr)
                    content = ""
            cap["_text"] = f"{cap.get('memo','')}\n{content}"
            cap["_plain_content"] = content
            parsed.append(cap)
        capsules_raw = []

    # ── v1.2.41: BM25 关键词检索 ────────────────────────
    bm25_scores: dict[str, float] = {}
    bm25_enabled = get_config("bm25_enabled") not in ("false", "0", "no")
    if bm25_enabled and mode in ("keyword", "auto", "hybrid"):
        try:
            from core.bm25 import BM25Searcher
            corpus = [c.get("_text", "") or "" for c in parsed]
            bm25 = BM25Searcher(corpus)
            bm25_raw = bm25.search(q, top_k=min(50, len(corpus)))
            bm25_scores = {parsed[i]["id"]: score for i, score in bm25_raw}
        except Exception as e:
            import sys
            print(f"[recall] BM25 failed: {e}", file=sys.stderr)

    # ── 关键词评分（解密后）────────────────────────
    def _kw_score(cap) -> tuple[float, list[str]]:
        """返回 (score, matched_terms)，matched_terms 用于可解释召回"""
        score = 0
        matched: list[str] = []
        qw = q_lower.split()
        memo = (cap.get("memo") or "").lower()
        tags = (cap.get("tags") or "").lower()
        text = (cap.get("_plain_content") or "").lower()
        for w in qw:
            if w in memo:
                score += 3
                matched.append(f"memo:{w}")
            if w in tags:
                score += 2
                matched.append(f"tags:{w}")
            if w in text:
                score += 1
                matched.append(f"content:{w}")
        if q_lower in memo:
            score += 10
            matched.append(f"exact:{q_lower[:30]}")
        if q_lower in text:
            score += 5
        return float(score), matched

    kw_scores = [(_kw_score(c), c) for c in parsed]
    max_kw = max((score for (score, _), _ in kw_scores), default=1.0) or 1.0
    # 归一化关键词分到 0-1
    kw_norm = [(score / max_kw, c, terms) for (score, terms), c in kw_scores]

    # ── P0-1: 语义评分（LanceDB 优先，on-the-fly 回退）────
    search_mode = mode
    sem_scores: dict[str, float] = {}  # capsule_id -> semantic similarity

    if mode in ("auto", "semantic", "hybrid"):
        # P0-1: 先用 LanceDB 向量检索
        try:
            vector_results = search_vectors(q, limit=limit * 3)
            if vector_results:
                for r in vector_results:
                    sem_scores[r["capsule_id"]] = r["lance_score"]
                search_mode = "hybrid" if mode in ("auto", "hybrid") else "semantic"
            else:
                raise FileNotFoundError("empty vector index")
        except Exception:
            # on-the-fly 回退
            try:
                import numpy as _np
                model = _get_embed_model(blocking=False)
                if model is None:
                    if _MODEL_LOADING:
                        return JSONResponse({
                            "error": "语义模型正在加载中，请稍后重试",
                            "code": "MODEL_LOADING",
                            "retry_after": 10,
                        }, status_code=503, headers=add_cors_headers(request))
                    raise ImportError("embedding model not available")
                q_vec = model.encode(q)
                texts = [c["_text"][:512] for c in parsed]
                if texts:
                    cap_vecs = model.encode(texts)
                    norms = _np.linalg.norm(cap_vecs, axis=1) * _np.linalg.norm(q_vec) + 1e-8
                    sims = _np.dot(cap_vecs, q_vec) / norms
                    for i, cap in enumerate(parsed):
                        sem_scores[cap["id"]] = float(sims[i])
                search_mode = "hybrid" if mode in ("auto", "hybrid") else "semantic"
            except ImportError:
                if mode == "semantic":
                    return JSONResponse(
                        {"error": "语义搜索需要 sentence-transformers，请运行：pip install sentence-transformers"},
                        status_code=400, headers=add_cors_headers(request)
                    )
                search_mode = "keyword"


    # ── 混合评分 + 排序（含 recency/hotness）────────────────
    now_ts = time.time()
    combined = []

    # ── P1-3: Recall Memory Cooldown — 压制最近 30 分钟内召回过的胶囊 ──
    COOLDOWN_SECONDS = max(60, int(get_config("recall_cooldown_seconds") or "1800"))  # 默认 30 分钟
    recent_hit_ids: set = set()
    try:
        cooldown_conn = _get_conn()
        cooldown_c = cooldown_conn.cursor()
        cooldown_cutoff = now_ts - COOLDOWN_SECONDS
        cooldown_rows = cooldown_c.execute(
            "SELECT DISTINCT capsule_id FROM memory_hits WHERE hit_at > ?",
            (cooldown_cutoff,)
        ).fetchall()
        recent_hit_ids = {r[0] for r in cooldown_rows}
        del cooldown_c, cooldown_conn
    except Exception:
        pass  # cooldown 查询失败不影响正常评分

    for kw_n, cap, terms in kw_norm:
        lance = sem_scores.get(cap["id"], 0.0)  # P0-1: LanceDB score (或 on-the-fly 回退)
        # v1.2.41: BM25 score (if available, blend with keyword score)
        bm25_score = bm25_scores.get(cap["id"], 0.0)
        # 如果有 BM25 分数，混合到 keyword 评分中
        if bm25_score > 0 and bm25_enabled:
            # BM25 归一化：取当前 batch 最大值
            max_bm25 = max(bm25_scores.values()) if bm25_scores else 1.0
            bm25_norm = bm25_score / (max_bm25 + 1e-8)
            kw_n = 0.5 * kw_n + 0.5 * bm25_norm  # 混合：原始关键词 + BM25
        # v1.2.32: 指数时间衰减，替代线性衰减。半衰期默认 30 天（可通过 recall_half_life_days 配置）
        days_old = (now_ts - cap.get("created_at", now_ts)) / 86400
        half_life_days = float(get_config("recall_half_life_days") or "30")
        recency = max(0.0, 0.5 ** (days_old / half_life_days))
        # 热力值：已有 hit 数据用于加权
        hotness = min(1.0, cap.get("hotness_score", 0) / 10)
        if search_mode == "hybrid":
            final = 0.30 * kw_n + 0.50 * lance + 0.12 * recency + 0.08 * hotness
        elif search_mode == "semantic":
            final = 0.80 * lance + 0.12 * recency + 0.08 * hotness
        else:
            final = 0.80 * kw_n + 0.15 * recency + 0.05 * hotness
        # P1-3: 完全压制冷却期内的胶囊
        if cap["id"] in recent_hit_ids:
            final = 0.0
        combined.append((final, kw_n, lance, recency, hotness, cap, terms))

    # 过滤掉完全无信号的结果
    if search_mode == "keyword":
        combined = [(s, kw_n, lance, r, h, c, terms) for s, kw_n, lance, r, h, c, terms in combined if s > 0]
    else:
        combined = [(s, kw_n, lance, r, h, c, terms) for s, kw_n, lance, r, h, c, terms in combined if s > 0.05]

    combined.sort(key=lambda x: x[0], reverse=True)
    top = combined[:limit]

    # ── 相关记忆关联（v1.2.8）──────────────────────────────
    def _keyword_overlap(words1: set, words2: set) -> float:
        if not words1 or not words2:
            return 0.0
        return len(words1 & words2) / min(len(words1), len(words2))

    def _find_related(cap_id: str, memo: str, tags: str, all_caps: list, top_ids: set, limit: int = 5) -> list:
        """
        v1.2.32: 混合排序 = 0.5*gene_co_score + 0.5*keyword_overlap。
        Gene co_score 来自历史共现图谱（优先级高于当前查询的关键词匹配）。
        """
        memo_w = set(memo.lower().split())
        tag_w = set(tags.lower().split())
        query_w = memo_w | tag_w

        # 从 gene graph 获取该胶囊的历史共现胶囊
        gene_map: dict[str, float] = {}
        try:
            genes = get_genes_for_capsule(cap_id, limit=20)
            for g in genes:
                gene_map[g["capsule_id"]] = g["co_score"]
        except Exception:
            pass

        scores = []
        for c in all_caps:
            if c["id"] == cap_id or c["id"] in top_ids:
                continue
            gene_score = gene_map.get(c["id"], 0.0)
            c_memo = (c.get("memo") or "").lower()
            c_tags = (c.get("tags") or "").lower()
            c_w = set(c_memo.split()) | set(c_tags.split())
            kw_overlap = _keyword_overlap(query_w, c_w)
            # 混合评分
            combined_score = 0.5 * gene_score + 0.5 * kw_overlap
            if combined_score > 0:
                scores.append((combined_score, gene_score, kw_overlap, c["id"]))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [cid for _, _, _, cid in scores[:limit]]

    top_ids = {c["id"] for _, _, _, _, _, c, _ in top}
    related_map: dict[str, list] = {}
    for _, _, _, _, _, cap, _ in top:
        memo = cap.get("memo", "") or ""
        tags = cap.get("tags", "") or ""
        plain = cap.get("_plain_content", "") or ""
        try:
            related_map[cap["id"]] = _find_related(cap["id"], memo + " " + plain, tags, parsed, top_ids)
        except Exception as e:
            import sys
            print(f"[recall] _find_related failed for {cap.get('id','?')}: {e}", file=sys.stderr)
            related_map[cap["id"]] = []

    # ── 组装返回 ─────────────────────────────────
    def _build_memory(score: float, kw_n: float, lance: float, recency: float, hotness: float, cap: dict, related_ids: list, matched_terms: list, wal_signal: dict | None) -> dict:
        memo = cap.get("memo", "")
        plain = cap.get("_plain_content", "")
        tags = cap.get("tags", "")
        cat = cap.get("category", "") or ""
        created = cap.get("created_at", 0)
        cat_label = f" [{cat}]" if cat else ""

        # v1.2.32: citation 模式 — 用 embedding 相似度裁剪出最相关的片段
        snippets: list[dict] = []
        injected_content = plain[:400]
        if citation and plain and len(plain) > 40:
            try:
                snippets = find_snippets(plain, q, top_k=3, min_score=0.3)
                if snippets:
                    injected_content = snippets[0]["text"]
            except Exception:
                pass
        injected = (
            f"[琥珀记忆{cat_label} | {tags}]\n"
            f"记忆：{memo}\n"
            f"内容：{injected_content}{'...' if len(injected_content) >= 400 and not citation else ''}"
        )
        # ── P0-3: 生成详细 reason（可解释召回）──────────────
        parts: list[str] = []
        if matched_terms:
            # 去重 + 限制显示前 5 个
            unique_terms = list(dict.fromkeys(matched_terms[:5]))
            terms_str = ", ".join(unique_terms)
            parts.append(f"关键词：{terms_str}")
        if lance > 0.6:
            parts.append(f"语义高度相似（{int(lance*100)}%）")
        elif lance > 0.3:
            parts.append(f"语义相关（{int(lance*100)}%）")
        if recency > 0.8:
            parts.append("近期记忆")
        elif recency < 0.3:
            parts.append("久远记忆")
        if hotness > 0.6:
            parts.append("高热记忆")
        if wal_signal:
            t = wal_signal.get("type", "")
            if t == "correction":
                original = wal_signal.get("data", {}).get("original", "")
                parts.append(f"⚠️ 已修正：'{original[:30]}'")
            elif t == "preference":
                parts.append("🟢 用户偏好信号")
            elif t == "decision":
                parts.append("🔵 用户决定信号")
        reason = "；".join(parts) if parts else "综合相关"
        return {
            "id":              cap["id"],
            "memo":            memo,
            "content":         plain[:500] if not citation else (snippets[0]["text"] if snippets else plain[:500]),
            "tags":            tags,
            "category":        cat,
            "category_path":    cap.get("category_path", "general/default"),
            "source_type":     cap.get("source_type", ""),
            "created_at":      created,
            "relevance_score": round(score, 3),
            "breakdown": {
                "keyword_score": round(kw_n, 3),
                "semantic_score": round(lance, 3),
                "recency_score": round(recency, 3),
                "hotness_score": round(hotness, 3),
                "matched_terms": matched_terms[:5],  # P0-3: 去重限制
                "wal_signal": wal_signal.get("type") if wal_signal else None,  # P0-3
            },
            "related_ids":     related_ids,
            "reason":          reason,  # P0-3: 详细自然语言
            "injected_prompt": injected,
            "hit_url":         f"/recall/{cap['id']}/hit",
            # v1.2.32: citation 模式返回 snippet 片段
            "snippets": [
                {"text": s["text"], "source": f"{cap['id']}#{s['offset']}", "sim_score": s["sim_score"]}
                for s in snippets
            ] if citation and snippets else [],
        }

    memories = [
        _build_memory(s, kw_n, lance, r, h, c, related_map.get(c["id"], []), terms, None)
        for s, kw_n, lance, r, h, c, terms in top
    ]

    # v1.2.32: 记录本次 recall session 的胶囊对共现关系（gene graph）
    if len(top) >= 2:
        try:
            cap_ids = [c["id"] for _, _, _, _, _, c, _ in top]
            rel_scores = [s for s, _, _, _, _, _, _ in top]
            record_recall_session_genes(cap_ids, rel_scores)
        except Exception:
            pass  # gene 记录失败不影响正常返回

    # 清理解密明文
    del parsed
    gc.collect()

    # 可选：重排序（自动降级：模型 → LLM → 原顺序）
    if memories:
        engine = "llm" if rerank else rerank_engine
        if engine != "none":
            # v1.2.41: Cross-Encoder Reranker (rerank_engine=model)
            if engine == "model":
                t0 = _time.time()
                try:
                    from core.reranker import Reranker as _CrossReranker
                    rr = _CrossReranker()
                    doc_texts = [m.get("content", "")[:512] or m.get("memo", "")[:512] for m in memories]
                    reranked = rr.rerank(q, doc_texts, top_k=len(memories))
                    # Apply reranked order to memories
                    if reranked:
                        reranked_ids = [memories[i]["id"] for i, _ in reranked]
                        memories = sorted(memories, key=lambda m: reranked_ids.index(m["id"]))
                except Exception as e:
                    import sys
                    print(f"[recall] Cross-encoder rerank failed: {e}", file=sys.stderr)
                rerank_time_ms = (_time.time() - t0) * 1000
            else:
                memories = _rerank_memories(q, memories, engine)

    # ── P0-2: WAL 热状态检测 ──────────────────────────────────
    # 在返回前，检测 session 中的偏好/决定/修正信号并写入 WAL
    if q:
        try:
            session_key = get_current_session_key()
            if session_key:
                messages = read_session_messages(session_key, limit=10)
                for m in messages:
                    if m.get("role") != "user":
                        continue
                    text = m.get("text", "")
                    if not text or len(text) < 5:
                        continue
                    sig_type = _detect_signal_type(text)
                    if sig_type:
                        entry_data = {"text": text[:500], "signal": sig_type, "capsule_id": ""}
                        # 幂等写入：检查近 20 条中是否已有相同内容哈希
                        recent = read_wal_entries(session_key, processed=None)[:20]
                        import hashlib, json as _json
                        content_hash = hashlib.sha1(
                            _json.dumps(entry_data, sort_keys=True).encode()
                        ).hexdigest()[:12]
                        already_written = any(
                            e.get("data", {}).get("text") == entry_data["text"]
                            and e.get("type") == sig_type
                            for e in recent
                        )
                        if not already_written:
                            write_wal_entry(session_key, sig_type, entry_data)
                        # P2-2: WAL correction 信号写入 correction_log
                        if sig_type == "correction":
                            try:
                                from core.correction import record_rejection
                                record_rejection(memo=text[:200], reason="wal_correction",
                                               session_id=session_key)
                            except Exception:
                                pass
                        # 懒 GC：未处理条目超过 50 条时清理 24 小时前的已处理条目
                        stats = get_wal_stats()
                        unprocessed = stats.get("total", 0) - stats.get("processed_count", 0)
                        if unprocessed > 50:
                            wal_gc(age_hours=24.0)
        except Exception:
            pass  # WAL 失败不影响 recall 返回

    # ── P1-1: 注入 user_profile 到 recall 响应 ─────────────
    _profile: dict = {}
    try:
        from core.profile import get_full_profile, build_or_update_profile
        _profile = get_full_profile()
        # 如果 PREFERENCES 为空，尝试从当前 session 构建
        if not _profile.get("PREFERENCES", {}).get("content"):
            _sk = get_current_session_key()
            if _sk:
                build_or_update_profile(_sk)
                _profile = get_full_profile()
    except Exception:
        _profile = {}

    return JSONResponse({
        "memories":          memories[:limit],
        "profile":           _profile,
        "query":             q,
        "mode":              search_mode,
        "count":             len(memories),
        "semantic_available": _semantic_available(),
        # v1.2.32: citation 模式
        "citation":          bool(citation),
        "half_life_days":    float(get_config("recall_half_life_days") or "30"),
        # v1.2.41: RAG timing
        "rerank_time_ms":    round(rerank_time_ms, 2),
        "hyde_time_ms":      round(hyde_time_ms, 2),
        "retrieval_hops":    retrieval_hops,
    }, headers=add_cors_headers(request))


# ── v1.2.41: RAG Recall Evaluation ─────────────────────────────────
class RecallEvaluateIn(BaseModel):
    queries: list[dict]  # [{"q": "...", "expected_capsule_ids": ["..."]}]


@app.post("/recall/evaluate")
def evaluate_recall_endpoint(
    body: RecallEvaluateIn,
    request: Request,
    authorization: str = Header(None),
):
    """
    Evaluate recall quality using RAGAS metrics.

    POST /recall/evaluate
    Body: {"queries": [{"q": "...", "expected_capsule_ids": ["..."]}]}
    Returns: {"ragas_scores": {...}, "ndcg_at_5": 0.x, ...}
    """
    verify_token(_extract_bearer_token(request, authorization))

    try:
        from benchmark.recall_eval import evaluate_recall as _eval_recall
        result = _eval_recall(
            test_queries=body.queries,
            amber_url="http://localhost:18998",
        )
        return JSONResponse(result, headers=add_cors_headers(request))
    except ImportError:
        return JSONResponse(
            {
                "error": "RAGAS not installed",
                "code": "RAGAS_UNAVAILABLE",
                "detail": "Please install ragas: pip install ragas",
            },
            status_code=400,
            headers=add_cors_headers(request),
        )
    except Exception as e:
        import sys
        print(f"[evaluate] recall evaluation failed: {e}", file=sys.stderr)
        return JSONResponse(
            {"error": str(e), "code": "EVALUATION_FAILED"},
            status_code=500,
            headers=add_cors_headers(request),
        )


# ── v1.2.8: Hit tracking ───────────────────────────────────────────
class HitIn(BaseModel):
    session_id: Optional[str] = None
    search_query: Optional[str] = None
    relevance_score: Optional[float] = None


@app.patch("/recall/{capsule_id}/hit")
def record_hit(
    capsule_id: str,
    body: HitIn,
    request: Request,
    authorization: str = Header(None),
):
    """
    Record that a recalled memory was useful (hit tracking v1.2.8).

    Body: {"session_id": "...", "search_query": "...", "relevance_score": 0.85}
    Returns: {"ok": True}
    """
    headers = add_cors_headers(request)
    verify_token(authorization)

    hit_id = secrets.token_hex(8)
    rel = body.relevance_score if body.relevance_score is not None else 0.5

    insert_memory_hit(hit_id, capsule_id, body.session_id, body.search_query, rel)
    update_capsule_hit(capsule_id, rel)

    return JSONResponse({"ok": True}, headers=headers)


# ── v1.2.32: Gene Co-occurrence Graph API ───────────────────────────────────

@app.get("/genes/{capsule_id}")
def get_capsule_genes(
    capsule_id: str,
    request: Request,
    limit: int = 10,
    authorization: str = Header(None),
):
    """
    返回与指定胶囊共现过的所有胶囊及其 gene 分数。

    GET /genes/{capsule_id}?limit=10

    响应:
    {
      "capsule_id": "...",
      "genes": [
        {"capsule_id": "...", "co_score": 0.75, "co_count": 12, "avg_relevance": 0.85, "last_seen": 1773000000},
        ...
      ]
    }
    """
    headers = add_cors_headers(request)
    verify_token(_extract_bearer_token(request, authorization))
    genes = get_genes_for_capsule(capsule_id, limit=limit)
    return JSONResponse({
        "capsule_id": capsule_id,
        "genes": genes,
    }, headers=headers)


# ── v1.2.32: Citation — Get specific snippet lines from a capsule ───────────

@app.get("/recall/{capsule_id}/snippet")
def get_capsule_snippet(
    capsule_id: str,
    request: Request,
    from_line: int = 1,
    lines: int = 20,
    authorization: str = Header(None),
):
    """
    精确拉取胶囊内容的指定行范围（用于 citation 引用）。

    GET /recall/{capsule_id}/snippet?from_line=1&lines=20

    响应:
    {
      "capsule_id": "...",
      "from_line": 1,
      "lines": 20,
      "content": "...（原始内容，未解密）...",
      "plain": "...（解密后内容）..."
    }
    """
    headers = add_cors_headers(request)
    verify_token(_extract_bearer_token(request, authorization))
    cap = get_capsule(capsule_id)
    if not cap:
        return JSONResponse({"error": "Capsule not found"}, status_code=404, headers=headers)

    plain = cap.get("content") or ""
    if cap.get("salt") and cap.get("nonce") and plain:
        try:
            import base64 as _b64
            salt = _b64.b64decode(cap["salt"])
            nonce = _b64.b64decode(cap["nonce"])
            ciphertext = _b64.b64decode(plain)
            master_pw = get_master_password()
            if master_pw:
                key = derive_key(master_pw, salt)
                plaintext = decrypt_content(ciphertext, key, nonce)
                plain = plaintext.decode("utf-8") if plaintext else ""
        except Exception:
            pass

    # 行裁剪（from_line 1-indexed）
    all_lines = plain.split("\n")
    start = max(0, from_line - 1)
    end = min(len(all_lines), start + lines)
    snippet_lines = all_lines[start:end]
    snippet_text = "\n".join(snippet_lines)

    return JSONResponse({
        "capsule_id": capsule_id,
        "from_line": from_line,
        "lines": lines,
        "total_lines": len(all_lines),
        "content": snippet_text,
    }, headers=headers)


def _rerank_memories_model(query: str, memories: list[dict]) -> list[dict]:
    """
    用本地 AmberTrainer 模型对 memories 重排序。
    返回重排序后的列表；如果模型未训练或失败，返回空列表（由调用方决定是否降级）。
    """
    try:
        from core.trainer import get_trainer
        at = get_trainer()
        if not at.is_ready():
            return []  # 模型未训练，交给 LLM
        texts = [(m.get("memo") or "") + " " + (m.get("content") or "")[:200] for m in memories]
        ranked = at.rerank(query, texts, top_k=len(texts))
        reranked = []
        for new_idx, (orig_idx, score) in enumerate(ranked):
            m = dict(memories[orig_idx])
            m["relevance_score"] = round(score, 3)
            m["_rerank_source"] = "model"
            reranked.append(m)
        return reranked
    except Exception:
        return []


def _rerank_memories(query: str, memories: list[dict], engine: str = "auto") -> list[dict]:
    """
    重排序 dispatcher。

    engine:
      auto   — 先尝试模型，失败则降级 LLM
      model  — 仅用本地模型（无模型则返回原顺序）
      llm    — 仅用 LLM
      none   — 不重排序
    """
    if not memories:
        return memories

    if engine == "none":
        return memories

    if engine in ("auto", "model"):
        reranked = _rerank_memories_model(query, memories)
        if reranked:
            return reranked
        if engine == "model":
            return memories  # model 模式不允许降级

    if engine in ("auto", "llm"):
        return _rerank_memories_llm(query, memories)

    return memories


def _rerank_memories_llm(query: str, memories: list[dict]) -> list[dict]:
    """Re-rank a list of memory candidates using LLM.

    Sends the query + all memory summaries to the LLM and asks it to score
    and reorder them by relevance to the query. Returns reordered list.

    If LLM is unavailable or fails, returns the original list unchanged.
    """
    if not memories or not LLM_READY:
        return memories

    try:
        llm = get_llm()
        if not llm.config.api_key:
            return memories
    except Exception:
        return memories

    # Build a compact summary of each memory for the LLM context
    mem_lines = []
    for i, m in enumerate(memories):
        memo = (m.get("memo") or "").strip()
        content = (m.get("content") or "")[:200].strip()
        tags = (m.get("tags") or "").strip()
        mem_lines.append(f"[{i}] [{tags}] {memo} | {content}")

    mem_context = "\n".join(mem_lines)

    prompt = (
        "You are a relevance ranker. Given a user query and a list of memory entries, "
        "score each entry 0-10 for how relevant it is to the query, then return the top entries.\n\n"
        f"Query: {query}\n\n"
        f"Memories:\n{mem_context}\n\n"
        "Your task: Rate each memory [0-10] for relevance to the query, "
        "then return the top 3-5 most relevant memories in JSON format.\n"
        "Return STRICTLY valid JSON only, no markdown, no explanation:\n"
        "[{\"index\": N, \"score\": S, \"reason\": \"brief reason\"}, ...]\n"
        "Score guide: 10=directly answers query, 7-9=highly relevant, 4-6=somewhat relevant, 0-3=irrelevant."
    )

    try:
        result = llm.complete(prompt, max_tokens=400)
        if result.startswith("[ERROR") or not result.strip():
            return memories

        # Parse JSON response
        import json as _json
        cleaned = result.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            cleaned = "\n".join(lines[1:] if lines[0].startswith("```") else lines)
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

        scores = _json.loads(cleaned)
        if not isinstance(scores, list):
            return memories

        # Build index → score map
        score_map = {item["index"]: item["score"] for item in scores if "index" in item}

        # Reorder: scored items first (descending), then unscored
        scored = [(score_map.get(i, 0), m) for i, m in enumerate(memories)]
        scored.sort(key=lambda x: x[0], reverse=True)

        # Update relevance_score
        reranked = []
        for raw_score, m in scored:
            m = dict(m)  # copy
            m["relevance_score"] = round(min(raw_score / 10.0, 1.0), 2)
            reranked.append(m)

        return reranked

    except Exception:
        return memories


@app.post("/rerank")
async def rerank_memories(request: Request, authorization: str = Header(None)):
    """
    Re-rank a list of memory candidates.
    自动降级：模型 → LLM → 原顺序（cold-start 用户也能用）。

    Body: {"query": "...", "memories": [...], "engine": "auto"}
    engine: auto | model | llm | none（默认 auto）
    Returns: {"memories": [...reranked...]}
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    try:
        body = await request.json()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    query = body.get("query", "")
    memories = body.get("memories", [])
    engine = body.get("engine", "auto")

    if not query or not memories:
        return JSONResponse({"memories": memories}, headers=add_cors_headers(request))

    # 自动降级：模型失败则 LLM
    import asyncio
    reranked = await asyncio.to_thread(_rerank_memories, query, memories, engine)
    return JSONResponse({"memories": reranked, "engine": engine}, headers=add_cors_headers(request))


def _semantic_available() -> bool:
    """检查是否安装了语义搜索依赖（带缓存）"""
    global _SEMANTIC_AVAILABLE
    if _SEMANTIC_AVAILABLE is not None:
        return _SEMANTIC_AVAILABLE
    try:
        import sentence_transformers as _
        import numpy as _
        _SEMANTIC_AVAILABLE = True
        return True
    except ImportError:
        _SEMANTIC_AVAILABLE = False
        return False


# ── 云端同步（需认证）────────────────────────────────


# ── 分类推断 helper（v1.1.9）─────────────────────────────
_CATEGORY_KEYWORDS = {
    "thought":    ["想法", "想到", "突然想", "有个念头", "脑海中", "感觉", "觉得", "意识到",
                   "realize", "just thought", "idea", "thought", "occurred to me"],
    "learning":   ["读了", "看了", "书里", "文章", "这本书", "学到", "理解了", "课程",
                   "reading", "book", "learned", "course", "study"],
    "decision":   ["决定", "选择了", "打算", "确定了", "我们选", "不再", "放弃", "要去", "方案",
                   "decided", "going with", "we chose", "commit to", "will"],
    "reflection": ["反思", "复盘", "回顾", "总结", "想清楚", "发现自己",
                   "reviewed", "reflecting", "looking back", "in retrospect", "realized", "lesson"],
    "people":     ["和.{1,8}聊", "跟.{1,8}说", "和朋友", "跟朋友", "和同事", "跟同事",
                   "聊了", "聊天", "见了", "对话", "和他", "和她",
                   "talked to", "met with", "conversation with", "catchup", "friend"],
    "life":       ["心情", "情绪", "感受", "低落", "开心", "难过", "疲惫", "疲倦", "焦虑",
                   "运动", "睡眠", "跑步", "冥想", "饮食", "健身", "休息",
                   "sleep", "exercise", "workout", "meditation", "health", "mood", "feeling", "tired"],
    "creative":   ["灵感", "创意", "设计", "想做", "想象", "写作", "作品",
                   "inspiration", "design idea", "creative", "writing"],
    "dev":        ["python", "javascript", "git", "docker", "api", "sql",
                   "error", "bug", "code", "deploy", "server", "代码", "报错", "修复", "接口", "部署"],
}

import re as _re

def _infer_category(text: str) -> str:
    """从文本推断大类，返回 category 字符串"""
    t = text.lower()
    scores = {}
    for cat, kws in _CATEGORY_KEYWORDS.items():
        score = 0
        for kw in kws:
            try:
                score += len(_re.findall(kw, t))
            except Exception:
                score += t.count(kw)
        if score > 0:
            scores[cat] = score
    if not scores:
        return ""
    return max(scores, key=scores.get)


# ── /ingest 端点（v1.1.9）─────────────────────────────────
class IngestIn(BaseModel):
    memo: str
    context: str = ""
    category: str = ""
    tags: str = ""
    source: str = "unknown"
    confidence: float = 0.7
    review_required: bool = True
    agent_tag: str = ""  # v1.2.8: agent标识标签，如 "agent:openclaw"


def _get_capsule_count() -> int:
    """获取当前胶囊数量"""
    db_path = Path.home() / ".amber-hunter" / "hunter.db"
    if not db_path.exists():
        return 0
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    row = c.execute("SELECT COUNT(*) FROM capsules").fetchone()
    conn.close()
    return row[0] if row else 0


def _insert_sample_memories() -> None:
    """首次启动时插入3条示例记忆（仅执行一次）"""
    samples = [
        ("我偏好简洁的解决方案，会拒绝过度工程化",
         "展示偏好类记忆的用途", "preference", "python, architecture"),
        ("我主要使用 Python 和 JavaScript 开发",
         "展示技能类记忆的用途", "skill", "python, javascript"),
        ("我和 Anke 合作 huper 项目，用 huper 管理项目记忆",
         "展示项目类记忆的用途", "project", "huper, anke"),
    ]
    now = time.time()
    for memo, content, cat, tags in samples:
        cap_id = secrets.token_hex(8)
        insert_capsule(
            capsule_id=cap_id,
            memo=memo,
            content=content,
            tags=f"#sample {tags}",
            session_id=None,
            window_title=None,
            url=None,
            created_at=now,
            source_type="sample",
            category=cat,
        )
        now += 0.01  # 避免时间戳完全相同


@app.post("/ingest")
def ingest_memory(body: IngestIn, request: Request = None,
                  authorization: str = Header(None)):
    """
    AI 主动写入记忆端点（v1.2.8 / v1.2.34 去重）。
    - capsule_count==0 → 首次体验引导，直接写入并返回 welcome
    - v1.2.34: 精确去重 — 相同 content_hash 的胶囊不重复写入，返回已有 ID
    - v1.2.34: 语义去重 — 高度相似的胶囊在响应中提示（不阻止写入）
    - review_required=False 且 confidence>=0.95 → 直接写入 capsules
    - 其余 → 写入 memory_queue 等待用户审核
    支持 Bearer header 或 ?token= query param。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    h = add_cors_headers(request) if request else {}

    # ── v1.2.34: 计算 content_hash（用于精确去重）────────────
    import hashlib
    content_hash: str | None = None
    if body.context:
        # 使用 SHA-256，内容为空时不计算 hash
        content_hash = hashlib.sha256(body.context.encode("utf-8")).hexdigest()

    # ── v1.2.34: 精确去重检查 ───────────────────────────────
    # 注意：首次 ingest（capsule_count==0）跳过去重，因为是引导体验
    capsule_count = _get_capsule_count()
    if capsule_count > 0:
        existing_id = find_capsule_by_content_hash(content_hash)
        if existing_id:
            # 语义相似度检查（软提示，不阻止）
            similar = find_similar_capsules(body.memo, top_k=3, min_score=0.85)
            return JSONResponse({
                "duplicate": True,
                "capsule_id": existing_id,
                "message": "内容已存在，未重复写入",
                "similar_capsules": similar,
            }, headers=h)

    # 推断缺失的 category
    category = body.category or _infer_category(body.memo + " " + body.context)

    # ── 首次 ingest：引导体验 + 样例记忆 ─────────────────────
    is_first_ingest = (capsule_count == 0)
    final_tags = _normalize_tags(body.tags) if body.tags else ""
    if body.agent_tag:
        agent_part = _normalize_tags(body.agent_tag)
        final_tags = f"{final_tags},agent:{agent_part}" if final_tags else f"agent:{agent_part}"

    # 推断 category_path（MFS 路径）
    category_path = _infer_category_path(body.memo, body.context or "", final_tags)

    # ── v1.2.39: 自动应用 tag 纠错规则 ─────────────────────────
    # 如果输入 tags 命中已知纠错规则，在写入前自动替换
    if final_tags:
        try:
            from core.correction import get_tag_rules
            rules = get_tag_rules()  # {original: corrected}
            if rules:
                corrected_parts = []
                changed = False
                for t in final_tags.split(","):
                    t = t.strip()
                    if t in rules:
                        corrected_parts.append(rules[t])
                        changed = True
                    else:
                        corrected_parts.append(t)
                if changed:
                    final_tags = ",".join(corrected_parts)
        except Exception:
            pass  # 纠错失败不影响写入

    if is_first_ingest:
        # 先插入3条样例记忆（仅首次）
        _insert_sample_memories()
        # 强制直接写入，不进队列
        from core.contradiction import parse_dates
        vf, vt = parse_dates(body.memo)
        cap_id = secrets.token_hex(8)
        insert_capsule(
            capsule_id=cap_id,
            memo=body.memo,
            content=body.context or "",
            tags=final_tags,
            session_id=None,
            window_title=None,
            url=None,
            created_at=time.time(),
            source_type="ai_chat",
            category=category,
            category_path=category_path,
            content_hash=content_hash,  # v1.2.34
            valid_from=vf,
            valid_to=vt,
        )
        return JSONResponse({
            "queued": False,
            "capsule_id": cap_id,
            "welcome": True,
            "message": "这是你的第一条记忆！试着问我一些问题来验证它的效果。",
            "sample_count": 3,
        }, headers=h)

    # 高置信度直接写入
    if not body.review_required and body.confidence >= 0.95:
        # v1.2.39: 时间解析 + 矛盾检测
        from core.contradiction import check_contradiction_on_ingest
        valid_from, valid_to, contradictions = check_contradiction_on_ingest(
            body.memo, category_path
        )
        cap_id = secrets.token_hex(8)
        insert_capsule(
            capsule_id=cap_id,
            memo=body.memo,
            content=body.context or "",
            tags=final_tags,
            session_id=None,
            window_title=None,
            url=None,
            created_at=time.time(),
            source_type="ai_chat",
            category=category,
            category_path=category_path,
            content_hash=content_hash,  # v1.2.34
            valid_from=valid_from,
            valid_to=valid_to,
        )
        resp = {"queued": False, "capsule_id": cap_id,
                "message": "Saved directly"}
        if contradictions:
            resp["contradictions"] = contradictions
        return JSONResponse(resp, headers=h)

    # 其余进审核队列
    qid = queue_insert(
        memo=body.memo,
        context=body.context,
        category=category,
        tags=final_tags,
        source=body.source,
        confidence=body.confidence,
    )
    return JSONResponse({"queued": True, "queue_id": qid,
                         "message": "Added to review queue"}, headers=h)


# ── /queue 端点（v1.1.9）─────────────────────────────────

@app.get("/queue")
def get_queue(request: Request = None, authorization: str = Header(None)):
    """列出待审核记忆"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    h = add_cors_headers(request) if request else {}
    pending = queue_list_pending()
    return JSONResponse({"pending": pending, "count": len(pending)}, headers=h)


class QueueEditIn(BaseModel):
    memo: str = ""
    category: str = ""
    tags: str = ""


@app.post("/queue/{qid}/approve")
def approve_queue_item(qid: str, request: Request = None,
                       authorization: str = Header(None)):
    """接受待审核记忆 → 写入 capsules"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    h = add_cors_headers(request) if request else {}

    item = queue_get(qid)
    if not item:
        return JSONResponse({"error": "not found"}, status_code=404, headers=h)
    if item["status"] != "pending":
        return JSONResponse({"error": "already processed"}, status_code=400, headers=h)

    cap_id = secrets.token_hex(8)
    cap_path = _infer_category_path(item["memo"], item.get("context") or "", item["tags"])
    # v1.2.39: 时间解析 + 矛盾检测
    from core.contradiction import check_contradiction_on_ingest
    valid_from, valid_to, contradictions = check_contradiction_on_ingest(
        item["memo"], cap_path
    )
    insert_capsule(
        capsule_id=cap_id,
        memo=item["memo"],
        content=item.get("context") or "",
        tags=item["tags"],
        session_id=None,
        window_title=None,
        url=None,
        created_at=time.time(),
        source_type="ai_chat",
        category=item["category"],
        category_path=cap_path,
        valid_from=valid_from,
        valid_to=valid_to,
    )
    queue_set_status(qid, "approved")
    resp = {"capsule_id": cap_id, "message": "Approved and saved"}
    if contradictions:
        resp["contradictions"] = contradictions
    return JSONResponse(resp, headers=h)


@app.post("/queue/{qid}/reject")
def reject_queue_item(qid: str, request: Request = None,
                      authorization: str = Header(None)):
    """忽略待审核记忆"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    h = add_cors_headers(request) if request else {}

    item = queue_get(qid)
    if not item:
        return JSONResponse({"error": "not found"}, status_code=404, headers=h)
    queue_set_status(qid, "rejected")
    return JSONResponse({"message": "Rejected"}, headers=h)


@app.post("/queue/{qid}/edit")
def edit_queue_item(qid: str, body: QueueEditIn, request: Request = None,
                    authorization: str = Header(None)):
    """编辑后接受待审核记忆"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    h = add_cors_headers(request) if request else {}

    item = queue_get(qid)
    if not item:
        return JSONResponse({"error": "not found"}, status_code=404, headers=h)

    final_memo = body.memo or item["memo"]
    final_category = body.category or item["category"]
    final_tags = body.tags or item["tags"]

    # ── G1: 记录校正事件 ────────────────────────────────
    cap_id_for_correction = secrets.token_hex(8)  # 预生成用于关联校正记录
    try:
        from core.correction import record_tag_correction, record_category_correction
        # 标签校正
        if body.tags and body.tags != (item.get("tags") or ""):
            orig_tags = [(t.strip().lower()) for t in (item.get("tags") or "").split(",") if t.strip()]
            new_tags_list = [(t.strip().lower()) for t in body.tags.split(",") if t.strip()]
            for ot in orig_tags:
                for nt in new_tags_list:
                    if nt and nt != ot:
                        record_tag_correction(ot, nt, queue_id=qid)
        # 分类校正
        if body.category and body.category != (item.get("category") or ""):
            record_category_correction(
                item.get("category") or "",
                body.category,
                queue_id=qid,
            )
    except Exception:
        pass  # 校正记录失败不影响入库

    queue_update(qid, final_memo, final_category, final_tags)
    cap_id = cap_id_for_correction
    insert_capsule(
        capsule_id=cap_id,
        memo=final_memo,
        content=item.get("context") or "",
        tags=final_tags,
        session_id=None,
        window_title=None,
        url=None,
        created_at=time.time(),
        source_type="ai_chat",
        category=final_category,
    )
    return JSONResponse({"capsule_id": cap_id, "message": "Edited and saved"}, headers=h)


# ── /-review 端点（v1.2.8 — 终端友好队列审阅）────────────────

@app.get("/-review")
def review_queue(request: Request = None, authorization: str = Header(None)):
    """
    终端友好的待审核记忆列表。
    curl "http://localhost:18998/-review?token=$TOKEN"
    ?format=text （默认）返回纯文本 lines 数组，适合 curl 管道
    ?format=json 返回完整 JSON 格式
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    h = add_cors_headers(request) if request else {}

    fmt = request.query_params.get("format", "text") if request else "text"
    pending = queue_list_pending()
    if not pending:
        if fmt == "json":
            return JSONResponse({"lines": [], "count": 0}, headers=h)
        return JSONResponse({"lines": ["📋 待审阅记忆 (0条)"], "count": 0}, headers=h)

    lines = [f"📋 待审阅记忆 ({len(pending)}条)\n"]
    for i, item in enumerate(pending, 1):
        memo = item.get("memo", "")[:60]
        tags = item.get("tags", "") or "无标签"
        conf = item.get("confidence", 0)
        cat = item.get("category", "") or "general"
        ctx = item.get("context", "")[:80]

        emoji = "💭" if cat == "preference" else "🎯" if cat == "decision" else "📖"
        lines.append(f"[{i}] {emoji} \"{memo}\"")
        lines.append(f"   标签: {tags} | 置信度: {conf:.2f}")
        if ctx:
            lines.append(f"   上下文: {ctx}")
        lines.append("")

    lines.append("---")
    lines.append("操作: curl -X POST \"/-review/{id}?action=approve&token=$TOKEN\"")
    lines.append("     curl -X POST \"/-review/{id}?action=reject&token=$TOKEN\"")

    if fmt == "json":
        return JSONResponse({"lines": lines, "count": len(pending), "items": pending}, headers=h)
    return JSONResponse({"lines": lines, "count": len(pending)}, headers=h)


@app.post("/-review/{qid}")
def review_item(qid: str, request: Request = None, authorization: str = Header(None)):
    """
    审阅单个队列项（approve / reject / edit）。
    curl -X POST "http://localhost:18998/-review/abc123?action=approve&token=$TOKEN"
    curl -X POST "http://localhost:18998/-review/abc123?action=reject&token=$TOKEN"
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    h = add_cors_headers(request) if request else {}

    action = request.query_params.get("action") if request else None
    if action not in ("approve", "reject"):
        return JSONResponse({"error": "action must be approve or reject"}, status_code=400, headers=h)

    item = queue_get(qid)
    if not item:
        return JSONResponse({"error": "not found"}, status_code=404, headers=h)
    if item["status"] != "pending":
        return JSONResponse({"error": "already processed"}, status_code=400, headers=h)

    if action == "approve":
        cap_id = secrets.token_hex(8)
        cap_path = _infer_category_path(item["memo"], item.get("context") or "", item["tags"])
        insert_capsule(
            capsule_id=cap_id,
            memo=item["memo"],
            content=item.get("context") or "",
            tags=item["tags"],
            session_id=None,
            window_title=None,
            url=None,
            created_at=time.time(),
            source_type="ai_chat",
            category=item["category"],
            category_path=cap_path,
        )
        queue_set_status(qid, "approved")
        return JSONResponse({"capsule_id": cap_id, "action": "approved"}, headers=h)
    else:
        queue_set_status(qid, "rejected")
        return JSONResponse({"qid": qid, "action": "rejected"}, headers=h)


# ── Push Notifications（v1.2.34）────────────────────────────
class NotifyBody(BaseModel):
    title: str = "琥珀记忆"
    body: str = ""
    tag: str = "amber-hunter"
    url: str = ""


@app.post("/notify")
def send_notification(request: Request, body: NotifyBody, authorization: str = Header(None)):
    """
    通过 huper.org 推送浏览器通知。
    需要 master_password 已配置（通知权限验证）。
    curl -X POST http://localhost:18998/notify \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"title":"新记忆","body":"已捕获一条重要记忆"}'
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    h = add_cors_headers(request)

    api_token = get_api_token()
    huper_url = get_huper_url() or "https://huper.org/api"
    if not api_token:
        return JSONResponse({"error": "huper API token not configured"}, status_code=400, headers=h)

    try:
        import httpx
        payload = {
            "title": body.title,
            "body": body.body,
            "tag": body.tag,
            "url": body.url or f"{huper_url}/dashboard",
        }
        resp = httpx.post(
            f"{huper_url}/notify",
            json=payload,
            headers={"Authorization": f"Bearer {api_token}"},
            timeout=10.0,
        )
        if resp.status_code in (200, 201):
            return JSONResponse({"sent": True, "title": body.title}, headers=h)
        return JSONResponse({"sent": False, "status": resp.status_code, "detail": resp.text[:200]}, status_code=502, headers=h)
    except httpx.ConnectError:
        # huper.org 不可达（本地网络或服务器宕机）
        return JSONResponse({"sent": False, "error": "huper.org unreachable"}, status_code=503, headers=h)
    except Exception as e:
        import sys
        print(f"[notify] failed: {e}", file=sys.stderr)
        return JSONResponse({"sent": False, "error": str(e)}, status_code=500, headers=h)


# ── 后台同步 helper（供 freeze 自动触发 & 定时器共用）────────────
def _do_sync_capsules(unsynced: list, api_token: str, huper_url: str, master_pw: str) -> dict:
    """
    核心同步逻辑（v1.2.15）。
    - 单个 httpx.Client 复用连接，避免每条胶囊建立新 TCP 连接
    - payload 包含 source_type / category，确保云端字段完整
    - P1-4: 5xx 最多重试 2 次（指数退避 1s/2s）
    - P2-9: 网络可达性预检
    - 返回 {"synced": int, "total": int, "errors": list}
    """
    import httpx
    from urllib.parse import urlparse
    import socket

    synced_count = 0
    errors = []

    # P2-9: 网络可达性预检
    parsed = urlparse(huper_url)
    host = parsed.netloc or parsed.path.split("/")[0]
    try:
        sock = socket.create_connection((host, 443), timeout=3.0)
        sock.close()
    except OSError:
        return {"synced": 0, "total": len(unsynced),
                "errors": [{"error": f"network unreachable: {host}"}]}

    try:
        with httpx.Client(timeout=15.0, trust_env=False) as client:
            for capsule in unsynced:
                # ── 准备加密 payload（支持 DID key）─────────────
                salt_b64 = capsule.get("salt")
                if not salt_b64:
                    errors.append({"id": capsule["id"], "error": "no salt, skipped"})
                    continue

                key_source = capsule.get("key_source", "pbkdf2")
                if key_source == "did":
                    # DID 加密胶囊：读取 did.json 派生密钥
                    did_cfg = {}
                    if DID_CONFIG_PATH.exists():
                        try:
                            did_cfg = json.loads(DID_CONFIG_PATH.read_text())
                        except Exception:
                            pass
                    device_priv = did_cfg.get("device_priv")
                    if device_priv:
                        key, _ = derive_capsule_key(device_priv, capsule["id"])
                    else:
                        errors.append({"id": capsule["id"], "error": "DID key missing in did.json, skipped"})
                        continue
                else:
                    salt = base64.b64decode(salt_b64)
                    key = derive_key(master_pw, salt)

                content_enc   = capsule.get("content") or ""
                content_nonce = capsule.get("nonce")   or ""

                memo_bytes = (capsule.get("memo") or "").encode("utf-8")
                memo_ct, memo_nonce = encrypt_content(memo_bytes, key)
                memo_enc       = base64.b64encode(memo_ct).decode()
                memo_nonce_b64 = base64.b64encode(memo_nonce).decode()

                tags_bytes = (capsule.get("tags") or "").encode("utf-8")
                tags_ct, tags_nonce = encrypt_content(tags_bytes, key)
                tags_enc       = base64.b64encode(tags_ct).decode()
                tags_nonce_b64 = base64.b64encode(tags_nonce).decode()

                payload = {
                    "e2e":           True,
                    "salt":          salt_b64,
                    "memo_enc":      memo_enc,
                    "memo_nonce":    memo_nonce_b64,
                    "content_enc":   content_enc,
                    "content_nonce": content_nonce,
                    "tags_enc":      tags_enc,
                    "tags_nonce":    tags_nonce_b64,
                    "created_at":    capsule.get("created_at"),
                    "session_id":    capsule.get("session_id"),
                    "source_type":   capsule.get("source_type") or "manual",
                    "category":      capsule.get("category") or "",
                }

                # P1-4: 重试逻辑（5xx 最多重试 2 次，指数退避）
                last_err = None
                for attempt in range(3):
                    try:
                        resp = client.post(
                            f"{huper_url}/capsules",
                            json=payload,
                            headers={"Authorization": f"Bearer {api_token}"}
                        )
                        if resp.status_code in (200, 201):
                            mark_synced(capsule["id"])
                            synced_count += 1
                            last_err = None
                            break
                        elif resp.status_code >= 500:
                            # 5xx：还有重试机会则等待后重试
                            if attempt < 2:
                                time.sleep(2 ** attempt)
                                continue
                            # attempt == 2: 重试耗尽，记录错误
                            last_err = {"id": capsule["id"], "status": resp.status_code,
                                        "body": resp.text[:120]}
                        else:
                            # 4xx：不可重试，直接记录错误
                            last_err = {"id": capsule["id"], "status": resp.status_code,
                                        "body": resp.text[:120]}
                    except Exception as e:
                        last_err = {"id": capsule["id"], "error": str(e)}
                        if attempt < 2:
                            time.sleep(2 ** attempt)
                            continue
                if last_err is not None:
                    errors.append(last_err)

    except Exception as e:
        errors.append({"error": f"httpx init failed: {e}"})

    # P3-11: 同步完成后更新 last_sync_at（无论成功与否）
    set_config("last_sync_at", str(time.time()))
    return {"synced": synced_count, "total": len(unsynced), "errors": errors}


def _background_sync() -> dict:
    """后台线程同步入口（无 HTTP 上下文）。"""
    try:
        api_token = get_api_token()
        huper_url = get_huper_url() or "https://huper.org/api"
        master_pw = get_master_password()
        if not master_pw:
            logging.warning("[amber-hunter] auto-sync: master_password not set, skip")
            return {"synced": 0, "total": 0, "errors": ["master_password not set"]}
        unsynced = get_unsynced_capsules()
        if not unsynced:
            return {"synced": 0, "total": 0, "errors": []}
        result = _do_sync_capsules(unsynced, api_token, huper_url, master_pw)
        logging.info(f"[amber-hunter] auto-sync: {result['synced']}/{result['total']}")
        return result
    except Exception as e:
        logging.error(f"[amber-hunter] _background_sync error: {e}")
        set_config("sync_last_error", json.dumps({
            "ts": time.time(), "msg": str(e),
        }))
        return {"synced": 0, "total": 0, "errors": [str(e)]}


# P1-6: 同步并发锁，防止重复并发同步
_sync_lock = threading.Lock()


def _spawn_sync_if_enabled():
    """如果 auto_sync 已启用，在守护线程里执行同步（非阻塞）。"""
    if get_config("auto_sync") == "true":
        if not _sync_lock.acquire(blocking=False):
            logging.debug("[amber-hunter] sync already running, skipping")
            return
        try:
            t = threading.Thread(target=_background_sync_locked, daemon=True)
            t.start()
        except Exception:
            _sync_lock.release()
            raise


def _background_sync_locked():
    """在锁内运行的 _background_sync wrapper，释放锁"""
    try:
        _background_sync()
    finally:
        _sync_lock.release()


@app.get("/sync")
def sync_to_cloud(request: Request, authorization: str = Header(None)):
    """
    E2E 加密同步到 huper 云端。
    - memo + tags 圤本地加密后上传，服务端仅存密文
    - content 已圤本地加密，直接传输密文，无需解密
    - 服务端永远看不到任何明文内容
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    api_token = get_api_token()
    huper_url = get_huper_url() or "https://huper.org/api"
    master_pw = get_master_password()
    if not master_pw:
        return JSONResponse(
            {"error": "master_password not set", "detail": "请在 dashboard 设置 master_password"},
            status_code=400, headers=add_cors_headers(request)
        )

    # P2-3: 增量 sync — 使用 last_sync_at 时间戳
    last_sync_ts = float(get_config("last_sync_at") or "0")
    unsynced = get_unsynced_capsules(since=last_sync_ts)
    if not unsynced:
        return JSONResponse({"synced": 0, "total": 0, "message": "没有需要同步的胶囊"},
                            headers=add_cors_headers(request))

    # P1-5: 分批处理，每批 50 条，避免大量胶囊时超时/内存爆炸
    BATCH_SIZE = 50
    total_synced = 0
    all_errors = []
    for i in range(0, len(unsynced), BATCH_SIZE):
        batch = unsynced[i:i + BATCH_SIZE]
        result = _do_sync_capsules(batch, api_token, huper_url, master_pw)
        total_synced += result["synced"]
        all_errors.extend(result["errors"])
        if i + BATCH_SIZE < len(unsynced):
            time.sleep(0.3)  # 批次间稍作延迟，避免瞬时过载

    logging.info(f"[amber-hunter] /sync: {total_synced}/{len(unsynced)}")
    h = add_cors_headers(request)

    # P2-3: 增量 sync — 成功后更新 last_sync_at
    if total_synced > 0:
        set_config("last_sync_at", str(time.time()))

    return JSONResponse({
        "synced": total_synced,
        "total":  len(unsynced),
        "failed": len(all_errors),
        "errors": all_errors[:10] if all_errors else None,
        "partial": total_synced > 0 and total_synced < len(unsynced),
        "all_synced": total_synced == len(unsynced),
        "incremental": last_sync_ts > 0,
    }, headers=h)


# ── P2-3: Cross-device Sync — Pull from Cloud ─────────────────────────────
def _pull_from_cloud(api_token: str, huper_url: str, master_pw: str) -> dict:
    """
    从云端拉取本设备不存在的胶囊。
    返回 {"pulled": int, "conflicts": int, "errors": list}
    """
    import httpx
    from urllib.parse import urlparse

    pulled = 0
    conflicts = 0
    errors = []

    # 网络可达性检查
    parsed = urlparse(huper_url)
    host = parsed.netloc or parsed.path.split("/")[0]
    try:
        import socket
        sock = socket.create_connection((host, 443), timeout=3.0)
        sock.close()
    except OSError:
        return {"pulled": 0, "conflicts": 0, "errors": [{"error": f"network unreachable: {host}"}]}

    try:
        with httpx.Client(timeout=15.0, trust_env=False) as client:
            # 获取云端胶囊列表
            resp = client.get(
                f"{huper_url}/capsules",
                headers={"Authorization": f"Bearer {api_token}"},
                params={"limit": 300},
            )
            if resp.status_code == 401:
                return {"pulled": 0, "conflicts": 0, "errors": [{"error": "unauthorized, check api_token"}]}
            if resp.status_code not in (200, 201):
                return {"pulled": 0, "conflicts": 0, "errors": [{"error": f"cloud returned {resp.status_code}"}]}

            cloud_capsules = resp.json() if resp.text else []
            if isinstance(cloud_capsules, dict):
                cloud_capsules = cloud_capsules.get("capsules", [])

        # 获取本地所有胶囊的 ID 和 updated_at
        conn = _get_conn()
        c = conn.cursor()
        local_rows = c.execute("SELECT id, updated_at FROM capsules").fetchall()
        local_map = {str(r[0]): float(r[1] or r[0]) for r in local_rows}  # id -> updated_at

        for cloud_cap in cloud_capsules:
            cloud_id = cloud_cap.get("id") or cloud_cap.get("capsule_id")
            if not cloud_id:
                continue

            cloud_updated = float(cloud_cap.get("updated_at", 0) or cloud_cap.get("created_at", 0))

            if cloud_id in local_map:
                # 冲突检测：LWW
                local_updated = local_map[cloud_id]
                if cloud_updated > local_updated:
                    # 云端更新，保留云端（覆盖本地）
                    try:
                        _import_cloud_capsule(cloud_cap, master_pw)
                        pulled += 1
                    except Exception as e:
                        errors.append({"id": cloud_id, "error": str(e)})
                    conflicts += 1
                # else: 本地更新，保留本地，不操作
            else:
                # 云端有，本地没有 → 导入
                try:
                    _import_cloud_capsule(cloud_cap, master_pw)
                    pulled += 1
                except Exception as e:
                    errors.append({"id": cloud_id, "error": str(e)})

    except Exception as e:
        errors.append({"error": f"pull failed: {e}"})

    return {"pulled": pulled, "conflicts": conflicts, "errors": errors}


def _import_cloud_capsule(cloud_cap: dict, master_pw: str) -> None:
    """解密并导入云端胶囊到本地数据库。"""
    from core.crypto import derive_key, decrypt_content
    import base64

    cap_id = cloud_cap.get("id") or cloud_cap.get("capsule_id")
    memo_enc = cloud_cap.get("memo_enc", "")
    memo_nonce = cloud_cap.get("memo_nonce", "")
    content_enc = cloud_cap.get("content_enc", "")
    content_nonce = cloud_cap.get("content_nonce", "")
    tags_enc = cloud_cap.get("tags_enc", "")
    tags_nonce = cloud_cap.get("tags_nonce", "")
    salt_b64 = cloud_cap.get("salt", "")
    created_at = float(cloud_cap.get("created_at", time.time()))
    updated_at = float(cloud_cap.get("updated_at", created_at))

    if not salt_b64:
        return  # 无法解密

    # 解密
    try:
        salt = base64.b64decode(salt_b64)
        key = derive_key(master_pw, salt)

        def _decrypt_text(enc_b64, nonce_b64):
            if not enc_b64 or not nonce_b64:
                return ""
            try:
                ct = base64.b64decode(enc_b64)
                nonce = base64.b64decode(nonce_b64)
                pt = decrypt_content(ct, key, nonce)
                return pt.decode("utf-8") if pt else ""
            except Exception:
                return ""

        memo = _decrypt_text(memo_enc, memo_nonce)
        content = _decrypt_text(content_enc, content_nonce)
        tags = _decrypt_text(tags_enc, tags_nonce)
    except Exception:
        memo = cloud_cap.get("memo", "") or ""
        content = ""
        tags = cloud_cap.get("tags", "") or ""

    category = cloud_cap.get("category", "") or ""
    source_type = cloud_cap.get("source_type", "sync") or "sync"
    session_id = cloud_cap.get("session_id")

    # 写入本地 DB
    conn = _get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO capsules
          (id, memo, content, tags, session_id, window_title, url, created_at, updated_at,
           salt, nonce, encrypted_len, content_hash, synced, source_type, category, category_path, key_source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, 'general/default', 'pbkdf2')
    """, (
        cap_id, memo, content, tags, session_id,
        cloud_cap.get("window_title"), cloud_cap.get("url"),
        created_at, updated_at,
        salt_b64, cloud_cap.get("nonce", ""),
        len(content_enc), cloud_cap.get("content_hash", ""),
        source_type, category,
    ))
    conn.commit()


@app.get("/sync/pull")
def sync_pull(request: Request, authorization: str = Header(None)):
    """
    从云端拉取新胶囊到本地（双向同步之 Pull 方向）。
    使用 LWW（Last Write Wins）策略解决冲突。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    api_token = get_api_token()
    huper_url = get_huper_url() or "https://huper.org/api"
    master_pw = get_master_password()
    if not master_pw:
        return JSONResponse(
            {"error": "master_password not set"},
            status_code=400, headers=add_cors_headers(request)
        )

    result = _pull_from_cloud(api_token, huper_url, master_pw)
    logging.info(f"[amber-hunter] /sync/pull: {result}")
    return JSONResponse(result, headers=add_cors_headers(request))


@app.post("/sync/resolve/{capsule_id}")
def resolve_conflict(capsule_id: str, request: Request, resolution: str = "local",
                    authorization: str = Header(None)):
    """
    手动解决同步冲突。
    resolution: 'local' = 保留本地版本，'cloud' = 保留云端版本
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    if resolution not in ("local", "cloud"):
        return JSONResponse({"error": "resolution must be local or cloud"}, status_code=400)

    if resolution == "cloud":
        # 从云端重新拉取该胶囊
        api_token = get_api_token()
        huper_url = get_huper_url() or "https://huper.org/api"
        master_pw = get_master_password()
        try:
            import httpx
            with httpx.Client(timeout=10.0, trust_env=False) as client:
                resp = client.get(
                    f"{huper_url}/capsules/{capsule_id}",
                    headers={"Authorization": f"Bearer {api_token}"}
                )
                if resp.status_code == 200:
                    cloud_cap = resp.json()
                    _import_cloud_capsule(cloud_cap, master_pw)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
    else:
        # 保留本地：标记本地为已同步（强制上传）
        from core.db import _get_conn
        conn = _get_conn()
        c = conn.cursor()
        now = time.time()
        c.execute("UPDATE capsules SET synced=1, updated_at=? WHERE id=?", (now, capsule_id))
        conn.commit()
        conn.close()

    return JSONResponse({"id": capsule_id, "resolution": resolution})


class NotifyIn(BaseModel):
    title: str = "琥珀记忆提醒"
    body: str
    url: str = ""

@app.post("/notify")
def push_notify(body_in: NotifyIn, request: Request = None, authorization: str = Header(None)):
    """
    通过 huper.org 推送浏览器通知（需要用户已在 huper.org 授权推送）。
    amber-proactive agent 在主动召回成功时调用此端点。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    api_token = get_api_token()
    huper_url = get_huper_url() or "https://huper.org/api"

    try:
        import httpx
        with httpx.Client(timeout=10.0, trust_env=False) as client:
            resp = client.post(
                f"{huper_url}/notify",
                json={"title": body_in.title, "body": body_in.body, "url": body_in.url},
                headers={"Authorization": f"Bearer {api_token}"},
            )
            if resp.status_code in (200, 201):
                return JSONResponse({"ok": True})
            return JSONResponse({"ok": False, "error": f"huper responded {resp.status_code}"}, status_code=502)
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)


class SyncResolveIn(BaseModel):
    capsule_id: str
    decision: str  # "keep_local" | "keep_cloud"

@app.post("/sync/resolve")
def sync_resolve(body: SyncResolveIn, request: Request, authorization: str = Header(None)):
    """
    手动解决同步冲突。
    decision: "keep_local" → 上传本地版本到云端覆盖
             "keep_cloud"  → 从云端拉取覆盖本地
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    if body.decision not in ("keep_local", "keep_cloud"):
        return JSONResponse({"error": "decision must be keep_local or keep_cloud"}, status_code=400)

    api_token = get_api_token()
    huper_url = get_huper_url() or "https://huper.org/api"
    master_pw = get_master_password()
    if not master_pw:
        return JSONResponse({"error": "master_password not set"}, status_code=400)

    cap_id = body.capsule_id
    conn = _get_conn()
    c = conn.cursor()

    if body.decision == "keep_local":
        # 读取本地胶囊并重新上传到云端
        row = c.execute(
            "SELECT id,memo,content,tags,session_id,window_title,url,created_at,updated_at,"
            "salt,nonce,encrypted_len,content_hash,source_type,category "
            "FROM capsules WHERE id=?",
            (cap_id,)
        ).fetchone()
        if not row:
            return JSONResponse({"error": "capsule not found locally"}, status_code=404)
        # 构造 single-capsule list 调用 _do_sync_capsules
        capsule = {
            "id": row[0], "memo": row[1], "content": row[2], "tags": row[3],
            "session_id": row[4], "window_title": row[5], "url": row[6],
            "created_at": row[7], "updated_at": row[8],
            "salt": row[9], "nonce": row[10], "encrypted_len": row[11],
            "content_hash": row[12], "source_type": row[13], "category": row[14],
            "key_source": "pbkdf2",
        }
        result = _do_sync_capsules([capsule], api_token, huper_url, master_pw)
        return JSONResponse({"ok": True, "synced": result["synced"], "errors": result.get("errors", [])[:3]})
    else:
        # 从云端拉取覆盖本地
        try:
            import httpx
            with httpx.Client(timeout=15.0, trust_env=False) as client:
                resp = client.get(
                    f"{huper_url}/capsules/{cap_id}",
                    headers={"Authorization": f"Bearer {api_token}"},
                )
                if resp.status_code == 404:
                    return JSONResponse({"error": "capsule not found on cloud"}, status_code=404)
                cloud_cap = resp.json()
            _import_cloud_capsule(cloud_cap, master_pw)
            return JSONResponse({"ok": True, "source": "cloud"})
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)


# ── 配置读取（Dashboard 用）────────────────────────────
class ConfigIn(BaseModel):
    auto_sync: Optional[bool] = None
    sync_interval_minutes: Optional[int] = None  # P3-13

@app.get("/config")
def get_config_handler(request: Request, authorization: str = Header(None)):
    """获取配置（auto_sync、sync_interval_minutes 等）"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    auto_sync = get_config("auto_sync")
    sync_interval = get_config("sync_interval_minutes")
    return JSONResponse({
        "auto_sync": auto_sync == "true",
        "sync_interval_minutes": int(sync_interval) if sync_interval else 30,
    }, headers=add_cors_headers(request))

@app.post("/config")
def set_config_handler(cfg_in: ConfigIn, request: Request, authorization: str = Header(None)):
    """更新配置"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    if cfg_in.auto_sync is not None:
        set_config("auto_sync", "true" if cfg_in.auto_sync else "false")
    if cfg_in.sync_interval_minutes is not None:
        set_config("sync_interval_minutes", str(cfg_in.sync_interval_minutes))
    return JSONResponse({"ok": True}, headers=add_cors_headers(request))

@app.get("/config/llm")
async def get_llm_config(request: Request, authorization: str = Header(None)):
    """获取当前 LLM provider 配置（不返回 api_key 明文）"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    cfg = load_llm_config()
    safe_config = {
        "provider": cfg.provider,
        "model": cfg.model,
        "base_url": cfg.base_url,
    }
    return JSONResponse(safe_config, headers=add_cors_headers(request))

@app.put("/config/llm")
async def update_llm_config(request: Request, authorization: str = Header(None)):
    """更新 LLM provider 配置"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    body = await request.json()
    provider = body.get("provider")
    model = body.get("model")
    if provider not in ("minimax", "openai", "claude", "local"):
        return JSONResponse({"error": "invalid provider"}, status_code=400)
    cfg = load_llm_config()
    if provider:
        cfg.provider = provider
    if model:
        cfg.model = model
    save_llm_config(cfg)
    return JSONResponse({"ok": True, "provider": cfg.provider}, headers=add_cors_headers(request))

# ── P1-2: Embedding 配置（Dashboard 用）───────────────────
@app.get("/config/embedding")
async def get_embed_config(request: Request, authorization: str = Header(None)):
    """获取当前 embedding provider 配置（不返回 api_key 明文）"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    from core.embedding import get_cached_embed
    cfg = get_cached_embed().config
    return JSONResponse({
        "provider": cfg.provider,
        "model": cfg.model,
        "base_url": cfg.base_url,
        "dimension": cfg.dimension,
    }, headers=add_cors_headers(request))

@app.put("/config/embedding")
async def update_embed_config(request: Request, authorization: str = Header(None)):
    """更新 embedding provider 配置"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    body = await request.json()
    from core.embedding import EmbedConfig, save_embed_config, reset_embed_provider
    cfg = EmbedConfig()
    if body.get("provider"):
        cfg.provider = body["provider"]
    if body.get("model"):
        cfg.model = body["model"]
    if body.get("base_url"):
        cfg.base_url = body["base_url"]
    if body.get("api_key"):
        cfg.api_key = body["api_key"]
    if body.get("dimension"):
        cfg.dimension = int(body["dimension"])
    save_embed_config(cfg)
    reset_embed_provider()  # 清除缓存，下次使用时重新加载
    return JSONResponse({"ok": True, "provider": cfg.provider}, headers=add_cors_headers(request))

# ── master_password 设置（Dashboard 用）────────────────
from pydantic import BaseModel
class BindApiKeyIn(BaseModel):
    api_key: str

@app.post("/bind-apikey")
def bind_apikey_handler(payload: BindApiKeyIn, request: Request):
    """更新 Huper 云端 API Key（仅限本机请求）"""
    client = request.client
    if client and client.host not in ("127.0.0.1", "::1", "localhost"):
        return JSONResponse({"error": "forbidden"}, status_code=403)
    try:
        import json as _json
        cfg = {}
        if CONFIG_PATH.exists():
            cfg = _json.loads(CONFIG_PATH.read_text())
        cfg["api_key"] = payload.api_key
        CONFIG_PATH.parent.mkdir(exist_ok=True)
        CONFIG_PATH.write_text(_json.dumps(cfg, indent=2))
        return JSONResponse({"ok": True}, headers=add_cors_headers(request))
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500, headers=add_cors_headers(request))

class MasterPasswordIn(BaseModel):
    password: str

@app.post("/master-password")
def set_master_password_handler(password_in: MasterPasswordIn, request: Request):
    """设置 master_password（存 macOS Keychain + config.json 双备份）"""
    client = request.client
    if client and client.host not in ("127.0.0.1", "::1", "localhost"):
        return JSONResponse({"error": "forbidden"}, status_code=403)
    ok1 = set_master_password(password_in.password)
    # 同时写到 config.json 作为 fallback（Keychain 访问可能受限）
    try:
        import json as _json
        cfg = {}
        if CONFIG_PATH.exists():
            cfg = _json.loads(CONFIG_PATH.read_text())
        cfg["master_password"] = password_in.password
        CONFIG_PATH.parent.mkdir(exist_ok=True)
        CONFIG_PATH.write_text(_json.dumps(cfg, indent=2))
        ok2 = True
    except Exception:
        ok2 = False
    return JSONResponse({"ok": ok1 or ok2, "keychain": ok1, "config": ok2}, headers=add_cors_headers(request))

# ── 本地 Token（仅 localhost 可读）──────────────────────
@app.get("/token")
def get_local_token(request: Request):
    """返回本地 API token（仅限本机请求，browser→amber-hunter 直连用）"""
    client = request.client
    if client and client.host not in ("127.0.0.1", "::1", "localhost"):
        return JSONResponse({"error": "forbidden"}, status_code=403)
    token = get_api_token()
    if not token:
        return JSONResponse({"api_key": None}, headers=add_cors_headers(request))
    return JSONResponse({"api_key": token}, headers=add_cors_headers(request))

# ── MFS 路径归类（需认证）────────────────────────────────
@app.post("/admin/backfill-paths")
def backfill_paths(request: Request, authorization: str = Header(None), dry_run: bool = True):
    """
    批量归类历史胶囊的 category_path。
    dry_run=true（默认）只报告不写入。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    stats = backfill_category_paths(dry_run=dry_run)
    return JSONResponse({
        "dry_run": dry_run,
        "total_checked": stats["total"],
        "would_update": stats["updated"],
        "by_path": stats["by_path"],
    }, headers=add_cors_headers(request))


# ── 向量索引重建（需认证）────────────────────────────────
@app.post("/admin/reindex-vectors")
def reindex_vectors(request: Request, authorization: str = Header(None)):
    """
    重建 LanceDB 向量索引，遍历所有胶囊并重新索引 memo 字段。
    用于首次填充向量索引或切换 embedding provider 后的重建。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    from core.vector import init_vector_db, index_capsule, reset_embed_provider
    import time

    # 重置 embedding provider 缓存，确保使用最新配置
    reset_embed_provider()

    conn = _get_conn()
    c = conn.cursor()
    rows = c.execute(
        "SELECT id, memo, created_at FROM capsules WHERE memo IS NOT NULL AND memo != ''"
    ).fetchall()

    indexed = 0
    failed = 0
    start = time.time()

    for cid, memo, created_at in rows:
        try:
            if index_capsule(cid, memo, created_at or time.time()):
                indexed += 1
            else:
                failed += 1
        except Exception:
            failed += 1

    from core.vector import get_vector_stats
    stats = get_vector_stats()
    elapsed = time.time() - start

    logging.info(f"[reindex-vectors] indexed={indexed} failed={failed} elapsed={elapsed:.1f}s")
    return JSONResponse({
        "indexed": indexed,
        "failed": failed,
        "total": len(rows),
        "vector_count": stats.get("count", 0),
        "elapsed_seconds": round(elapsed, 1),
    }, headers=add_cors_headers(request))


# ── 本地 GPT Fine-tune（需认证）──────────────────────────────
class TrainIn(BaseModel):
    vocab_size: int = 2500
    iterations: int = 300
    lr: float = 1e-3
    batch_size: int = 32
    use_gpt2_pretrain: bool = True  # 是否用 GPT-2 预训练权重初始化
    incremental: bool = True         # 是否从 checkpoint 继续


@app.post("/admin/train")
def admin_train(request: Request, body: TrainIn, authorization: str = Header(None)):
    """
    在用户记忆数据上 fine-tune AmberGPT。
    使用 auto-research 优化超参（N_HEAD=1, BLOCK_SIZE=96, N_EMBED=256, N_LAYER=6）。
    支持 GPT-2 预训练初始化和增量训练。

    curl -X POST http://localhost:18998/admin/train \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"vocab_size":2500,"iterations":300,"use_gpt2_pretrain":true}'
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    h = add_cors_headers(request)

    import threading

    def run_train():
        from core.trainer import fine_tune, get_trainer, AmberTrainer
        result = fine_tune(
            vocab_size=body.vocab_size,
            iterations=body.iterations,
            lr=body.lr,
            batch_size=body.batch_size,
            use_gpt2_pretrain=body.use_gpt2_pretrain,
            incremental=body.incremental,
        )
        # 重置 trainer 单例以加载新模型
        AmberTrainer._instance = None
        get_trainer()

    thread = threading.Thread(target=run_train, daemon=True)
    thread.start()
    return JSONResponse({
        "started": True,
        "message": f"Training started (vocab_size={body.vocab_size}, iterations={body.iterations}, gpt2={body.use_gpt2_pretrain}, incremental={body.incremental})",
        "check_status": "GET /admin/train/status",
    }, headers=h)


@app.get("/admin/train/status")
def train_status(request: Request, authorization: str = Header(None)):
    """检查本地模型训练状态"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    from core.trainer import is_trained, AmberTrainer, get_trainer, MODEL_PATH
    import torch
    at = get_trainer()
    trained_info = {}
    if is_trained():
        try:
            ckpt = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
            trained_info = {
                "iterations": ckpt.get("iterations", "?"),
                "val_loss": round(ckpt.get("val_loss", 0), 4),
                "tag_vocab_size": ckpt.get("tag_vocab_size", 0),
            }
        except Exception:
            pass
    return JSONResponse({
        "is_trained": is_trained(),
        "model_ready": at.is_ready(),
        "has_tag_head": at.has_tag_head(),
        **trained_info,
    }, headers=add_cors_headers(request))


@app.get("/admin/train/score")
def train_score(request: Request, authorization: str = Header(None)):
    """对 query 和 memory 文本评分（需先训练）"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    query = request.query_params.get("q", "")
    memory = request.query_params.get("memory", "")
    if not query or not memory:
        return JSONResponse({"error": "q and memory params required"}, status_code=400)
    from core.trainer import get_trainer
    at = get_trainer()
    if not at.is_ready():
        return JSONResponse({"error": "model not trained yet", "trained": False}, status_code=400)
    score = at.score(query, memory)
    return JSONResponse({"score": round(score, 4), "trained": True}, headers=add_cors_headers(request))


@app.get("/admin/train/tags")
def train_tags(request: Request, authorization: str = Header(None)):
    """预测文本标签（需先训练有分类头的模型）"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    text = request.query_params.get("text", "")
    if not text:
        return JSONResponse({"error": "text param required"}, status_code=400)
    from core.trainer import get_trainer
    at = get_trainer()
    if not at.has_tag_head():
        return JSONResponse({"error": "tag head not available (needs training with incremental=True)", "has_tag_head": False}, status_code=400)
    tags = at.predict_tags(text)
    return JSONResponse({"tags": [{"tag": t, "score": round(s, 4)} for t, s in tags], "has_tag_head": True}, headers=add_cors_headers(request))


# ── 统计面板（需认证）────────────────────────────────────
@app.get("/stats")
def get_stats(request: Request, authorization: str = Header(None)):
    """
    返回记忆统计：总数、分类分布、热度分布、同步状态。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    conn = _get_conn()
    c = conn.cursor()

    # 总数
    total = c.execute("SELECT COUNT(*) FROM capsules").fetchone()[0]
    total_content = c.execute("SELECT COUNT(*) FROM capsules WHERE content IS NOT NULL AND content != ''").fetchone()[0]

    # 分类分布
    cat_rows = c.execute(
        "SELECT category_path, COUNT(*) as cnt FROM capsules GROUP BY category_path ORDER BY cnt DESC LIMIT 20"
    ).fetchall()
    category_dist = [{"path": r[0] or "general/default", "count": r[1]} for r in cat_rows]

    # 热度分布
    hot_buckets = {
        "high (>5 hits)": c.execute("SELECT COUNT(*) FROM capsules WHERE hotness_score > 5").fetchone()[0],
        "medium (1-5 hits)": c.execute("SELECT COUNT(*) FROM capsules WHERE hotness_score BETWEEN 1 AND 5").fetchone()[0],
        "low (0 hits)": c.execute("SELECT COUNT(*) FROM capsules WHERE hotness_score < 1").fetchone()[0],
    }

    # 同步状态
    synced = c.execute("SELECT COUNT(*) FROM capsules WHERE synced = 1").fetchone()[0]
    unsynced = total - synced

    # 待审阅队列
    pending = c.execute("SELECT COUNT(*) FROM memory_queue WHERE status = 'pending'").fetchone()[0]

    # 向量索引
    from core.vector import get_vector_stats
    vstats = get_vector_stats()

    # WAL 统计
    from core.wal import get_wal_stats
    wal = get_wal_stats()

    # Insight 数量
    insights = c.execute("SELECT COUNT(*) FROM insights").fetchone()[0]

    # 最近7天新增
    import time
    week_ago = time.time() - 7 * 86400
    week_new = c.execute("SELECT COUNT(*) FROM capsules WHERE created_at > ?", (week_ago,)).fetchone()[0]

    return JSONResponse({
        "capsules": {
            "total": total,
            "with_content": total_content,
            "synced": synced,
            "unsynced": unsynced,
            "last_week": week_new,
        },
        "categories": category_dist,
        "hotness": hot_buckets,
        "queue": {"pending": pending},
        "vectors": vstats,
        "insights": insights,
        "wal": wal,
    }, headers=add_cors_headers(request))


# ── 备份导出（需认证）────────────────────────────────────
@app.get("/admin/export")
def export_backup(request: Request, authorization: str = Header(None)):
    """
    导出所有胶囊为加密 JSON 文件（AES-256-GCM）。
    ?include_content=1 包含加密 content（默认只导出 memo）
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    include_content = request.query_params.get("include_content", "0") == "1"

    conn = _get_conn()
    c = conn.cursor()
    cols = "id,memo,tags,session_id,window_title,url,created_at,synced,source_type,category,category_path,updated_at"
    if include_content:
        cols += ",content,salt,nonce,encrypted_len,content_hash,key_source"
    rows = c.execute(f"SELECT {cols} FROM capsules ORDER BY created_at DESC").fetchall()
    conn.close()

    keys = cols.split(",")
    capsules = [dict(zip(keys, r)) for r in rows]

    # 添加向量统计
    from core.vector import get_vector_stats
    vstats = get_vector_stats()

    export_data = {
        "version": "1.0",
        "exported_at": time.time(),
        "capsule_count": len(capsules),
        "vector_stats": vstats,
        "capsules": capsules,
    }

    # 序列化为 JSON（不加密，因为内容字段已是加密的）
    import json
    json_bytes = json.dumps(export_data, ensure_ascii=False, indent=2).encode("utf-8")

    # 返回文件下载
    from fastapi.responses import Response
    import base64
    b64 = base64.b64encode(json_bytes).decode()
    return JSONResponse({
        "filename": f"amber-backup-{int(time.time())}.json",
        "size_bytes": len(json_bytes),
        "capsule_count": len(capsules),
        "data": b64,
        "note": "内容字段已是 AES-256-GCM 加密格式，需密钥解密",
    }, headers=add_cors_headers(request))


# ── MCP Server 端点（需认证）────────────────────────────────
@app.post("/mcp")
async def mcp_handler(request: Request, authorization: str = Header(None)):
    """
    MCP (Model Context Protocol) 接口。
    支持 tools/list、tools/call、resources/list、resources/read。
    用于让 Claude Code 或其他 MCP Client 访问 amber-hunter 记忆工具。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": {"code": -32700, "message": "Invalid JSON"}}, status_code=400)

    from core.mcp import MCPServer
    server = MCPServer(token=raw_token)
    result = server.handle_request(body)
    return JSONResponse(result, headers=add_cors_headers(request))


# ── Knowledge Compiler 端点（需认证）v1.2.38 ──────────────────────────────

@app.get("/concepts")
def list_concepts(
    request: Request,
    authorization: str = Header(None),
    limit: int = 50,
    offset: int = 0,
):
    """
    列出所有已有的 concept pages（轻量列表）。
    GET /concepts?limit=50&offset=0
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    conn = _get_conn()
    c = conn.cursor()

    total = c.execute("""
        SELECT COUNT(*) FROM insights
        WHERE wiki_content IS NOT NULL AND wiki_content != ''
    """).fetchone()[0]

    rows = c.execute("""
        SELECT path, concept_slug, summary, capsule_ids, hotness_score, updated_at
        FROM insights
        WHERE wiki_content IS NOT NULL AND wiki_content != ''
        ORDER BY hotness_score DESC
        LIMIT ? OFFSET ?
    """, (limit, offset)).fetchall()

    concepts = []
    for row in rows:
        capsule_ids = json.loads(row[3]) if row[3] else []
        concepts.append({
            "path": row[0],
            "concept_slug": row[1] or "",
            "summary": row[2] or "",
            "capsule_count": len(capsule_ids),
            "hotness_score": row[4],
            "updated_at": row[5],
        })

    return JSONResponse({
        "concepts": concepts,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(concepts) < total,
    }, headers=add_cors_headers(request))


@app.get("/concepts/{path:path}")
def get_concept(request: Request, path: str, authorization: str = Header(None)):
    """
    获取指定 path 的完整 concept page（wiki markdown）。
    GET /concepts/dev/python
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    conn = _get_conn()
    c = conn.cursor()

    row = c.execute("""
        SELECT path, concept_slug, wiki_content, capsule_ids, hotness_score, updated_at
        FROM insights
        WHERE path=? AND wiki_content IS NOT NULL AND wiki_content != ''
        LIMIT 1
    """, (path,)).fetchone()

    if not row:
        raise HTTPException(404, f"No concept page for path: {path}")

    capsule_ids = json.loads(row[3]) if row[3] else []

    return JSONResponse({
        "path": row[0],
        "concept_slug": row[1] or "",
        "wiki_content": row[2],
        "capsule_ids": capsule_ids,
        "hotness_score": row[4],
        "updated_at": row[5],
    }, headers=add_cors_headers(request))


@app.post("/admin/compile")
def admin_compile(request: Request, authorization: str = Header(None), path: str = ""):
    """
    手动触发 concept page 编译。
    path='' 时编译所有覆盖缺口路径，否则只编译指定 path。
    POST /admin/compile?path=dev/python
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    conn = _get_conn()
    c = conn.cursor()

    result = {"compiled": 0, "skipped": 0, "paths": []}

    if path:
        # 指定 path 编译
        rows = c.execute(
            "SELECT id, memo, hotness_score FROM capsules WHERE category_path=? ORDER BY hotness_score DESC LIMIT 20",
            (path,),
        ).fetchall()
        if len(rows) < 3:
            return JSONResponse({"compiled": 0, "reason": "need >=3 capsules"}, headers=add_cors_headers(request))

        ids = [r[0] for r in rows]
        memos = [r[1] for r in rows if r[1]]
        avg_hot = sum(r[2] or 0 for r in rows) / len(rows)
        insight = _generate_wiki_insight(path, ids, memos, avg_hot)
        if insight:
            c.execute("""
                INSERT OR REPLACE INTO insights
                  (id, capsule_ids, summary, path, concept_slug, wiki_content, hotness_score, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                insight["id"], insight["capsule_ids"], insight["summary"],
                insight["path"], insight["concept_slug"], insight["wiki_content"],
                insight["hotness_score"], insight["created_at"], insight["updated_at"],
            ))
            conn.commit()
            result["compiled"] = 1
            result["paths"].append(path)
        else:
            result["skipped"] = 1
    else:
        # 批量编译覆盖缺口
        from core.wiki_compiler import detect_coverage_gaps, _run_batch_compile
        stats = _run_batch_compile(conn)
        result = {"compiled": stats["compiled"], "skipped": stats["skipped"], "paths": stats["paths"]}

    return JSONResponse(result, headers=add_cors_headers(request))


@app.get("/admin/compile/status")
def compile_status(request: Request, authorization: str = Header(None)):
    """
    返回编译状态 + 覆盖缺口 + daemon 健康状态。
    GET /admin/compile/status
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    conn = _get_conn()
    c = conn.cursor()

    # 已编译的 path
    compiled_rows = c.execute("""
        SELECT path, updated_at FROM insights
        WHERE wiki_content IS NOT NULL AND wiki_content != ''
        ORDER BY updated_at DESC
    """).fetchall()

    # 覆盖缺口
    from core.wiki_compiler import detect_coverage_gaps, get_compile_daemon_status
    gaps = detect_coverage_gaps(conn)
    daemon = get_compile_daemon_status()

    last_at = compiled_rows[0][1] if compiled_rows else None

    return JSONResponse({
        "last_compile_at": last_at,
        "compiled_paths": [r[0] for r in compiled_rows],
        "compiled_count": len(compiled_rows),
        "coverage_gaps": gaps,
        "gaps_count": len(gaps),
        "daemon": daemon,
    }, headers=add_cors_headers(request))


# ── Insight 缓存生成（需认证）v1.2.38: 改用 wiki 编译器 ─────────────────────
@app.post("/admin/generate-insights")
def generate_insights(request: Request, authorization: str = Header(None), path: str = ""):
    """
    手动触发 insight 压缩任务（使用 wiki 编译器 v1.2.38）。
    path='' 时压缩所有路径（至少3个胶囊），否则只压缩指定路径。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    conn = _get_conn()
    c = conn.cursor()

    stats = {"total": 0, "by_path": {}}

    if path:
        rows = c.execute(
            "SELECT id, memo, hotness_score FROM capsules WHERE category_path=? ORDER BY hotness_score DESC LIMIT 20",
            (path,)
        ).fetchall()
        if len(rows) >= 3:
            ids = [r[0] for r in rows]
            memos = [r[1] for r in rows if r[1]]
            avg_hot = sum(r[2] or 0 for r in rows) / len(rows)
            insight = _generate_wiki_insight(path, ids, memos, avg_hot)
            if insight:
                c.execute(
                    "INSERT OR REPLACE INTO insights (id, capsule_ids, summary, path, concept_slug, wiki_content, hotness_score, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (insight["id"], insight["capsule_ids"], insight["summary"], insight["path"],
                     insight["concept_slug"], insight["wiki_content"],
                     insight["hotness_score"], insight["created_at"], insight["updated_at"])
                )
                conn.commit()
                stats["total"] = 1
                stats["by_path"][path] = 1
    else:
        paths = c.execute(
            "SELECT category_path FROM capsules WHERE category_path!='general/default' GROUP BY category_path HAVING COUNT(*)>=3"
        ).fetchall()
        for (p,) in paths:
            rows = c.execute(
                "SELECT id, memo, hotness_score FROM capsules WHERE category_path=? ORDER BY hotness_score DESC LIMIT 20",
                (p,)
            ).fetchall()
            if len(rows) < 3:
                continue
            # 跳过已有近期 insight（7天内更新过）
            recent = c.execute(
                "SELECT 1 FROM insights WHERE path=? AND updated_at>?",
                (p, time.time() - 86400 * 7)
            ).fetchone()
            if recent:
                continue
            ids = [r[0] for r in rows]
            memos = [r[1] for r in rows if r[1]]
            avg_hot = sum(r[2] or 0 for r in rows) / len(rows)
            insight = _generate_wiki_insight(p, ids, memos, avg_hot)
            if insight:
                c.execute(
                    "INSERT OR REPLACE INTO insights (id, capsule_ids, summary, path, concept_slug, wiki_content, hotness_score, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (insight["id"], insight["capsule_ids"], insight["summary"], insight["path"],
                     insight["concept_slug"], insight["wiki_content"],
                     insight["hotness_score"], insight["created_at"], insight["updated_at"])
                )
                stats["total"] += 1
                stats["by_path"][p] = stats["by_path"].get(p, 0) + 1

        if stats["total"] > 0:
            conn.commit()

    return JSONResponse({
        "insights_generated": stats["total"],
        "by_path": stats["by_path"],
    }, headers=add_cors_headers(request))

# ── P2-2: Pattern Detection 端点 ────────────────────────────
@app.get("/patterns")
def get_patterns(request: Request, authorization: str = Header(None)):
    """
    返回检测到的标签/分类校正模式。
    基于 correction_log 表分析重复校正规律。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    from core.correction import analyze_corrections
    return JSONResponse(analyze_corrections(), headers=add_cors_headers(request))

# ── A2: DID 多设备身份 v1.2.22 ─────────────────────────────

@app.post("/did/setup")
def did_setup(request: Request, authorization: str = Header(None)):
    """
    在本设备设置 DID 身份（生成助记词，派生设备密钥）。
    助记词仅此一次显示，需用户备份。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    from core.crypto import generate_mnemonic, mnemonic_to_master, derive_identity_keypair, derive_device_key, pubkey_to_did, privkey_to_hex, pubkey_to_hex

    # 生成助记词
    mnemonic = generate_mnemonic(256)
    # 派生密钥
    master = mnemonic_to_master(mnemonic, "amber@local")
    identity_priv, identity_pub = derive_identity_keypair(master)
    device_uuid = secrets.token_hex(8)
    device_priv, device_pub = derive_device_key(master, device_uuid)
    did_str = pubkey_to_did(identity_pub)
    device_priv_hex = privkey_to_hex(device_priv)
    device_pub_hex = pubkey_to_hex(device_pub)

    # 保存到本地配置（设备私钥 hex 明文存储，用户需知情）
    import json
    did_config = {
        "did": did_str,
        "device_id": device_uuid,
        "device_priv": device_priv_hex,  # D2: 用于胶囊密钥派生
        "device_pub": device_pub_hex,
        "mnemonic": mnemonic,  # 仅此一次
    }
    did_path = HOME / ".amber-hunter" / "did.json"
    did_path.parent.mkdir(parents=True, exist_ok=True)
    did_path.write_text(json.dumps(did_config))

    return JSONResponse({
        "did": did_str,
        "mnemonic": mnemonic,
        "device_id": device_uuid,
    }, headers=add_cors_headers(request))


@app.get("/did/status")
def did_status(request: Request, authorization: str = Header(None)):
    """查询本设备 DID 身份状态"""
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    import json
    did_path = HOME / ".amber-hunter" / "did.json"
    if not did_path.exists():
        return JSONResponse({"has_did": False})
    cfg = json.loads(did_path.read_text())
    return JSONResponse({
        "has_did": True,
        "did": cfg.get("did"),
        "device_id": cfg.get("device_id"),
    })


@app.post("/did/register-device")
def did_register_device(request: Request, authorization: str = Header(None)):
    """
    将本设备注册到云端 DID（需要云端账户已设置 DID）。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    import json
    did_path = HOME / ".amber-hunter" / "did.json"
    if not did_path.exists():
        return JSONResponse({"error": "请先调用 /did/setup 设置 DID 身份"}, status_code=400)

    cfg = json.loads(did_path.read_text())
    huper_url = get_huper_url()
    api_token = get_api_token()

    # 调用云端 /api/did/devices/register 注册设备公钥
    import httpx
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.post(
                f"{huper_url}/did/devices/register",
                json={
                    "device_id": cfg["device_id"],
                    "device_pub": cfg["device_pub"],
                    "did": cfg["did"],
                },
                headers={"Authorization": f"Bearer {api_token}"}
            )
        if resp.status_code == 200:
            return JSONResponse({"ok": True, "device_id": cfg["device_id"]})
        else:
            return JSONResponse({"error": f"云端注册失败: {resp.status_code}"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"网络错误: {e}"}, status_code=500)


@app.post("/did/auth/challenge")
def did_auth_challenge(request: Request, authorization: str = Header(None)):
    """
    获取 DID 认证挑战（调用云端 /api/did/auth/challenge）。
    返回 challenge_id, challenge, expires_at。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    import json
    did_path = HOME / ".amber-hunter" / "did.json"
    if not did_path.exists():
        return JSONResponse({"error": "请先调用 /did/setup 设置 DID 身份"}, status_code=400)

    cfg = json.loads(did_path.read_text())
    huper_url = get_huper_url()
    api_token = get_api_token()

    import httpx
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.post(
                f"{huper_url}/api/did/auth/challenge",
                json={"did": cfg["did"]},
                headers={"Authorization": f"Bearer {api_token}"}
            )
        if resp.status_code == 200:
            return JSONResponse(resp.json())
        else:
            return JSONResponse({"error": f"获取挑战失败: {resp.status_code}", "detail": resp.text}, status_code=resp.status_code)
    except Exception as e:
        return JSONResponse({"error": f"网络错误: {e}"}, status_code=500)


@app.post("/did/auth/sign-challenge")
def did_auth_sign_challenge(
    challenge_id: str,
    challenge: str,
    request: Request = None,
    authorization: str = Header(None),
):
    """
    用本设备 Ed25519 私钥签名 challenge，提交云端验证，返回 DID token。
    云端返回 { token, expires_at }，本服务保存到 did.json。
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)

    import json
    did_path = HOME / ".amber-hunter" / "did.json"
    if not did_path.exists():
        return JSONResponse({"error": "请先调用 /did/setup 设置 DID 身份"}, status_code=400)

    cfg = json.loads(did_path.read_text())
    device_priv_hex = cfg.get("device_priv")
    if not device_priv_hex:
        return JSONResponse({"error": "设备私钥不存在，请重新运行 /did/setup"}, status_code=400)

    # Ed25519 签名
    from cryptography.hazmat.primitives.asymmetric import ed25519
    priv_bytes = bytes.fromhex(device_priv_hex)
    priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(priv_bytes)
    signature = priv_key.sign(challenge.encode()).hex()

    huper_url = get_huper_url()
    api_token = get_api_token()

    import httpx
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.post(
                f"{huper_url}/api/did/auth/verify",
                json={
                    "challenge_id": challenge_id,
                    "challenge": challenge,
                    "signature": signature,
                    "device_id": cfg["device_id"],
                },
                headers={"Authorization": f"Bearer {api_token}"}
            )
        if resp.status_code == 200:
            result = resp.json()
            did_token = result.get("token")
            if did_token:
                # 保存 DID token 到 did.json
                cfg["did_token"] = did_token
                cfg["did_token_expires_at"] = result.get("expires_at")
                did_path.write_text(json.dumps(cfg))
            return JSONResponse(result)
        else:
            return JSONResponse({"error": f"验证失败: {resp.status_code}", "detail": resp.text}, status_code=resp.status_code)
    except Exception as e:
        return JSONResponse({"error": f"网络错误: {e}"}, status_code=500)


# ── P0-2: WAL 热存储端点（无需认证）──────────────────────

@app.get("/wal/status")
def wal_status():
    """返回 WAL 统计信息（总数 + 各类型计数）"""
    return JSONResponse(get_wal_stats())


@app.get("/wal/entries")
def wal_entries(session_id: str = ""):
    """
    读取当前（或指定）session 的 WAL 条目。
    ?session_id=xxx 可指定，不提供则用当前 session
    """
    key = session_id or get_current_session_key()
    if not key:
        return JSONResponse({"entries": []})
    return JSONResponse({"entries": read_wal_entries(key)})


@app.post("/wal/gc")
def wal_gc_endpoint(age_hours: float = 24.0):
    """
    WAL 垃圾回收：删除已处理的条目（默认 24 小时前的）。
    POST /wal/gc 或 POST /wal/gc?age_hours=48
    """
    result = wal_gc(age_hours=age_hours)
    return JSONResponse(result)


# ── P1-1: User Profile 端点 ─────────────────────────────────

@app.get("/profile")
def get_full_profile():
    """返回完整四段 profile（无需认证）"""
    from core.profile import get_full_profile
    return JSONResponse(get_full_profile())


@app.get("/profile/{section}")
def get_profile_section(section: str):
    """读取单个 profile section"""
    from core.db import get_profile
    valid = {"WHO_I_AM", "STACK", "GOALS", "PREFERENCES"}
    section_upper = section.upper()
    if section_upper not in valid:
        raise HTTPException(400, f"Invalid section. Must be one of: {valid}")
    p = get_profile(section_upper)
    if not p:
        raise HTTPException(404, f"Profile section '{section}' not found")
    return JSONResponse(p)


@app.put("/profile/{section}")
def update_profile_section(section: str, body: dict, authorization: str = Header(None)):
    """手动更新 profile section（需认证）"""
    verify_token(authorization)
    from core.db import update_profile, insert_profile, get_profile
    valid = {"WHO_I_AM", "STACK", "GOALS", "PREFERENCES"}
    section_upper = section.upper()
    if section_upper not in valid:
        raise HTTPException(400, f"Invalid section. Must be one of: {valid}")
    content = body.get("content", "")
    existing = get_profile(section_upper)
    if existing:
        update_profile(section_upper, content, source="manual")
    else:
        insert_profile(section_upper, content, source="manual")
    return JSONResponse({"status": "ok", "section": section_upper})


@app.post("/profile/build")
def build_profile_endpoint(authorization: str = Header(None)):
    """从当前 session 的 WAL 条目构建 profile（需认证）"""
    verify_token(authorization)
    from core.profile import build_or_update_profile
    sk = get_current_session_key()
    if not sk:
        return JSONResponse({"error": "No active session"}, status_code=400)
    result = build_or_update_profile(sk)
    if not result:
        return JSONResponse({"error": "No signals found in session"}, status_code=404)
    return JSONResponse({"status": "ok", "profile": result})


# ── P2-1: Mem0 Auto-Extraction 端点 ─────────────────────────────────

@app.post("/extract/auto")
def extract_auto(request: Request, session_key: str = ""):
    """
    自动从当前 session 抽取 facts/preferences/decisions（供 proactive hook 调用）。
    高置信(>=0.9) 直接入库，中置信(>=0.5) 进审核队列。
    """
    from core.extractor import auto_extract
    sk = session_key if session_key else None
    result = auto_extract(sk)
    return JSONResponse(result)


@app.get("/extract/status")
def extract_status():
    """返回上次抽取统计"""
    from core.db import get_config
    last = get_config("auto_extract_last")
    count = get_config("auto_extract_count")
    return JSONResponse({
        "last_run": float(last) if last else None,
        "total_extracted": int(count) if count else 0,
    })


# ── G1: Self-Correction 端点 ─────────────────────────────────

@app.get("/corrections/stats")
def corrections_stats(field: str = ""):
    """
    返回校正统计数据。
    ?field=tag 可只看标签校正
    """
    from core.correction import analyze_corrections
    return JSONResponse(analyze_corrections(field=field))


@app.get("/corrections/suggestions")
def corrections_suggestions(threshold: int = 3):
    """返回自动替换建议（某个 original 被纠正 >= threshold 次）"""
    from core.db import get_correction_suggestions
    return JSONResponse({"suggestions": get_correction_suggestions(threshold=threshold)})


@app.post("/corrections/apply")
def apply_correction_rule(body: dict, authorization: str = Header(None)):
    """采纳一条校正规则：original → corrected 自动替换"""
    verify_token(authorization)
    original = (body.get("original") or "").strip().lower()
    corrected = (body.get("corrected") or "").strip().lower()
    field = body.get("field", "tag")
    if not original or not corrected:
        return JSONResponse({"error": "original and corrected required"}, status_code=400)
    if field == "tag":
        from core.correction import apply_tag_rule
        apply_tag_rule(original, corrected)
    return JSONResponse({"status": "ok", "rule": f"{original} → {corrected}"})


@app.post("/admin/corrections/gc")
def corrections_gc(request: Request, authorization: str = Header(None),
                   age_days: float = 30.0):
    """
    清理 correction_log 中 age_days 天前的旧条目。
    POST /admin/corrections/gc?age_days=30
    """
    raw_token = _extract_bearer_token(request, authorization)
    verify_token(raw_token)
    from core.db import cleanup_correction_log
    result = cleanup_correction_log(age_days=age_days)
    return JSONResponse(result, headers=add_cors_headers(request))


# ── 服务状态（无需认证）────────────────────────────────
@app.get("/status")
def get_status(request: Request):
    session_key = get_current_session_key()
    master_pw = get_master_password()
    api_token = get_api_token()
    h = add_cors_headers(request)

    # v1.2.3: DB 统计 + 模型状态 + 队列信息
    db_stats = {"capsule_count": 0, "queue_pending": 0, "last_sync": None}
    try:
        db_path = HOME / ".amber-hunter" / "hunter.db"
        if db_path.exists():
            _conn = sqlite3.connect(str(db_path))
            _c = _conn.cursor()
            row = _c.execute("SELECT COUNT(*) FROM capsules").fetchone()
            db_stats["capsule_count"] = row[0] if row else 0
            row2 = _c.execute(
                "SELECT COUNT(*) FROM memory_queue WHERE status='pending'"
            ).fetchone()
            db_stats["queue_pending"] = row2[0] if row2 else 0
            _conn.close()
    except Exception:
        pass

    # P3-11: last_sync 改用独立 config 记录（不受 created_at 影响）
    last_sync_ts = get_config("last_sync_at")
    db_stats["last_sync"] = float(last_sync_ts) if last_sync_ts else None
    # P1-7: 同步错误持久化
    sync_last_err = get_config("sync_last_error")
    sync_last_error = None
    if sync_last_err:
        try:
            sync_last_error = json.loads(sync_last_err)
        except Exception:
            sync_last_error = sync_last_err

    return JSONResponse({
        "running":            True,
        "version":            "1.2.41",
        "platform":           get_os(),
        "headless":           is_headless(),
        "session_key":        session_key,
        "has_master_password": bool(master_pw),
        "has_api_token":      bool(api_token),
        "workspace":          str(HOME / ".openclaw" / "workspace"),
        "huper_url":          get_huper_url(),
        "semantic_model_loaded": _EMBED_MODEL is not None,
        "semantic_model_state": (
            "loading" if _MODEL_LOADING
            else "ready" if _EMBED_MODEL is not None
            else "error" if _MODEL_LOAD_ERROR
            else "unavailable"
        ),
        "semantic_model_error": _MODEL_LOAD_ERROR,
        "capsule_count":      db_stats["capsule_count"],
        "queue_pending":      db_stats["queue_pending"],
        "last_sync":          db_stats["last_sync"],
        "sync_last_error":   sync_last_error,
        "vector_index":      get_vector_stats(),
    }, headers=h)

@app.get("/")
def root(request: Request):
    h = add_cors_headers(request)
    return JSONResponse({"service": "amber-hunter", "version": "1.2.41", "docs": "/docs"}, headers=h)

# ── 启动 ───────────────────────────────────────────────
def main():
    init_db()
    print("🌙 Amber-Hunter v1.2.31 启动")
    print(f"   Session目录: {HOME / '.openclaw' / 'agents'}")
    print(f"   Workspace:   {HOME / '.openclaw' / 'workspace'}")
    print(f"   数据库:      {HOME / '.amber-hunter' / 'hunter.db'}")
    print(f"   API:        http://localhost:18998/")
    print(f"   CORS:       https://huper.org + localhost")
    print(f"   认证:       本地 API token")
    # P3-13: 启动定时同步守护线程（间隔可配置，默认 30 分钟）
    def _periodic_sync_loop():
        while True:
            interval_minutes = int(get_config("sync_interval_minutes") or 30)
            interval_seconds = interval_minutes * 60
            time.sleep(interval_seconds)   # 先休眠再执行，避免启动时立即同步
            _spawn_sync_if_enabled()
    t = threading.Thread(target=_periodic_sync_loop, daemon=True, name="amber-periodic-sync")
    t.start()

    # ── 自动训练触发器 ───────────────────────────────────
    _auto_train_last_count = count_capsules()
    set_config("auto_train_last_count", str(_auto_train_last_count))

    def _auto_train_if_needed():
        """检查是否需要触发训练：每新增 N 个胶囊触发一次增量训练"""
        try:
            from core.trainer import is_trained
            threshold = int(get_config("auto_train_threshold") or "100")
            interval_hours = int(get_config("auto_train_interval_hours") or "6")
            last_count_str = get_config("auto_train_last_count") or "0"
            last_count = int(last_count_str)
            current_count = count_capsules()
            new_capsules = current_count - last_count

            if new_capsules >= threshold:
                # 达到阈值，触发训练
                set_config("auto_train_last_count", str(current_count))
                _spawn_train_if_enabled()
            elif not is_trained() and current_count >= 50:
                # cold-start：50 个胶囊且无模型时触发首次训练
                set_config("auto_train_last_count", str(current_count))
                _spawn_train_if_enabled()
        except Exception:
            pass

    def _spawn_train_if_enabled():
        """后台启动增量训练（已在 daemon 线程中）"""
        try:
            from core.trainer import is_trained, fine_tune, AmberTrainer, get_trainer
            if not is_trained():
                return  # 无模型时不自动训练，等用户手动触发
            print("[auto-train] Triggering incremental training...")
            result = fine_tune(iterations=100, use_gpt2_pretrain=True, incremental=True)
            print(f"[auto-train] Done: {result.get('status')}")
            AmberTrainer._instance = None  # 重置单例
            get_trainer()
        except Exception as e:
            print(f"[auto-train] Failed: {e}")

    def _periodic_train_loop():
        """定时训练守护线程（默认每 6 小时一次）"""
        while True:
            interval_hours = int(get_config("auto_train_interval_hours") or "6")
            time.sleep(interval_hours * 3600)
            try:
                from core.trainer import is_trained
                if is_trained():
                    print("[auto-train] Periodic incremental training triggered.")
                    _spawn_train_if_enabled()
            except Exception:
                pass

    # 启动定时训练线程
    t2 = threading.Thread(target=_periodic_train_loop, daemon=True, name="amber-periodic-train")
    t2.start()

    # 启动时若未训练且胶囊数>=50，触发首次训练
    try:
        from core.trainer import is_trained
        if not is_trained() and count_capsules() >= 50:
            print(f"[auto-train] Cold-start: {count_capsules()} capsules, scheduling first training...")
            def _cold_start_train():
                time.sleep(10)  # 等待服务完全启动
                _spawn_train_if_enabled()
            t3 = threading.Thread(target=_cold_start_train, daemon=True, name="amber-cold-start-train")
            t3.start()
    except Exception:
        pass

    # 后台预加载语义模型
    _preload_embed_model()

    # v1.2.38: 启动知识编译器 daemon
    try:
        from core.wiki_compiler import start_compile_daemon
        start_compile_daemon(interval_hours=6.0, capsule_threshold=100)
        print("[wiki-compiler] daemon started (interval=6h, threshold=100 capsules)")
        # cold-start: 立即编译一次（等待 10 秒让服务就绪）
        def _cold_start_compile():
            time.sleep(10)
            try:
                from core.wiki_compiler import _run_batch_compile
                import core.db as _db
                conn = _db._get_conn()
                stats = _run_batch_compile(conn)
                conn.close()
                if stats["compiled"] > 0:
                    print(f"[wiki-compiler] cold-start: compiled {stats['compiled']} concept pages")
            except Exception as e:
                print(f"[wiki-compiler] cold-start skipped: {e}")
        t4 = threading.Thread(target=_cold_start_compile, daemon=True, name="amber-cold-start-compile")
        t4.start()
    except Exception as e:
        print(f"[wiki-compiler] daemon start failed: {e}")

    uvicorn.run(app, host="127.0.0.1", port=18998, log_level="warning")

if __name__ == "__main__":
    main()
