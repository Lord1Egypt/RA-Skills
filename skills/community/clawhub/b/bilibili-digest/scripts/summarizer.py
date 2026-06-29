"""
AI Summary Generator for Bilibili content.
Calls LLM (DeepSeek) to generate structured summaries, key points,
resources, action steps, and multi-mode outputs.
Supports fallback when LLM is unavailable.
"""
import json
import logging
from typing import Dict, List, Optional, Any
import os

logger = logging.getLogger(__name__)


def _call_llm(prompt: str, system_prompt: str = "",
              temperature: float = 0.3, max_tokens: int = 4096) -> Optional[str]:
    """
    Call the LLM (DeepSeek) for text generation.
    
    In production, this calls the configured model API.
    For skill context, it returns None to signal the caller to use fallback logic.
    """
    # This function is a hook for the agent runtime to inject the LLM call.
    # The actual invocation is handled by OpenClaw's model pipeline.
    # When used as a skill, model_id defaults to deepseek/deepseek-v4-flash.
    logger.debug("LLM call requested (handled by agent runtime)")
    return None


def generate_summary_prompt(
    title: str,
    author: str,
    description: str,
    transcript_preview: str,
    chapters: List[Dict],
    summary_mode: str = "detailed",
    language: str = "zh-CN",
) -> str:
    """
    Build the LLM prompt for video summary generation.
    
    Args:
        title: Video title.
        author: Uploader name.
        description: Video description.
        transcript_preview: Full or partial transcript text.
        chapters: Detected chapters list.
        summary_mode: One of "minimal", "overview", "detailed", "mindmap".
        language: Output language.
        
    Returns:
        Prompt string ready for LLM.
    """
    mode_instructions = {
        "minimal": """Generate a ONE-SENTENCE summary plus 3-5 key bullet points.
Keep it extremely concise for social sharing.""",
        "overview": """Generate a structured overview:
- Background/context (1-2 sentences)
- Main content (3-5 sentences)
- Conclusion/takeaway (1-2 sentences)""",
        "detailed": """Generate a comprehensive structured note with:
1. One-sentence summary
2. Key points with timestamps (3-8 items)
3. Chapter summaries
4. Important data/statistics mentioned
5. Actionable takeaways
6. Related resources mentioned""",
        "mindmap": """Generate a mind map outline suitable for Obsidian/幕布.
Use nested bullet hierarchy with `- ` and `  - ` indentation.
Root: video title.""",
    }
    
    # Build chapters text
    chapters_text = ""
    if chapters:
        chapters_text = "\nDetected chapters:\n"
        for ch in chapters:
            start_m = int(ch.get("start_seconds", 0) // 60)
            start_s = int(ch.get("start_seconds", 0) % 60)
            chapters_text += f"- [{start_m:02d}:{start_s:02d}] Chapter {ch.get('index', '?')}\n"
    
    # Build transcript excerpt
    transcript_limit = 4000
    transcript_excerpt = transcript_preview[:transcript_limit]
    if len(transcript_preview) > transcript_limit:
        transcript_excerpt += "\n... [transcript truncated]"
    
    prompt = f"""You are a professional note-taker and content analyst.

Title: {title}
Author: {author}
Description: {description}
{chapters_text}

Transcript excerpt:
{transcript_excerpt}

Instructions ({summary_mode} mode):
{mode_instructions.get(summary_mode, mode_instructions["detailed"])}

IMPORTANT: 
- Always include the original video source attribution (title + author + link)
- Timestamps must be accurate to the second (MM:SS format)
- Output in {language}

Generate the structured summary now:"""
    
    return prompt


def parse_llm_response(response: Optional[str]) -> Dict:
    """
    Parse LLM response and extract structured data.
    Falls back to basic summary if LLM response is None or empty.
    
    Args:
        response: Raw text from LLM or None.
        
    Returns:
        Dict with summary results.
    """
    if not response or not response.strip():
        return {
            "summary_one_liner": "",
            "summary_overview": "",
            "key_points": [],
            "summary_raw": "",
            "llm_status": "unavailable",
        }
    
    # Try to extract JSON if present
    try:
        json_match = False
        # Look for JSON block in markdown
        import re
        json_pattern = re.compile(r'```(?:json)?\s*\n?(.*?)\n?```', re.DOTALL)
        match = json_pattern.search(response)
        if match:
            parsed = json.loads(match.group(1))
        else:
            parsed = json.loads(response)
        
        return {
            "summary_one_liner": parsed.get("one_liner", parsed.get("summary_one_liner", "")),
            "summary_overview": parsed.get("overview", parsed.get("summary", "")),
            "key_points": parsed.get("key_points", parsed.get("points", [])),
            "summary_raw": response,
            "llm_status": "success",
        }
    except (json.JSONDecodeError, AttributeError):
        # Return raw text as-is
        return {
            "summary_one_liner": response.split("\n")[0] if response else "",
            "summary_overview": response[:500] if response else "",
            "key_points": [],
            "summary_raw": response,
            "llm_status": "success_raw",
        }


def generate_fallback_summary(title: str, author: str, description: str) -> Dict:
    """
    Generate a basic summary without LLM (rule-based fallback).
    
    Args:
        title: Video title.
        author: Uploader name.
        description: Video description.
        
    Returns:
        Basic summary dict.
    """
    # Remove URLs from description for cleaner output
    import re
    clean_desc = re.sub(r'https?://\S+', '', description).strip()
    
    # Use first 2 sentences of description as overview
    sentences = [s.strip() for s in re.split(r'[。！？.!?\n]', clean_desc) if s.strip()]
    
    overview = sentences[0] if sentences else ""
    if len(sentences) > 1:
        overview += "。" + sentences[1]
    
    return {
        "summary_one_liner": f"{title} by {author}",
        "summary_overview": overview,
        "key_points": [],
        "summary_raw": "",
        "llm_status": "fallback",
    }


def format_as_markdown(summary: Dict, metadata: Dict, export_format: str = "markdown") -> str:
    """
    Format the complete summary as Markdown/JSON/Obsidian.
    """
    title = metadata.get("title", "Untitled")
    author = metadata.get("author", "Unknown")
    url = metadata.get("url", "")
    duration = metadata.get("duration_seconds", 0)
    
    minutes = duration // 60
    seconds = duration % 60
    
    yaml_lines = [
        "---",
        f'title: "{title}"',
        f"author: {author}",
        f"url: {url}",
        f"duration: {minutes:02d}:{seconds:02d}",
        f"date: {metadata.get('publish_date', '')}",
        "tags: [bilibili, digest]",
        "---",
        "",
    ]
    
    if export_format == "obsidian":
        # Obsidian uses WikiLinks
        body = f"# {title}\n\n"
        body += f"Source: [{title}]({url}) by [[{author}]]\n\n"
    elif export_format == "json":
        return json.dumps({"metadata": metadata, "summary": summary},
                          ensure_ascii=False, indent=2)
    else:
        # Standard Markdown
        body = "\n".join(yaml_lines)
        body += f"# {title}\n\n"
        body += f"> Source: [{title}]({url}) by **{author}**  \n"
        body += f"> Duration: {minutes:02d}:{seconds:02d}\n\n"
    
    # One-liner
    if summary.get("summary_one_liner"):
        body += f"## 📌 One-Liner\n\n{summary['summary_one_liner']}\n\n"
    
    # Overview
    if summary.get("summary_overview"):
        body += f"## 📝 Overview\n\n{summary['summary_overview']}\n\n"
    
    # Key Points
    if summary.get("key_points"):
        body += "## 📊 Key Points\n\n"
        for kp in summary["key_points"]:
            timestamp = kp.get("timestamp", "")
            point = kp.get("point", kp.get("content", ""))
            if timestamp:
                body += f"- [{timestamp}] {point}\n"
            else:
                body += f"- {point}\n"
        body += "\n"
    
    # Chapters
    if summary.get("chapters"):
        body += "## 📑 Chapters\n\n"
        for ch in summary["chapters"]:
            start_m = int(ch.get("start_seconds", 0) // 60)
            start_s = int(ch.get("start_seconds", 0) % 60)
            body += f"- **{ch.get('title', 'Chapter')}** `[{start_m:02d}:{start_s:02d}]`"
            if ch.get("summary"):
                body += f": {ch['summary']}"
            body += "\n"
        body += "\n"
    
    # Resources
    if summary.get("resources"):
        body += "## 📚 Resources\n\n"
        for r in summary["resources"]:
            body += f"- [{r.get('name', r.get('url', ''))}]({r.get('url', '')})\n"
        body += "\n"
    
    # Attribution
    body += f"---\n*Content source: [{title}]({url}) by {author}*\n"
    
    return body


def build_summary_prompt_for_column(column_text: str, title: str, author: str,
                                    summary_mode: str = "detailed") -> str:
    """Build a summary prompt for Bilibili columns/articles."""
    prompt = f"""Summarize the following column/article.

Title: {title}
Author: {author}

Text:
{column_text[:6000]}

Generate a structured Markdown note with:
1. Core thesis (1 sentence)
2. Key arguments (3-5 points)
3. Notable quotes or data
4. Your takeaway

Keep it concise but comprehensive."""
    return prompt
