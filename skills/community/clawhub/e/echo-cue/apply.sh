#!/usr/bin/env bash
# completion-cue · apply.sh
# Idempotent local patch: append a Web Audio "ding" IIFE to the OpenClaw
# Control UI bundle. Patches **every** OpenClaw install we can find (brew + nvm),
# because Gateway might run under a different one than `which openclaw` resolves.
# Skips itself when upstream PR #73894 (or equivalent) has landed.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAYLOAD="$SKILL_DIR/inject/completion-cue.iife.js"
MARKER="__milly_cue_v1__"
UPSTREAM_MARKER="responseCompletionSound"

[[ -f "$PAYLOAD" ]] || { echo "✗ payload missing: $PAYLOAD" >&2; exit 2; }

red()    { printf '\033[31m%s\033[0m\n' "$*"; }
green()  { printf '\033[32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }
dim()    { printf '\033[2m%s\033[0m\n' "$*"; }

# ---------- collect every OpenClaw install root we can find ----------
CANDIDATES=()

[[ -n "${OPENCLAW_HOME:-}" && -d "$OPENCLAW_HOME" ]] && CANDIDATES+=("$OPENCLAW_HOME")

if command -v npm >/dev/null 2>&1; then
  R="$(npm root -g 2>/dev/null || true)"
  [[ -n "$R" && -d "$R/openclaw" ]] && CANDIDATES+=("$R/openclaw")
fi
if command -v pnpm >/dev/null 2>&1; then
  R="$(pnpm root -g 2>/dev/null || true)"
  [[ -n "$R" && -d "$R/openclaw" ]] && CANDIDATES+=("$R/openclaw")
fi

if command -v openclaw >/dev/null 2>&1; then
  RES="$(command -v openclaw)"
  command -v realpath >/dev/null 2>&1 && RES="$(realpath "$RES" 2>/dev/null || echo "$RES")"
  CUR="$(dirname "$RES")"
  for _ in 1 2 3 4 5 6; do
    if [[ -f "$CUR/package.json" ]] && grep -q '"name": *"openclaw"' "$CUR/package.json" 2>/dev/null; then
      CANDIDATES+=("$CUR"); break
    fi
    NEXT="$(dirname "$CUR")"; [[ "$NEXT" == "$CUR" ]] && break; CUR="$NEXT"
  done
fi

# Walk every nvm/n node version (gateway may run under a different node than `which openclaw`)
for NVM_BASE in "$HOME/.nvm/versions/node" "/usr/local/n/versions/node"; do
  [[ -d "$NVM_BASE" ]] || continue
  while IFS= read -r d; do
    [[ -n "$d" ]] && CANDIDATES+=("$d")
  done < <(find "$NVM_BASE" -maxdepth 4 -path "*/lib/node_modules/openclaw" -type d 2>/dev/null)
done

# Dedupe (preserve order)
DEDUPED=("")  # placeholder so set -u doesn't bite on empty array expansion
DEDUPED=()
for R in "${CANDIDATES[@]}"; do
  skip=0
  if [[ ${#DEDUPED[@]} -gt 0 ]]; then
    for E in "${DEDUPED[@]}"; do [[ "$E" == "$R" ]] && { skip=1; break; }; done
  fi
  [[ $skip -eq 0 ]] && DEDUPED+=("$R")
done
CANDIDATES=("${DEDUPED[@]}")

[[ ${#CANDIDATES[@]} -eq 0 ]] && { red "✗ No OpenClaw install found."; exit 3; }

# ---------- patch every install that has a Control UI dist ----------
PATCHED_ANY=0
SKIPPED_NO_DIST=()
for ROOT in "${CANDIDATES[@]}"; do
  CAND_BASE=""
  for REL in "dist/control-ui" "ui/dist"; do
    [[ -d "$ROOT/$REL/assets" ]] && { CAND_BASE="$ROOT/$REL"; break; }
  done
  if [[ -z "$CAND_BASE" ]]; then
    SKIPPED_NO_DIST+=("$ROOT")
    continue
  fi
  ASSETS="$CAND_BASE/assets"
  INDEX_HTML="$CAND_BASE/index.html"

  # Find current entry bundle from index.html (more reliable than listing files,
  # since previous renames may leave stale .milly-*.js around).
  ENTRY_NAME=""
  if [[ -f "$INDEX_HTML" ]]; then
    ENTRY_NAME="$(grep -oE 'src="[^"]*assets/index-[^"]*\.js"' "$INDEX_HTML" | head -n1 | sed 's|.*/||;s|"$||')"
  fi
  if [[ -z "$ENTRY_NAME" ]]; then
    ENTRY_NAME="$(ls -1t "$ASSETS"/index-*.js 2>/dev/null | head -n1 | xargs -n1 basename || true)"
  fi
  [[ -z "$ENTRY_NAME" ]] && { yellow "⚠ no entry bundle in $ASSETS, skipping"; continue; }

  DIST_JS="$ASSETS/$ENTRY_NAME"
  [[ -f "$DIST_JS" ]] || { yellow "⚠ entry $DIST_JS missing, skipping"; continue; }

  dim "→ openclaw root: $ROOT"
  dim "→ entry bundle:  $DIST_JS"

  if grep -q "$UPSTREAM_MARKER" "$DIST_JS"; then
    yellow "⚠ Upstream cue already shipped at $ROOT, skipping."
    continue
  fi

  if grep -q "$MARKER" "$DIST_JS"; then
    green "✓ Already patched at $ROOT."
    PATCHED_ANY=1
    continue
  fi

  # Backup + inject
  [[ -f "$DIST_JS.milly.bak" ]] || cp "$DIST_JS" "$DIST_JS.milly.bak"
  {
    printf '\n;/* milly:completion-cue v0.1 */\n'
    cat "$PAYLOAD"
  } >> "$DIST_JS"

  if ! grep -q "$MARKER" "$DIST_JS"; then
    red "✗ Patch append failed at $ROOT, restoring."
    cp "$DIST_JS.milly.bak" "$DIST_JS"
    continue
  fi

  # Cache-bust: rename and update index.html
  if [[ -f "$INDEX_HTML" ]]; then
    if [[ "$ENTRY_NAME" == *.milly-*.js ]]; then
      dim "→ already cache-busted ($ENTRY_NAME)"
    else
      BUST="milly-$(date +%s | tail -c 6)"
      NEW_NAME="${ENTRY_NAME%.js}.${BUST}.js"
      NEW_PATH="$ASSETS/$NEW_NAME"
      mv "$DIST_JS" "$NEW_PATH"
      [[ -f "$DIST_JS.milly.bak" ]] && mv "$DIST_JS.milly.bak" "$NEW_PATH.milly.bak"
      [[ -f "$INDEX_HTML.milly.bak" ]] || cp "$INDEX_HTML" "$INDEX_HTML.milly.bak"
      sed -i.tmp "s|$ENTRY_NAME|$NEW_NAME|g" "$INDEX_HTML" && rm -f "$INDEX_HTML.tmp"
      green "✓ Patched + cache-busted: $ENTRY_NAME → $NEW_NAME"
    fi
  else
    yellow "⚠ index.html not found at $INDEX_HTML; cache may persist."
  fi

  PATCHED_ANY=1
done

if [[ $PATCHED_ANY -eq 0 ]]; then
  red "✗ No Control UI dist found in any OpenClaw install."
  if [[ ${#SKIPPED_NO_DIST[@]} -gt 0 ]]; then
    for r in "${SKIPPED_NO_DIST[@]}"; do echo "    - $r (no dist/control-ui or ui/dist)" >&2; done
  fi
  exit 3
fi

dim "  Refresh your Control UI tab to activate (regular Cmd+R is enough; cache-busted)."
dim "  Disable per browser:  localStorage.setItem('milly.completionCue', 'off')"
