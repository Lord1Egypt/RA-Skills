#!/usr/bin/env python3
"""
Memory System Initializer

Creates the directory structure and template files for a structured memory system.

Usage:
    python init_memory.py <workspace-path>

The workspace path should be the agent's workspace root (e.g., ~/.openclaw/workspace).
"""

import os
import sys
from datetime import datetime
from pathlib import Path


def create_memory_system(workspace: str):
    ws = Path(workspace)
    if not ws.exists():
        print(f"Error: workspace path does not exist: {ws}")
        sys.exit(1)

    memory_dir = ws / "memory"
    topics_dir = memory_dir / "topics"

    # Create directories
    memory_dir.mkdir(exist_ok=True)
    topics_dir.mkdir(exist_ok=True)
    print(f"[OK] Created: {memory_dir}")
    print(f"[OK] Created: {topics_dir}")

    # MEMORY.md template
    memory_template = f"""# MEMORY.md - Long-term Memory

> **Classification**: user(human) | feedback(guidance)->`memory/feedback.md` | project(work) | reference(resources)
> **Principle**: High-frequency info here, low-frequency details in `memory/topics/`

---

## 👤 User — <Human Name>

- **Timezone**: <timezone>
- **Preferences**: <list key preferences>

## 📍 Environment

- <OS/platform info>
- <key runtime details>

## 🔧 Reference — Connected Services

- <service 1>
- <service 2>

## 🐛 Project — Known Issues

- <issue 1>
- <issue 2>

## 📋 Project — Scheduled Tasks

- <task 1>

## 🗑️ Project — Archived

- <archived item 1>

---

*Last restructured: {datetime.now().strftime('%Y-%m-%d')}*
"""
    memory_file = ws / "MEMORY.md"
    if not memory_file.exists():
        memory_file.write_text(memory_template, encoding="utf-8")
        print(f"[OK] Created: {memory_file}")
    else:
        print(f"[SKIP] {memory_file} already exists")

    # feedback.md template
    feedback_template = """# Feedback Memory — Corrections and Guidance

> **Purpose**: Record corrections and confirmed practices from your human. Avoid repeating mistakes.
> **Format**: Rule -> **Why:** Root cause -> **How to apply:** Usage scenarios
> **Source**: Direct feedback in conversations

---

## Feedback List

<!-- Add entries like this:
### F001: Rule description (date)
- **Why**: Root cause explanation
- **How to apply**: Concrete usage scenarios
-->
"""
    feedback_file = memory_dir / "feedback.md"
    if not feedback_file.exists():
        feedback_file.write_text(feedback_template, encoding="utf-8")
        print(f"[OK] Created: {feedback_file}")
    else:
        print(f"[SKIP] {feedback_file} already exists")

    # today's daily note
    today = datetime.now().strftime("%Y-%m-%d")
    daily_template = f"""# {today} Daily Note

<!-- Log significant events, decisions, and lessons learned today. -->
"""
    daily_file = memory_dir / f"{today}.md"
    if not daily_file.exists():
        daily_file.write_text(daily_template, encoding="utf-8")
        print(f"[OK] Created: {daily_file}")

    print(f"\n[Done] Memory system initialized at: {ws}")
    print(f"\nNext steps:")
    print(f"  1. Edit {memory_file} with actual content")
    print(f"  2. Update AGENTS.md with memory rules (see references/agents-rules.md in this skill)")
    print(f"  3. Update HEARTBEAT.md with memory maintenance checklist")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <workspace-path>")
        print(f"Example: python {sys.argv[0]} ~/.openclaw/workspace")
        sys.exit(1)
    create_memory_system(sys.argv[1])
