#!/usr/bin/env python3
"""
Phase 4: Generate content from tasks.

This module is designed to be imported and called by an OpenClaw agent,
because content generation requires LLM calls that only the agent can make.

The agent workflow:
  1. Agent reads task files (via get_tasks_for_generation())
  2. Agent calls its own LLM with build_generation_prompt(task_data)
  3. Agent parses JSON response and saves via save_generated(content_data)
  4. For Eir mode, agent calls eir_post.post_content() to upload

This is not a standalone CLI script — there is no main() because the
LLM generation step requires agent context and cannot be scripted.
"""

import json
from pathlib import Path

from .config import (
    GENERATED_DIR, TASKS_DIR,
    ensure_dirs,
)
from .workspace import SKILL_DIR

# Writer prompt paths
WRITER_PROMPT_PATH = SKILL_DIR / "references" / "writer-prompt-eir.md"
WRITER_PROMPT_STANDALONE_PATH = SKILL_DIR / "references" / "writer-prompt-standalone.md"


def load_writer_prompt():
    """Load writer prompt based on mode (eir or standalone)."""
    from .workspace import load_settings
    settings = load_settings()
    mode = settings.get("mode", "standalone")
    return _load_prompt_by_mode(mode)


def _load_prompt_by_mode(mode):
    """Load writer prompt file for the given mode."""
    if mode == "eir" and WRITER_PROMPT_PATH.exists():
        return WRITER_PROMPT_PATH.read_text()
    if WRITER_PROMPT_STANDALONE_PATH.exists():
        return WRITER_PROMPT_STANDALONE_PATH.read_text()
    if WRITER_PROMPT_PATH.exists():
        return WRITER_PROMPT_PATH.read_text()
    return "Generate structured content from the sources below."


def build_generation_prompt(task_data):
    """Build the LLM prompt for content generation from task data."""
    slug = task_data.get("topic_slug", "")
    angle = task_data.get("suggested_angle", "")
    reason = task_data.get("reason", "")
    source_text = task_data.get("source_text", "")
    reader_context = task_data.get("reader_context", "")

    # Resolve output language: task > directives cache > settings
    # If still empty, SKILL.md instructs agent to use the user's chat language
    output_lang = task_data.get("output_lang", "")
    if not output_lang:
        try:
            from .config import DIRECTIVES_FILE, load_json
            directives = load_json(DIRECTIVES_FILE, {})
            output_lang = directives.get("user", {}).get("primaryLanguage", "")
        except Exception:
            pass
    if not output_lang:
        try:
            from .workspace import load_settings
            output_lang = load_settings().get("language", "")
        except Exception:
            pass
    
    # Load writer prompt: use mode marker from task (v2), fall back to embedded prompt (v1)
    writer_prompt_mode = task_data.get("writer_prompt_mode", "")
    if writer_prompt_mode:
        writer_prompt = _load_prompt_by_mode(writer_prompt_mode)
    else:
        writer_prompt = task_data.get("writer_prompt", "") or load_writer_prompt()

    prompt = """%s

---

## Task

Topic slug: %s
Angle: %s
Why: %s
Output language: %s
%s
Source material:
%s

Output ONLY the JSON. No other text or markdown fences.""" % (
        writer_prompt, slug, angle, reason, output_lang, 
        "\nReader context:\n" + reader_context if reader_context else "",
        source_text)

    return prompt


def save_generated(content_data, suffix=""):
    """Save generated content to file."""
    ensure_dirs()
    slug = content_data.get("slug", "unknown")
    lang = content_data.get("lang", "zh")
    name = "%s_%s%s.json" % (slug, lang, suffix)
    path = GENERATED_DIR / name
    path.write_text(json.dumps(content_data, indent=2, ensure_ascii=False))
    return path


# === Functions for standalone generation ===

def get_tasks_for_generation():
    """Return task files ready for generation."""
    ensure_dirs()
    task_files = list(TASKS_DIR.glob("*.json"))
    task_files = [f for f in task_files if f.stem != "manifest"]
    
    tasks = []
    for task_file in task_files:
        try:
            task_data = json.loads(task_file.read_text())
            tasks.append({
                "file": task_file,
                "data": task_data,
                "prompt": build_generation_prompt(task_data),
            })
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ Skipping invalid task file {task_file.name}: {e}")
    
    return tasks