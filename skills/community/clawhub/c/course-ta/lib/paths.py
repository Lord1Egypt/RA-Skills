"""Centralized path resolution for the Course TA skill module.

All paths are relative to the skill root directory:
    ~/.openclaw/skills/course-ta/

Layout:
    lib/              Python modules (this file lives here)
    config/           Runtime configs (course-ta.json, canvas-config.json, etc.)
    data/
      courses/        Course content (Canvas sync cache, GDrive slides)
      memory/         Generated markdown files for RAG indexing
      logs/           Interaction audit logs (JSONL per day)
      credentials/    API tokens (gitignored)
      tests/          Test checklists
"""

from pathlib import Path

# Skill root: two levels up from lib/paths.py
SKILL_DIR = Path(__file__).resolve().parent.parent

# Configuration
CONFIG_DIR = SKILL_DIR / "config"
COURSE_TA_CONFIG = CONFIG_DIR / "course-ta.json"
CANVAS_CONFIG = CONFIG_DIR / "canvas-config.json"
COURSE_CONFIGS_DIR = CONFIG_DIR / "course-configs"
RATE_LIMIT_STATE = CONFIG_DIR / "ta-rate-limit.json"

# Data
DATA_DIR = SKILL_DIR / "data"
COURSES_DIR = DATA_DIR / "courses"
MEMORY_DIR = DATA_DIR / "memory"
LOGS_DIR = DATA_DIR / "logs"
CREDENTIALS_DIR = DATA_DIR / "credentials"
CANVAS_CREDENTIALS = CREDENTIALS_DIR / "canvas.json"

# Also expose the workspace path for OpenClaw memory indexing
WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"
