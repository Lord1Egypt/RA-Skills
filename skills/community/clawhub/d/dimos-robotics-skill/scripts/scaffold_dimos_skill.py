#!/usr/bin/env python3
"""Scaffold a DimOS skill-container file.

Example:
    python scripts/scaffold_dimos_skill.py \
      --class-name RoomReporterSkill \
      --skill-name report_room_status \
      --out room_reporter_skill.py
"""

from __future__ import annotations

import argparse
import keyword
import re
from pathlib import Path

_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(value: str, label: str) -> str:
    if not _IDENTIFIER.match(value) or keyword.iskeyword(value):
        raise argparse.ArgumentTypeError(f"{label} must be a valid Python identifier: {value!r}")
    return value


def _snake_to_module_var(class_name: str) -> str:
    chars: list[str] = []
    for i, char in enumerate(class_name):
        if char.isupper() and i > 0 and (not class_name[i - 1].isupper()):
            chars.append("_")
        chars.append(char.lower())
    name = "".join(chars)
    if name.endswith("_skill"):
        return name
    return f"{name}_blueprint"


def render_template(class_name: str, skill_name: str) -> str:
    module_var = _snake_to_module_var(class_name)
    return f'''"""Generated DimOS skill container.

Add real logic inside `{skill_name}` and include `{class_name}.blueprint()` in
an MCP-enabled blueprint. Test in replay or simulation before real hardware.
"""

from __future__ import annotations

from dimos.agents.annotation import skill
from dimos.core.core import rpc
from dimos.core.module import Module


class {class_name}(Module):
    """Agent-callable DimOS skill container."""

    @rpc
    def start(self) -> None:
        super().start()

    @rpc
    def stop(self) -> None:
        super().stop()

    @skill
    def {skill_name}(self, dry_run: bool = True) -> str:
        """Run the {skill_name.replace('_', ' ')} skill.

        Args:
            dry_run: When true, describe what would happen without acting.
        """
        if dry_run:
            return "Dry run only: {skill_name} is wired and ready."

        # TODO: Add bounded, testable robot logic here.
        # Keep physical actions conservative and return a factual status string.
        return "{skill_name} completed."


{module_var} = {class_name}.blueprint()
'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--class-name", required=True, type=lambda x: _validate_identifier(x, "class-name"))
    parser.add_argument("--skill-name", required=True, type=lambda x: _validate_identifier(x, "skill-name"))
    parser.add_argument("--out", required=True, type=Path, help="Output Python file path")
    args = parser.parse_args()

    text = render_template(args.class_name, args.skill_name)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
