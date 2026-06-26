#!/bin/bash
# Tests for GitHub Actions workflow validity

set -e

echo "=== Automate Workflow Tests ==="

# Test 1: Workflow files exist
echo "Test 1: Workflow files..."
workflows=(
    ".github/workflows/agent-task.yml"
    ".github/workflows/orchestrator.yml"
    ".github/workflows/task-runner.yml"
    ".github/workflows/scheduled.yml"
    ".github/workflows/secure-comm.yml"
)

for workflow in "${workflows[@]}"; do
    if [ -f "$workflow" ]; then
        echo "  ✅ $workflow exists"
    else
        echo "  ❌ Missing: $workflow"
        exit 1
    fi
done

# Test 2: Workflow YAML syntax
echo "Test 2: Workflow YAML syntax..."
if command -v yamllint &> /dev/null; then
    for workflow in "${workflows[@]}"; do
        if yamllint "$workflow" 2>/dev/null; then
            echo "  ✅ $workflow syntax OK"
        else
            echo "  ⚠️  $workflow has YAML warnings (non-fatal)"
        fi
    done
else
    echo "  ⚠️  yamllint not installed, skipping syntax check"
fi

# Test 3: Issue templates exist
echo "Test 3: Issue templates..."
templates=(
    ".github/ISSUE_TEMPLATE/task.md"
    ".github/ISSUE_TEMPLATE/agent-task.md"
)

for template in "${templates[@]}"; do
    if [ -f "$template" ]; then
        echo "  ✅ $template exists"
    else
        echo "  ❌ Missing: $template"
        exit 1
    fi
done

# Test 4: Agent task template has required fields
echo "Test 4: Agent task template fields..."
template=".github/ISSUE_TEMPLATE/agent-task.md"
required_fields=(
    "Agent"
    "Task Description"
    "Priority"
    "Expected Output"
)

for field in "${required_fields[@]}"; do
    if grep -qi "$field" "$template"; then
        echo "  ✅ Field: $field"
    else
        echo "  ⚠️  Missing field: $field"
    fi
done

# Test 5: package.json has scripts
echo "Test 5: package.json scripts..."
if [ -f "package.json" ]; then
    if grep -q '"scripts"' package.json; then
        echo "  ✅ package.json has scripts section"
        # Try to parse and list scripts if jq available
        if command -v jq &> /dev/null; then
            echo "  Scripts:"
            jq '.scripts | keys[]' package.json 2>/dev/null | sed 's/"//g' | sed 's/^/    - /' || echo "    (unable to parse)"
        fi
    else
        echo "  ❌ package.json missing scripts section"
        exit 1
    fi
else
    echo "  ❌ package.json not found"
    exit 1
fi

echo ""
echo "=== Workflow Tests Passed ✅ ==="
