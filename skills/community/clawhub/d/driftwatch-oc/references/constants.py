"""
Driftwatch — Source-Verified OpenClaw Constants
Verified against OpenClaw source code, March 2026.

These constants govern how OpenClaw processes bootstrap files,
handles truncation, and manages compaction. All values are
confirmed from the actual source files listed in comments.
"""

# --- bootstrap.ts ---
BOOTSTRAP_MAX_CHARS_PER_FILE = 20_000
BOOTSTRAP_TOTAL_MAX_CHARS = 150_000
MIN_BOOTSTRAP_FILE_BUDGET_CHARS = 64
TRUNCATION_HEAD_RATIO = 0.70  # Applied to the LIMIT, not the file size
TRUNCATION_TAIL_RATIO = 0.20  # Applied to the LIMIT, not the file size
TRUNCATION_MARKER_RATIO = 0.10

# --- workspace.ts ---
BOOTSTRAP_FILE_ORDER = [
    "AGENTS.md",
    "SOUL.md",
    "TOOLS.md",
    "IDENTITY.md",
    "USER.md",
    "HEARTBEAT.md",
    "BOOTSTRAP.md",
    "MEMORY.md",
]

SUBAGENT_FILES = [
    "AGENTS.md",
    "SOUL.md",
    "TOOLS.md",
    "IDENTITY.md",
    "USER.md",
]

MEMORY_CANDIDATES = ["MEMORY.md", "memory.md"]

# --- workspace convention (not source-enforced) ---
# These headings are recommended best practices for AGENTS.md.
# They are NOT referenced by OpenClaw source code. The compaction-safeguard
# extension handles LLM-based history summarization, not heading re-injection.
# Checking for their presence is a hygiene convention, not a source requirement.
COMPACTION_SURVIVING_HEADINGS = ["Session Startup", "Red Lines"]
COMPACTION_HEADING_CAP_CHARS = 3_000
MAX_SUMMARY_CONTEXT_CHARS = 2_000

# --- pruner.ts ---
CHARS_PER_TOKEN_ESTIMATE = 4

# --- run.ts ---
MAX_OVERFLOW_COMPACTION_ATTEMPTS = 3

# --- Version stamp ---
OPENCLAW_VERSION_TAG = "2026.03"
DRIFTWATCH_VERSION = "1.1.1"
