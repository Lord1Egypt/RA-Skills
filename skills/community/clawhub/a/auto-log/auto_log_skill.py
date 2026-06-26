#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Log Skill — Daily Activity Logger for AI Agents
Automatically records AI activity to structured daily memory log files.
Author: socneo
Version: v1.0
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class AutoLogSkill:
    """Auto Log Skill — creates and manages daily activity logs for AI agents."""

    def __init__(self, config_path: str = None):
        """
        Initialize the Auto Log Skill.

        Args:
            config_path: Path to config.json (defaults to config.json in skill directory)
        """
        self.config = self.load_config(config_path)
        self.memory_dir = Path(self.config.get("memory_dir", "~/openclaw/workspace/memory")).expanduser()
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self, path: str = None) -> Dict:
        """Load configuration from JSON file, falling back to defaults."""
        if path is None:
            path = Path(__file__).parent / "config.json"

        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "memory_dir": "~/openclaw/workspace/memory",
                "auto_save": True,
                "format": "markdown",
                "sections": ["Basic Info", "Events", "Tasks", "Todos"]
            }

    def get_today_log_path(self) -> Path:
        """Return the file path for today's log."""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.memory_dir / f"{today}.md"

    def create_daily_log(self, ai_name: str = "agent") -> Path:
        """
        Create a daily log file from the template (skips if already exists).

        Args:
            ai_name: Agent name to embed in the log header

        Returns:
            Path to the log file
        """
        log_path = self.get_today_log_path()
        today = datetime.now().strftime("%Y-%m-%d")

        template = f"""# {ai_name} Daily Log — {today}

## 📅 Basic Info
- Date: {today}
- Timezone: UTC+8
- Agent: {ai_name}

## 🎯 Events
<!-- Record important events here -->

## ✅ Tasks
| Task | Status | Result |
|------|--------|--------|
| <!-- Task 1 --> | ⏳ | <!-- result --> |

## 📝 Todos
- [ ] <!-- Todo 1 -->

---
**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Author**: {ai_name}
"""

        if not log_path.exists():
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(template)

        return log_path

    def append_event(self, event: str, section: str = "Events") -> bool:
        """
        Append an event entry to the log.

        Args:
            event: Event description
            section: Target section heading

        Returns:
            True if successful
        """
        log_path = self.get_today_log_path()

        if not log_path.exists():
            self.create_daily_log()

        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()

            section_marker = f"## {section}"
            section_pos = content.find(section_marker)
            timestamp = datetime.now().strftime('%H:%M')

            if section_pos == -1:
                # Section not found — append at end
                new_content = f"\n### {section} ({timestamp})\n- {event}\n"
            else:
                new_content = f"\n- {timestamp} {event}"
                next_section_pos = content.find("\n## ", section_pos + 1)
                if next_section_pos == -1:
                    next_section_pos = len(content)

                insert_pos = content.find("\n", section_pos)
                while insert_pos < next_section_pos and content[insert_pos:insert_pos + 3] == "\n- ":
                    insert_pos = content.find("\n", insert_pos + 1)

                content = content[:insert_pos] + new_content + content[insert_pos:]
                with open(log_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True

            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(new_content)

            return True

        except Exception as e:
            print(f"Failed to append event: {e}")
            return False

    def append_task(self, task: str, status: str = "⏳", result: str = "") -> bool:
        """
        Append a task row to the Tasks table.

        Args:
            task: Task description
            status: Status emoji (⏳ / ✅ / ❌)
            result: Result description

        Returns:
            True if successful
        """
        log_path = self.get_today_log_path()

        if not log_path.exists():
            self.create_daily_log()

        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()

            section_marker = "## ✅ Tasks"
            section_pos = content.find(section_marker)

            if section_pos == -1:
                new_line = f"\n| {task} | {status} | {result} |\n"
                content = content.rstrip() + f"\n\n## ✅ Tasks\n| Task | Status | Result |\n|------|--------|--------|\n{new_line}\n"
            else:
                table_end = content.find("\n\n", section_pos)
                if table_end == -1:
                    table_end = len(content)
                new_line = f"| {task} | {status} | {result} |\n"
                content = content[:table_end] + new_line + content[table_end:]

            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True

        except Exception as e:
            print(f"Failed to append task: {e}")
            return False

    def add_todo(self, todo: str) -> bool:
        """
        Add a todo item to the Todos section.

        Args:
            todo: Todo description

        Returns:
            True if successful
        """
        log_path = self.get_today_log_path()

        if not log_path.exists():
            self.create_daily_log()

        try:
            with open(log_path, 'r+', encoding='utf-8') as f:
                content = f.read()

                section_marker = "## 📝 Todos"
                section_pos = content.find(section_marker)

                if section_pos == -1:
                    content += f"\n## 📝 Todos\n- [ ] {todo}\n"
                else:
                    new_line = f"- [ ] {todo}\n"
                    insert_pos = content.find("\n", section_pos)
                    while insert_pos < len(content) and content[insert_pos:insert_pos + 3] == "\n-":
                        insert_pos = content.find("\n", insert_pos + 1)
                    content = content[:insert_pos] + "\n" + new_line + content[insert_pos:]

                f.seek(0)
                f.write(content)

            return True

        except Exception as e:
            print(f"Failed to add todo: {e}")
            return False

    def get_summary(self) -> str:
        """
        Return a brief summary of today's log (first 500 chars).

        Returns:
            Summary string
        """
        log_path = self.get_today_log_path()

        if not log_path.exists():
            return "📝 No log created for today yet"

        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()

            summary = content[:500]
            if len(content) > 500:
                summary += "\n... (see full log for more)"

            return summary

        except Exception as e:
            return f"Failed to read log: {e}"

    def execute(self, action: str, **kwargs) -> str:
        """
        Execute a skill action via the OpenClaw tool_call interface.

        Args:
            action: One of log_event / log_task / add_todo / get_summary
            **kwargs: Action-specific parameters

        Returns:
            Result message
        """
        if action == "log_event":
            success = self.append_event(kwargs.get("event", ""), kwargs.get("section", "Events"))
            return "✅ Event logged" if success else "❌ Failed to log event"

        elif action == "log_task":
            success = self.append_task(kwargs.get("task", ""), kwargs.get("status", "⏳"), kwargs.get("result", ""))
            return "✅ Task logged" if success else "❌ Failed to log task"

        elif action == "add_todo":
            success = self.add_todo(kwargs.get("todo", ""))
            return "✅ Todo added" if success else "❌ Failed to add todo"

        elif action == "get_summary":
            return self.get_summary()

        else:
            return f"⚠️ Unknown action: {action}"


# ── Convenience functions ─────────────────────────────────────────────────

def log_event(event: str, section: str = "Events") -> bool:
    """Quick helper: log an event."""
    return AutoLogSkill().append_event(event, section)


def log_task(task: str, status: str = "⏳", result: str = "") -> bool:
    """Quick helper: log a task."""
    return AutoLogSkill().append_task(task, status, result)


def add_todo(todo: str) -> bool:
    """Quick helper: add a todo."""
    return AutoLogSkill().add_todo(todo)


def get_today_summary() -> str:
    """Quick helper: get today's summary."""
    return AutoLogSkill().get_summary()


# ── CLI entry point ───────────────────────────────────────────────────────

if __name__ == "__main__":
    skill = AutoLogSkill()

    if len(sys.argv) > 1:
        action = sys.argv[1]

        if action == "event" and len(sys.argv) > 2:
            event = " ".join(sys.argv[2:])
            print(skill.execute("log_event", event=event))

        elif action == "summary":
            print(skill.get_summary())

        else:
            print(f"Usage: python auto_log_skill.py <action> [args]")
            print("Actions: event, task, todo, summary")
    else:
        # Default: create today's log
        log_path = skill.create_daily_log("auto")
        print(f"✅ Today's log created: {log_path}")
