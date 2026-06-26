"""
Utility helpers for the geo-template-library skill.

These helpers provide deterministic building blocks that subagents or tools can reuse
instead of re-implementing the same logic in every run. They are intentionally simple
and generic so they can be combined with different workflows.

Note: This module does not need to be imported by the main SKILL.md instructions, but
can be referenced from there if desired.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping


@dataclass
class Template:
    """Simple text template with placeholder substitution.

    Placeholders are defined using the pattern ``{{placeholder_name}}``.
    """

    name: str
    body: str

    def render(self, values: Mapping[str, str]) -> str:
        """Render the template with the given placeholder values.

        Any placeholder that is not present in ``values`` will be left as-is.
        """
        rendered = self.body
        for key, val in values.items():
            rendered = rendered.replace("{{" + key + "}}", str(val))
        return rendered


def build_template_from_markdown(name: str, markdown_body: str) -> Template:
    """Factory to wrap a markdown template string into a Template object."""
    return Template(name=name, body=markdown_body)


def render_with_defaults(
    template: Template, values: Mapping[str, str], defaults: Dict[str, str] | None = None
) -> str:
    """Render a template, applying default values where explicit values are missing."""
    merged: Dict[str, str] = {}
    if defaults:
        merged.update(defaults)
    merged.update(values)
    return template.render(merged)


