"""
Export Bilibili digest results in various formats:
- Markdown (default)
- Obsidian (WikiLinks + YAML frontmatter)
- JSON
- Notion API (placeholder)
- Feishu API (placeholder)
"""
import json
import os
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def export_markdown(result: Dict, output_dir: str, filename: Optional[str] = None) -> str:
    """
    Export a single video result as a Markdown file.
    
    Args:
        result: The video result dict from processing.
        output_dir: Directory to write the file to.
        filename: Optional filename (derived from title if not provided).
        
    Returns:
        Path to the written file.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    metadata = result.get("metadata", {})
    content = result.get("content", {})
    
    title = metadata.get("title", "Untitled")
    safe_title = _sanitize_filename(title)
    
    if not filename:
        filename = f"{safe_title}.md"
    elif not filename.endswith(".md"):
        filename += ".md"
    
    filepath = os.path.join(output_dir, filename)
    
    # Build YAML frontmatter
    yaml = [
        "---",
        f'title: "{title}"',
        f"author: {metadata.get('author', '')}",
        f"url: {result.get('url', '')}",
        f"source: bilibili",
        f"date: {datetime.now().strftime('%Y-%m-%d')}",
        "---",
        "",
    ]
    
    body_lines = []
    
    # Title
    body_lines.append(f"# {title}")
    body_lines.append("")
    
    # Metadata line
    duration = metadata.get("duration_seconds", 0)
    duration_str = f"{duration // 60:02d}:{duration % 60:02d}" if duration else "N/A"
    body_lines.append(f"> **{metadata.get('author', '')}** | ⏱ {duration_str} | 👁 {metadata.get('view_count', 'N/A')}")
    body_lines.append(f"> [🔗 Original Video]({result.get('url', '')})")
    body_lines.append("")
    
    # One-liner
    one_liner = content.get("summary_one_liner", "")
    if one_liner:
        body_lines.append("## 📌 One-Liner")
        body_lines.append(one_liner)
        body_lines.append("")
    
    # Overview
    overview = content.get("summary_overview", "")
    if overview:
        body_lines.append("## 📝 Overview")
        body_lines.append(overview)
        body_lines.append("")
    
    # Key Points
    key_points = content.get("key_points", [])
    if key_points:
        body_lines.append("## 📊 Key Points")
        body_lines.append("")
        for kp in key_points:
            ts = kp.get("timestamp", "")
            point = kp.get("point", kp.get("content", ""))
            if ts:
                body_lines.append(f"- **[{ts}]** {point}")
            else:
                body_lines.append(f"- {point}")
        body_lines.append("")
    
    # Chapters
    chapters = content.get("chapters", [])
    if chapters:
        body_lines.append("## 📑 Chapters")
        body_lines.append("")
        for ch in chapters:
            start_s = ch.get("start_seconds", 0)
            ts = f"{int(start_s // 60):02d}:{int(start_s % 60):02d}"
            title_ch = ch.get("title", "Untitled")
            summary_ch = ch.get("summary", "")
            body_lines.append(f"- **{title_ch}** `{ts}`")
            if summary_ch:
                body_lines.append(f"  - {summary_ch}")
        body_lines.append("")
    
    # Action Steps
    action_steps = content.get("action_steps", [])
    if action_steps:
        body_lines.append("## 🔧 Action Steps")
        body_lines.append("")
        for step in action_steps:
            body_lines.append(f"- [ ] {step}")
        body_lines.append("")
    
    # Resources
    resources = content.get("resources", [])
    if resources:
        body_lines.append("## 📚 Resources")
        body_lines.append("")
        for r in resources:
            r_name = r.get("name", "")
            r_url = r.get("url", "")
            if r_name and r_url:
                body_lines.append(f"- [{r_name}]({r_url})")
            elif r_url:
                body_lines.append(f"- {r_url}")
        body_lines.append("")
    
    # Attribution (copyright notice)
    body_lines.append("---")
    body_lines.append(f"*Content source: [{title}]({result.get('url', '')}) by {metadata.get('author', '')}*")
    body_lines.append("")
    
    full_content = "\n".join(yaml + body_lines)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_content)
    
    logger.info("Exported Markdown to %s", filepath)
    return filepath


def export_obsidian(result: Dict, output_dir: str) -> str:
    """
    Export as Obsidian-compatible note (WikiLinks + tags).
    """
    os.makedirs(output_dir, exist_ok=True)
    
    metadata = result.get("metadata", {})
    content = result.get("content", {})
    title = metadata.get("title", "Untitled")
    safe_title = _sanitize_filename(title)
    
    filepath = os.path.join(output_dir, f"{safe_title}.md")
    
    # Obsidian frontmatter
    lines = [
        "---",
        f'title: "{title}"',
        f"author: \"[[{metadata.get('author', '')}]]\"",
        f"url: {result.get('url', '')}",
        "tags: [bilibili/digest]",
        f"created: {datetime.now().strftime('%Y-%m-%d')}",
        "---",
        "",
    ]
    
    # Body - uses WikiLinks
    one_liner = content.get("summary_one_liner", "")
    if one_liner:
        lines.append(f"**{one_liner}**")
        lines.append("")
    
    key_points = content.get("key_points", [])
    if key_points:
        lines.append("## Key Points")
        for kp in key_points:
            ts = kp.get("timestamp", "")
            point = kp.get("point", kp.get("content", ""))
            if ts:
                lines.append(f"- `{ts}` {point}")
            else:
                lines.append(f"- {point}")
        lines.append("")
    
    lines.append(f"---\nSource: [{title}]({result.get('url', '')}) by [[{metadata.get('author', '')}]]")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    
    return filepath


def export_json(result: Dict, output_dir: str) -> str:
    """
    Export as raw JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)
    metadata = result.get("metadata", {})
    title = metadata.get("title", "Untitled")
    safe_title = _sanitize_filename(title)
    
    filepath = os.path.join(output_dir, f"{safe_title}.json")
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return filepath


def export_notion(result: Dict, api_key: str, database_id: str) -> Dict:
    """
    Export to Notion (placeholder - requires notion client library).
    
    Returns dict with status.
    """
    logger.warning("Notion export requires 'notion-client' package and API configuration")
    return {"status": "not_configured", "message": "Notion API not configured"}


def export_feishu( result: Dict, app_id: str, app_secret: str) -> Dict:
    """
    Export to Feishu document (placeholder).
    
    Returns dict with status.
    """
    logger.warning("Feishu export requires feishu API configuration")
    return {"status": "not_configured", "message": "Feishu API not configured"}


def _sanitize_filename(name: str) -> str:
    """Remove characters that are problematic in filenames."""
    # Keep Chinese characters, alphanumeric, spaces, hyphens, underscores
    import re
    sanitized = re.sub(r'[<>:"/\\|?*]', '', name)
    sanitized = sanitized.strip()
    # Truncate if too long
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    return sanitized or "untitled"


def export_batch(results: list, output_dir: str, export_format: str = "markdown") -> dict:
    """
    Export multiple video results.
    
    Args:
        results: List of video result dicts.
        output_dir: Base output directory.
        export_format: One of "markdown", "obsidian", "json".
        
    Returns:
        Dict with export paths and stats.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    export_paths = []
    failed = []
    
    for result in results:
        try:
            if export_format == "obsidian":
                path = export_obsidian(result, output_dir)
            elif export_format == "json":
                path = export_json(result, output_dir)
            else:
                path = export_markdown(result, output_dir)
            export_paths.append(path)
        except (OSError, IOError) as e:
            failed.append({"url": result.get("url", ""), "error": str(e)})
            logger.error("Export failed for %s: %s", result.get("url", ""), e)
    
    return {
        "exported": len(export_paths),
        "failed": len(failed),
        "paths": export_paths,
        "error_details": failed,
    }
