#!/bin/bash
# wiki-lint.sh - Health check for llm-wiki
# Usage: ./scripts/wiki-lint.sh [--fix]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIKI_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WIKI_DIR="$WIKI_ROOT/wiki"

FIX_MODE=false
if [ "$1" == "--fix" ]; then
    FIX_MODE=true
fi

echo "🔍 LLM-Wiki Lint"
echo "================"
echo ""

# Use Python if available, otherwise use bash fallback
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD=python
else
    echo "⚠️  Python not found, using basic bash lint"
    bash_lint
    exit 0
fi

# Try to use virtual environment if exists
if [ -f "$WIKI_ROOT/.venv/bin/python" ]; then
    PYTHON_CMD="$WIKI_ROOT/.venv/bin/python"
elif [ -f "$WIKI_ROOT/.venv/Scripts/python.exe" ]; then
    PYTHON_CMD="$WIKI_ROOT/.venv/Scripts/python.exe"
fi

# Run Python lint if module available
if $PYTHON_CMD -c "from src.llm_wiki.core import WikiManager" 2>/dev/null; then
    $PYTHON_CMD -c "
from src.llm_wiki.core import WikiManager, find_wiki_root
from pathlib import Path

wiki = WikiManager(Path('$WIKI_DIR'))
issues = wiki.lint()

has_issues = any(issues.values())

if not has_issues:
    print('✅ All checks passed!')
else:
    if issues['orphans']:
        print(f'⚠️  Orphan pages ({len(issues[\"orphans\"])}):')
        for p in issues['orphans'][:5]:
            print(f'    - {p}')
    if issues['dead_links']:
        print(f'⚠️  Dead links ({len(issues[\"dead_links\"])}):')
        for link in issues['dead_links'][:5]:
            print(f'    - [[{link}]]')
    if issues['stale']:
        print(f'📅 Stale pages ({len(issues[\"stale\"])}):')
        for p in issues['stale'][:5]:
            print(f'    - {p}')
    if issues['empty_pages']:
        print(f'⚪ Empty pages ({len(issues[\"empty_pages\"])}):')
        for p in issues['empty_pages'][:5]:
            print(f'    - {p}')
    if issues['duplicate_titles']:
        print(f'🔁 Duplicate titles ({len(issues[\"duplicate_titles\"])}):')
        for p in issues['duplicate_titles'][:5]:
            print(f'    - {p}')
    if issues['noncanonical_links']:
        print(f'🔗 Non-canonical links ({len(issues[\"noncanonical_links\"])}):')
        for p in issues['noncanonical_links'][:5]:
            print(f'    - {p}')
    if issues['drafts']:
        print(f'📝 Draft pages ({len(issues[\"drafts\"])}):')
        for p in issues['drafts'][:5]:
            print(f'    - {p}')
"
else
    echo "⚠️  CLI module not available, install with: pip install -r src/requirements.txt"
    exit 1
fi
