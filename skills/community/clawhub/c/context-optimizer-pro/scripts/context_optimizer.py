#!/usr/bin/env python3
"""
Context Optimizer - Monitor and manage context usage for OpenClaw sessions.
"""

import json
import os
import re
import sys
from pathlib import Path

# Configuration
MAX_CONTEXT = 200000  # 200k tokens
DEFAULT_THRESHOLD = 0.95  # 95%
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def get_session_status():
    """Get current session status using session_status tool."""
    # This would be called via OpenClaw's exec or tool system
    # For now, return placeholder - actual implementation uses tool
    return {
        "context": 25000,  # Default example
        "max": MAX_CONTEXT,
        "percentage": 13
    }


def check_context_usage():
    """Check current context usage."""
    status = get_session_status()
    used = status["context"]
    max_ctx = status["max"]
    pct = (used / max_ctx) * 100
    
    print(f"Context: {used:,}/{max_ctx:,} ({pct:.1f}%)")
    
    if pct >= (DEFAULT_THRESHOLD * 100):
        print(f"⚠️  Context usage ({pct:.1f}%) exceeds threshold ({DEFAULT_THRESHOLD*100:.0f}%)")
        print("Consider running: context-optimizer split")
        return True
    else:
        print(f"✓ Context usage OK ({pct:.1f}% < {DEFAULT_THRESHOLD*100:.0f}%)")
        return False


def extract_key_information(history: list) -> dict:
    """Extract key information from conversation history."""
    
    extracted = {
        "unfinished_tasks": [],
        "key_decisions": [],
        "critical_context": [],
        "user_preferences": [],
        "recent_progress": [],
        "important_files": []
    }
    
    # Patterns to identify important content
    task_patterns = [
        r"(?:TODO|FIXME|pending|in progress|working on)",
        r"(?:will|need to|should|have to).+(?:do|finish|complete)",
    ]
    
    decision_patterns = [
        r"decided to",
        r"chose to",
        r"going with",
        r"best approach is",
        r"decided that",
    ]
    
    file_patterns = [
        r"(?:read|write|edit|create|modify).+?(\/\S+\.\w+)",
    ]
    
    for msg in history:
        content = msg.get("content", "").lower()
        
        # Extract unfinished tasks
        for pattern in task_patterns:
            if re.search(pattern, content):
                # Add to unfinished if not completed
                if "done" not in content and "completed" not in content:
                    extracted["unfinished_tasks"].append(content[:200])
                    
        # Extract decisions
        for pattern in decision_patterns:
            if re.search(pattern, content):
                extracted["key_decisions"].append(content[:200])
                
        # Extract file paths
        for pattern in file_patterns:
            matches = re.findall(pattern, content)
            extracted["important_files"].extend(matches)
    
    # Deduplicate
    for key in extracted:
        extracted[key] = list(set(extracted[key]))[:10]  # Max 10 each
    
    return extracted


def generate_continuation_prompt(extracted: dict, recent_history: list) -> str:
    """Generate continuation prompt for new session."""
    
    prompt = """# Previous Session Summary

## Unfinished Tasks
"""
    
    if extracted["unfinished_tasks"]:
        for task in extracted["unfinished_tasks"][:5]:
            prompt += f"- {task}\n"
    else:
        prompt += "- None recorded\n"
        
    prompt += "\n## Key Decisions\n"
    if extracted["key_decisions"]:
        for decision in extracted["key_decisions"][:3]:
            prompt += f"- {decision}\n"
    else:
        prompt += "- None recorded\n"
        
    prompt += "\n## Important Context\n"
    if extracted["critical_context"]:
        for ctx in extracted["critical_context"][:3]:
            prompt += f"- {ctx}\n"
    else:
        # Extract from recent history
        prompt += "- (See recent conversation below)\n"
        
    prompt += "\n## Recent Progress\n"
    for msg in recent_history[-3:]:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")[:150]
        prompt += f"- {role}: {content}...\n"
        
    prompt += "\n---\n\n## Continuation Task\n"
    prompt += "Continue from where the previous session left off. "
    prompt += "Focus on completing unfinished tasks and preserving the work done."
    
    return prompt


def split_session(threshold: float = DEFAULT_THRESHOLD):
    """Split session by extracting context and creating continuation."""
    
    print(f"Context Optimizer - Creating Session Split")
    print(f"Threshold: {threshold*100:.0f}%")
    print("-" * 40)
    
    # Check current usage
    status = get_session_status()
    pct = status["context"] / status["max"]
    
    if pct < threshold:
        print(f"Context usage ({pct*100:.1f}%) below threshold ({threshold*100:.0f}%)")
        print("Use --force to override")
        return
    
    print("Proceeding with context extraction...")
    
    # In actual implementation, this would:
    # 1. Get full session history via sessions_history tool
    # 2. Extract key information
    # 3. Generate continuation prompt
    # 4. Create new session via sessions_spawn
    
    print("\n[Would extract and create continuation session]")
    print("Note: This requires integration with OpenClaw's tool system")


def preview_extraction():
    """Preview what would be extracted."""
    print("Context Optimizer - Extraction Preview")
    print("-" * 40)
    print("\nThis would extract:")
    print("- Unfinished tasks and TODOs")
    print("- Key decisions made")
    print("- Critical context and preferences")
    print("- Important file paths")
    print("- Recent progress")
    print("\nRun 'split' to actually perform extraction")


def main():
    if len(sys.argv) < 2:
        print("Usage: context-optimizer <command>")
        print("Commands:")
        print("  check    - Check current context usage")
        print("  split    - Split session at threshold")
        print("  preview  - Preview extraction")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "check":
        check_context_usage()
    elif cmd == "split":
        threshold = DEFAULT_THRESHOLD
        if len(sys.argv) > 2 and sys.argv[2] == "--threshold":
            threshold = float(sys.argv[3]) / 100
        split_session(threshold)
    elif cmd == "preview":
        preview_extraction()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
