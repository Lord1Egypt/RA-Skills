#!/usr/bin/env python3
"""
Extract structured learnings from AI conversation exports using a local Ollama model or OpenAI-compatible API.

Usage:
    python3 extract.py --dir /path/to/exports [--limit 3] [--dry-run]
    python3 extract.py --file single-conversation.json
    python3 extract.py --dir /path/to/exports --since 2026-04-01 --model gpt-4o-mini

Flags:
    --dir DIR              Directory of conversation export JSON files
    --file FILE            Single conversation export file
    --limit N              Process only first N conversations
    --since YYYY-MM-DD     Skip conversations before this date
    --model MODEL          Model name (auto-selected: gpt-4o-mini for OpenAI, gemma4:26b for Ollama)
    --dry-run              Print output without writing to disk

Environment Variables:
    OLLAMA_BASE_URL        Ollama API endpoint (default: http://127.0.0.1:11434)
    OPENAI_API_KEY         OpenAI API key (enables OpenAI-compatible mode)
    OPENAI_BASE_URL        OpenAI-compatible API base URL (default: https://api.openai.com/v1)
    OPENCLAW_WORKSPACE     Path to agent workspace (default: ~/.openclaw/workspace)
"""

import sys
import os
import json
import argparse
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import Generator, Optional, Dict, List

# Import parsers bundled with this skill
parser_dir = Path(__file__).parent
sys.path.insert(0, str(parser_dir))
from parse_openai import parse as parse_openai
from parse_anthropic import parse as parse_anthropic


# Chunking constants for Ollama mode
CHUNK_SIZE = 40  # messages per chunk
MAX_MSG_CHARS = 1500  # max chars per message


def get_workspace() -> Path:
    """Get workspace path from env or fallback."""
    workspace = Path.home() / ".openclaw" / "workspace"
    if (env_ws := os.environ.get("OPENCLAW_WORKSPACE")):
        workspace = Path(env_ws)
    return workspace


def use_openai_api() -> bool:
    """Check if OpenAI API key is configured."""
    return bool(os.environ.get("OPENAI_API_KEY"))


def openai_extract(summary: str, model: str = "gpt-4o-mini") -> str:
    """Send prompt to OpenAI-compatible API and return extracted learnings."""
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not set", file=sys.stderr)
        return ""
    
    prompt = f"""You are an expert at identifying actionable insights from AI conversations.

Given a conversation summary, extract four categories of learnings:

1. **Lessons Learned** — What worked, what didn't, what was surprising
2. **Decisions Made** — Architectural, technical, or product choices discussed
3. **Patterns Noticed** — Recurring problems, approaches, or themes
4. **Dead Ends** — Things tried that failed or were abandoned

Keep responses focused and concise. Use bullet points. Skip categories if nothing notable applies.

---

{summary}

---

Return ONLY the structured markdown below. No preamble or explanation:

### Lessons Learned
[bullet points or "None"]

### Decisions Made
[bullet points or "None"]

### Patterns Noticed
[bullet points or "None"]

### Dead Ends
[bullet points or "None"]
"""

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }).encode()

    url = f"{base_url}/chat/completions"
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]["content"]
            return ""
    except Exception as e:
        print(f"Error querying OpenAI API: {e}", file=sys.stderr)
        return ""


def ollama_extract(summary: str, model: str = "gemma4:26b") -> str:
    """Send prompt to Ollama and return extracted learnings."""
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    
    prompt = f"""You are an expert at identifying actionable insights from AI conversations.

Given a conversation summary, extract four categories of learnings:

1. **Lessons Learned** — What worked, what didn't, what was surprising
2. **Decisions Made** — Architectural, technical, or product choices discussed
3. **Patterns Noticed** — Recurring problems, approaches, or themes
4. **Dead Ends** — Things tried that failed or were abandoned

Keep responses focused and concise. Use bullet points. Skip categories if nothing notable applies.

---

{summary}

---

Return ONLY the structured markdown below. No preamble or explanation:

### Lessons Learned
[bullet points or "None"]

### Decisions Made
[bullet points or "None"]

### Patterns Noticed
[bullet points or "None"]

### Dead Ends
[bullet points or "None"]
"""

    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False
    }).encode()

    url = f"{base_url}/api/generate"
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            return result.get("response", "")
    except Exception as e:
        print(f"Error querying Ollama: {e}", file=sys.stderr)
        return ""


def condense_conversation(chat: Dict) -> str:
    """Condense conversation to key excerpts for context (OpenAI mode)."""
    title = chat.get("title", "Untitled")
    date = chat.get("date", "")
    messages = chat.get("messages", [])

    # Build a summary with key messages only (skip long content)
    lines = [f"Title: {title}", f"Date: {date}", ""]

    for msg in messages:
        role = msg.get("role", "unknown").upper()
        content = msg.get("content", "")[:200]  # Truncate long messages
        timestamp = msg.get("timestamp", "")[:10]  # Date only
        lines.append(f"[{timestamp}] {role}: {content}")

    return "\n".join(lines)


def condense_chunk(title: str, date: str, messages: List[Dict], chunk_num: int, total_chunks: int) -> str:
    """Build a prompt string for a chunk of messages (Ollama mode)."""
    lines = [f"Title: {title} (part {chunk_num}/{total_chunks})", f"Date: {date}", ""]
    for msg in messages:
        role = msg.get("role", "unknown").upper()
        content = msg.get("content", "")[:MAX_MSG_CHARS]
        timestamp = msg.get("timestamp", "")[:10]
        lines.append(f"[{timestamp}] {role}: {content}")
    return "\n".join(lines)


def merge_learnings(results: List[str]) -> str:
    """Merge multiple learnings extractions into one deduplicated output."""
    sections = {
        "Lessons Learned": set(),
        "Decisions Made": set(),
        "Patterns Noticed": set(),
        "Dead Ends": set(),
    }
    current = None
    for result in results:
        for line in result.splitlines():
            line = line.strip()
            for section in sections:
                if f"## {section}" in line or f"**{section}**" in line:
                    current = section
                    break
            else:
                if current and line.startswith("*") and len(line) > 3:
                    sections[current].add(line)

    output = []
    for section, bullets in sections.items():
        output.append(f"## {section}")
        if bullets:
            output.extend(sorted(bullets))
        else:
            output.append("None")
        output.append("")
    return "\n".join(output)


def extract_learnings_for_chat(chat: Dict, model: str) -> str:
    """Extract learnings from a chat, chunking if it's too long (Ollama mode)."""
    title = chat.get("title", "Untitled")
    date = chat.get("date", "")
    messages = chat.get("messages", [])

    if not messages:
        return "### Lessons Learned\nNone\n\n### Decisions Made\nNone\n\n### Patterns Noticed\nNone\n\n### Dead Ends\nNone"

    # Split into chunks
    chunks = [messages[i:i + CHUNK_SIZE] for i in range(0, len(messages), CHUNK_SIZE)]
    total = len(chunks)

    if total == 1:
        summary = condense_chunk(title, date, chunks[0], 1, 1)
        return ollama_extract(summary, model)

    # Multi-chunk: extract from each, then merge
    results = []
    for i, chunk in enumerate(chunks, 1):
        summary = condense_chunk(title, date, chunk, i, total)
        result = ollama_extract(summary, model)
        if result:
            results.append(result)

    return merge_learnings(results) if results else "### Lessons Learned\nNone\n\n### Decisions Made\nNone\n\n### Patterns Noticed\nNone\n\n### Dead Ends\nNone"


def parse_conversations(file_path: Path) -> Generator[Dict, None, None]:
    """Auto-detect format and parse conversation file."""
    if file_path.suffix != ".json":
        return

    openai_chats = []
    anthropic_chats = []

    try:
        openai_chats = list(parse_openai(str(file_path)))
    except Exception:
        pass

    try:
        anthropic_chats = list(parse_anthropic(str(file_path)))
    except Exception:
        pass

    # Prefer whichever parser yielded more messages (smarter scoring)
    def scored(chats):
        return sum(len(c.get("messages", [])) for c in chats)

    openai_score = scored(openai_chats)
    anthropic_score = scored(anthropic_chats)

    if openai_score >= anthropic_score and openai_chats:
        print(f"Processing {file_path.name} (format: openai)...", file=sys.stderr)
        yield from openai_chats
    elif anthropic_chats:
        print(f"Processing {file_path.name} (format: anthropic)...", file=sys.stderr)
        yield from anthropic_chats
    else:
        print(f"Warning: Could not parse {file_path}", file=sys.stderr)


def load_processed_ids(workspace: Path) -> set:
    """Load set of already-processed chat IDs."""
    processed_file = workspace / ".processed_ids"
    if processed_file.exists():
        return set(processed_file.read_text().strip().split("\n"))
    return set()


def save_processed_ids(workspace: Path, processed: set) -> None:
    """Save set of processed chat IDs."""
    processed_file = workspace / ".processed_ids"
    processed_file.write_text("\n".join(sorted(processed)))


def main():
    parser = argparse.ArgumentParser(description="Extract learnings from conversation exports")
    parser.add_argument("--dir", type=Path, help="Directory of export files")
    parser.add_argument("--file", type=Path, help="Single export file")
    parser.add_argument("--limit", type=int, default=None, help="Process first N conversations")
    parser.add_argument("--since", type=str, help="Skip conversations before YYYY-MM-DD")
    parser.add_argument("--model", type=str, default=None, help="Model name (auto-selected by default)")
    parser.add_argument("--dry-run", action="store_true", help="Print without writing")

    args = parser.parse_args()

    if not args.dir and not args.file:
        print("Error: provide --dir or --file", file=sys.stderr)
        sys.exit(1)

    # Determine model if not specified
    if args.model is None:
        args.model = "gpt-4o-mini" if use_openai_api() else "gemma4:26b"

    workspace = get_workspace()
    processed = load_processed_ids(workspace)
    since_date = datetime.fromisoformat(args.since) if args.since else None

    output_file = workspace / "memory" / "semantic" / "learnings-from-exports.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Collect export files
    export_files = []
    if args.file:
        export_files = [args.file]
    elif args.dir:
        export_files = sorted(args.dir.glob("*.json"))

    count = 0
    for file_path in export_files:
        if count >= (args.limit or float("inf")):
            break

        for chat in parse_conversations(file_path):
            chat_id = chat.get("id")
            if chat_id in processed:
                continue

            # Check date filter first (before counting toward limit)
            chat_date = datetime.fromisoformat(chat.get("date", ""))
            if since_date and chat_date < since_date:
                continue

            # Now check limit
            if args.limit and count >= args.limit:
                break

            # Extract learnings with mode-appropriate method
            msg_count = len(chat.get("messages", []))
            
            if use_openai_api():
                # OpenAI mode: simple condense + extract
                summary = condense_conversation(chat)
                print(f"Processing {chat_id}...", file=sys.stderr)
                learnings = openai_extract(summary, args.model)
            else:
                # Ollama mode: chunked extraction with deduplication
                chunks_needed = max(1, msg_count // CHUNK_SIZE)
                print(f"Processing {chat_id} ({msg_count} msgs, {chunks_needed} chunk(s))...", file=sys.stderr)
                learnings = extract_learnings_for_chat(chat, args.model)

            # Format output
            output = f"\n## {chat.get('title', 'Untitled')} ({chat.get('date')})\n\n{learnings}\n"

            if args.dry_run:
                print(output)
            else:
                with open(output_file, "a") as f:
                    f.write(output)

            processed.add(chat_id)
            count += 1

    # Save dedup state
    if not args.dry_run:
        save_processed_ids(workspace, processed)
        print(f"Processed {count} conversations. Saved to {output_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
