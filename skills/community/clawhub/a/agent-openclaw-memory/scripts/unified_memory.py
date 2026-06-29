#!/usr/bin/env python3
"""Unified memory system — auto search and inject for OpenClaw agents"""

import json, sys, os, re, hashlib
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shared_config import (
    VAULT_DIR, LLM_BASE_URL, LLM_API_KEY, LLM_MODEL,
    QDRANT_HOST, QDRANT_PORT, KB_COLLECTION,
)
from qdrant_utils import search as _qdrant_search, scroll_all as _qdrant_scroll, is_available as _qdrant_available

VAULT_SUBDIRS = {
    "diary": "01-日记",
    "knowledge": "06-收件箱",
    "lessons": "06-收件箱",
    "projects": "06-收件箱",
}

PROFILE_FILE = VAULT_DIR / "00-索引" / "project_profile.json"
INJECTION_CHAR_BUDGET = 6000

INTENT_CATEGORIES = {
    "reflective": ["为什么", "原因", "分析", "think", "why", "看法", "评价", "判断", "反思", "总结"],
    "procedural": ["怎么", "如何", "步骤", "方法", "流程", "how to", "教程", "配置"],
    "factual": ["什么", "谁", "哪", "多", "what", "when", "where", "多少", "地址", "API", "命令"],
    "recency": ["最近", "刚才", "昨天", "上次", "之前", "recent", "最新", "最后"],
}

INTENT_STRATEGIES = {
    "factual": {"method": "keywords_first", "fallback": "vector"},
    "procedural": {"method": "path_pattern", "fallback": "vector"},
    "reflective": {"method": "vector", "fallback": None},
    "recency": {"method": "recency_first", "fallback": "vector"},
    "general": {"method": "hybrid", "fallback": None},
}

_mem0 = None
MEM0_CONFIG = None
_MEM0_AVAILABLE = None

def _init_mem0_config():
    global MEM0_CONFIG
    if MEM0_CONFIG is not None:
        return
    from shared_config import LMSTUDIO_EMBED_URL, LMSTUDIO_KEY, EMBED_MODEL
    MEM0_CONFIG = {
        "llm": {"provider": "openai", "config": {
            "model": LLM_MODEL, "api_key": LLM_API_KEY,
            "openai_base_url": LLM_BASE_URL, "temperature": 0.1
        }},
        "embedder": {"provider": "openai", "config": {
            "model": EMBED_MODEL, "api_key": LMSTUDIO_KEY,
            "openai_base_url": LMSTUDIO_EMBED_URL.replace("/embeddings", ""), "embedding_dims": 768
        }},
        "vector_store": {"provider": "qdrant", "config": {
            "host": QDRANT_HOST, "port": QDRANT_PORT,
            "collection_name": KB_COLLECTION, "embedding_model_dims": 768
        }}
    }


def get_mem0():
    global _mem0, _MEM0_AVAILABLE
    if _MEM0_AVAILABLE is False:
        return None
    if _mem0 is None:
        _init_mem0_config()
        try:
            from mem0 import Memory
            _mem0 = Memory.from_config(MEM0_CONFIG)
            _MEM0_AVAILABLE = True
        except ImportError:
            _MEM0_AVAILABLE = False
            print("[WARN] mem0ai not installed. Mem0 search disabled. Install: pip install mem0ai", file=sys.stderr)
            return None
        except Exception as e:
            _MEM0_AVAILABLE = False
            print(f"[WARN] Mem0 init failed: {e}", file=sys.stderr)
            return None
    return _mem0


def classify_intent(query: str) -> str:
    q = query.lower().strip()
    for intent, keywords in INTENT_CATEGORIES.items():
        if any(kw in q for kw in keywords):
            return intent
    return "general"


def keyword_match(query: str, kb_results: list) -> list:
    q_words = set(w.lower() for w in query.split() if len(w) > 1)
    scored = []
    for r in kb_results:
        content = r.get("content", "").lower()
        words_in_content = set(w.lower() for w in content.split() if len(w) > 1)
        if q_words & words_in_content:
            overlap = len(q_words & words_in_content)
            scored.append((r, overlap / len(q_words) if q_words else 0))
    scored.sort(key=lambda x: -x[1])
    return [s[0] for s in scored if s[1] >= 0.3]


def search_knowledge_base(query, limit=3, include_old=False):
    try:
        m = get_mem0()
        embedding = m.embedding_model.embed(query)
        filter_dict = None
        if not include_old:
            filter_dict = {"must": [{"key": "is_latest", "match": {"value": True}}]}
        raw_results = _qdrant_search(embedding, limit=limit, filter_dict=filter_dict)
        return [{
            "content": r.get("payload", {}).get("text", r.get("payload", {}).get("narrative", "")),
            "source": r.get("payload", {}).get("source", ""),
            "title": r.get("payload", {}).get("title", ""),
            "score": r.get("score", 0),
        } for r in raw_results]
    except Exception as e:
        print(f"[KB search error] {e}", file=sys.stderr)
        return []


def search_mem0(query, user_id="main", limit=3):
    m = get_mem0()
    if m is None:
        return []
    try:
        results = m.search(query, filters={"user_id": user_id}, limit=limit)
        return results.get("results", [])
    except Exception as e:
        print(f"[Mem0 search error] {e}", file=sys.stderr)
        return []


def unified_search(query, user_id="main", limit=5):
    results = {"preferences": [], "knowledge": []}
    mem0_results = search_mem0(query, user_id, limit=limit)
    results["preferences"] = [{"memory": r["memory"], "score": r.get("score", 0)} for r in mem0_results]
    results["knowledge"] = search_knowledge_base(query, limit=limit)
    return results


def format_for_injection(results, max_tokens=500):
    lines = []
    token_count = 0
    if results["preferences"]:
        lines.append("## Known preferences")
        for r in results["preferences"]:
            line = f"- {r['memory']}"
            if token_count + len(line) // 4 > max_tokens: break
            lines.append(line)
            token_count += len(line) // 4
    if results["knowledge"]:
        lines.append("\n## Related knowledge")
        for r in results["knowledge"]:
            content = r["content"][:200]
            line = f"- [{r.get('source','')}] {content}"
            if token_count + len(line) // 4 > max_tokens: break
            lines.append(line)
            token_count += len(line) // 4
    return "\n".join(lines)


def need_memory(message):
    if len(message.strip()) < 8: return False
    skip = ["你好", "嗯", "好的", "谢谢", "ok", "OK", "hi", "hello", "NO_REPLY"]
    if message.strip() in skip: return False
    if '?' in message or '？' in message: return True
    keywords = ['怎么', '如何', '为什么', '帮我', '配置', '设置', '优化', '问题', '错误']
    return any(kw in message for kw in keywords) or len(message.strip()) > 20


def save_to_vault(text, subdir="auto"):
    from datetime import datetime
    if subdir == "auto":
        subdir = "knowledge"
    target_dir = VAULT_DIR / VAULT_SUBDIRS.get(subdir, "02-知识")
    target_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    if subdir == "diary":
        filepath = target_dir / f"{today}.md"
        if filepath.exists():
            existing = filepath.read_text(encoding='utf-8')
            if text[:50] not in existing:
                with open(filepath, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n{text}")
        else:
            filepath.write_text(f"# {today}\n\n{text}", encoding='utf-8')
    else:
        safe_name = text[:40]
        for ch in '/\\:*?"<>|\n\r\t': safe_name = safe_name.replace(ch, '-')
        safe_name = safe_name.strip('- ')[:40]
        filepath = target_dir / f"{today}-{safe_name}.md"
        if not filepath.exists():
            filepath.write_text(f"# {text.split(chr(10))[0][:50]}\n\n{text}", encoding='utf-8')
    return str(filepath)


def cmd_search(args):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--query", "-q", required=True)
    p.add_argument("--user", "-u", default="main")
    p.add_argument("--inject", action="store_true")
    p.add_argument("--limit", "-l", type=int, default=5)
    opts = p.parse_args(args)
    results = unified_search(opts.query, opts.user, opts.limit)
    if opts.inject:
        print(format_for_injection(results))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))


def cmd_add(args):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--text", "-t", required=True)
    p.add_argument("--user", "-u", default="main")
    opts = p.parse_args(args)
    if len(opts.text) < 30: return
    vault_path = save_to_vault(opts.text, "auto")
    print(f"Saved to vault: {vault_path}")


def cmd_auto_inject(args):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--message", "-m", required=True)
    p.add_argument("--user", "-u", default="main")
    opts = p.parse_args(args)
    if not need_memory(opts.message):
        print("")
        return
    results = unified_search(opts.message, opts.user, limit=3)
    print(format_for_injection(results, max_tokens=INJECTION_CHAR_BUDGET // 3))


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  unified_memory.py search -q 'query' [--inject]")
        print("  unified_memory.py auto-inject -m 'user message'")
        print("  unified_memory.py add -t 'memory content'")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "search": cmd_search(sys.argv[2:])
    elif cmd == "auto-inject": cmd_auto_inject(sys.argv[2:])
    elif cmd == "add": cmd_add(sys.argv[2:])
    else: print(f"Unknown command: {cmd}"); sys.exit(1)


if __name__ == "__main__":
    main()
