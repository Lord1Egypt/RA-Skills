"""
Forge Configuration — AI Workspace Architect
=============================================

Copy this file to forge_config.py and customize for your workspace.
Every setting is documented. Read before editing.
"""

import os

# =============================================================================
# WORKSPACE ROOT
# =============================================================================
# Absolute path to your AI agent's workspace directory.
# All scanning, planning, and auditing operates within this directory.
WORKSPACE_ROOT = os.path.expanduser("~/workspace")

# =============================================================================
# BACKUP SETTINGS
# =============================================================================
# Directory for backups. Forge refuses to plan without a verified backup.
BACKUP_DIR = os.path.join(WORKSPACE_ROOT, "backups")

# Create a backup before generating any plan
REQUIRE_BACKUP_BEFORE_PLAN = True

# Maximum age of backup (in hours) to consider "fresh enough"
MAX_BACKUP_AGE_HOURS = 24

# Files/dirs to exclude from backups (glob patterns)
BACKUP_EXCLUDES = [
    "backups/*.tar.gz",
    ".git",
    "__pycache__",
    "*.pyc",
    "node_modules",
    "venv",
    ".env",
]

# =============================================================================
# PROTECTED FILES — NEVER MODIFY OR MOVE
# =============================================================================
# These files are sacred. Forge will not include them in any move plan.
# Add your agent's critical files here.
PROTECTED_FILES = [
    # Identity / personality files
    # "SOUL.md",
    # "IDENTITY.md",
    # "AGENTS.md",

    # Memory files
    # "MEMORY.md",
    # "memory/*.md",

    # State files (active processes depend on these)
    # "drift_state.json",

    # Configuration
    # "USER.md",
    # "TOOLS.md",
]

# =============================================================================
# PROTECTED DIRECTORIES — NEVER TOUCH CONTENTS
# =============================================================================
# Entire directories that Forge must not scan for moves.
# Use for live systems, running bots, etc.
PROTECTED_DIRS = [
    # "bots",           # Live bot directory
    # "skills",         # Installed agent skills
    # ".secrets",       # Credentials
]

# =============================================================================
# DIRECTORY TEMPLATE — YOUR DESIRED STRUCTURE
# =============================================================================
# Define the target directory structure. Forge will plan moves to match this.
# Each entry is: directory_path -> description (used in _README.md generation)
#
# Customize this entirely for your use case.
DIRECTORY_TEMPLATE = {
    "archive": "Retired files. Nothing is deleted — it comes here instead.",
    "backups": "System backups. Automated and manual snapshots.",
    "docs": "Documentation, guides, and reference material.",
    "inbox": "Quick-capture landing zone. New files go here first, then get sorted.",
    "memory": "Agent memory files. Daily notes, long-term memory.",
    "memory/archive": "Archived monthly memory rollups.",
    "projects": "Active projects and their working files.",
    "scripts": "Utility scripts, automation, and tools.",
    "config": "Configuration files for various systems.",
    "templates": "Reusable templates and scaffolds.",
}

# =============================================================================
# FILE CLASSIFICATION RULES
# =============================================================================
# Rules for automatically classifying files during scan.
# Format: (glob_pattern, target_directory)
# Files matching a pattern get suggested for the target directory in the plan.
# These are SUGGESTIONS — the plan is always human-reviewed.
FILE_CLASSIFICATION_RULES = [
    # ("*.log", "logs"),
    # ("DRAFT-*.md", "inbox"),
    # ("*.tar.gz", "backups"),
    # ("*.bak", "archive"),
    # ("memory/????-??-??.md", "memory"),  # Daily memory files stay in memory/
]

# =============================================================================
# REFERENCE SCANNING
# =============================================================================
# File extensions to scan for cross-references
REFERENCE_SCAN_EXTENSIONS = [
    ".md", ".txt", ".py", ".sh", ".js", ".ts",
    ".json", ".yaml", ".yml", ".toml", ".cfg", ".ini",
]

# Patterns to detect file references (regex)
# These are used to find mentions of files inside other files.
REFERENCE_PATTERNS = [
    r'(?:^|[\s"`\'/\\(])([A-Za-z0-9_\-./]+\.(?:md|txt|py|sh|js|json|yaml|yml|toml))',
    r'(?:path|file|source|include|import)\s*[:=]\s*["\']?([^\s"\']+)',
]

# =============================================================================
# PROCESS DETECTION
# =============================================================================
# Forge checks for running processes that depend on workspace files.
# If a process is found using a file, that file becomes protected.
DETECT_RUNNING_PROCESSES = True

# Commands to check for running processes (platform-specific)
PROCESS_CHECK_COMMANDS = [
    "ps aux",           # Unix/Linux/macOS
    # "tasklist /v",    # Windows
]

# =============================================================================
# AUDIT SETTINGS
# =============================================================================
# Directory where audit reports and manifests are stored
AUDIT_DIR = os.path.join(WORKSPACE_ROOT, "backups")

# Secrets patterns — files containing these patterns trigger warnings
SECRETS_PATTERNS = [
    r"(?i)api[_\-]?key",
    r"(?i)password\s*[:=]",
    r"(?i)secret\s*[:=]",
    r"(?i)token\s*[:=]",
    r"sk-[a-zA-Z0-9]{20,}",
    r"(?i)BEGIN\s+(RSA|DSA|EC|OPENSSH)\s+PRIVATE\s+KEY",
]

# Maximum file size to scan for references (skip huge files)
MAX_SCAN_FILE_SIZE_MB = 10

# =============================================================================
# OUTPUT SETTINGS
# =============================================================================
# Where Forge writes its reports and plans
OUTPUT_DIR = os.path.join(WORKSPACE_ROOT, "forge-output")

# Generate _README.md files for new directories
GENERATE_README_FILES = True

# README template for new directories
README_TEMPLATE = """# {dir_name}

{description}

## What belongs here
{belongs_here}

## What does NOT belong here
Files that don't match this directory's purpose should go in `inbox/` for triage.
"""

# =============================================================================
# ARCHIVE SETTINGS
# =============================================================================
ARCHIVE_DIR = os.path.join(WORKSPACE_ROOT, "archive")

# Use year subdirectories in archive (archive/2026/, archive/2025/)
ARCHIVE_YEAR_SUBDIRS = True

# =============================================================================
# SAFETY SETTINGS
# =============================================================================
# These are the hardline rules. Override at your own risk.

# Never delete any file (moves to archive instead)
ZERO_DELETION_POLICY = True

# Require file count verification before and after moves
REQUIRE_FILE_COUNT_CHECK = True

# Maximum number of files to move in a single plan (safety limit)
MAX_MOVES_PER_PLAN = 500

# Abort if more than this percentage of files would be moved
MAX_MOVE_PERCENTAGE = 80  # If >80% of files need moving, something is wrong

# Require manifest creation before any plan
REQUIRE_PRE_MANIFEST = True
