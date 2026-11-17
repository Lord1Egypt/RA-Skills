"""
LLM-Wiki CLI entry point

Usage:
    python -m llm_wiki [command] [options]
    python -m src.llm_wiki [command] [options]
"""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
