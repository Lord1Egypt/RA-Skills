#!/bin/bash
# Master test runner for Automate

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

echo "🧪 Automate Test Suite"
echo "======================"
echo ""

# Run each test
echo "Running configuration tests..."
bash tests/test-config.sh
echo ""

echo "Running workflow tests..."
bash tests/test-workflows.sh
echo ""

echo "======================"
echo "✅ All tests passed!"
