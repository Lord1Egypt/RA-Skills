#!/bin/bash
set -euo pipefail

# Agent Maker - Validate Agent Configuration
# Usage: ./validate-agent.sh --name=agent-name

AGENT_NAME=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --name=*)
            AGENT_NAME="${1#*=}"
            shift
            ;;
        --help)
            echo "Usage: $0 --name=agent-name"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [[ -z "$AGENT_NAME" ]]; then
    echo "❌ Error: --name is required"
    exit 1
fi

AGENT_DIR="${HOME}/.openclaw/agents/${AGENT_NAME}"

echo "🔍 Validating Agent: ${AGENT_NAME}"
echo "   Location: ${AGENT_DIR}"
echo ""

if [[ ! -d "$AGENT_DIR" ]]; then
    echo "❌ Agent directory not found: ${AGENT_DIR}"
    exit 1
fi

# Required files
REQUIRED_FILES=(
    "IDENTITY.md"
    "SYSTEM.md"
    "SOUL.md"
    "AGENTS.md"
    "USER.md"
    "HEARTBEAT.md"
)

# Optional but recommended
OPTIONAL_FILES=(
    "QUICKSTART.md"
)

ERRORS=0
WARNINGS=0

echo "📋 Checking required files..."
for file in "${REQUIRED_FILES[@]}"; do
    if [[ -f "${AGENT_DIR}/${file}" ]]; then
        echo "   ✅ ${file}"
    else
        echo "   ❌ ${file} - MISSING"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""
echo "📋 Checking optional files..."
for file in "${OPTIONAL_FILES[@]}"; do
    if [[ -f "${AGENT_DIR}/${file}" ]]; then
        echo "   ✅ ${file}"
    else
        echo "   ⚠️  ${file} - missing (recommended)"
        WARNINGS=$((WARNINGS + 1))
    fi
done

echo ""
echo "📋 Checking file content..."

# Check IDENTITY.md has basic structure
if [[ -f "${AGENT_DIR}/IDENTITY.md" ]]; then
    if grep -q "Name:" "${AGENT_DIR}/IDENTITY.md"; then
        echo "   ✅ IDENTITY.md has Name field"
    else
        echo "   ⚠️  IDENTITY.md missing Name field"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# Check SYSTEM.md has workspace restrictions
if [[ -f "${AGENT_DIR}/SYSTEM.md" ]]; then
    if grep -qi "workspace\|工作目录" "${AGENT_DIR}/SYSTEM.md"; then
        echo "   ✅ SYSTEM.md has workspace definition"
    else
        echo "   ⚠️  SYSTEM.md missing workspace definition"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

echo ""
echo "=========================="
if [[ $ERRORS -eq 0 && $WARNINGS -eq 0 ]]; then
    echo "✅ Validation passed! Agent configuration is complete."
elif [[ $ERRORS -eq 0 ]]; then
    echo "✅ Validation passed with ${WARNINGS} warning(s)."
else
    echo "❌ Validation failed with ${ERRORS} error(s) and ${WARNINGS} warning(s)."
    exit 1
fi