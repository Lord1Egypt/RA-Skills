#!/bin/bash
# init-wiki.sh - Initialize a new llm-wiki project
# Usage: ./scripts/init-wiki.sh [target-directory]

set -e

TARGET_DIR="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🚀 Initializing new LLM-Wiki project..."
echo "Target: $TARGET_DIR"
echo ""

# Create directory structure
mkdir -p "$TARGET_DIR"/{wiki,sources,assets,scripts,src/llm_wiki,examples}

# Copy core protocol files
cp "$TEMPLATE_DIR/CLAUDE.md" "$TARGET_DIR/"
cp "$TEMPLATE_DIR/SKILL.md" "$TARGET_DIR/"
cp "$TEMPLATE_DIR/AGENTS.md" "$TARGET_DIR/"
cp "$TEMPLATE_DIR/README.md" "$TARGET_DIR/"

# Copy templates
cp "$TEMPLATE_DIR/assets/page_template.md" "$TARGET_DIR/assets/"
cp "$TEMPLATE_DIR/assets/ingest_rules.md" "$TARGET_DIR/assets/"

# Copy Python source
cp -r "$TEMPLATE_DIR/src/"* "$TARGET_DIR/src/"

# Copy scripts
cp "$TEMPLATE_DIR/scripts/"*.sh "$TARGET_DIR/scripts/"

# Create initial files
touch "$TARGET_DIR/log.md"
cat > "$TARGET_DIR/log.md" << 'EOF'
# Wiki Log

## [$(date +%Y-%m-%d)] init | Project initialized
- Created llm-wiki structure
- Ready for first ingest
EOF

cat > "$TARGET_DIR/wiki/index.md" << 'EOF'
# Wiki Index

> Knowledge base entry point

## Recent Activity
See [log.md](../log.md) for full history.

## Quick Start

1. Add source materials to `sources/`
2. Ask your agent: "请摄入 sources/[filename] 到 wiki"
3. Explore and query the generated knowledge

## Status

- 🟡 Empty — waiting for first ingest
EOF

cat > "$TARGET_DIR/sources/README.md" << 'EOF'
# Sources Directory

Place your raw materials here:
- Research papers (PDF)
- Articles and notes (Markdown, TXT)
- Code snippets
- Images (with vision-capable LLM)

Files here are **not** tracked by git by default (see `.gitignore`).

Use `请摄入 [filename] 到 wiki` to process new materials.
EOF

cat > "$TARGET_DIR/.gitignore" << 'EOF'
# Python
__pycache__/
*.py[cod]
*.egg-info/

# Virtual environments
.venv/
venv/

# Claude Code
.claude/

# Wiki sources (user-managed)
sources/*
!sources/README.md
!sources/.gitkeep

# Obsidian
.obsidian/
.trash/

# OS
.DS_Store
Thumbs.db
EOF

# Make scripts executable
chmod +x "$TARGET_DIR/scripts/"*.sh

echo "✅ LLM-Wiki initialized successfully!"
echo ""
echo "Next steps:"
echo "  1. cd $TARGET_DIR"
echo "  2. Add source files to sources/"
echo "  3. Ask your agent: '请摄入 sources/my-file.pdf 到 wiki'"
echo ""
echo "Optional: Install CLI tools"
echo "  uv venv && uv pip install -r src/requirements.txt"
