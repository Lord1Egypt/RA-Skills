#!/usr/bin/env python3
"""
Task Decomposition Validator
Validates that subtasks follow the proper format and use only actions from the action bank.
Also validates new action additions to prevent duplicates.
"""

import re
import sys
from pathlib import Path

# Load action bank
ACTION_BANK_PATH = Path(__file__).parent.parent / "references" / "action-bank.md"

def load_actions():
    """Extract actions from the action bank markdown."""
    if not ACTION_BANK_PATH.exists():
        return None
    
    with open(ACTION_BANK_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    actions = []
    for line in content.split('\n'):
        if '|' in line and not line.strip().startswith('|---'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3 and parts[1] and not parts[1].lower().startswith('action'):
                action = parts[1].lower().strip()
                if action:
                    actions.append(action)
    
    return set(actions)

def load_action_descriptions():
    """Extract action descriptions for duplicate checking."""
    if not ACTION_BANK_PATH.exists():
        return {}
    
    with open(ACTION_BANK_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    descriptions = {}
    in_table = False
    for line in content.split('\n'):
        if '| Action |' in line or '| action |' in line:
            in_table = True
            continue
        if in_table and line.startswith('|---'):
            continue
        if in_table and '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                action = parts[1].lower().strip()
                desc = parts[2].lower().strip() if len(parts) > 2 else ""
                if action and desc and action not in ['action', 'description', '']:
                    descriptions[action] = desc
    
    return descriptions

def check_action_duplicate(new_action, new_desc=None):
    """
    Check if a new action is significantly different from existing ones.
    Returns (is_duplicate, similar_actions)
    """
    actions = load_actions()
    descriptions = load_action_descriptions()
    
    if not actions:
        return False, []
    
    new_action_lower = new_action.lower().strip()
    new_verb = new_action_lower.split()[0] if new_action_lower.split() else ""
    
    # Check exact match
    if new_action_lower in actions:
        return True, [new_action_lower]
    
    similar = []
    
    # Check same first verb (root word)
    for existing in actions:
        existing_verb = existing.split()[0] if existing.split() else ""
        if new_verb == existing_verb:
            similar.append(existing)
    
    # If description provided, check for semantic overlap
    # Only flag as duplicate if action name is similar AND description is similar
    if new_desc and new_verb:
        new_desc_lower = new_desc.lower()
        for action, desc in descriptions.items():
            action_verb = action.split()[0] if action.split() else ""
            # Only check if same verb family
            if action_verb == new_verb:
                # Check for significant word overlap in descriptions
                new_words = set(new_desc_lower.split())
                existing_words = set(desc.split())
                overlap = new_words & existing_words
                # If more than 2 key words overlap, consider similar
                if len(overlap) > 2:
                    if action not in similar:
                        similar.append(action)
    
    return len(similar) > 0, similar

def validate_subtask(subtask, actions):
    """Validate a single subtask format."""
    errors = []
    
    gripper_pattern = r'with (left|right|either) gripper'
    if not re.search(gripper_pattern, subtask):
        errors.append("Missing gripper specification (left/right/either gripper)")
    
    parts = subtask.strip().split()
    if parts:
        # Handle multi-word actions like "pick up", "take out"
        action = parts[0].lower()
        # Check if first two words form an action (e.g., "pick up")
        if len(parts) >= 2 and f"{parts[0]} {parts[1]}" in actions:
            action = f"{parts[0]} {parts[1]}"
        elif action not in actions:
            errors.append(f"Action '{action}' not in action bank")
    
    return errors

def validate_decomposition(subtasks_text):
    """Validate a decomposition output."""
    actions = load_actions()
    if not actions:
        print("Warning: Could not load action bank")
        return False
    
    lines = subtasks_text.strip().split('\n')
    subtasks = [re.sub(r'^\d+[\.\)]\s*', '', l) for l in lines if re.match(r'^\d+', l)]
    
    if not subtasks:
        print("No numbered subtasks found")
        return False
    
    all_valid = True
    for i, st in enumerate(subtasks, 1):
        errors = validate_subtask(st, actions)
        if errors:
            print(f"Subtask {i} errors:")
            for e in errors:
                print(f"  - {e}")
            all_valid = False
    
    if all_valid:
        print(f"[OK] Validated {len(subtasks)} subtasks")
    
    return all_valid

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--check-action':
            if len(sys.argv) < 3:
                print("Usage: validate.py --check-action <action_name> [description]")
                sys.exit(1)
            new_action = sys.argv[2]
            new_desc = sys.argv[3] if len(sys.argv) > 3 else None
            is_dup, similar = check_action_duplicate(new_action, new_desc)
            if is_dup:
                print(f"[X] Duplicate: '{new_action}' is similar to: {', '.join(similar)}")
                sys.exit(1)
            else:
                print(f"[OK] '{new_action}' is significantly different from existing actions")
                sys.exit(0)
        else:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                content = f.read()
            validate_decomposition(content)
    else:
        print("Enter subtasks (Ctrl+D to finish):")
        content = sys.stdin.read()
        validate_decomposition(content)

if __name__ == "__main__":
    main()