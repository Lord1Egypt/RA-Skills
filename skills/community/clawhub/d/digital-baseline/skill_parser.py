"""
OpenClaw skill.md file parser

Parses OpenClaw-format skill.md files, extracting YAML frontmatter
agent metadata (name, description, capabilities, version, author, etc.).

skill.md format example::

    ---
    name: my-agent
    description: An intelligent assistant
    capabilities:
      - summarization
      - translation
    version: 1.0.0
    author: "@twitterhandle"
    ---

    # My Agent

    Detailed agent description...
"""

from __future__ import annotations

import re
from typing import Any

# Try to import PyYAML; fall back to simple parser if unavailable
try:
    import yaml

    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False


def parse_skill_md(path: str) -> dict[str, Any]:
    """Parse OpenClaw skill.md file

    Extracts YAML frontmatter from file and returns structured dict.
    Missing fields are filled with sensible defaults.

    Args:
        path: Path to skill.md file

    Returns:
        Dict with fields:
        - name (str): Agent name
        - description (str): Agent description
        - capabilities (list[str]): Capability tag list
        - version (str): Version number
        - author (str): Author identifier
        - body (str): Markdown body after frontmatter

    Raises:
        FileNotFoundError: When file does not exist
        ValueError: When no valid YAML frontmatter found
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return parse_skill_md_content(content)


def parse_skill_md_content(content: str) -> dict[str, Any]:
    """Parse skill.md text content (no file read)

    Same as parse_skill_md but accepts string input instead of file path,
    for use when filesystem access is unavailable.

    Args:
        content: Full text content of skill.md

    Returns:
        Structured dict, fields same as parse_skill_md

    Raises:
        ValueError: When no valid YAML frontmatter found in text
    """
    # Match YAML frontmatter block: starts and ends with ---
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)", content, re.DOTALL)
    if not match:
        raise ValueError(
            "No valid YAML frontmatter found. "
            "skill.md should start with ---, end the frontmatter block with ---."
        )

    frontmatter_raw = match.group(1)
    body = match.group(2).strip()

    # Parse YAML frontmatter
    if _HAS_YAML:
        frontmatter = yaml.safe_load(frontmatter_raw) or {}
    else:
        frontmatter = _simple_yaml_parse(frontmatter_raw)

    # Extract fields, use defaults when missing
    result: dict[str, Any] = {
        "name": str(frontmatter.get("name", "unnamed-agent")),
        "description": str(frontmatter.get("description", "")),
        "capabilities": _ensure_list(frontmatter.get("capabilities", [])),
        "version": str(frontmatter.get("version", "0.1.0")),
        "author": str(frontmatter.get("author", "")),
        "body": body,
    }

    return result


def _ensure_list(value: Any) -> list[str]:
    """Ensure value is a list of strings

    Args:
        value: Arbitrary input value

    Returns:
        List of strings
    """
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        # Support comma-separated string format
        return [item.strip() for item in value.split(",") if item.strip()]
    return []


def _simple_yaml_parse(raw: str) -> dict[str, Any]:
    """Simple YAML parser (fallback when PyYAML is unavailable)

    Supports basic key: value pairs and YAML lists (- item).
    Does NOT support nested structures, anchors, references,
    or other advanced YAML features.

    Args:
        raw: YAML text

    Returns:
        Parsed dictionary
    """
    result: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[str] | None = None

    for line in raw.splitlines():
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith("#"):
            # If collecting a list, empty line ends it
            if current_key and current_list is not None:
                result[current_key] = current_list
                current_key = None
                current_list = None
            continue

        # Check for list item (- item)
        if stripped.startswith("- ") and current_key is not None:
            if current_list is None:
                current_list = []
            current_list.append(stripped[2:].strip().strip('"').strip("'"))
            continue

        # If previously collecting a list, save it
        if current_key and current_list is not None:
            result[current_key] = current_list
            current_list = None
            current_key = None

        # Check for key: value pair
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if value:
                result[key] = value
            else:
                # Empty value, may be followed by a list
                current_key = key
                current_list = []

    # Handle trailing unclosed list
    if current_key and current_list is not None:
        result[current_key] = current_list

    return result
