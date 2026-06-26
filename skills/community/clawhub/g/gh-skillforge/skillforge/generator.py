"""
SKILL.md generator.

Produces valid ClawHub-compatible SKILL.md files with proper
YAML frontmatter and Markdown body.
"""

import re

import yaml

_SLUG_CLEAN_RE = re.compile(r"[^a-z0-9-]")
_MULTI_DASH_RE = re.compile(r"-{2,}")


def to_slug(name: str) -> str:
    """Convert a name to a ClawHub-compatible slug.

    Rules: ^[a-z0-9][a-z0-9-]*$
    """
    slug = name.lower().strip()
    slug = slug.replace(" ", "-")
    slug = _SLUG_CLEAN_RE.sub("", slug)
    slug = _MULTI_DASH_RE.sub("-", slug)
    slug = slug.strip("-")
    if not slug:
        slug = "unnamed-skill"
    return slug


def generate_skill_md(
    name: str,
    description: str,
    instructions: str,
    version: str = "1.0.0",
    env_vars: list[str] | None = None,
    bins: list[str] | None = None,
) -> str:
    """Generate a valid SKILL.md string."""
    slug = to_slug(name)

    frontmatter: dict = {
        "name": slug,
        "description": description,
        "version": version,
    }

    if env_vars or bins:
        requires: dict = {}
        if env_vars:
            requires["env"] = env_vars
        if bins:
            requires["bins"] = bins
        frontmatter["metadata"] = {"openclaw": {"requires": requires}}

    fm_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)

    body = f"# {name}\n\n{description}\n\n{instructions}\n"

    return f"---\n{fm_str}---\n{body}"
