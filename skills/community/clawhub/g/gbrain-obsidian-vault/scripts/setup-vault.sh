#!/usr/bin/env bash
# Wire OpenClaw memory + gbrain wiki for Obsidian — idempotent.
set -euo pipefail

WIKI_DIR="${WIKI_DIR:-$HOME/wiki}"
MEMORY_DIR="${MEMORY_DIR:-$HOME/.openclaw/workspace/memory}"
OBSIDIAN_DIR="$WIKI_DIR/.obsidian"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
log() { echo -e "${GREEN}[gbrain-obsidian-vault]${NC} $*"; }
warn() { echo -e "${YELLOW}[gbrain-obsidian-vault]${NC} $*"; }
fail() { echo -e "${RED}[gbrain-obsidian-vault]${NC} $*" >&2; exit 1; }

[[ -d "$WIKI_DIR" ]] || fail "Wiki dir not found: $WIKI_DIR (set WIKI_DIR=...)"
[[ -d "$MEMORY_DIR" ]] || fail "Memory dir not found: $MEMORY_DIR (set MEMORY_DIR=...)"

# --- memory symlink ---
if [[ -L "$WIKI_DIR/memory" ]]; then
  log "memory symlink already exists"
elif [[ -e "$WIKI_DIR/memory" ]]; then
  fail "$WIKI_DIR/memory exists and is not a symlink — resolve manually"
else
  ln -s "$MEMORY_DIR" "$WIKI_DIR/memory"
  log "Created symlink: $WIKI_DIR/memory -> $MEMORY_DIR"
fi

# --- .gitignore ---
GITIGNORE="$WIKI_DIR/.gitignore"
touch "$GITIGNORE"
append_ignore() {
  local line="$1"
  grep -qxF "$line" "$GITIGNORE" 2>/dev/null || echo "$line" >>"$GITIGNORE"
}
append_ignore ".obsidian/"
append_ignore "memory"
append_ignore ".raw/"
append_ignore ".DS_Store"
log "Ensured .gitignore entries (memory, .obsidian, .raw)"

# --- Obsidian config ---
mkdir -p "$OBSIDIAN_DIR"
cat >"$OBSIDIAN_DIR/app.json" <<'JSON'
{
  "useMarkdownLinks": false,
  "newLinkFormat": "absolute",
  "alwaysUpdateLinks": false,
  "showUnsupportedFiles": false,
  "attachmentFolderPath": "./",
  "promptDelete": true
}
JSON

cat >"$OBSIDIAN_DIR/core-plugins.json" <<'JSON'
{
  "file-explorer": true,
  "global-search": true,
  "switcher": true,
  "graph": true,
  "backlink": true,
  "outgoing-link": true,
  "tag-pane": true,
  "page-preview": true,
  "daily-notes": false,
  "templates": false,
  "note-composer": true,
  "command-palette": true,
  "editor-status": true,
  "outline": true,
  "word-count": true,
  "file-recovery": true
}
JSON
log "Wrote Obsidian config (wikilink mode, absolute paths, no auto relink)"

# --- summary ---
MD_COUNT=$(find "$WIKI_DIR" -name "*.md" -not -path "*/.obsidian/*" -not -path "*/memory/*" 2>/dev/null | wc -l | tr -d ' ')
MEM_COUNT=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

echo ""
log "Vault ready: $WIKI_DIR"
log "  gbrain .md files (excl memory): $MD_COUNT"
log "  memory diaries (via symlink):   $MEM_COUNT"
echo ""
log "Next steps:"
echo "  1. Open Obsidian → Open folder as vault → $WIKI_DIR"
echo "  2. If graph feels sparse: gbrain export --dir $WIKI_DIR"
echo "  3. Graph view (left ribbon) → explore clusters"
