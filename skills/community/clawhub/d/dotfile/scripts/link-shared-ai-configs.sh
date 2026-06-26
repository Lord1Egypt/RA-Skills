#!/bin/bash
set -euo pipefail
# link-shared-ai-configs.sh
# Symlink shared AI configs folders to Claude and Gemini directories

AGENT_DIR="$HOME/.agents"
CLAUDE_DIR="$HOME/.claude"
CODEX_DIR="$HOME/.codex"
GEMINI_DIR="$HOME/.gemini"
ANTIGRAVITY_DIR="$GEMINI_DIR/antigravity"

# WSL: .agent is on Windows side, resolve via /mnt/c
if [[ -f /proc/version ]] && grep -qi microsoft /proc/version 2>/dev/null; then
  WIN_USER=$(cmd.exe /C "echo %USERNAME%" 2>/dev/null | tr -d '\r')
  if [[ -n "$WIN_USER" ]]; then
    AGENT_DIR="/mnt/c/Users/$WIN_USER/.agents"
  fi
fi

# Exit if shared directory doesn't exist
[[ ! -d "$AGENT_DIR" ]] && exit 0

# Helper: create folder symlink if not already linked
link_folder() {
  local src="$AGENT_DIR/$1"
  local dst="$2"

  if [[ -L "$dst" ]]; then
    local current_target=$(readlink "$dst")
    if [[ "$current_target" == "$src" ]]; then
      echo "✓ Already linked: $dst"
      return 0
    fi
  fi

  if [[ -e "$dst" || -L "$dst" ]]; then
    # Backup existing folder/file
    local backup_path="$(dirname "$dst")/.bak/$(basename "$dst")-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$(dirname "$dst")/.bak"
    echo "⚠️ Backing up: $dst → $backup_path"
    if ! mv "$dst" "$backup_path"; then
      echo "❌ Failed to backup $dst. Skipping."
      return 1
    fi
  fi

  # Ensure parent directory of destination exists
  mkdir -p "$(dirname "$dst")"

  echo "→ Creating symlink: $dst → $src"
  if ! ln -sfn "$src" "$dst"; then
    echo "❌ Failed to create symlink: $dst"
    return 1
  fi
}

# Skills
link_folder skills "$CLAUDE_DIR/skills"
link_folder skills "$CODEX_DIR/skills"
link_folder skills "$GEMINI_DIR/skills"
link_folder skills "$ANTIGRAVITY_DIR/skills"

# Rules
link_folder rules "$CLAUDE_DIR/rules"

# Agents -> Claude agents, Gemini global_workflows
link_folder agents "$CLAUDE_DIR/agents"
link_folder agents "$ANTIGRAVITY_DIR/global_workflows"
