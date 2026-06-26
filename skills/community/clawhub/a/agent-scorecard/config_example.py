"""
Agent Scorecard — Configuration Example (Python Reference)
===========================================================
⚠️  Config is now JSON format. Use config_example.json instead.
    cp config_example.json scorecard_config.json

This file is kept as a human-readable reference only. The active
config loader requires a .json file and will raise ValueError on .py.
All settings have sensible defaults; override only what you need.
"""

# ---------------------------------------------------------------------------
# QUALITY DIMENSIONS
# ---------------------------------------------------------------------------
# Each dimension is a dict with:
#   name        — unique identifier (snake_case)
#   label       — human-readable name
#   weight      — relative importance (floats; will be normalised)
#   threshold   — minimum score (1-5) to "pass" this dimension
#   rubric      — dict mapping scores 1-5 to descriptions
#   auto_checks — list of automated check names to run (see AUTO_CHECKS)

DIMENSIONS = [
    {
        "name": "accuracy",
        "label": "Accuracy",
        "weight": 2.0,
        "threshold": 3,
        "rubric": {
            1: "Contains significant factual errors or hallucinations",
            2: "Multiple minor inaccuracies; some unverified claims",
            3: "Mostly accurate with minor gaps",
            4: "Accurate with well-supported claims",
            5: "Fully accurate, verifiable, no hallucinations detected",
        },
        "auto_checks": ["hedge_words"],
    },
    {
        "name": "completeness",
        "label": "Completeness",
        "weight": 1.5,
        "threshold": 3,
        "rubric": {
            1: "Misses most required sections or information",
            2: "Addresses some requirements but significant gaps remain",
            3: "Covers core requirements; minor omissions",
            4: "Thorough coverage with only trivial omissions",
            5: "Comprehensive — every requirement addressed in full",
        },
        "auto_checks": ["required_sections", "response_length"],
    },
    {
        "name": "tone",
        "label": "Tone & Professionalism",
        "weight": 1.0,
        "threshold": 2,
        "rubric": {
            1: "Inappropriate, rude, or wildly off-register",
            2: "Inconsistent tone; occasional sycophancy or filler",
            3: "Generally appropriate tone throughout",
            4: "Consistently professional and well-calibrated",
            5: "Perfect register — confident, clear, zero filler",
        },
        "auto_checks": ["sycophancy", "filler_words"],
    },
    {
        "name": "format_compliance",
        "label": "Format Compliance",
        "weight": 1.0,
        "threshold": 3,
        "rubric": {
            1: "Ignores requested format entirely",
            2: "Partially follows format; missing key structural elements",
            3: "Follows format with minor deviations",
            4: "Clean format compliance throughout",
            5: "Perfect adherence to requested structure and style",
        },
        "auto_checks": ["format_structure", "code_blocks"],
    },
    {
        "name": "consistency",
        "label": "Consistency",
        "weight": 0.8,
        "threshold": 2,
        "rubric": {
            1: "Contradicts itself; wildly varying style",
            2: "Noticeable inconsistencies in terminology or approach",
            3: "Generally consistent with minor variation",
            4: "Consistent terminology, style, and reasoning",
            5: "Perfectly uniform voice, style, and logic throughout",
        },
        "auto_checks": ["style_consistency"],
    },
]


# ---------------------------------------------------------------------------
# AUTOMATED CHECK CONFIGURATION
# ---------------------------------------------------------------------------
# Each check can be tuned independently. These feed into the auto_checks
# referenced by dimensions above.

AUTO_CHECKS = {
    # Response length — flag outputs that are too short or too long
    "response_length": {
        "min_chars": 100,           # below this → flag as too short
        "max_chars": 15000,         # above this → flag as too long
        "ideal_min": 300,           # sweet-spot lower bound
        "ideal_max": 8000,          # sweet-spot upper bound
        "penalty_short": 2,         # score penalty when too short (deduct from 5)
        "penalty_long": 1,          # score penalty when too long
    },

    # Format structure — look for expected markdown elements
    "format_structure": {
        "expect_headers": True,             # should contain ## or ### headers
        "expect_lists": False,              # should contain bullet/numbered lists
        "expect_code_blocks": False,        # should contain ``` code blocks
        "custom_patterns": [],              # list of regex patterns that SHOULD appear
        "missing_penalty": 1,               # per-missing-element penalty
    },

    # Code block checks
    "code_blocks": {
        "require_language_tag": True,       # ``` should specify language
        "max_block_lines": 200,             # flag excessively long blocks
    },

    # Sycophancy markers — phrases that suggest hollow flattery
    "sycophancy": {
        "markers": [
            "great question",
            "excellent question",
            "wonderful question",
            "that's a really good",
            "what a fantastic",
            "i'm so glad you asked",
            "absolutely brilliant",
        ],
        "penalty_per_hit": 1,               # deducted per marker found
        "max_penalty": 3,                   # cap total deduction
    },

    # Filler / hedge words
    "filler_words": {
        "words": [
            "basically", "essentially", "actually", "literally",
            "obviously", "clearly", "simply", "just",
        ],
        "threshold_per_1000_chars": 3,      # flag if density exceeds this
        "penalty": 1,
    },

    # Hedge words (indicates uncertainty / low confidence)
    "hedge_words": {
        "words": [
            "might", "perhaps", "possibly", "could be",
            "i think", "i believe", "it seems", "arguably",
            "to some extent", "in a way",
        ],
        "threshold_per_1000_chars": 4,
        "penalty": 1,
    },

    # Required sections — check for presence of specific headings/phrases
    "required_sections": {
        "sections": [],                     # e.g. ["## Summary", "## Recommendations"]
        "case_sensitive": False,
        "penalty_per_missing": 1,
    },

    # Style consistency — checks variation in sentence length, vocabulary
    "style_consistency": {
        "max_sentence_length_std_dev": 30,  # in words; high std-dev = inconsistent
        "penalty": 1,
    },
}


# ---------------------------------------------------------------------------
# SCORING
# ---------------------------------------------------------------------------

# How to aggregate dimension scores into an overall score
# Options: "weighted_average", "minimum", "geometric_mean"
AGGREGATE_METHOD = "weighted_average"

# Overall pass threshold (on 1-5 scale)
OVERALL_PASS_THRESHOLD = 3.0

# Round displayed scores to this many decimal places
SCORE_PRECISION = 2


# ---------------------------------------------------------------------------
# TRACKING
# ---------------------------------------------------------------------------

# Where to store evaluation history (JSON lines file)
HISTORY_FILE = "scorecard_history.jsonl"

# Maximum evaluations to keep in history (0 = unlimited)
MAX_HISTORY = 0

# Agent identifier — used to group evaluations by agent
DEFAULT_AGENT = "default"

# Task type — used to group evaluations by task category
DEFAULT_TASK_TYPE = "general"


# ---------------------------------------------------------------------------
# REPORTS
# ---------------------------------------------------------------------------

# Default report format: "markdown" or "json"
DEFAULT_REPORT_FORMAT = "markdown"

# Output directory for generated reports
REPORT_OUTPUT_DIR = "reports"

# Include raw automated check details in reports
INCLUDE_CHECK_DETAILS = True

# Include rubric text in reports
INCLUDE_RUBRIC = True

# Include trend sparklines in markdown reports (uses ASCII art)
INCLUDE_TREND_SPARKLINES = True
