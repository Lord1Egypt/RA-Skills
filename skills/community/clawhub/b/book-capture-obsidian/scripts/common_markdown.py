"""Make untrusted text safe to place in Obsidian Markdown."""

from __future__ import annotations


def inert_markdown(text: str) -> str:
    # External text must not open code spans or fences: with Dataview JS
    # enabled, `$= ...` and dataviewjs blocks would run inside the vault.
    # Backslashes go first, or an existing "\`" would turn the escape back off.
    return text.replace("\\", "\\\\").replace("`", "\\`").replace("~", "\\~")


def inert_table_cell(text: str) -> str:
    return inert_markdown(text).replace("|", "\\|").replace("\n", " ")
