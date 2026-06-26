#!/usr/bin/env python3
"""
Session Extractor - Extract key information from OpenClaw session history.

This script integrates with OpenClaw tools to:
1. Fetch session status (context usage)
2. Fetch session history 
3. Extract key information (decisions, todos, context)
4. Generate continuation prompts
"""

import json
import re
import sys
from typing import Dict, List, Any


# Threshold configuration
MAX_CONTEXT = 200000
CONTINUATION_THRESHOLD = 0.95  # Trigger at 95%
TOKEN_WARNING_THRESHOLD = 0.85  # Warn at 85%


def parse_session_status(status_json: Dict) -> Dict:
    """Parse session status to get context usage."""
    # Extract context from status output
    # Format: "Context: 25k/200k (13%)"
    context_str = status_json.get("context", "0")
    
    # Parse "25k/200k (13%)" format
    match = re.search(r"(\d+(?:\.\d+)?)[kK]?/(\d+)[kK]?\s*\((\d+)%\)", context_str)
    if match:
        used_raw = match.group(1)
        max_raw = match.group(2)
        pct = int(match.group(3))
        
        # Convert k to number
        used = int(float(used_raw.replace("k", "").replace("K", "")) * 1000) if "k" in used_raw.lower() else int(used_raw)
        max_ctx = int(float(max_raw.replace("k", "").replace("K", "")) * 1000) if "k" in max_raw.lower() else int(max_raw)
        
        return {
            "used": used,
            "max": max_ctx,
            "percentage": pct
        }
    
    return {"used": 0, "max": MAX_CONTEXT, "percentage": 0}


def extract_tasks_and_todos(messages: List[Dict]) -> List[str]:
    """Extract unfinished tasks and TODOs from messages."""
    tasks = []
    
    task_indicators = [
        r"todo:?\s*(.+)",
        r"fixme:?\s*(.+)",
        r"pending:?\s*(.+)",
        r"in progress:?\s*(.+)",
        r"need to\s+(.+)",
        r"will\s+(.+)",
        r"should\s+(.+)",
        r"haven't\s+(.+)",
        r"hasn't\s+(.+)",
    ]
    
    for msg in messages:
        content = msg.get("content", "")
        
        # Skip if marked complete
        if "done" in content.lower() or "completed" in content.lower() or "finished" in content.lower():
            continue
            
        for pattern in task_indicators:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                task = match.strip() if isinstance(match, str) else match[0].strip()
                if task and len(task) > 10:
                    tasks.append(task[:150])
    
    return list(set(tasks))[:10]


def extract_decisions(messages: List[Dict]) -> List[str]:
    """Extract key decisions from messages."""
    decisions = []
    
    decision_patterns = [
        r"decided to\s+(.+)",
        r"chose to\s+(.+)",
        r"going with\s+(.+)",
        r"best approach is\s+(.+)",
        r"decided that\s+(.+)",
        r"agreed to\s+(.+)",
        r"will use\s+(.+)",
        r"choosing\s+(.+)",
    ]
    
    for msg in messages:
        content = msg.get("content", "")
        
        for pattern in decision_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                decision = match.strip() if isinstance(match, str) else match[0].strip()
                if decision and len(decision) > 5:
                    decisions.append(decision[:150])
    
    return list(set(decisions))[:5]


def extract_file_paths(messages: List[Dict]) -> List[str]:
    """Extract important file paths from messages."""
    files = []
    
    # Common file path patterns
    file_patterns = [
        r"(?:/[\w\-\.]+){2,}\.\w+",  # Unix paths
        r"[A-Za-z]:\\[\w\\\-\.]+\.\w+",  # Windows paths
    ]
    
    for msg in messages:
        content = msg.get("content", "")
        
        for pattern in file_patterns:
            matches = re.findall(pattern, content)
            files.extend(matches)
    
    return list(set(files))[:10]


def extract_preferences(messages: List[Dict]) -> List[str]:
    """Extract user preferences and requirements."""
    prefs = []
    
    pref_patterns = [
        r"prefer\s+(.+)",
        r"like\s+(.+)",
        r"want\s+(.+)",
        r"need\s+(.+)",
        r"require\s+(.+)",
        r"should\s+(.+)",
    ]
    
    # Look for explicit preference statements
    for msg in messages:
        content = msg.get("content", "")
        
        # Only check user messages for preferences
        if msg.get("role") != "user":
            continue
            
        for pattern in pref_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                pref = match.strip() if isinstance(match, str) else match[0].strip()
                if pref and len(pref) > 10:
                    prefs.append(pref[:150])
    
    return list(set(prefs))[:5]


def extract_important_context(messages: List[Dict]) -> List[str]:
    """Extract important context that should be preserved."""
    context = []
    
    # Look for:
    # - Error messages
    # - Configuration values
    # - API keys / credentials (masked)
    # - Important URLs
    
    important_patterns = [
        r"(?:error|failed|exception):\s*(.+)",
        r"config(?:uration)?:?\s*(.+)",
        r"(?:https?://)?[\w\-\.]+\.[\w/\-\.]+",  # URLs
    ]
    
    for msg in messages[-10:]:  # Only recent messages
        content = msg.get("content", "")
        
        for pattern in important_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                ctx = match.strip() if isinstance(match, str) else match[0].strip()
                if ctx and len(ctx) > 15:
                    context.append(ctx[:150])
    
    return list(set(context))[:10]


def generate_continuation(extracted: Dict, messages: List[Dict]) -> str:
    """Generate continuation prompt."""
    
    prompt = """# Session Continuation

## Task Status
"""
    
    # Unfinished tasks
    if extracted.get("tasks"):
        prompt += "### Uncompleted\n"
        for task in extracted["tasks"]:
            prompt += f"- {task}\n"
    else:
        prompt += "### Uncompleted\n- None recorded\n"
    
    # Completed (infer from messages)
    prompt += "\n### Completed\n"
    prompt += "- (See conversation history below)\n"
    
    # Key decisions
    prompt += "\n## Key Decisions\n"
    if extracted.get("decisions"):
        for decision in extracted["decisions"]:
            prompt += f"- {decision}\n"
    else:
        prompt += "- None recorded\n"
    
    # Important files
    prompt += "\n## Important Files\n"
    if extracted.get("files"):
        for f in extracted["files"][:5]:
            prompt += f"- {f}\n"
    else:
        prompt += "- None recorded\n"
    
    # User preferences
    prompt += "\n## User Preferences\n"
    if extracted.get("preferences"):
        for pref in extracted["preferences"]:
            prompt += f"- {pref}\n"
    else:
        prompt += "- None recorded\n"
    
    # Recent messages
    prompt += "\n## Recent Conversation\n"
    for msg in messages[-5:]:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")[:200]
        prompt += f"**{role}**: {content}\n\n"
    
    prompt += "\n---\n\n"
    prompt += "## Continuation Instructions\n"
    prompt += "Continue the previous session. Focus on:\n"
    prompt += "1. Completing any unfinished tasks\n"
    prompt += "2. Respecting key decisions made\n"
    prompt += "3. Preserving important context above\n"
    prompt += "4. Building on recent progress\n"
    
    return prompt


def analyze_session(status_json: Dict, messages: List[Dict]) -> Dict:
    """Full session analysis."""
    
    # Parse status
    status = parse_session_status(status_json)
    
    # Check if threshold exceeded
    threshold_pct = CONTINUATION_THRESHOLD * 100
    needs_continuation = status["percentage"] >= threshold_pct
    
    # Extract information
    extracted = {
        "tasks": extract_tasks_and_todos(messages),
        "decisions": extract_decisions(messages),
        "files": extract_file_paths(messages),
        "preferences": extract_preferences(messages),
        "context": extract_important_context(messages),
    }
    
    # Generate continuation if needed
    continuation = None
    if needs_continuation:
        continuation = generate_continuation(extracted, messages)
    
    return {
        "status": status,
        "extracted": extracted,
        "needs_continuation": needs_continuation,
        "continuation": continuation,
        "warnings": {
            "high_usage": status["percentage"] >= (TOKEN_WARNING_THRESHOLD * 100),
            "critical": needs_continuation
        }
    }


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Session Extractor for OpenClaw")
    parser.add_argument("command", choices=["analyze", "extract", "prompt"],
                       help="Command to run")
    parser.add_argument("--status", help="Session status JSON")
    parser.add_argument("--history", help="Session history JSON")
    parser.add_argument("--output", choices=["text", "json"], default="text",
                       help="Output format")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        # Read from stdin or files
        status = json.loads(args.status) if args.status else {}
        history = json.loads(args.history) if args.history else []
        
        result = analyze_session(status, history)
        
        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"Context: {result['status']['percentage']}%")
            if result['warnings']['high_usage']:
                print(f"⚠️  High context usage: {result['status']['percentage']}%")
            if result['needs_continuation']:
                print(f"🔴 Threshold exceeded! Continuation needed.")
            print(f"\nExtracted {len(result['extracted']['tasks'])} tasks, "
                  f"{len(result['extracted']['decisions'])} decisions")
    
    elif args.command == "extract":
        history = json.loads(args.history) if args.history else []
        
        extracted = {
            "tasks": extract_tasks_and_todos(history),
            "decisions": extract_decisions(history),
            "files": extract_file_paths(history),
            "preferences": extract_preferences(history),
            "context": extract_important_context(history),
        }
        
        if args.output == "json":
            print(json.dumps(extracted, indent=2))
        else:
            print("=== Tasks ===")
            for t in extracted["tasks"]:
                print(f"- {t}")
            print("\n=== Decisions ===")
            for d in extracted["decisions"]:
                print(f"- {d}")
    
    elif args.command == "prompt":
        history = json.loads(args.history) if args.history else []
        
        extracted = {
            "tasks": extract_tasks_and_todos(history),
            "decisions": extract_decisions(history),
            "files": extract_file_paths(history),
            "preferences": extract_preferences(history),
            "context": extract_important_context(history),
        }
        
        prompt = generate_continuation(extracted, history)
        print(prompt)


if __name__ == "__main__":
    main()
