#!/usr/bin/env bash
# completion-cue · remove.sh
# Restore every patched OpenClaw Control UI bundle from .milly.bak.
set -euo pipefail

red()    { printf '\033[31m%s\033[0m\n' "$*"; }
green()  { printf '\033[32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }
dim()    { printf '\033[2m%s\033[0m\n' "$*"; }

CANDIDATES=()
[[ -n "${OPENCLAW_HOME:-}" && -d "$OPENCLAW_HOME" ]] && CANDIDATES+=("$OPENCLAW_HOME")
command -v npm  >/dev/null 2>&1 && { R="$(npm  root -g 2>/dev/null || true)"; [[ -n "$R" && -d "$R/openclaw" ]] && CANDIDATES+=("$R/openclaw"); }
command -v pnpm >/dev/null 2>&1 && { R="$(pnpm root -g 2>/dev/null || true)"; [[ -n "$R" && -d "$R/openclaw" ]] && CANDIDATES+=("$R/openclaw"); }
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

for NVM_BASE in "$HOME/.nvm/versions/node" "/usr/local/n/versions/node"; do
  [[ -d "$NVM_BASE" ]] || continue
  while IFS= read -r d; do
    [[ -n "$d" ]] && CANDIDATES+=("$d")
  done < <(find "$NVM_BASE" -maxdepth 4 -path "*/lib/node_modules/openclaw" -type d 2>/dev/null)
done

# Dedupe
DEDUPED=()
for R in "${CANDIDATES[@]}"; do
  skip=0
  if [[ ${#DEDUPED[@]} -gt 0 ]]; then
    for E in "${DEDUPED[@]}"; do [[ "$E" == "$R" ]] && { skip=1; break; }; done
  fi
  [[ $skip -eq 0 ]] && DEDUPED+=("$R")
done
CANDIDATES=("${DEDUPED[@]}")

ANY=0
for ROOT in "${CANDIDATES[@]}"; do
  for REL_BASE in "dist/control-ui" "ui/dist"; do
    BASE="$ROOT/$REL_BASE"
    ASSETS="$BASE/assets"
    [[ -d "$ASSETS" ]] || continue
    INDEX_HTML="$BASE/index.html"

    # Restore index.html
    if [[ -f "$INDEX_HTML.milly.bak" ]]; then
      cp "$INDEX_HTML.milly.bak" "$INDEX_HTML"
      rm -f "$INDEX_HTML.milly.bak"
      green "✓ Restored $INDEX_HTML"
      ANY=1
    fi

    # Restore every patched bundle. Two cases:
    #   (a) appended-in-place: name = index-XXX.js, bak at index-XXX.js.milly.bak
    #   (b) cache-busted rename: name = index-XXX.milly-NNN.js, bak alongside it
    shopt -s nullglob
    for BAK in "$ASSETS"/index-*.js.milly.bak; do
      JS="${BAK%.milly.bak}"
      if [[ "$JS" == *.milly-*.js ]]; then
        # Cache-busted: restore original name from bak, drop renamed file
        ORIG="$(echo "$JS" | sed -E 's/\.milly-[0-9]+\.js$/.js/')"
        cp "$BAK" "$ORIG"
        rm -f "$BAK" "$JS"
        green "✓ Restored $ORIG (removed cache-busted $(basename "$JS"))"
      else
        cp "$BAK" "$JS"
        rm -f "$BAK"
        green "✓ Restored $JS"
      fi
      ANY=1
    done

    # Catch any bakless patched leftover
    for JS in "$ASSETS"/index-*.js; do
      [[ -f "$JS" ]] || continue
      if grep -q '__milly_cue_v1__' "$JS"; then
        yellow "⚠ Patched bundle without backup: $JS"
        yellow "  Leaving as-is. Run \`openclaw update --force\` or reinstall to fully reset."
      fi
    done
    shopt -u nullglob
  done
done

[[ $ANY -eq 0 ]] && dim "Nothing to remove (no .milly.bak found in known dist dirs)."
