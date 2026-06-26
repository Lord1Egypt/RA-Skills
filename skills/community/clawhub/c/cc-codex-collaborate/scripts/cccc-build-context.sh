#!/usr/bin/env bash
# Build context bundle for Codex review.
# Includes workspace files, git status, diff, and untracked files.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/cccc-common.sh"

ROOT="$(cccc_repo_root)"
cd "$ROOT"
cccc_init_dirs
NOW="$(cccc_now)"
OUT="docs/cccc/context-bundle.md"

# Maximum preview size for untracked files
MAX_LINES=200
MAX_SIZE_KB=20

# Helper to read a file with limit
read_file() {
  local file="$1"
  echo "\n## $file"
  if [[ -f "$file" ]]; then
    sed -n '1,240p' "$file"
  else
    echo "Missing: $file"
  fi
}

# Helper to check if file is safe to preview
is_safe_file() {
  local file="$1"
  # Skip secrets, keys, binary files, etc.
  case "$file" in
    *.env|*.pem|*.key|*.keystore|*.secret|*.credentials|*.token|*.jwt|*.private|*.wallet|*.seed|*secrets*|*credentials*)
      return 1
      ;;
    *.bin|*.exe|*.dll|*.so|*.dylib|*.class|*.jar|*.war|*.zip|*.tar|*.gz|*.png|*.jpg|*.jpeg|*.gif|*.pdf|*.mp4|*.mp3|*.wav)
      return 1
      ;;
    .git/*|.claude/settings*|.claude/hooks/*)
      return 1
      ;;
  esac

  # Check if binary file
  if file "$file" 2>/dev/null | grep -qE 'binary|executable|ELF|PE32|PDF|image|audio|video'; then
    return 1
  fi

  # Check file size
  local size_kb
  size_kb="$(du -k "$file" 2>/dev/null | cut -f1)"
  if [[ -n "$size_kb" && "$size_kb" -gt "$MAX_SIZE_KB" ]]; then
    return 1
  fi

  return 0
}

{
  echo "# CCCC Context Bundle"
  echo ""
  echo "Generated: $NOW"
  echo ""
  read_file "docs/cccc/state.json"
  read_file "docs/cccc/config.json"
  read_file "docs/cccc/project-brief.md"
  read_file "docs/cccc/project-map.md"
  read_file "docs/cccc/current-state.md"
  read_file "docs/cccc/architecture.md"
  read_file "docs/cccc/test-strategy.md"
  read_file "docs/cccc/roadmap.md"
  read_file "docs/cccc/milestone-backlog.md"
  read_file "docs/cccc/decision-log.md"
  read_file "docs/cccc/risk-register.md"
  read_file "docs/cccc/open-questions.md"

  echo "\n## Git status"
  git status --short 2>/dev/null || true

  echo "\n## Git diff stat"
  git diff --stat 2>/dev/null || true

  echo "\n## Git diff"
  git diff -- . ':!docs/cccc/context-bundle.md' 2>/dev/null || true

  echo "\n## Untracked Files"
  echo "Listing untracked files:"
  git ls-files --others --exclude-standard 2>/dev/null || true

  echo ""
  echo "### Untracked File Contents"
  echo "Preview of safe small untracked text files:"
  echo ""

  # Preview untracked files
  while IFS= read -r file; do
    [[ -n "$file" ]] || continue
    if [[ -f "$file" ]] && is_safe_file "$file"; then
      echo "---"
      echo "### $file"
      echo ""
      sed -n "1,${MAX_LINES}p" "$file" 2>/dev/null || echo "(cannot read)"
      echo ""
    fi
  done < <(git ls-files --others --exclude-standard 2>/dev/null)

  echo "\n## Recent logs"
  find docs/cccc/logs -type f -maxdepth 1 -print -exec tail -80 {} \; 2>/dev/null || true

  echo "\n## Recent reviews"
  find docs/cccc/reviews -type f -name '*.json' -maxdepth 3 -print -exec tail -120 {} \; 2>/dev/null || true

} > "$OUT"

echo "$OUT"