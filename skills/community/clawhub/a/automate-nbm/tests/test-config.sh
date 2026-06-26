#!/bin/bash
# Tests for Automate configuration validation

set -e

echo "=== Automate Config Tests ==="

# Test 1: YAML syntax
echo "Test 1: YAML syntax validation..."
if ! command -v yamllint &> /dev/null; then
    echo "  ⚠️  yamllint not installed, skipping"
else
    if yamllint config/automate.yml; then
        echo "  ✅ YAML syntax OK"
    else
        echo "  ❌ YAML syntax error"
        exit 1
    fi
fi

# Test 2: Required agent files exist
echo "Test 2: Agent profile files exist..."
required_agents=(
    "agents/engineering/backend-architect.md"
    "agents/engineering/frontend-developer.md"
    "agents/marketing/growth-hacker.md"
    "agents/testing/testing-reality-checker.md"
    "agents/project-management/project-manager-senior.md"
)

for agent in "${required_agents[@]}"; do
    if [ -f "$agent" ]; then
        echo "  ✅ $agent"
    else
        echo "  ❌ Missing: $agent"
        exit 1
    fi
done

# Test 3: Scripts are executable
echo "Test 3: Script executability..."
scripts=(
    "scripts/run-task.sh"
    "scripts/agent-dispatch.sh"
    "scripts/notify.sh"
)

for script in "${scripts[@]}"; do
    if [ -x "$script" ]; then
        echo "  ✅ $script is executable"
    else
        echo "  ⚠️  Making $script executable..."
        chmod +x "$script"
    fi
done

# Test 4: Makefile exists and has targets
echo "Test 4: Makefile targets..."
if [ -f "Makefile" ]; then
    if grep -q "^\.PHONY:" Makefile; then
        echo "  ✅ Makefile has .PHONY declaration"
    else
        echo "  ⚠️  Makefile missing .PHONY declaration"
    fi
else
    echo "  ❌ Makefile not found"
    exit 1
fi

# Test 5: Documentation completeness
echo "Test 5: Documentation files..."
docs=(
    "README.md"
    "AGENTS.md"
    "docs/QUICKSTART.md"
    "SKILL.md"
)

for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        lines=$(wc -l < "$doc")
        echo "  ✅ $doc ($lines lines)"
    else
        echo "  ❌ Missing: $doc"
        exit 1
    fi
done

echo ""
echo "=== All Tests Passed ✅ ==="
