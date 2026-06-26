#!/usr/bin/env python3
"""Canvas HTML-to-markdown converter and content formatters for RAG indexing.

Converts Canvas API responses into clean, RAG-optimized markdown files
following the existing memory/ naming conventions.

Usage as library:
    from canvas_content import html_to_markdown, format_page_markdown
    md = html_to_markdown(page["body"], base_url="https://your-canvas-instance.instructure.com")
    full_md = format_page_markdown(page, "ai-essentials-spring2026")
"""

import re
from datetime import datetime
from typing import Optional
from bs4 import BeautifulSoup, NavigableString, Tag


# ---------------------------------------------------------------------------
# HTML to Markdown conversion
# ---------------------------------------------------------------------------

def html_to_markdown(html: str, base_url: str = None) -> str:
    """Convert Canvas HTML to clean markdown.

    Handles standard HTML elements and strips Canvas-specific cruft
    (CSS classes, iframe embeds, LTI tool links, media_comment elements).
    """
    if not html or not html.strip():
        return ""

    soup = BeautifulSoup(html, "html.parser")

    # Remove Canvas-specific elements
    for tag in soup.find_all(["iframe", "script", "style"]):
        tag.decompose()
    for tag in soup.find_all(class_=re.compile(r"media_comment|lti-|instructure_")):
        tag.decompose()
    for tag in soup.find_all("a", class_="instructure_file_link"):
        # Keep the link text, just convert normally
        pass

    result = _convert_element(soup, base_url)

    # Clean up whitespace
    result = re.sub(r"\n{3,}", "\n\n", result)
    result = re.sub(r"[ \t]+\n", "\n", result)
    result = result.strip()

    return result


def _convert_element(element, base_url: str = None) -> str:
    """Recursively convert an HTML element to markdown."""
    if isinstance(element, NavigableString):
        text = str(element)
        # Collapse internal whitespace but preserve newlines
        text = re.sub(r"[ \t]+", " ", text)
        return text

    if not isinstance(element, Tag):
        return ""

    tag = element.name
    children_md = "".join(_convert_element(c, base_url) for c in element.children)
    children_md_stripped = children_md.strip()

    # Skip empty elements
    if not children_md_stripped and tag not in ("br", "hr", "img"):
        return ""

    # Headings
    if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
        level = int(tag[1])
        # Bump all headings down by one since we use h1 for the file title
        level = min(level + 1, 6)
        return f"\n\n{'#' * level} {children_md_stripped}\n\n"

    # Paragraphs
    if tag == "p":
        return f"\n\n{children_md_stripped}\n\n"

    # Line breaks
    if tag == "br":
        return "\n"

    # Horizontal rules
    if tag == "hr":
        return "\n\n---\n\n"

    # Bold
    if tag in ("strong", "b"):
        return f"**{children_md_stripped}**"

    # Italic
    if tag in ("em", "i"):
        return f"*{children_md_stripped}*"

    # Code (inline)
    if tag == "code":
        return f"`{children_md_stripped}`"

    # Code blocks
    if tag == "pre":
        code = element.find("code")
        if code:
            return f"\n\n```\n{code.get_text()}\n```\n\n"
        return f"\n\n```\n{element.get_text()}\n```\n\n"

    # Blockquotes
    if tag == "blockquote":
        lines = children_md_stripped.split("\n")
        quoted = "\n".join(f"> {line}" for line in lines)
        return f"\n\n{quoted}\n\n"

    # Links
    if tag == "a":
        href = element.get("href", "")
        if base_url and href.startswith("/"):
            href = base_url.rstrip("/") + href
        if children_md_stripped:
            return f"[{children_md_stripped}]({href})"
        return href

    # Images
    if tag == "img":
        src = element.get("src", "")
        alt = element.get("alt", "image")
        if base_url and src.startswith("/"):
            src = base_url.rstrip("/") + src
        return f"![{alt}]({src})"

    # Unordered lists
    if tag == "ul":
        items = []
        for li in element.find_all("li", recursive=False):
            li_md = _convert_element(li, base_url).strip()
            # Handle nested lists — indent continuation lines
            lines = li_md.split("\n")
            items.append(f"- {lines[0]}")
            for line in lines[1:]:
                if line.strip():
                    items.append(f"  {line}")
        return "\n\n" + "\n".join(items) + "\n\n"

    # Ordered lists
    if tag == "ol":
        items = []
        start = int(element.get("start", 1))
        for i, li in enumerate(element.find_all("li", recursive=False)):
            li_md = _convert_element(li, base_url).strip()
            lines = li_md.split("\n")
            items.append(f"{start + i}. {lines[0]}")
            for line in lines[1:]:
                if line.strip():
                    items.append(f"   {line}")
        return "\n\n" + "\n".join(items) + "\n\n"

    # List items (handled by parent ul/ol, but in case they appear standalone)
    if tag == "li":
        return children_md_stripped

    # Tables
    if tag == "table":
        return _convert_table(element, base_url)

    # Table sub-elements (handled by _convert_table)
    if tag in ("thead", "tbody", "tfoot", "tr", "th", "td", "caption"):
        return children_md

    # Div, span, section — just pass through children
    if tag in ("div", "span", "section", "article", "header", "footer",
               "main", "nav", "figure", "figcaption", "details", "summary"):
        return children_md

    # Default: pass through children
    return children_md


def _convert_table(table: Tag, base_url: str = None) -> str:
    """Convert an HTML table to markdown table."""
    rows = []
    for tr in table.find_all("tr"):
        cells = []
        for cell in tr.find_all(["th", "td"]):
            cell_md = _convert_element(cell, base_url).strip()
            # Remove newlines within cells
            cell_md = re.sub(r"\n+", " ", cell_md)
            cells.append(cell_md)
        if cells:
            rows.append(cells)

    if not rows:
        return ""

    # Normalize column count
    max_cols = max(len(r) for r in rows)
    for r in rows:
        while len(r) < max_cols:
            r.append("")

    # Build markdown table
    lines = []
    # Header row
    lines.append("| " + " | ".join(rows[0]) + " |")
    lines.append("| " + " | ".join("---" for _ in rows[0]) + " |")
    # Data rows
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")

    return "\n\n" + "\n".join(lines) + "\n\n"


# ---------------------------------------------------------------------------
# Content formatters — produce RAG-optimized markdown with frontmatter
# ---------------------------------------------------------------------------

def _slugify(text: str) -> str:
    """Convert text to a filename-safe slug."""
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")[:80]


def _format_date(iso_str: Optional[str]) -> str:
    """Format ISO date string to human-readable."""
    if not iso_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except (ValueError, TypeError):
        return iso_str


def format_page_markdown(page_data: dict, course_slug: str,
                         base_url: str = None) -> str:
    """Format a Canvas page API response into a RAG-optimized markdown file."""
    title = page_data.get("title", "Untitled Page")
    updated = _format_date(page_data.get("updated_at"))
    body_html = page_data.get("body", "")
    body_md = html_to_markdown(body_html, base_url)

    return f"""# {title}
> **Course:** {course_slug}
> **Type:** Canvas Page
> **Last Updated:** {updated}
> **URL:** {page_data.get('html_url', 'N/A')}

{body_md}
"""


def format_assignment_markdown(assignment: dict, course_slug: str,
                               base_url: str = None) -> str:
    """Format assignment for RAG indexing."""
    name = assignment.get("name", "Untitled Assignment")
    due = _format_date(assignment.get("due_at"))
    pts = assignment.get("points_possible", "N/A")
    sub_types = ", ".join(assignment.get("submission_types", []))
    desc_html = assignment.get("description", "") or ""
    desc_md = html_to_markdown(desc_html, base_url)

    lock_at = _format_date(assignment.get("lock_at"))
    unlock_at = _format_date(assignment.get("unlock_at"))

    meta = f"""# {name}
> **Course:** {course_slug}
> **Type:** Canvas Assignment
> **Due Date:** {due}
> **Points:** {pts}
> **Submission Types:** {sub_types}
> **Available:** {unlock_at} to {lock_at}
> **URL:** {assignment.get('html_url', 'N/A')}
"""

    if assignment.get("allowed_extensions"):
        meta += f"> **Allowed Extensions:** {', '.join(assignment['allowed_extensions'])}\n"

    if assignment.get("group_category_id"):
        meta += "> **Group Assignment:** Yes\n"

    meta += f"\n{desc_md}\n"
    return meta


def format_announcement_markdown(announcement: dict, course_slug: str,
                                 base_url: str = None) -> str:
    """Format announcement for RAG indexing."""
    title = announcement.get("title", "Untitled Announcement")
    posted = _format_date(announcement.get("posted_at"))
    author = announcement.get("user_name", announcement.get("author", {}).get("display_name", "Unknown"))
    body_html = announcement.get("message", "") or ""
    body_md = html_to_markdown(body_html, base_url)

    return f"""# {title}
> **Course:** {course_slug}
> **Type:** Canvas Announcement
> **Posted:** {posted}
> **Author:** {author}
> **URL:** {announcement.get('html_url', 'N/A')}

{body_md}
"""


def format_discussion_markdown(topic: dict, replies: list,
                               course_slug: str, base_url: str = None) -> str:
    """Format discussion topic with top replies for RAG indexing."""
    title = topic.get("title", "Untitled Discussion")
    posted = _format_date(topic.get("posted_at"))
    body_html = topic.get("message", "") or ""
    body_md = html_to_markdown(body_html, base_url)
    reply_count = topic.get("discussion_subentry_count", 0)

    result = f"""# {title}
> **Course:** {course_slug}
> **Type:** Canvas Discussion
> **Posted:** {posted}
> **Replies:** {reply_count}
> **URL:** {topic.get('html_url', 'N/A')}

{body_md}
"""

    if replies:
        result += "\n## Replies\n\n"
        for reply in replies[:20]:  # Cap at 20 replies
            author = reply.get("user_name", "Anonymous")
            msg = html_to_markdown(reply.get("message", ""), base_url)
            created = _format_date(reply.get("created_at"))
            result += f"**{author}** ({created}):\n{msg}\n\n---\n\n"

    return result


def format_quiz_markdown(quiz: dict, course_slug: str) -> str:
    """Format quiz metadata for RAG (no questions for academic integrity)."""
    title = quiz.get("title", "Untitled Quiz")
    due = _format_date(quiz.get("due_at"))
    pts = quiz.get("points_possible", "N/A")
    time_limit = quiz.get("time_limit")
    attempts = quiz.get("allowed_attempts", -1)
    q_count = quiz.get("question_count", "?")
    quiz_type = quiz.get("quiz_type", "?")

    time_str = f"{time_limit} minutes" if time_limit else "Unlimited"
    attempts_str = "Unlimited" if attempts == -1 else str(attempts)

    desc_html = quiz.get("description", "") or ""
    desc_md = html_to_markdown(desc_html) if desc_html else ""

    return f"""# {title}
> **Course:** {course_slug}
> **Type:** Canvas Quiz ({quiz_type})
> **Due Date:** {due}
> **Points:** {pts}
> **Questions:** {q_count}
> **Time Limit:** {time_str}
> **Allowed Attempts:** {attempts_str}
> **URL:** {quiz.get('html_url', 'N/A')}

{desc_md}
"""


def format_module_summary_markdown(modules: list, course_slug: str) -> str:
    """Format all modules as a course table of contents."""
    result = f"""# Course Modules — Table of Contents
> **Course:** {course_slug}
> **Type:** Canvas Module Structure
> **Modules:** {len(modules)}

"""
    for m in modules:
        pos = m.get("position", "?")
        name = m.get("name", "Untitled Module")
        items = m.get("items", [])
        result += f"## Module {pos}: {name}\n\n"

        if not items:
            result += "*No items*\n\n"
            continue

        for item in items:
            item_type = item.get("type", "?")
            item_title = item.get("title", "?")
            indent = ""
            if item.get("indent", 0) > 0:
                indent = "  " * item["indent"]

            type_icon = {
                "Assignment": "[Assignment]",
                "Quiz": "[Quiz]",
                "Discussion": "[Discussion]",
                "File": "[File]",
                "Page": "[Page]",
                "ExternalUrl": "[Link]",
                "ExternalTool": "[Tool]",
                "SubHeader": "**",
            }.get(item_type, f"[{item_type}]")

            if item_type == "SubHeader":
                result += f"{indent}- **{item_title}**\n"
            else:
                result += f"{indent}- {type_icon} {item_title}\n"

        result += "\n"

    return result


def format_syllabus_markdown(course_data: dict, course_slug: str,
                             base_url: str = None) -> str:
    """Format course syllabus body."""
    name = course_data.get("name", "Course")
    body_html = course_data.get("syllabus_body", "") or ""
    body_md = html_to_markdown(body_html, base_url)

    return f"""# Syllabus — {name}
> **Course:** {course_slug}
> **Type:** Canvas Syllabus

{body_md}
"""


def format_file_index_markdown(files: list, course_slug: str) -> str:
    """Format a file index for RAG (lists all files with metadata)."""
    result = f"""# Course Files Index
> **Course:** {course_slug}
> **Type:** Canvas File Index
> **Total Files:** {len(files)}

"""
    # Group by folder
    by_folder = {}
    for f in files:
        folder = f.get("folder_id", "root")
        by_folder.setdefault(folder, []).append(f)

    for folder_id, folder_files in by_folder.items():
        for f in sorted(folder_files, key=lambda x: x.get("display_name", "")):
            name = f.get("display_name", "?")
            size_mb = f.get("size", 0) / (1024 * 1024)
            updated = _format_date(f.get("updated_at"))
            result += f"- **{name}** ({size_mb:.1f} MB) — updated {updated}\n"

    return result


# ---------------------------------------------------------------------------
# Utility: memory file naming
# ---------------------------------------------------------------------------

def memory_filename(course_slug: str, content_type: str, name: str) -> str:
    """Generate a memory-compatible filename.

    Examples:
        memory_filename("ai-essentials-spring2026", "canvas-page", "homepage")
        -> "ai-essentials-spring2026__canvas-page__homepage.md"
    """
    safe_name = _slugify(name)
    return f"{course_slug}__{content_type}__{safe_name}.md"
