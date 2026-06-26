#!/usr/bin/env python3
"""
Analyze context window state and suggest optimizations.
Usage: python3 analyze_context.py --session current
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def analyze_session(session_path=None):
    """Analyze the current or specified session."""
    
    # Try to find session history
    # This is a simplified version - real implementation would hook into OpenClaw sessions
    
    print("📊 Context Window Analysis")
    print("=" * 40)
    
    # Placeholder metrics - in real use would read from OpenClaw
    metrics = {
        "message_count": 0,
        "estimated_tokens": 0,
        "oldest_message_age_hours": 0,
        "density_score": "unknown",
        "optimization_targets": []
    }
    
    # Check for session transcripts
    transcript_paths = [
        Path("~/.openclaw/agents/main/sessions/").expanduser(),
    ]
    
    total_messages = 0
    oldest = None
    newest = None
    
    for p in transcript_paths:
        if p.exists() and p.is_dir():
            jsonl_files = list(p.glob("*.jsonl"))
            if jsonl_files:
                latest = max(jsonl_files, key=lambda f: f.stat().st_mtime)
                with open(latest) as f:
                    for line in f:
                        if line.strip():
                            total_messages += 1
    
    metrics["message_count"] = total_messages
    
    # Estimate tokens (rough: ~4 chars per token, 500 tokens overhead)
    if total_messages > 0:
        metrics["estimated_tokens"] = (total_messages * 50) + 500  # rough estimate
    
    print(f"Messages: {metrics['message_count']}")
    print(f"Est. tokens: {metrics['estimated_tokens']}")
    
    if total_messages > 50:
        print("\n⚠️  Context is getting heavy.")
        print("   Consider running: summarize_session.py")
        print("   Or extract decisions with: extract_decisions.py")
    elif total_messages > 30:
        print("\n💡 Context is moderate. Start thinking about what can be archived.")
    else:
        print("\n✅ Context is lean. No action needed.")
    
    return metrics

if __name__ == "__main__":
    session = None
    if len(sys.argv) > 2 and sys.argv[1] == "--session":
        session = sys.argv[2]
    
    analyze_session(session)
