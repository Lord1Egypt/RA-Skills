#!/usr/bin/env python3
"""
Update project context with new information.
Appends to PROJECT.md iteration history.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

def find_project_file():
    """Find PROJECT.md in workspace"""
    current = Path.cwd()
    project_file = current / 'PROJECT.md'
    
    if project_file.exists():
        return project_file
    
    # Try parent directories
    for parent in current.parents:
        candidate = parent / 'PROJECT.md'
        if candidate.exists():
            return candidate
    
    return None

def append_to_history(project_file, entry_type, content):
    """Append entry to iteration history"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    entry = f"\n### {timestamp} - {entry_type}\n{content}\n"
    
    with open(project_file, 'a') as f:
        f.write(entry)

def main():
    parser = argparse.ArgumentParser(
        description='Update project context'
    )
    parser.add_argument(
        '--add-goal',
        help='Add a new goal'
    )
    parser.add_argument(
        '--add-constraint',
        help='Add a technical constraint'
    )
    parser.add_argument(
        '--add-note',
        help='Add a general note'
    )
    parser.add_argument(
        '--project-file',
        help='Path to PROJECT.md (default: auto-detect)'
    )
    
    args = parser.parse_args()
    
    # Find project file
    if args.project_file:
        project_file = Path(args.project_file)
    else:
        project_file = find_project_file()
    
    if not project_file or not project_file.exists():
        print("[ERROR] PROJECT.md not found. Run init_context.py first.", file=sys.stderr)
        sys.exit(1)
    
    # Add entries
    if args.add_goal:
        append_to_history(project_file, "Goal Added", f"- {args.add_goal}")
        print(f"✅ Added goal: {args.add_goal}")
    
    if args.add_constraint:
        append_to_history(project_file, "Constraint Added", f"- {args.add_constraint}")
        print(f"✅ Added constraint: {args.add_constraint}")
    
    if args.add_note:
        append_to_history(project_file, "Note", args.add_note)
        print(f"✅ Added note: {args.add_note}")
    
    if not any([args.add_goal, args.add_constraint, args.add_note]):
        print("[ERROR] No updates specified. Use --add-goal, --add-constraint, or --add-note", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
