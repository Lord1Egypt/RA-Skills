#!/usr/bin/env bash
# =============================================================================
# growth-reminder.sh
# AI Personal Brand Growth Engine — Session Start / End Auditor
# Scans .content/ for stale published posts and nudges the user to close loops.
# =============================================================================

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────────────────
CONTENT_DIR="./.content"
FEEDBACK_LOG="${CONTENT_DIR}/FEEDBACK_LOG.md"
STALE_THRESHOLD_DAYS=2
TODAY=$(date +%Y%m%d)

# ── Colors ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ── Helpers ───────────────────────────────────────────────────────────────────
print_header() {
  echo ""
  echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════${RESET}"
  echo -e "${CYAN}${BOLD}   📊 AI Personal Brand Growth Engine — Audit      ${RESET}"
  echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════${RESET}"
  echo ""
}

print_section() {
  echo -e "${BOLD}$1${RESET}"
  echo "───────────────────────────────────────────────────"
}

days_since() {
  local file_date="$1"
  local y="${file_date:0:4}"
  local m="${file_date:4:2}"
  local d="${file_date:6:2}"
  local then
  then=$(date -d "${y}-${m}-${d}" +%s 2>/dev/null \
    || date -j -f "%Y%m%d" "$file_date" +%s)
  local now
  now=$(date +%s)
  echo $(( (now - then) / 86400 ))
}

# ── Main Audit Logic ──────────────────────────────────────────────────────────
main() {
  print_header

  mkdir -p "$CONTENT_DIR"

  # Initialize FEEDBACK_LOG if missing
  if [[ ! -f "$FEEDBACK_LOG" ]]; then
    cat > "$FEEDBACK_LOG" <<'EOF'
# FEEDBACK_LOG.md
> Aggregated performance signals. Auto-appended by AI after each analyzed post.

| Date | Post ID | Platform | Hook-Type | ER% | Verdict | Key Signal |
|------|---------|----------|-----------|-----|---------|------------|
EOF
    echo -e "${GREEN}✓ Initialized FEEDBACK_LOG.md${RESET}"
  fi

  # ── Scan for stale [published] posts ────────────────────────────────────────
  stale_posts=()
  draft_posts=()
  analyzed_count=0
  total_posts=0

  if compgen -G "${CONTENT_DIR}/POST-*.md" > /dev/null 2>&1; then
    for post_file in "${CONTENT_DIR}"/POST-*.md; do
      total_posts=$((total_posts + 1))
      filename=$(basename "$post_file")

      status="unknown"
      if grep -q "\[x\] published\|\[X\] published" "$post_file" 2>/dev/null; then
        status="published"
      elif grep -q "\[x\] analyzed\|\[X\] analyzed" "$post_file" 2>/dev/null; then
        status="analyzed"
      elif grep -q "\[x\] draft\|\[X\] draft" "$post_file" 2>/dev/null; then
        status="draft"
      fi

      file_date=$(echo "$filename" | grep -oE '[0-9]{8}' | head -1)

      case "$status" in
        published)
          if [[ -n "$file_date" ]]; then
            age=$(days_since "$file_date" 2>/dev/null || echo "0")
            if (( age >= STALE_THRESHOLD_DAYS )); then
              stale_posts+=("${filename} (published ${age}d ago)")
            fi
          else
            stale_posts+=("${filename} (date unknown)")
          fi
          ;;
        draft)
          draft_posts+=("$filename")
          ;;
        analyzed)
          analyzed_count=$((analyzed_count + 1))
          ;;
      esac
    done
  fi

  # ── Report: Stale Published Posts ────────────────────────────────────────────
  if [[ ${#stale_posts[@]} -gt 0 ]]; then
    echo -e "${RED}${BOLD}⚠️  ACTION REQUIRED: ${#stale_posts[@]} post(s) awaiting data input${RESET}"
    echo ""
    print_section "📬 Posts Published — No Metrics Yet"
    for post in "${stale_posts[@]}"; do
      echo -e "  ${YELLOW}→ ${post}${RESET}"
    done
    echo ""
    echo -e "${BOLD}Feeding metrics back into the system is how this engine gets smarter.${RESET}"
    echo -e "Open each file above, fill in the Metrics section, then tell the AI:"
    echo -e "  ${CYAN}\"Here's the data for [post name]: X views, Y likes, Z comments\"${RESET}"
    echo ""
  else
    echo -e "${GREEN}✓ No stale published posts — all loops closed.${RESET}"
    echo ""
  fi

  # ── Report: Draft Posts ───────────────────────────────────────────────────────
  if [[ ${#draft_posts[@]} -gt 0 ]]; then
    print_section "📝 Drafts Awaiting Publish Decision"
    for post in "${draft_posts[@]}"; do
      echo -e "  ${YELLOW}→ ${post}${RESET}"
    done
    echo ""
    echo -e "Confirm which drafts you're publishing today so the AI can update their status."
    echo ""
  fi

  # ── Report: Progress Summary ─────────────────────────────────────────────────
  print_section "📈 Content Pipeline Summary"
  echo -e "  Total posts logged:      ${BOLD}${total_posts}${RESET}"
  echo -e "  Fully analyzed:          ${GREEN}${BOLD}${analyzed_count}${RESET}"
  echo -e "  Drafts pending:          ${YELLOW}${BOLD}${#draft_posts[@]}${RESET}"
  echo -e "  Published (needs data):  ${RED}${BOLD}${#stale_posts[@]}${RESET}"
  echo ""

  # ── Formula Library Check ─────────────────────────────────────────────────────
  formula_count=0
  if [[ -f "assets/VIRAL_FORMULAS.md" ]]; then
    formula_count=$(grep -c "^\*\*Formula ID:\*\*" "assets/VIRAL_FORMULAS.md" 2>/dev/null || echo 0)
  fi

  if [[ "$formula_count" -eq 0 ]]; then
    echo -e "${YELLOW}⚡ VIRAL_FORMULAS.md is empty. Analyze your first post to trigger a Memory Leap.${RESET}"
  else
    echo -e "${GREEN}✓ ${formula_count} promoted formula(s) in VIRAL_FORMULAS.md — ready for next generation run.${RESET}"
  fi

  echo ""
  echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════${RESET}"
  echo -e "${CYAN}  Audit complete — $(date '+%Y-%m-%d %H:%M')${RESET}"
  echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════${RESET}"
  echo ""
}

main "$@"
