#!/usr/bin/env python3
"""
Persister - Write facts to appropriate memory files with verification.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List

# SECTION MAP for WARM_MEMORY.md
SECTION_MAP = {
    "person": "### 👥 家庭成员/重要人物",
    "time": "### 🗓️ 日程安排",
    "location": "### 📍 地理位置",
    "preference": "### 💬 互动偏好",
    "system": "### 🔧 系统规则",
    "general": "### 📝 其他信息"
}


def append_to_warm_memory(fact: Dict, verify: bool = True) -> None:
    """Append a fact to WARM_MEMORY.md under the appropriate section."""
    path = Path("/home/admin/.openclaw/workspace/memory/warm/WARM_MEMORY.md")
    if not path.exists():
        return

    content = fact["content"]
    category = fact.get("category", "general")
    section = SECTION_MAP.get(category, SECTION_MAP["general"])

    entry = f"\n- [{datetime.now().date()}] {content}"

    # Read current content
    with open(path, "r", encoding="utf-8") as f:
        existing = f.read()

    # Simple append (could be smarter to insert under section)
    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)
        f.flush()

    if verify:
        # Verify write
        with open(path, "r", encoding="utf-8") as f:
            new_content = f.read()
        assert content in new_content, f"Failed to verify write: {content}"


def append_to_memory(fact: Dict, verify: bool = True) -> None:
    """Append to COLD MEMORY.md."""
    path = Path("/home/admin/.openclaw/workspace/MEMORY.md")
    if not path.exists():
        return

    entry = f"\n- [{datetime.now().date()}] {fact['content']}"

    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)
        f.flush()

    if verify:
        with open(path, "r", encoding="utf-8") as f:
            assert fact["content"] in f.read()


def update_user_md(fact: Dict, verify: bool = True) -> None:
    """Update USER.md with new info."""
    path = Path("/home/admin/.openclaw/workspace/USER.md")
    if not path.exists():
        return

    entry = f"\n- **更新 [{datetime.now().date()}]**: {fact['content']}"

    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)
        f.flush()

    if verify:
        with open(path, "r", encoding="utf-8") as f:
            assert fact["content"] in f.read()


def append_to_tools(fact: Dict, verify: bool = True) -> None:
    """Append system rule to TOOLS.md."""
    path = Path("/home/admin/.openclaw/workspace/TOOLS.md")
    if not path.exists():
        return

    entry = f"\n> **[{datetime.now().date()}]** {fact['content']}"

    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)
        f.flush()

    if verify:
        with open(path, "r", encoding="utf-8") as f:
            assert fact["content"] in f.read()


def update_ontology(fact: Dict) -> None:
    """Update ontology with person detail (placeholder)."""
    # TODO: Implement ontology update via bitable API or local file
    pass


def persist_facts(facts: List[Dict], config: Dict) -> None:
    """Route facts to their target files."""
    for fact in facts:
        targets = fact.get("targets", ["memory_md"])
        for target in targets:
            if target == "ontology":
                update_ontology(fact)
            elif target == "warm_memory":
                append_to_warm_memory(fact, verify=config["persistence"]["verify_after_write"])
            elif target == "user_md":
                update_user_md(fact, verify=config["persistence"]["verify_after_write"])
            elif target == "memory_md":
                append_to_memory(fact, verify=config["persistence"]["verify_after_write"])
            elif target == "tools_md":
                append_to_tools(fact, verify=config["persistence"]["verify_after_write"])
