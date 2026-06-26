#!/usr/bin/env bash
# =============================================================================
# pre-generation-hook.sh
# AI Personal Brand Growth Engine — Pre-Generation Context Injector
# Run before any content generation session to prime the AI context.
# Outputs an injection block ready to prepend to your prompt.
# =============================================================================

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────────────────
VIRAL_FORMULAS="./assets/VIRAL_FORMULAS.md"
AUDIENCE_PERSONA="./AUDIENCE_PERSONA.md"
SOUL="./SOUL.md"
CONTENT_DIR="./.content"

BOLD='\033[1m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RESET='\033[0m'

# ── Gather context ────────────────────────────────────────────────────────────
formula_count=0
if [[ -f "$VIRAL_FORMULAS" ]]; then
  formula_count=$(grep -c "^\*\*Formula ID:\*\*" "$VIRAL_FORMULAS" 2>/dev/null || echo 0)
fi

failure_count=0
if [[ -f "$SOUL" ]]; then
  failure_count=$(grep -c "^\*\*Avoid Pattern\*\*\|^### Avoid" "$SOUL" 2>/dev/null || echo 0)
fi

persona_status="⚠ MISSING — setup required before generation"
[[ -f "$AUDIENCE_PERSONA" && -s "$AUDIENCE_PERSONA" ]] && persona_status="Loaded ✓"

soul_status="⚠ MISSING — setup required before generation"
[[ -f "$SOUL" && -s "$SOUL" ]] && soul_status="Loaded ✓"

today=$(date +%Y-%m-%d)
today_stamp=$(date +%Y%m%d)

# ── Count today's posts by pillar ─────────────────────────────────────────────
value_count=0; story_count=0; engagement_count=0; conversion_count=0

if compgen -G "${CONTENT_DIR}/POST-${today_stamp}-*.md" > /dev/null 2>&1; then
  for f in "${CONTENT_DIR}"/POST-"${today_stamp}"-*.md; do
    grep -qi "\[x\] Value"      "$f" 2>/dev/null && value_count=$((value_count+1))
    grep -qi "\[x\] Story"      "$f" 2>/dev/null && story_count=$((story_count+1))
    grep -qi "\[x\] Engagement" "$f" 2>/dev/null && engagement_count=$((engagement_count+1))
    grep -qi "\[x\] Conversion" "$f" 2>/dev/null && conversion_count=$((conversion_count+1))
  done
fi

value_gap=$(( 2 - value_count < 0 ? 0 : 2 - value_count ))
story_gap=$(( 1 - story_count < 0 ? 0 : 1 - story_count ))
engagement_gap=$(( 1 - engagement_count < 0 ? 0 : 1 - engagement_count ))
conversion_gap=$(( 1 - conversion_count < 0 ? 0 : 1 - conversion_count ))

# ── Output injection block ────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}${BOLD}║   PRE-GENERATION CONTEXT INJECTION BLOCK            ║${RESET}"
echo -e "${CYAN}${BOLD}║   Copy everything inside the ━━━ lines into prompt  ║${RESET}"
echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════════╝${RESET}"
echo ""

cat <<INJECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[HOOK: PRE-GENERATION CONTEXT LOAD — ${today}]

MEMORY FILES STATUS:
  • AUDIENCE_PERSONA.md : ${persona_status}
  • VIRAL_FORMULAS.md   : ${formula_count} promoted formula(s) loaded
  • SOUL.md             : ${soul_status} | ${failure_count} failure pattern(s) active

TODAY'S CONTENT PILLAR CHECKLIST:
  [ ] Value Delivery   — need ${value_gap} more  (target: 2)
  [ ] Personal Story   — need ${story_gap} more  (target: 1)
  [ ] Engagement Hook  — need ${engagement_gap} more  (target: 1)
  [ ] Conversion/Offer — need ${conversion_gap} more  (target: 1)

MANDATORY GENERATION RULES:
  ✦ Read AUDIENCE_PERSONA.md first — extract top 3 pain points
  ✦ Read VIRAL_FORMULAS.md — at least 1 post MUST use a promoted formula (state ID)
  ✦ Read SOUL.md — avoid any hook type or structure listed in Failure Library
  ✦ Every post MUST declare: Pillar + Hook-Type + Formula ID
  ✦ Exactly 1 conversion post required in today's batch
  ✦ After generation, create .content/POST-${today_stamp}-XXX.md for each post (Status: draft)

INSTRUCTION TO AI:
Generate today's 5-post content batch. Display this context load as a status
card first, then produce posts in labeled blocks (POST 1 of 5 ... POST 5 of 5),
each followed by its proposed .content/ filename and Status: draft.
[END HOOK]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INJECTION

echo ""
echo -e "${GREEN}${BOLD}✓ Injection block ready.${RESET}"
echo ""

# ── Warn if Brand Foundation is incomplete ─────────────────────────────────────
if [[ "$persona_status" == *"MISSING"* ]] || [[ "$soul_status" == *"MISSING"* ]]; then
  echo -e "${YELLOW}${BOLD}⚠  WARNING: Brand Foundation files are incomplete.${RESET}"
  echo -e "${YELLOW}   The AI will pause and run the Initialization Checklist.${RESET}"
  echo -e "${YELLOW}   Complete AUDIENCE_PERSONA.md and SOUL.md first for best results.${RESET}"
  echo ""
fi
