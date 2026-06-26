#!/usr/bin/env python3
"""
Session Search — FTS5 full-text search over OpenClaw session histories.
Usage: python search-sessions.py "query" [--limit 5] [--llm] [--all-agents]

Search is fully offline. LLM summarization is opt-in (use --llm to enable).
"""
import sqlite3
import os
import sys
import re
import argparse
import json
import urllib.request
import urllib.error

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.environ.get("SESSION_SEARCH_DB_DIR", os.path.join(SKILL_DIR, "db"))
DB_PATH = os.path.join(DB_DIR, "sessions.db")

def get_api_key():
    """Find MiniMax/OpenAI API key from environment or OpenClaw config."""
    # Try OpenClaw config
    try:
        cfg_path = os.path.expanduser("~/.openclaw/openclaw.json")
        with open(cfg_path) as f:
            config = json.load(f)
        # Check minimax provider in config
        providers = config.get("providers", {})
        for p_name, p_cfg in providers.items():
            for key_name in ("apiKey", "api_key"):
                if key_name in p_cfg:
                    return p_cfg[key_name], p_name
    except Exception:
        pass

    # Env vars
    for var in ("MINIMAX_API_KEY", "OPENAI_API_KEY"):
        key = os.environ.get(var)
        if key:
            return key, var

    return None, None

def fts_search(query, limit=5, all_agents=False):
    """Run FTS5 search, fall back to LIKE on FTS5 errors."""
    if not os.path.exists(DB_PATH):
        print("❌ Database not found. Run index-sessions.py first.", file=sys.stderr)
        return []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Process query for FTS5: handle hyphenated words (memory-core → memory* OR core*)
    processed_words = []
    for word in query.split():
        if re.match(r'^[\w-]+$', word) and '-' in word:
            parts = word.split('-')
            processed_words.append(' OR '.join(f'{p}*' for p in parts))
        elif re.match(r'^[\w*]+$', word):
            processed_words.append(f'"{word}"' if '*' not in word else word)
        else:
            processed_words.append(f'"{word}"')
    fts_query = ' '.join(processed_words)

    try:
        c.execute(f"""
            SELECT session_id, message_id, role, text, timestamp,
                   bm25(sessions_fts) as rank
            FROM sessions_fts
            WHERE sessions_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (fts_query, limit))
        rows = c.fetchall()
    except sqlite3.OperationalError:
        like_q = f"%{query}%"
        c.execute("""
            SELECT session_id, message_id, role, text, timestamp, 0 as rank
            FROM sessions_fts
            WHERE text LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (like_q, limit))
        rows = c.fetchall()

    conn.close()
    return [dict(r) for r in rows]

def format_results(results):
    """Format search results for display."""
    if not results:
        return "No matching sessions found."

    lines = []
    for i, r in enumerate(results, 1):
        ts = str(r.get("timestamp", ""))[:10] if r.get("timestamp") else "?"
        role_label = "👤 user" if r.get("role") == "user" else "🤖 assistant"
        text = r.get("text", "")[:400]
        if len(r.get("text", "")) > 400:
            text += "..."
        lines.append(f"{i}. [{ts}] {role_label}\n   {text}\n")
    return "\n".join(lines)

def summarize(query, results_text):
    """Summarize search results using MiniMax LLM."""
    api_key, provider = get_api_key()
    if not api_key:
        return None, "⚠️  No API key found. Skipping summary."

    # MiniMax compatible OpenAI endpoint
    BASE_URL = "https://api.minimax.chat/v1"
    MODEL = "MiniMax-M2.7"

    prompt = f"""User asked: "{query}"

Relevant conversation excerpts:
---
{results_text}
---

Briefly summarize whether these excerpts answer the user's question. Answer in Chinese, 1-2 sentences."""

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.3,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return content, None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")[:200]
        return None, f"API error {e.code}: {body}"
    except Exception as e:
        return None, f"Request failed: {e}"

def main():
    parser = argparse.ArgumentParser(description="Search session histories")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Result count (default: 5)")
    parser.add_argument("--llm", action="store_true", help="Enable LLM summary (requires API key in ~/.openclaw/openclaw.json)")
    args = parser.parse_args()

    results = fts_search(args.query, limit=args.limit)
    if not results:
        print("🔍 No matching sessions found.")
        sys.exit(0)

    formatted = format_results(results)
    print(f"🔍 {len(results)} results:\n\n{formatted}")

    if args.llm:
        summary, err = summarize(args.query, formatted)
        if err:
            print(f"\n{err}")
        elif summary:
            print(f"\n💡 {summary}")

if __name__ == "__main__":
    main()
