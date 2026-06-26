#!/bin/bash
# install.sh — One-click setup for agent-guardrails in a project
# Usage: bash install.sh [project_directory]
# Installs: git pre-commit hook, check scripts, registry template

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_DIR="${1:-.}"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Directory not found: $PROJECT_DIR"
    echo "Usage: bash install.sh [project_directory]"
    exit 1
fi

PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"

echo "╔══════════════════════════════════════════════════╗"
echo "║       Agent Guardrails — Install                 ║"
echo "╚══════════════════════════════════════════════════╝"
echo "  Project: $PROJECT_DIR"
echo "  Skill:   $SKILL_DIR"
echo ""

# 1. Copy check scripts
echo "📋 Installing check scripts..."
mkdir -p "$PROJECT_DIR/scripts"
cp "$SKILL_DIR/scripts/pre-create-check.sh" "$PROJECT_DIR/scripts/"
cp "$SKILL_DIR/scripts/post-create-validate.sh" "$PROJECT_DIR/scripts/"
cp "$SKILL_DIR/scripts/check-secrets.sh" "$PROJECT_DIR/scripts/"
chmod +x "$PROJECT_DIR/scripts/pre-create-check.sh"
chmod +x "$PROJECT_DIR/scripts/post-create-validate.sh"
chmod +x "$PROJECT_DIR/scripts/check-secrets.sh"
echo "  ✅ Copied to $PROJECT_DIR/scripts/"

# 2. Install git pre-commit hook (if git repo)
if [ -d "$PROJECT_DIR/.git" ]; then
    echo ""
    echo "🔗 Installing git pre-commit hook..."
    HOOKS_DIR="$PROJECT_DIR/.git/hooks"
    mkdir -p "$HOOKS_DIR"
    
    if [ -f "$HOOKS_DIR/pre-commit" ]; then
        echo "  ⚠️  Existing pre-commit hook found — backing up to pre-commit.bak"
        cp "$HOOKS_DIR/pre-commit" "$HOOKS_DIR/pre-commit.bak"
    fi
    
    cp "$SKILL_DIR/assets/pre-commit-hook" "$HOOKS_DIR/pre-commit"
    chmod +x "$HOOKS_DIR/pre-commit"
    echo "  ✅ Pre-commit hook installed"
else
    echo ""
    echo "ℹ️  Not a git repo — skipping pre-commit hook"
fi

# 3. Create registry template if no __init__.py exists
if [ ! -f "$PROJECT_DIR/__init__.py" ]; then
    echo ""
    echo "📦 Creating module registry template..."
    cp "$SKILL_DIR/assets/registry-template.py" "$PROJECT_DIR/__init__.py"
    echo "  ✅ Created $PROJECT_DIR/__init__.py (edit to list your modules)"
else
    echo ""
    echo "ℹ️  __init__.py already exists — skipping registry template"
fi

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  ✅ Installation complete!                       ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║  Before new .py files:                           ║"
echo "║    bash scripts/pre-create-check.sh .            ║"
echo "║  After editing .py files:                        ║"
echo "║    bash scripts/post-create-validate.sh <file>   ║"
echo "║  Scan for secrets:                               ║"
echo "║    bash scripts/check-secrets.sh .               ║"
echo "╚══════════════════════════════════════════════════╝"
