#!/bin/bash
# Frugal Orchestrator structure verifier

echo "=== Skill Structure Verification ==="
dirs=("scripts" "templates" "examples" "tools" "integration_tests" ".a0proj/instructions" ".a0proj/knowledge/solutions" ".a0proj/skills" "demo")

for dir in "${dirs[@]}"; do
 if [ -d "/a0/usr/projects/frugal_orchestrator/$dir" ]; then
 echo "$(green)OK$(reset): $dir"
 else
 echo "$(red)MISS$(reset): $dir"
 fi
done

echo ""
echo "=== Specialty Matrix ==="
grep -A 8 "## Delegation Patterns" /a0/usr/projects/frugal_orchestrator/SKILL.md 2>/dev/null || echo "SKILL.md not yet complete"
