#!/usr/bin/env bash
#
# skill-audit - Safety inspector for newly installed OpenClaw skills
#

set -uo pipefail

# Colors
RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

SKILL_PATH="${1:-}"

# Track severity: 0=pass, 1=warn, 2=fail
SEVERITY=0

print_info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
print_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; [[ $SEVERITY -lt 1 ]] && SEVERITY=1; }
print_fail()  { echo -e "${RED}[FAIL]${NC}  $*"; SEVERITY=2; }
print_pass()  { echo -e "${GREEN}[PASS]${NC}  $*"; }

header() {
  echo ""
  echo "========================================"
  echo "  skill-audit: $*"
  echo "========================================"
}

# ---- Argument check ----
if [[ -z "$SKILL_PATH" ]]; then
  echo "Usage: $0 <skill-path>"
  echo ""
  echo "Example:"
  echo "  $0 ~/.openclaw/skills/my-new-skill"
  echo "  $0 /workspace/skills/awesome-skill"
  exit 1
fi

# Normalize path
SKILL_PATH="$(realpath "$SKILL_PATH" 2>/dev/null || echo "$SKILL_PATH")"

header "Skill: $SKILL_PATH"

# ---- 1. Existence ----
if [[ ! -d "$SKILL_PATH" ]]; then
  print_fail "Skill directory does not exist: $SKILL_PATH"
  exit 2
fi
print_pass "Skill directory exists"

cd "$SKILL_PATH"

# ---- 2. Structure Validation ----
header "Structure Validation"

if [[ ! -f "SKILL.md" ]]; then
  print_fail "SKILL.md is missing"
else
  print_pass "SKILL.md exists"

  if ! grep -q "^# " SKILL.md; then
    print_warn "SKILL.md missing title (first line should be # Skill Name)"
  else
    print_pass "SKILL.md has title"
  fi

  if ! grep -q "^## Purpose" SKILL.md; then
    print_warn "SKILL.md missing '## Purpose' section"
  else
    print_pass "SKILL.md has Purpose section"
  fi

  if ! grep -q "^## When to Use" SKILL.md; then
    print_warn "SKILL.md missing '## When to Use' section"
  else
    print_pass "SKILL.md has When to Use section"
  fi
fi

for subdir in scripts references; do
  if [[ -d "$subdir" ]]; then
    print_info "Has $subdir/ directory"
  fi
done

if [[ -f "README.md" ]]; then
  print_pass "README.md present"
else
  print_warn "No README.md found (optional but recommended)"
fi

# ---- 3. Security Scan ----
header "Security Scan"

FOUND_CRITICAL=0
if grep -rqE "sk-[a-zA-Z0-9]{20,}" . --include="*.md" --include="*.sh" --include="*.js" --include="*.json" 2>/dev/null; then
  print_fail "Possible OpenAI/API key detected"
  FOUND_CRITICAL=1
fi
if grep -rqE "password\s*=\s*[\"']" . --include="*.md" --include="*.sh" --include="*.js" --include="*.json" 2>/dev/null; then
  print_fail "Possible hardcoded password detected"
  FOUND_CRITICAL=1
fi
if grep -rqE "api_key\s*=\s*[\"']" . --include="*.md" --include="*.sh" --include="*.js" --include="*.json" 2>/dev/null; then
  print_fail "Possible hardcoded api_key detected"
  FOUND_CRITICAL=1
fi
if grep -rqE "-----BEGIN.*PRIVATE KEY-----" . --include="*.md" --include="*.sh" 2>/dev/null; then
  print_fail "Private key found in skill files"
  FOUND_CRITICAL=1
fi

if [[ $FOUND_CRITICAL -eq 0 ]]; then
  print_pass "No obvious hardcoded secrets found"
fi

if grep -rqE "http://(?!localhost|127\.0\.0\.1)" . --include="*.md" --include="*.sh" 2>/dev/null; then
  print_warn "Non-localhost HTTP URL found (consider HTTPS)"
fi

if find . -name "*.sh" -perm -002 2>/dev/null | grep -q .; then
  print_warn "World-writable shell scripts found (should be 755)"
else
  print_pass "No world-writable scripts"
fi

# ---- 4. Health Check ----
header "Health Check"

if [[ -f "SKILL.md" ]]; then
  SKILL_NAME=$(grep "^# " SKILL.md | head -1 | sed 's/^# //' | xargs)
  if [[ -n "$SKILL_NAME" ]]; then
    print_info "Skill name: $SKILL_NAME"
  else
    print_warn "Could not determine skill name from SKILL.md"
  fi
fi

MISSING_SHEBANG=0
find . -name "*.sh" -type f 2>/dev/null | while read -r f; do
  first=$(head -1 "$f" 2>/dev/null || true)
  if [[ ! "$first" =~ ^#! ]]; then
    MISSING_SHEBANG=1
    print_warn "Shell script missing shebang: $f"
  fi
done

# ---- Summary ----
header "Audit Complete"

if [[ $SEVERITY -eq 2 ]]; then
  echo -e "${RED}Critical issues found. Do NOT enable this skill until resolved.${NC}"
elif [[ $SEVERITY -eq 1 ]]; then
  echo -e "${YELLOW}Warnings found. Review above and decide whether to proceed.${NC}"
else
  echo -e "${GREEN}All checks passed!${NC} Skill looks good to enable."
fi

exit $SEVERITY
