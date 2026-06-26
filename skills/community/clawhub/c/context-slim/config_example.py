"""
ContextSlim Configuration Example

Copy this file to `config.py` and customize for your needs.

Author: Shadow Rose
License: MIT
"""

# ====================
# Provider Settings
# ====================

# AI provider type for token estimation
# Options: 'openai', 'anthropic', 'google', 'generic'
PROVIDER = 'generic'

# Specific model name (optional)
# Used for accurate context limit lookup
# Examples: 'gpt-4', 'claude-3-opus', 'gemini-pro'
MODEL = None


# ====================
# Token Estimation
# ====================

# Custom token-to-word ratios (overrides defaults)
# Only needed if you want to fine-tune estimation accuracy
CUSTOM_RATIOS = {
    # 'openai': 0.75,
    # 'anthropic': 0.80,
    # 'google': 0.73,
}


# ====================
# Context Limits
# ====================

# Custom context limits (tokens)
# Only needed for models not in the built-in list
CUSTOM_LIMITS = {
    # 'my-custom-model': 100000,
}


# ====================
# Analysis Settings
# ====================

# Truncation risk thresholds (percentage of context used)
TRUNCATION_THRESHOLDS = {
    'none': 50,      # < 50% utilization
    'low': 70,       # 50-70%
    'medium': 85,    # 70-85%
    'high': 95,      # 85-95%
    'critical': 100  # > 95%
}


# ====================
# Compression Settings
# ====================

# Minimum confidence level for compression suggestions
# Options: 'high', 'medium', 'low'
MIN_CONFIDENCE = 'low'

# Maximum suggestions per category
MAX_SUGGESTIONS_PER_CATEGORY = 5

# Enable/disable specific compression categories
COMPRESSION_CATEGORIES = {
    'redundancy': True,     # Redundant phrases
    'verbosity': True,      # Verbose language
    'examples': True,       # Excessive examples
    'formatting': True,     # Formatting inefficiencies
    'repetition': True,     # Repetitive instructions
}


# ====================
# Report Settings
# ====================

# Default output format for reports
# Options: 'text', 'json', 'html'
DEFAULT_OUTPUT_FORMAT = 'text'

# HTML report styling theme
# Options: 'default', 'dark', 'minimal'
REPORT_THEME = 'default'

# Include compression suggestions in reports by default
INCLUDE_SUGGESTIONS = True


# ====================
# File Processing
# ====================

# Supported file extensions for analysis
SUPPORTED_EXTENSIONS = [
    '.txt', '.md', '.json', '.yaml', '.yml',
    '.py', '.js', '.html', '.xml', '.csv'
]

# Default encoding for file reading
FILE_ENCODING = 'utf-8'

# Maximum file size to process (bytes)
# 0 = no limit
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# ====================
# Advanced Settings
# ====================

# Enable debug output
DEBUG = False

# Cache token estimates for repeated text
# (useful for batch processing)
ENABLE_CACHE = False
