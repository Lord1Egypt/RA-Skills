#!/usr/bin/env bash
# english-memory-method installer v3 (Linux / macOS)
#
# One-liner (installs to EVERY detected agent platform):
#   curl -fsSL https://raw.githubusercontent.com/yxdwind/english-memory-method/main/install.sh | bash
#
# Install to specific platform(s), comma-separated:
#   ./install.sh claude,codex,trae
#
# Supported aliases:
#   autoclaw, openclaw, agents, claude, codex, trae, lingma, comate,
#   codebuddy, windsurf, continue, roo, kimi, qoder, qwen, workbuddy, minimax

set -euo pipefail

REPO="yxdwind/english-memory-method"
BRANCH="main"
SKILL="english-memory-method"
RAW="https://raw.githubusercontent.com/$REPO/$BRANCH"
FILES=("SKILL.md" "assets/plan-template.html")

# download sources with fallback: raw -> jsdelivr CDN (China-friendly)
SOURCES=("https://raw.githubusercontent.com/$REPO/$BRANCH" "https://cdn.jsdelivr.net/gh/$REPO@$BRANCH")

fetch() {
  local rel="$1" out="$2"
  for s in "${SOURCES[@]}"; do
    if curl -fsSL --max-time 25 "$s/$rel" -o "$out"; then
      echo "  [OK] $rel  <- $s"
      return 0
    fi
  done
  echo "  [FAIL] $rel (all sources)" >&2
  return 1
}

# platform alias -> skills dir (relative to $HOME)
declare -A PLATFORMS=(
  [autoclaw]=".openclaw-autoclaw/skills"
  [openclaw]=".openclaw/skills"
  [agents]=".agents/skills"
  [claude]=".claude/skills"
  [codex]=".codex/skills"
  [trae]=".trae/skills"
  [lingma]=".lingma/skills"
  [comate]=".comate/skills"
  [codebuddy]=".codebuddy/skills"
  [windsurf]=".windsurf/skills"
  [continue]=".continue/skills"
  [roo]=".roo/skills"
  [kimi]=".kimi-code/skills"
  [qoder]=".qoderwork/skills"
  [qwen]=".qwenworkcn/skills"
  [workbuddy]=".workbuddy/skills"
  [minimax]=".minimax/skills"
)

install_to() {
  local dir="$1"
  local dest="$dir/$SKILL"
  for f in "${FILES[@]}"; do
    mkdir -p "$(dirname "$dest/$f")"
    if ! fetch "$f" "$dest/$f"; then exit 1; fi
  done
  echo "$dest"
}

DESTS=()

if [ $# -gt 0 ] && [ -n "$1" ]; then
  TARGET="$1"
  if [ -d "$TARGET" ]; then
    echo "Custom target: $TARGET"
    DESTS+=("$(install_to "$TARGET")")
  else
    IFS=',' read -ra NAMES <<< "$TARGET"
    for name in "${NAMES[@]}"; do
      name=$(echo "$name" | tr '[:upper:]' '[:lower:]' | tr -d ' ')
      if [[ -n "${PLATFORMS[$name]:-}" ]]; then
        dir="$HOME/${PLATFORMS[$name]}"
        mkdir -p "$dir"
        echo "Platform [$name] -> $dir"
        DESTS+=("$(install_to "$dir")")
      else
        echo "WARNING: unknown platform alias: $name" >&2
      fi
    done
  fi
else
  echo "Auto-detecting agent platforms..."
  FOUND=0
  for name in "${!PLATFORMS[@]}"; do
    dir="$HOME/${PLATFORMS[$name]}"
    if [ -d "$dir" ]; then
      FOUND=$((FOUND+1))
      echo "Platform [$name] detected -> $dir"
      DESTS+=("$(install_to "$dir")")
    fi
  done
  if [ "$FOUND" -eq 0 ]; then
    echo "WARNING: no known platform found - falling back to Claude Code default"
    dir="$HOME/${PLATFORMS[claude]}"
    mkdir -p "$dir"
    DESTS+=("$(install_to "$dir")")
  fi
fi

echo ""
echo "[DONE] $SKILL installed to ${#DESTS[@]} location(s):"
for d in "${DESTS[@]}"; do echo "  - $d"; done
echo ""
echo "Trigger: give your agent an English article and say"
echo '"memorization plan" / "memory tricks" / "bei song fang an".'
