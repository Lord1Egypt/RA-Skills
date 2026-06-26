#!/usr/bin/env python3
"""
BeastXA Memory Pro — Memory Structure Setup

Creates the memory directory structure and templates.
Safe to run multiple times — won't overwrite existing files.

Usage:
    python3 setup_memory.py
    python3 setup_memory.py --workspace /path/to/workspace
"""

import argparse
import os
from pathlib import Path
from datetime import datetime

SESSION_NOTES_TEMPLATE = """# Session Notes
_Auto-maintained by BeastXA Memory Pro_

# Current State
_Describe what you're currently working on_

# Task Specification
_Core objectives and requirements_

# Files and Functions
_Key files you're working with_

# Errors and Corrections
_Mistakes made and how they were fixed_

# Learnings
_Lessons learned during this session_

# Key Results
_Important outputs and achievements_

# Worklog
_Chronological log of work done_
"""

MEMORY_TEMPLATE = """# MEMORY.md — Long-Term Memory

_Last updated: {date}_

## About You
- Name:
- Timezone:
- Key context:

## Active Projects
- Project 1: status
- Project 2: status

## Decisions & Lessons
- Decision 1: rationale
- Lesson 1: what happened and what to do differently

## Preferences & Rules
- Communication style:
- Work preferences:
- Red lines:

## Tools & Environment
- Platform:
- Key tools:
- Accounts:
"""


def create_file_if_missing(path: Path, content: str, label: str):
    """Create a file only if it doesn't exist."""
    if path.exists():
        print(f'   ⏭️  {label}: already exists, skipping')
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    print(f'   ✅ {label}: created')
    return True


def main():
    parser = argparse.ArgumentParser(description='Set up memory structure')
    parser.add_argument('--workspace', '-w', default='.',
                        help='Workspace root directory (default: current dir)')
    args = parser.parse_args()
    
    workspace = Path(args.workspace).resolve()
    print(f'🏗️  Setting up memory structure in: {workspace}')
    print()
    
    created = 0
    
    # Create directories
    dirs = ['memory', 'memory/topics']
    for d in dirs:
        dirpath = workspace / d
        if not dirpath.exists():
            dirpath.mkdir(parents=True, exist_ok=True)
            print(f'   📁 Created {d}/')
            created += 1
        else:
            print(f'   ⏭️  {d}/ already exists')
    
    print()
    
    # Create session-notes.md
    if create_file_if_missing(
        workspace / 'memory' / 'session-notes.md',
        SESSION_NOTES_TEMPLATE,
        'memory/session-notes.md'
    ):
        created += 1
    
    # Create MEMORY.md (only if it doesn't exist)
    if create_file_if_missing(
        workspace / 'MEMORY.md',
        MEMORY_TEMPLATE.format(date=datetime.now().strftime('%Y-%m-%d')),
        'MEMORY.md'
    ):
        created += 1
    
    # Create today's daily log
    today = datetime.now().strftime('%Y-%m-%d')
    daily_content = f'# {today}\n\n_Daily log created by BeastXA Memory Pro_\n'
    if create_file_if_missing(
        workspace / 'memory' / f'{today}.md',
        daily_content,
        f'memory/{today}.md'
    ):
        created += 1
    
    print()
    if created > 0:
        print(f'✅ Setup complete! {created} items created.')
    else:
        print('✅ Everything already set up. No changes needed.')
    
    print()
    print('Next steps:')
    print('  1. Edit MEMORY.md with your key information')
    print('  2. Run: bash scripts/install.sh  (to set up crons and compaction)')
    print('  3. Start chatting — your agent will auto-maintain memory from here')


if __name__ == '__main__':
    main()
