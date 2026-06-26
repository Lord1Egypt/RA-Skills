#!/usr/bin/env bash
# Install Fleece skills for Claude Code and/or OpenClaw / Codex agents.
#
# Usage:
#   bash install.sh           # auto-detect
#   bash install.sh --claude  # Claude Code only
#   bash install.sh --agents  # OpenClaw / Codex only
#   bash install.sh --all     # both

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

install_claude() {
  TARGET=".claude/skills"
  mkdir -p "$TARGET"
  for f in "$SCRIPT_DIR"/.claude/skills/fleece-*.md; do
    dest="$TARGET/$(basename "$f")"
    [ "$(realpath "$f")" = "$(realpath "$dest" 2>/dev/null)" ] && continue
    cp "$f" "$dest"
  done
  echo "✓ Claude Code skills installed to $TARGET/"
  echo "  Research:    /fleece-card /fleece-rates /fleece-partners /fleece-credits"
  echo "               /fleece-news /fleece-compare /fleece-wallet /fleece-roi /fleece-recommend"
  echo "  Redemption:  /fleece-mcc /fleece-flights /fleece-hotels"
  echo "  Profile:     /fleece-profile"
}

install_agents() {
  TARGET=".agents/skills/fleece"
  mkdir -p "$TARGET"
  src="$SCRIPT_DIR/.agents/skills/fleece/SKILL.md"
  dest="$TARGET/SKILL.md"
  [ "$(realpath "$src")" != "$(realpath "$dest" 2>/dev/null)" ] && cp "$src" "$dest"
  echo "✓ Agent skill installed to $TARGET/SKILL.md"
}

install_gemini() {
  src="$SCRIPT_DIR/GEMINI.md"
  [ "$(realpath "$src")" = "$(realpath "GEMINI.md" 2>/dev/null)" ] && return
  cp "$src" "GEMINI.md"
  echo "✓ Gemini CLI context installed to GEMINI.md"
}

install_copilot() {
  mkdir -p ".github"
  src="$SCRIPT_DIR/.github/copilot-instructions.md"
  dest=".github/copilot-instructions.md"
  [ "$(realpath "$src")" = "$(realpath "$dest" 2>/dev/null)" ] && return
  cp "$src" "$dest"
  echo "✓ GitHub Copilot instructions installed to $dest"
}

install_cursor() {
  mkdir -p ".cursor/rules"
  src="$SCRIPT_DIR/.cursor/rules/fleece.mdc"
  dest=".cursor/rules/fleece.mdc"
  [ "$(realpath "$src")" = "$(realpath "$dest" 2>/dev/null)" ] && return
  cp "$src" "$dest"
  echo "✓ Cursor rule installed to $dest"
}

install_windsurf() {
  src="$SCRIPT_DIR/.windsurfrules"
  [ "$(realpath "$src")" = "$(realpath ".windsurfrules" 2>/dev/null)" ] && return
  cp "$src" ".windsurfrules"
  echo "✓ Windsurf rules installed to .windsurfrules"
}

auto_detect() {
  INSTALLED=0
  if [ -d ".claude" ];    then install_claude;   INSTALLED=1; fi
  if [ -d ".agents" ];    then install_agents;   INSTALLED=1; fi
  if [ -d ".gemini" ] || command -v gemini &>/dev/null; then install_gemini;   INSTALLED=1; fi
  if [ -d ".github" ];    then install_copilot;  INSTALLED=1; fi
  if [ -d ".cursor" ];    then install_cursor;   INSTALLED=1; fi
  if [ -d ".windsurf" ] || [ -f ".windsurfrules" ]; then install_windsurf; INSTALLED=1; fi
  if [ "$INSTALLED" -eq 0 ]; then
    echo "No agent directory detected. Pass --all to install everything."
    exit 1
  fi
}

case "${1:-auto}" in
  --claude)   install_claude ;;
  --agents)   install_agents ;;
  --gemini)   install_gemini ;;
  --copilot)  install_copilot ;;
  --cursor)   install_cursor ;;
  --windsurf) install_windsurf ;;
  --all)      install_claude; install_agents; install_gemini; install_copilot; install_cursor; install_windsurf ;;
  auto)       auto_detect ;;
  *)          echo "Usage: bash install.sh [--claude|--agents|--gemini|--copilot|--cursor|--windsurf|--all]"; exit 1 ;;
esac

echo ""
echo ""
echo "BRAVE_API_KEY is optional — mcc, flights, hotels, and profile work without it."
echo "Set BRAVE_API_KEY in your environment or .env file to enable live research commands."
