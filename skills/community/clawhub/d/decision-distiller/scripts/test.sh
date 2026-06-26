#!/bin/bash
#
# test.sh - Run tests for decision-distiller skill
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "🧪 Testing decision-distiller skill"
echo "==================================="

# Test 1: SKILL.md exists
echo "Test 1: Check SKILL.md exists..."
if [[ -f "$SKILL_DIR/SKILL.md" ]]; then
    echo "  ✅ PASS: SKILL.md exists"
else
    echo "  ❌ FAIL: SKILL.md not found"
    exit 1
fi

# Test 2: YAML frontmatter
echo "Test 2: Check YAML frontmatter..."
if grep -q "^---$" "$SKILL_DIR/SKILL.md"; then
    echo "  ✅ PASS: YAML frontmatter present"
else
    echo "  ❌ FAIL: Missing YAML frontmatter"
    exit 1
fi

# Test 3: Required fields
echo "Test 3: Check required fields..."
for field in "name:" "description:"; do
    if grep -q "^$field" "$SKILL_DIR/SKILL.md"; then
        echo "  ✅ PASS: Found $field"
    else
        echo "  ❌ FAIL: Missing $field"
        exit 1
    fi
done

# Test 4: References directory
echo "Test 4: Check references directory..."
if [[ -d "$SKILL_DIR/references" ]]; then
    echo "  ✅ PASS: references/ directory exists"
else
    echo "  ❌ FAIL: references/ directory not found"
    exit 1
fi

# Test 5: Decision templates exist
echo "Test 5: Check decision templates..."
if [[ -f "$SKILL_DIR/references/decision-templates.md" ]]; then
    echo "  ✅ PASS: decision-templates.md exists"
else
    echo "  ❌ FAIL: decision-templates.md not found"
    exit 1
fi

# Test 6: Analysis frameworks exist
echo "Test 6: Check analysis frameworks..."
if [[ -f "$SKILL_DIR/references/analysis-frameworks.md" ]]; then
    echo "  ✅ PASS: analysis-frameworks.md exists"
else
    echo "  ❌ FAIL: analysis-frameworks.md not found"
    exit 1
fi

# Test 7: Scripts are executable
echo "Test 7: Check scripts are executable..."
for script in "$SKILL_DIR/scripts/"*.sh; do
    if [[ -f "$script" ]]; then
        if [[ -x "$script" ]]; then
            echo "  ✅ PASS: $(basename "$script") is executable"
        else
            echo "  ⚠️  WARN: $(basename "$script") is not executable"
        fi
    fi
done

echo ""
echo "==================================="
echo "✅ All critical tests passed!"
