"""
LLM-Wiki CLI entry point

Usage:
    python -m llm_wiki [command] [options]
    python -m src.llm_wiki [command] [options]

Commands:
    status              Show wiki status overview
    lint [--fix]        Check wiki health
    ingest <path>       Ingest source material (dry-run only)
    query <text>        Query wiki (lists pages only)

Examples:
    python -m src.llm_wiki status
    python -m src.llm_wiki lint
    python -m src.llm_wiki lint --fix
"""

from .commands import cli

if __name__ == '__main__':
    cli()
