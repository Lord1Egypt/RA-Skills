#!/usr/bin/env python3
"""
Safety checker for screen-vision skill.
Validates actions before execution to prevent dangerous operations.
"""

import json
import re
import os

# Patterns that should always be blocked
BLOCKED_PATTERNS = [
    r"rm\s+(-rf?|--recursive).*(/|\s~)",
    r"mkfs\.",
    r"dd\s+if=.*of=/dev/",
    r"format\s+[a-zA-Z]:",
    r"shutdown",
    r"reboot",
    r"init\s+[06]",
    r"fork\s*bomb",
    r":\(\)\{.*\}",
    r"drop\s+database",
    r"factory\s+reset",
    r"del\s+/[sS]\s+[a-zA-Z]:\\",
]

# Patterns that require user confirmation
CONFIRM_PATTERNS = [
    r"\brm\b",
    r"\bdelete\b",
    r"\bremove\b",
    r"\bsudo\b",
    r"\bformat\b",
    r"payment",
    r"转账",
    r"支付",
    r"删除",
    r"确认购买",
]

# Maximum limits
MAX_DURATION_MIN = 5
MAX_ACTIONS = 100
MAX_TEXT_LENGTH = 5000


def check_action(action):
    """
    Validate a single action for safety.
    
    Returns:
        dict: {
            "safe": bool,
            "needs_confirm": bool,
            "reason": str,
            "blocked": bool
        }
    """
    action_type = action.get("type", "")
    text = action.get("text", "")
    reason = action.get("reason", "")
    
    combined_text = f"{text} {reason}".lower()
    
    # Check blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, combined_text, re.IGNORECASE):
            return {
                "safe": False,
                "needs_confirm": False,
                "reason": f"Blocked: matches dangerous pattern '{pattern}'",
                "blocked": True
            }
    
    # Check confirm patterns
    needs_confirm = False
    for pattern in CONFIRM_PATTERNS:
        if re.search(pattern, combined_text, re.IGNORECASE):
            needs_confirm = True
            break
    
    # Validate coordinates (must be positive integers)
    for coord in ["x", "y", "x1", "y1", "x2", "y2"]:
        val = action.get(coord)
        if val is not None:
            if not isinstance(val, int) or val < 0:
                return {
                    "safe": False,
                    "needs_confirm": False,
                    "reason": f"Invalid coordinate: {coord}={val}",
                    "blocked": False
                }
    
    # Validate text length
    if len(text) > MAX_TEXT_LENGTH:
        return {
            "safe": False,
            "needs_confirm": False,
            "reason": f"Text too long: {len(text)} > {MAX_TEXT_LENGTH}",
            "blocked": False
        }
    
    # Validate action type
    valid_types = ["click", "type", "key", "scroll", "drag", "wait", "done", "failed"]
    if action_type not in valid_types:
        return {
            "safe": False,
            "needs_confirm": False,
            "reason": f"Invalid action type: {action_type}",
            "blocked": False
        }
    
    return {
        "safe": True,
        "needs_confirm": needs_confirm,
        "reason": "OK" if not needs_confirm else "Requires user confirmation",
        "blocked": False
    }


def check_task_limits(task_duration_min, action_count):
    """Check if task has exceeded limits."""
    issues = []
    
    if task_duration_min > MAX_DURATION_MIN:
        issues.append(f"Task exceeded {MAX_DURATION_MIN}min timeout")
    
    if action_count > MAX_ACTIONS:
        issues.append(f"Task exceeded {MAX_ACTIONS} action limit")
    
    return {
        "within_limits": len(issues) == 0,
        "issues": issues
    }


if __name__ == "__main__":
    # CLI test
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--action-json", required=True, help="Action JSON string")
    args = parser.parse_args()
    
    action = json.loads(args.action_json)
    result = check_action(action)
    print(json.dumps(result, indent=2))
