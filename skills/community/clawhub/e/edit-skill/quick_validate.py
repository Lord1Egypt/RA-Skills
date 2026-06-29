#!/usr/bin/env python3
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "SKILL.md"
CARD = ROOT / "skill-card.md"
OPENAI = ROOT / "agents" / "openai.yaml"

required_sections = [
    "# Edit Skill",
    "## Rules",
    "## Pass Order",
    "## Output",
    "## Anti-Patterns",
]

required_phrases = [
    "review, edit, tighten, shorten, deduplicate",
    "Preserve the skill's real job",
    "Keep frontmatter compatible",
    "Review-only",
    "Edit-in-repo",
]


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main() -> int:
    for path in [SKILL, CARD, OPENAI]:
        if not path.exists():
            return fail(f"{path.relative_to(ROOT)} is missing")

    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return fail("frontmatter opening marker is missing")

    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return fail("frontmatter closing marker is missing")

    frontmatter = match.group(1)
    if "name: edit-skill" not in frontmatter:
        return fail("frontmatter name is wrong")
    if "description:" not in frontmatter:
        return fail("frontmatter description is missing")

    unsupported = {"triggers:", "tools:", "mutating:", "version:"}
    found_unsupported = [key for key in unsupported if key in frontmatter]
    if found_unsupported:
        return fail(f"unsupported frontmatter keys present: {', '.join(found_unsupported)}")

    missing_sections = [section for section in required_sections if section not in text]
    if missing_sections:
        return fail(f"missing sections: {', '.join(missing_sections)}")

    missing_phrases = [phrase for phrase in required_phrases if phrase not in text]
    if missing_phrases:
        return fail(f"missing routing/contract phrases: {', '.join(missing_phrases)}")

    print("PASS: edit-skill package validates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
