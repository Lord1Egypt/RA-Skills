from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


MARKDOWN_EXTENSIONS = (".md", ".mdx")
TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{1,63}")


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def docs_root() -> Path:
    return skill_root() / "openclaw_docs"


def state_root() -> Path:
    return skill_root() / "state"


def references_root() -> Path:
    return skill_root() / "references"


def root_docs_json() -> Path:
    return skill_root() / "docs.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_markdown_files(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in MARKDOWN_EXTENSIONS:
            yield path


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def extract_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in strip_frontmatter(text).splitlines():
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if heading:
                headings.append(heading)
    return headings


def extract_summary(text: str) -> str:
    for line in strip_frontmatter(text).splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith(">"):
            stripped = stripped.lstrip("> ").strip()
        if stripped:
            return stripped[:240]
    return ""


def tokenize(*parts: str) -> list[str]:
    tokens: set[str] = set()
    for part in parts:
        for token in TOKEN_RE.findall(part.lower()):
            if not any(ch.isalpha() for ch in token):
                continue
            tokens.add(token)
            for piece in re.split(r"[-_/.:]", token):
                if len(piece) >= 3 and any(ch.isalpha() for ch in piece):
                    tokens.add(piece)
    return sorted(tokens)


def flatten_pages(node: Any) -> list[str]:
    pages: list[str] = []
    if isinstance(node, str):
        pages.append(node)
        return pages
    if isinstance(node, list):
        for item in node:
            pages.extend(flatten_pages(item))
        return pages
    if isinstance(node, dict):
        for key in ("pages", "groups", "tabs", "navigation", "languages"):
            if key in node:
                pages.extend(flatten_pages(node[key]))
        return pages
    return pages


def resolve_page_path(page: str) -> str:
    candidate = page.lstrip("/").replace("\\", "/")
    if candidate.endswith(MARKDOWN_EXTENSIONS):
        return candidate
    return f"{candidate}.md"
