#!/usr/bin/env bash
# One-line install (multi-host by default):
#   macOS/Linux:
#     curl -fsSL https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.sh | bash
#   Windows PowerShell:
#     irm https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.ps1 | iex
#
# Clones once to ~/.agent-expression/skill, then symlinks into mainstream
# Agent / IDE skill directories (Cursor, Claude Code, Codex, Agents, Hermes…).
#
# Flags:
#   --all                 multi-host links (default)
#   --project             also link into cwd: .agents/.cursor/.claude skills
#   --hermes|--cursor|--claude|--codex|--agents|--home
#                         single target only (no multi-link)
#   --dir PATH            custom clone/link directory
#   --no-link             clone only, do not create host links
#   --pack                ensure meme-packs/.../memes exists
#   -h|--help
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/yyh-001/agent-expression.git}"
BRANCH="${BRANCH:-main}"
MODE="${INSTALL_MODE:-all}"          # all | single | project-extra
INSTALL_TARGET="${INSTALL_TARGET:-}" # when MODE=single
INSTALL_DIR="${INSTALL_DIR:-}"
WANT_PACK=0
NO_LINK=0
WANT_PROJECT=0
SKILL_NAME="agent-expression"

usage() {
  cat <<'EOF'
Install agent-expression for mainstream Agents / IDEs.

  curl -fsSL https://raw.githubusercontent.com/yyh-001/agent-expression/main/install.sh | bash

Default: clone → ~/.agent-expression/skill, symlink into:
  ~/.agents/skills/agent-expression     (Codex / Cursor / cross-tool)
  ~/.cursor/skills/agent-expression     (Cursor IDE)
  ~/.claude/skills/agent-expression     (Claude Code)
  ~/.codex/skills/agent-expression      (Codex legacy)
  ~/.hermes/skills/media/agent-expression  (if ~/.hermes exists)

Options:
  --all                 multi-host (default)
  --project             also link into current repo (.agents / .cursor / .claude)
  --hermes|--cursor|--claude|--codex|--agents|--home
  --dir PATH            custom destination
  --no-link             clone only
  --pack                mkdir meme pack tree
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage ;;
    --all) MODE=all ;;
    --project) WANT_PROJECT=1 ;;
    --no-link) NO_LINK=1 ;;
    --pack) WANT_PACK=1 ;;
    --hermes) MODE=single; INSTALL_TARGET=hermes ;;
    --cursor) MODE=single; INSTALL_TARGET=cursor ;;
    --claude) MODE=single; INSTALL_TARGET=claude ;;
    --codex) MODE=single; INSTALL_TARGET=codex ;;
    --agents) MODE=single; INSTALL_TARGET=agents ;;
    --home) MODE=single; INSTALL_TARGET=home ;;
    --dir)
      MODE=single
      INSTALL_TARGET=custom
      INSTALL_DIR="${2:-}"
      [[ -n "$INSTALL_DIR" ]] || { echo "ERROR: --dir needs a path" >&2; exit 2; }
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 2
      ;;
  esac
  shift
done

abs_path() {
  # Resolve to absolute path; create parent if needed.
  local p="$1"
  local parent base
  parent="$(dirname "$p")"
  base="$(basename "$p")"
  mkdir -p "$parent"
  (cd "$parent" && printf '%s/%s\n' "$(pwd -P)" "$base")
}

single_dest() {
  case "$INSTALL_TARGET" in
    hermes) echo "${HERMES_HOME:-$HOME/.hermes}/skills/media/${SKILL_NAME}" ;;
    cursor) echo "${HOME}/.cursor/skills/${SKILL_NAME}" ;;
    claude) echo "${HOME}/.claude/skills/${SKILL_NAME}" ;;
    codex)  echo "${CODEX_HOME:-$HOME/.codex}/skills/${SKILL_NAME}" ;;
    agents) echo "${HOME}/.agents/skills/${SKILL_NAME}" ;;
    home)   echo "${MEME_HOME:-$HOME/.agent-expression}/skill" ;;
    custom) echo "$INSTALL_DIR" ;;
    *) echo "${MEME_HOME:-$HOME/.agent-expression}/skill" ;;
  esac
}

CANON="${MEME_HOME:-$HOME/.agent-expression}/skill"
if [[ "$MODE" == "single" ]]; then
  CANON="$(single_dest)"
fi
CANON="$(abs_path "$CANON")"

clone_or_update() {
  local dest="$1"
  echo "==> Skill content → $dest"
  if command -v git >/dev/null 2>&1; then
    if [[ -d "$dest/.git" ]]; then
      echo "==> Existing git install, updating…"
      git -C "$dest" fetch --depth 1 origin "$BRANCH"
      git -C "$dest" checkout -q "$BRANCH"
      git -C "$dest" reset --hard "origin/$BRANCH"
    elif [[ -L "$dest" ]]; then
      echo "ERROR: $dest is a symlink; remove it or use --dir" >&2
      exit 1
    else
      rm -rf "$dest"
      mkdir -p "$(dirname "$dest")"
      git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$dest"
    fi
  else
    echo "ERROR: git is required" >&2
    exit 1
  fi
}

link_into() {
  local target="$1"
  local parent
  parent="$(dirname "$target")"
  mkdir -p "$parent"
  if [[ "$target" == "$CANON" ]]; then
    return 0
  fi
  if [[ -L "$target" ]]; then
    rm -f "$target"
  elif [[ -e "$target" ]]; then
    echo "==> skip (exists, not a symlink): $target"
    return 0
  fi
  if ln -sfn "$CANON" "$target" 2>/dev/null; then
    echo "==> link $target → $CANON"
  else
    echo "==> symlink failed, copying → $target"
    rm -rf "$target"
    mkdir -p "$parent"
    cp -a "$CANON" "$target"
  fi
}

collect_host_links() {
  # stdout: one path per line
  echo "${HOME}/.agents/skills/${SKILL_NAME}"
  echo "${HOME}/.cursor/skills/${SKILL_NAME}"
  echo "${HOME}/.claude/skills/${SKILL_NAME}"
  echo "${CODEX_HOME:-$HOME/.codex}/skills/${SKILL_NAME}"
  if [[ -d "${HERMES_HOME:-$HOME/.hermes}" ]]; then
    echo "${HERMES_HOME:-$HOME/.hermes}/skills/media/${SKILL_NAME}"
  fi
  if [[ "$WANT_PROJECT" -eq 1 ]]; then
    echo "$(pwd)/.agents/skills/${SKILL_NAME}"
    echo "$(pwd)/.cursor/skills/${SKILL_NAME}"
    echo "$(pwd)/.claude/skills/${SKILL_NAME}"
  fi
}

clone_or_update "$CANON"

LINKED=()
if [[ "$NO_LINK" -eq 0 && "$MODE" == "all" ]]; then
  while IFS= read -r t; do
    [[ -z "$t" ]] && continue
    link_into "$(abs_path "$t")"
    LINKED+=("$t")
  done < <(collect_host_links)
elif [[ "$NO_LINK" -eq 0 && "$WANT_PROJECT" -eq 1 ]]; then
  while IFS= read -r t; do
    [[ -z "$t" ]] && continue
    link_into "$(abs_path "$t")"
    LINKED+=("$t")
  done < <(collect_host_links)
fi

# Data / pack root — prefer bundled pack (images + captions + embeddings)
if [[ -d "${HERMES_HOME:-$HOME/.hermes}/meme-packs" ]]; then
  DATA_HOME="${HERMES_HOME:-$HOME/.hermes}"
else
  DATA_HOME="${MEME_HOME:-$HOME/.agent-expression}"
fi
PACK_DIR="${MEME_PACK:-$DATA_HOME/meme-packs/${MEME_PACK_ID:-official-001}}"
BUNDLED="$CANON/packs/official-001"

deploy_bundled_pack() {
  local dest="$1"
  local src="$2"
  [[ -f "$src/index.db" && -d "$src/memes" ]] || return 1
  mkdir -p "$dest"
  # Copy images if missing / incomplete; always refresh portable index when absent or --pack
  if [[ ! -d "$dest/memes" ]] || [[ "$WANT_PACK" -eq 1 ]]; then
    rm -rf "$dest/memes"
    cp -a "$src/memes" "$dest/"
  fi
  if [[ ! -f "$dest/index.db" ]] || [[ "$WANT_PACK" -eq 1 ]]; then
    cp -a "$src/index.db" "$dest/index.db"
  fi
  [[ -f "$src/manifest.json" ]] && cp -a "$src/manifest.json" "$dest/"
  [[ -f "$src/CREDITS.md" ]] && cp -a "$src/CREDITS.md" "$dest/"
  echo "==> Bundled pack ready: $dest (index + embeddings included)"
  return 0
}

if deploy_bundled_pack "$PACK_DIR" "$BUNDLED"; then
  :
elif [[ "$WANT_PACK" -eq 1 ]] || [[ ! -d "$PACK_DIR/memes" ]]; then
  mkdir -p "$PACK_DIR/memes"
  echo "==> Pack dir ready: $PACK_DIR/memes/<tag>/ (no bundled pack in this checkout)"
fi

echo
echo "OK. agent-expression ready."
echo
echo "  Content:  $CANON"
echo "  Pack:     $PACK_DIR"
if [[ ${#LINKED[@]} -gt 0 ]]; then
  echo "  Linked:"
  for t in "${LINKED[@]}"; do
    echo "    - $t"
  done
fi
cat <<EOF

Next (bundled pack already searchable):
  python3 "$CANON/scripts/search-meme.py" "无语" --pick

Optional re-index / re-embed only if you change files or model:
  python3 "$CANON/scripts/index-memes.py" --sync-only
  python3 "$CANON/scripts/embed-memes.py"

Hosts & delivery: $CANON/references/hosts.md
Agent rules:      $CANON/SKILL.md

EOF
