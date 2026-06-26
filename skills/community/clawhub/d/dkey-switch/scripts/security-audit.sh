#!/usr/bin/env bash
set +e

echo "🔒 DKey Switch Agent Security Audit"
echo "==================================="

ISSUES=0
WARNINGS=0

warn() {
    echo "⚠️  WARNING: $1"
    ((WARNINGS++))
}

fail() {
    echo "❌ ISSUE: $1"
    ((ISSUES++))
}

pass() {
    echo "✅ $1"
}

echo "1) Checking required files..."
for f in "SKILL.md" "_meta.json" "scripts/d-switch.sh" "scripts/d-switch.ps1" "scripts/d-switch.cmd" "scripts/security-audit.sh" "scripts/security-audit.ps1" "scripts/security-audit.cmd" "references/ai-e2e-cases.md"; do
    if [[ -f "$f" ]]; then
        pass "$f exists"
    else
        fail "$f missing"
    fi
done

echo "2) Checking command hints..."
if grep -q "Dalt\|Dctrl\|find-window\|list-windows\|activate-window\|activate-process\|activate-handle" "SKILL.md"; then
    pass "SKILL.md contains command hints"
else
    warn "SKILL.md may be missing command hints"
fi

echo "3) Checking usage reference updates..."
if grep -q "find-window\|activate-window\|activate-process\|activate-handle\|--json" "references/usage-patterns.md"; then
    pass "references/usage-patterns.md contains new window commands"
else
    warn "references/usage-patterns.md may be missing new window commands"
fi

echo "4) Checking JSON output hints..."
if grep -q -- "--json" "SKILL.md"; then
    pass "SKILL.md contains json output hints"
else
    warn "SKILL.md may be missing json output hints"
fi

echo "5) Checking AI canonical routing hints..."
if grep -q "AI 决策模板\|Canonical" "SKILL.md" && grep -q "Canonical Intent -> Command" "references/usage-patterns.md"; then
    pass "AI canonical routing hints exist in SKILL and usage docs"
else
    warn "Canonical routing hints may be missing"
fi

echo "6) Checking status contract references..."
if grep -q "activated\|not_found\|choice_out_of_range\|activation_failed" "SKILL.md" && grep -q "ok\|activated\|not_found\|choice_out_of_range\|activation_failed" "references/usage-patterns.md"; then
    pass "Status contract appears in SKILL and usage docs"
else
    warn "Status contract may be incomplete"
fi

echo "7) Checking exit code references..."
if grep -q "退出码约定" "SKILL.md" && grep -q "Exit Codes" "references/usage-patterns.md" && grep -q "0\|1\|2\|3\|4" "references/usage-patterns.md"; then
    pass "Exit code references exist"
else
    warn "Exit code references may be missing"
fi

echo "8) Checking memory fact alignment..."
if grep -q "scripts/d-switch.ps1" "assets/MEMORY.md" && grep -q "activate-window\|activate-process\|activate-handle" "assets/MEMORY.md"; then
    pass "assets/MEMORY.md is aligned with current command surface"
else
    warn "assets/MEMORY.md may be outdated"
fi

echo "9) Checking onboarding release checklist..."
if grep -q "Release Checklist" "assets/ONBOARDING.md" && grep -q "Fast Verification Commands" "assets/ONBOARDING.md"; then
    pass "assets/ONBOARDING.md contains release checklist"
else
    warn "assets/ONBOARDING.md may be missing release checklist"
fi

echo "10) Checking AI E2E cases coverage..."
CASE_COUNT=$(grep -c "^[0-9]\+\. Intent:" "references/ai-e2e-cases.md" 2>/dev/null)
if grep -q "Expected status" "references/ai-e2e-cases.md" && [[ $CASE_COUNT -ge 10 ]]; then
    pass "references/ai-e2e-cases.md has $CASE_COUNT cases"
else
    warn "AI E2E cases may be insufficient (found: $CASE_COUNT)"
fi

echo "11) Checking script executable bit (best effort)..."
if [[ -x "scripts/d-switch.sh" ]]; then
    pass "scripts/d-switch.sh is executable"
else
    warn "scripts/d-switch.sh may not be executable on this filesystem"
fi

echo "==================================="
if [[ $ISSUES -eq 0 ]]; then
    echo "Audit complete: $WARNINGS warning(s), 0 issue(s)."
else
    echo "Audit complete: $WARNINGS warning(s), $ISSUES issue(s)."
fi
