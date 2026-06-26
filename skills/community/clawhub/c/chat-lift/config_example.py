#!/usr/bin/env python3
"""
ChatLift — Configuration Example
Copy to config.py and customize.

Author: Shadow Rose
License: MIT
"""

# ==============================================================================
# ARCHIVE SETTINGS
# ==============================================================================

# Directory where imported conversations are stored
archive_dir = 'chat-archive'

# Default output formats for imports
# Options: 'markdown', 'html', 'json'
default_formats = ['markdown', 'html', 'json']

# ==============================================================================
# IMPORT SETTINGS
# ==============================================================================

# Automatically detect source platform from export file structure
auto_detect_source = True

# Handle duplicate conversations (by ID)
# Options: 'skip', 'overwrite', 'rename'
duplicate_handling = 'skip'

# ==============================================================================
# SEARCH SETTINGS
# ==============================================================================

# Number of context characters around search matches
search_context_chars = 80

# Maximum search results to display (0 = unlimited)
search_result_limit = 0

# ==============================================================================
# HTML ARCHIVE SETTINGS
# ==============================================================================

# Directory for generated HTML archive
web_output_dir = 'chat-archive/web'

# Theme/color scheme
# Options: 'light', 'dark', 'auto'
archive_theme = 'light'

# Show message timestamps in archive
show_timestamps = True

# Enable syntax highlighting for code blocks
syntax_highlighting = False  # Requires external library

# ==============================================================================
# CONVERSATION FORMATTING
# ==============================================================================

# Markdown heading levels for roles
role_heading_level = 2  # ## USER

# Include metadata in exports (source, timestamps, etc.)
include_metadata = True

# Date format for timestamps
# See: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
timestamp_format = '%Y-%m-%d %H:%M:%S'

# ==============================================================================
# PERFORMANCE
# ==============================================================================

# Load conversations lazily (only when accessed)
lazy_loading = False

# Cache search results
enable_search_cache = False

# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================

# To use this config:
# 1. Copy to config.py: cp config_example.py config.py
# 2. Edit config.py with your preferences
# 3. Import in scripts:
#
#    try:
#        from config import archive_dir, default_formats
#    except ImportError:
#        archive_dir = 'chat-archive'
#        default_formats = ['markdown', 'html', 'json']

# ==============================================================================
# CUSTOM IMPORTER SETTINGS
# ==============================================================================

# Add support for custom export formats
# custom_importers = {
#     'my_chatbot': {
#         'file_pattern': '*.mychat',
#         'parser_function': my_custom_parser,
#     }
# }

# ==============================================================================
# NOTES
# ==============================================================================

# - All paths are relative to current working directory
# - archive_dir is created automatically if it doesn't exist
# - JSON exports preserve full conversation structure
# - Markdown/HTML are for human readability
