#!/usr/bin/env python3
"""
Content Repurposer - Transform one piece of content into 10+ marketing formats.

Usage:
    uv run python scripts/repurpose.py "Your content here" [--type auto] [--tone professional] [--output ./output]

Output Formats:
    - Twitter Thread (5-7 tweets)
    - LinkedIn Post
    - Blog Intro
    - Email Newsletter
    - Discord Announcement
    - Reddit Post
    - Quora Answer
    - Instagram Caption
    - Email Subject Lines (5 variants)
    - Meta Descriptions (3 variants)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# API configuration
MINIMAX_API_URL = "https://api.minimax.chat/v1/text/chatcompletion_pro"
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")


def load_prompt_template() -> dict:
    """Load the prompt template for content repurposing."""
    return {
        "system_prompt": """You are an expert content repurposing AI. Transform a single piece of content into 10 different marketing formats. Always follow the user's specified tone. Output ONLY valid JSON — no markdown, no explanation, no preamble.""",
        
        "user_template": """Transform the following content into 10 marketing formats.

Content: {content}

Type: {content_type}
Tone: {tone}

Output exactly this JSON structure (no keys beyond these):
{{
  "twitter_thread": ["tweet 1", "tweet 2", "tweet 3", "tweet 4", "tweet 5"],
  "linkedin_post": "full linkedin post here",
  "blog_intro": "200-word blog introduction here",
  "email_newsletter": "full newsletter paragraph here",
  "discord_announcement": "discord-friendly announcement with emoji",
  "reddit_post": {{"title": "post title", "body": "post body"}},
  "quora_answer": "informative quora-style answer",
  "instagram_caption": "caption with hashtags",
  "email_subject_lines": ["subject 1", "subject 2", "subject 3", "subject 4", "subject 5"],
  "meta_descriptions": ["meta 1", "meta 2", "meta 3"]
}}

Rules:
- twitter_thread: 5-7 tweets, each under 280 chars
- linkedin_post: professional tone, 150-300 words
- blog_intro: engaging, ~200 words
- email_newsletter: conversational, one compelling paragraph
- discord_announcement: use emoji, keep it scannable
- reddit_post: catchy title, helpful body
- quora_answer: informative, answer-focused
- instagram_caption: punchy, include relevant hashtags
- email_subject_lines: 5 variants, under 60 chars each
- meta_descriptions: 3 variants, 150-160 chars each
- NEVER wrap output in markdown code blocks
- Output valid JSON only"""
    }


def detect_content_type(content: str) -> str:
    """Auto-detect content type based on length and structure."""
    content = content.strip()
    
    if len(content) < 100:
        return "tweet"
    elif content.startswith("http") or len(content) > 500:
        return "article"
    elif content.startswith("Subject:") or "@" in content:
        return "email"
    elif content.startswith("Dear") or "Best regards" in content:
        return "email"
    else:
        return "description"


def call_minimax_api(content: str, content_type: str, tone: str) -> dict:
    """Call MiniMax API for content generation."""
    template = load_prompt_template()
    
    user_prompt = template["user_template"].format(
        content=content,
        content_type=content_type,
        tone=tone
    )
    
    payload = {
        "model": "MiniMax-Text-01",
        "messages": [
            {"role": "system", "content": template["system_prompt"]},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 3000
    }
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            import urllib.request
            req = urllib.request.Request(
                MINIMAX_API_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...", file=sys.stderr)
                time.sleep(wait_time)
            else:
                return None
    
    return None


def parse_json_output(raw_output: str) -> dict:
    """Parse and validate the JSON output from API."""
    # Remove markdown code blocks if present
    raw_output = raw_output.strip()
    if raw_output.startswith("```json"):
        raw_output = raw_output[7:]
    elif raw_output.startswith("```"):
        raw_output = raw_output[3:]
    if raw_output.endswith("```"):
        raw_output = raw_output[:-3]
    
    # Try to find JSON object
    raw_output = raw_output.strip()
    
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        # Try to find JSON in the text
        start = raw_output.find("{")
        end = raw_output.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(raw_output[start:end + 1])
            except json.JSONDecodeError:
                pass
        raise ValueError(f"Could not parse JSON from output: {raw_output[:200]}")


def save_outputs(results: dict, output_dir: str):
    """Save individual format outputs to files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    files = {
        "twitter_thread.json": results.get("twitter_thread", []),
        "linkedin_post.txt": results.get("linkedin_post", ""),
        "blog_intro.txt": results.get("blog_intro", ""),
        "email_newsletter.txt": results.get("email_newsletter", ""),
        "discord_announcement.txt": results.get("discord_announcement", ""),
        "reddit_post.json": results.get("reddit_post", {}),
        "quora_answer.txt": results.get("quora_answer", ""),
        "instagram_caption.txt": results.get("instagram_caption", ""),
        "email_subject_lines.json": results.get("email_subject_lines", []),
        "meta_descriptions.json": results.get("meta_descriptions", [])
    }
    
    for filename, content in files.items():
        filepath = output_path / filename
        if isinstance(content, (list, dict)):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
        else:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(str(content))


def main():
    parser = argparse.ArgumentParser(
        description="Repurpose content into 10+ marketing formats"
    )
    parser.add_argument(
        "content",
        nargs="+",
        help="The content to repurpose (as string or @file to read from file)"
    )
    parser.add_argument(
        "--type",
        choices=["auto", "tweet", "article", "description", "speech", "email"],
        default="auto",
        help="Content type for better generation"
    )
    parser.add_argument(
        "--tone",
        choices=["professional", "casual", "humorous", "inspirational", "technical"],
        default="professional",
        help="Writing tone"
    )
    parser.add_argument(
        "--output",
        default="./output",
        help="Output directory for individual files"
    )
    
    args = parser.parse_args()
    
    # Handle content input
    content_input = " ".join(args.content)
    if content_input.startswith("@"):
        filepath = content_input[1:]
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
        except FileNotFoundError:
            return {"success": False, "error_code": "FILE_NOT_FOUND", "error_message": f"Could not read file: {filepath}"}
    else:
        content = content_input.strip()
    
    # Validate content
    if not content:
        return {"success": False, "error_code": "EMPTY_CONTENT", "error_message": "Content cannot be empty"}
    
    if len(content) < 10:
        return {"success": False, "error_code": "CONTENT_TOO_SHORT", "error_message": "Content must be at least 10 characters"}
    
    # Detect or use specified content type
    content_type = args.type if args.type != "auto" else detect_content_type(content)
    
    print(f"Repurposing content ({content_type}, {args.tone})...", file=sys.stderr)
    
    # Call API
    raw_output = call_minimax_api(content, content_type, args.tone)
    
    if not raw_output:
        return {"success": False, "error_code": "API_ERROR", "error_message": "Failed to get response from API"}
    
    # Parse output
    try:
        results = parse_json_output(raw_output)
    except ValueError as e:
        return {"success": False, "error_code": "PARSE_ERROR", "error_message": str(e)}
    
    # Save outputs if output dir specified
    if args.output:
        save_outputs(results, args.output)
    
    # Return structured response
    output = {
        "success": True,
        "results": results,
        "meta": {
            "content_type": content_type,
            "tone": args.tone,
            "output_dir": args.output
        }
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return output


if __name__ == "__main__":
    main()