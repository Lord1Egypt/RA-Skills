#!/usr/bin/env python3
"""
Summarize a session into a compact summary file.
Usage: python3 summarize_session.py --session current --output summary.md
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

def summarize_session(session_path=None, output_path=None):
    """Create a summary of the session."""
    
    print("📝 Creating session summary...")
    
    # Find session transcript (JSONL format)
    transcript_paths = [
        Path("~/.openclaw/agents/main/sessions/").expanduser(),
    ]
    
    messages = []
    for p in transcript_paths:
        if p.exists() and p.is_dir():
            jsonl_files = list(p.glob("*.jsonl"))
            if jsonl_files:
                latest = max(jsonl_files, key=lambda f: f.stat().st_mtime)
                with open(latest) as f:
                    for line in f:
                        if line.strip():
                            try:
                                msg = json.loads(line)
                                messages.append(msg)
                            except:
                                pass
    
    if not messages:
        print("No session data found.")
        return
    
    # Categorize messages
    decisions = []
    completed = []
    open_items = []
    key_facts = []
    
    for msg in messages:
        content = msg.get("content", "").lower()
        role = msg.get("role", "")
        
        # Simple heuristics - in real use would use LLM
        if "decision" in content or "decided" in content or "agreed" in content:
            decisions.append(msg)
        elif "done" in content or "completed" in content or "finished" in content:
            completed.append(msg)
        elif "?" in content or "help" in content or "need" in content:
            open_items.append(msg)
        else:
            key_facts.append(msg)
    
    # Build summary
    date = datetime.now().strftime("%Y-%m-%d")
    summary = f"""# Session Summary: {date}

## Overview
- Total messages: {len(messages)}
- Decisions made: {len(decisions)}
- Items completed: {len(completed)}
- Open questions: {len(open_items)}

## Decisions Made
"""
    
    if decisions:
        for i, d in enumerate(decisions[:10], 1):
            content = d.get("content", "")[:200]
            summary += f"{i}. {content}...\n"
    else:
        summary += "_None recorded_\n"
    
    summary += "\n## Work Completed\n"
    if completed:
        for i, c in enumerate(completed[:10], 1):
            content = c.get("content", "")[:200]
            summary += f"{i}. {content}...\n"
    else:
        summary += "_None recorded_\n"
    
    summary += "\n## Open Questions / Next Steps\n"
    if open_items:
        for i, q in enumerate(open_items[:10], 1):
            content = q.get("content", "")[:200]
            summary += f"{i}. {content}...\n"
    else:
        summary += "_None recorded_\n"
    
    summary += f"\n---\n_Summary generated: {datetime.now().isoformat()}_"
    
    # Output
    if output_path:
        output = Path(output_path).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(summary)
        print(f"✅ Summary saved to: {output}")
    else:
        print(summary)
    
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize session")
    parser.add_argument("--session", default="current")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    
    summarize_session(args.session, args.output)
