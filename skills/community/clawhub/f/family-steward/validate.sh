#!/usr/bin/env bash
#
# ClawHub Skill Validation Script
# Validates that all required files and configurations are present and correct
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔍 Validating Family Steward ClawHub Skill..."
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0
WARN=0

# Check function
check() {
    local name=$1
    local command=$2
    local type=${3:-required}  # required, optional, warning

    if eval "$command" &>/dev/null; then
        echo -e "${GREEN}✓${NC} $name"
        ((PASS++))
        return 0
    else
        if [ "$type" = "required" ]; then
            echo -e "${RED}✗${NC} $name"
            ((FAIL++))
        elif [ "$type" = "warning" ]; then
            echo -e "${YELLOW}⚠${NC} $name"
            ((WARN++))
        else
            echo -e "${YELLOW}○${NC} $name (optional)"
        fi
        return 1
    fi
}

echo "📁 Required Files:"
check "SKILL.md exists" "test -f SKILL.md"
check "skill.json exists" "test -f skill.json"
check "README.md exists" "test -f README.md"
check ".clawhubrc exists" "test -f .clawhubrc"
check "CHANGELOG.md exists" "test -f CHANGELOG.md"
echo ""

echo "📝 File Content Validation:"
check "SKILL.md has frontmatter" "head -1 SKILL.md | grep -q '^---$'"
check "SKILL.md has name field" "grep -q '^name:' SKILL.md"
check "SKILL.md has description" "grep -q '^description:' SKILL.md"
check "skill.json is valid JSON" "jq empty skill.json"
check "skill.json has id field" "jq -e '.id' skill.json"
check "skill.json has version field" "jq -e '.version' skill.json"
check "skill.json has description" "jq -e '.description' skill.json"
echo ""

echo "🔗 External References:"
check "Parent src/ exists" "test -d ../src"
check "Parent package.json exists" "test -f ../package.json"
check "Parent README exists" "test -f ../README.md"
check "Parent ARCHITECTURE.md exists" "test -f ../ARCHITECTURE.md"
echo ""

echo "⚙️  Configuration Checks:"
check "Version is 1.0.0" "jq -e '.version == \"1.0.0\"' skill.json"
check "ID is 'family-steward'" "jq -e '.id == \"family-steward\"' skill.json"
check "Name is set" "jq -e '.name' skill.json"
check "License is MIT" "jq -e '.license == \"MIT\"' skill.json"
check "Repository URL is set" "jq -e '.repository.url' skill.json"
echo ""

echo "🤖 Agent Tools:"
check "Tools array exists" "jq -e '.tools' skill.json"
check "Has 17+ tools" "jq -e '.tools | length >= 17' skill.json"
check "Tools have names" "jq -e '.tools[0].name' skill.json"
check "Tools have descriptions" "jq -e '.tools[0].description' skill.json"
echo ""

echo "📦 Installation Config:"
check "Installation type is npm" "jq -e '.installation.type == \"npm\"' skill.json"
check "Package name is set" "jq -e '.installation.package' skill.json"
check "Install command is set" "jq -e '.installation.command' skill.json"
echo ""

echo "🏷️  Categories & Tags:"
check "Category is set" "jq -e '.category' skill.json"
check "Tags array exists" "jq -e '.tags | length > 0' skill.json"
check "Author is set" "jq -e '.author.name' skill.json"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Summary
TOTAL=$((PASS + FAIL + WARN))
echo "📈 Validation Summary:"
echo -e "   ${GREEN}Passed${NC}:  $PASS/$TOTAL"
echo -e "   ${RED}Failed${NC}:  $FAIL/$TOTAL"
echo -e "   ${YELLOW}Warnings${NC}: $WARN/$TOTAL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✅ All validations passed!${NC}"
    echo ""
    echo "Ready to publish:"
    echo "  clawhub publish . --slug family-steward --version 1.0.0"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Validation failed with $FAIL error(s)${NC}"
    echo ""
    echo "Please fix the errors above before publishing."
    echo ""
    exit 1
fi
