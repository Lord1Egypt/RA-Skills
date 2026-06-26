"""Prompt-only OpenClaw skill handler.

This skill intentionally does not read local skill directories, inspect wallets,
or access the filesystem. The published SKILL.md carries the actual guidance.
"""


def handle(args):
    args = args or {}
    return {
        "result": "done",
        "mode": str(args.get("mode", "guide")),
        "input": str(args.get("input", "")),
        "note": "Prompt-only skill; no local file, wallet, or account inspection is performed.",
    }
