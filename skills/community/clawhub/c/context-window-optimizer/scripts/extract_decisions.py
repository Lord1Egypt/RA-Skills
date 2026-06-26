#!/usr/bin/env python3
"""
Extract decisions and key facts from session.
Usage: python3 extract_decisions.py --session current [--no-llm]
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

def load_messages():
    """Load messages from the latest session transcript."""
    p = Path("~/.openclaw/agents/main/sessions/").expanduser()
    
    if not p.exists():
        return []
    
    jsonl_files = [f for f in p.glob("*.jsonl") if ".lock" not in str(f)]
    if not jsonl_files:
        return []
    
    latest = max(jsonl_files, key=lambda f: f.stat().st_mtime)
    
    messages = []
    with open(latest) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if entry.get("type") == "message":
                    msg = entry.get("message", {})
                    role = msg.get("role", "unknown")
                    content = msg.get("content", [])
                    
                    text = ""
                    if isinstance(content, str):
                        text = content
                    elif isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict):
                                if block.get("type") == "text":
                                    text += block.get("text", "")
                                elif block.get("type") == "toolCall":
                                    args = block.get("arguments", {})
                                    if isinstance(args, dict):
                                        cmd = args.get("command", "")
                                        if cmd:
                                            text += f"[TOOL: {block.get('name', 'unknown')}] {cmd[:80]}\n"
                                    else:
                                        text += f"[TOOL: {block.get('name', 'unknown')}]\n"
                    
                    if text.strip():
                        messages.append({
                            "role": role,
                            "content": text[:1500]
                        })
            except Exception:
                continue
    
    return messages

def extract_decisions_keyword(messages):
    """Extract decisions using keywords and patterns."""
    patterns = {
        "decisions": [
            "decided", "agreed", "choice", "chose", "selected",
            "decision", "going with", "will use", "settled on",
            "concluded", "let's go with", "approved", "confirmed"
        ],
        "actions": [
            "installed", "created", "built", "done", "completed",
            "finished", "implemented", "set up", "configured",
            "wrote", "added", "modified", "updated", "packaged"
        ],
        "preferences": [
            "prefer", "like", "want", "need", "always", "never",
            "i prefer", "user prefers", "style is", "vibe"
        ]
    }
    
    results = {"decisions": [], "actions": [], "preferences": []}
    
    for msg in messages:
        content_lower = msg.get("content", "").lower()
        role = msg.get("role", "")
        
        # Check each category
        for cat, keywords in patterns.items():
            for kw in keywords:
                if kw in content_lower:
                    # Get surrounding context
                    idx = content_lower.find(kw)
                    start = max(0, idx - 50)
                    end = min(len(msg["content"]), idx + 100)
                    context = msg["content"][start:end]
                    
                    if context not in [x["context"] for x in results[cat]]:
                        results[cat].append({
                            "role": role,
                            "keyword": kw,
                            "context": context
                        })
                    break
    
    return results

def format_output(results, date):
    """Format extraction results as markdown."""
    output = f"# Decisions & Key Facts: {date}\n\n"
    
    output += "## Decisions Made\n"
    if results["decisions"]:
        for i, d in enumerate(results["decisions"][:15], 1):
            output += f"{i}. *[{d['role']}]* \"{d['context'].strip()}\"\n"
    else:
        output += "_None explicitly marked_\n"
    
    output += "\n## Actions Completed\n"
    if results["actions"]:
        for i, d in enumerate(results["actions"][:15], 1):
            output += f"{i}. *[{d['role']}]* \"{d['context'].strip()}\"\n"
    else:
        output += "_None found_\n"
    
    output += "\n## Preferences/Stated\n"
    if results["preferences"]:
        for i, d in enumerate(results["preferences"][:10], 1):
            output += f"{i}. *[{d['role']}]* \"{d['context'].strip()}\"\n"
    else:
        output += "_None found_\n"
    
    output += f"\n---\n_Extracted: {datetime.now().isoformat()}_\n"
    return output

def main():
    parser = argparse.ArgumentParser(description="Extract decisions from session")
    parser.add_argument("--session", default="current")
    parser.add_argument("--output", default=None)
    parser.add_argument("--no-llm", action="store_true", help="Force keyword extraction")
    args = parser.parse_args()
    
    print("🎯 Extracting decisions and key facts...")
    
    messages = load_messages()
    if not messages:
        print("No session data found.")
        return
    
    print(f"📊 Loaded {len(messages)} messages from session")
    
    # Keyword extraction (always works)
    print("🔍 Analyzing conversation patterns...")
    results = extract_decisions_keyword(messages)
    
    total = sum(len(v) for v in results.values())
    print(f"📝 Found {total} items ({len(results['decisions'])} decisions, {len(results['actions'])} actions)")
    
    date = datetime.now().strftime("%Y-%m-%d")
    output = format_output(results, date)
    
    if args.output:
        output_file = Path(args.output).expanduser()
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(output)
        print(f"✅ Results saved to: {output_file}")
    else:
        print("\n" + output)
    
    return output

if __name__ == "__main__":
    main()
