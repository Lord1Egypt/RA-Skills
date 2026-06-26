#!/usr/bin/env bash
#
# ClawMobile Skill Validation Script
# Validates the skill structure and configuration

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# Functions
print_header() {
    echo ""
    echo "=========================================="
    echo "  $1"
    echo "=========================================="
    echo ""
}

print_check() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    echo -n "[$TOTAL_CHECKS] $1 ... "
}

print_pass() {
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
    echo -e "${GREEN}✓ PASS${NC}"
}

print_fail() {
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
    echo -e "${RED}✗ FAIL${NC}"
    echo "  Error: $1"
}

print_warn() {
    WARNING_CHECKS=$((WARNING_CHECKS + 1))
    echo -e "${YELLOW}⚠ WARN${NC}"
    echo "  Warning: $1"
}

# Validation functions
validate_skill_md() {
    print_check "Checking SKILL.md"

    if [ ! -f "$SKILL_ROOT/SKILL.md" ]; then
        print_fail "SKILL.md not found"
        return 1
    fi

    # Check frontmatter
    if ! grep -q "^---" "$SKILL_ROOT/SKILL.md"; then
        print_fail "SKILL.md missing frontmatter"
        return 1
    fi

    # Check required fields
    if ! grep -q "^name:" "$SKILL_ROOT/SKILL.md"; then
        print_fail "SKILL.md missing 'name' field"
        return 1
    fi

    if ! grep -q "^description:" "$SKILL_ROOT/SKILL.md"; then
        print_fail "SKILL.md missing 'description' field"
        return 1
    fi

    print_pass
}

validate_skill_structure() {
    print_check "Checking skill directory structure"

    REQUIRED_DIRS=(
        "skill"
        "config"
        "scripts"
        "docs"
    )

    for dir in "${REQUIRED_DIRS[@]}"; do
        if [ ! -d "$SKILL_ROOT/$dir" ]; then
            print_fail "Required directory '$dir' not found"
            return 1
        fi
    done

    print_pass
}

validate_python_files() {
    print_check "Checking Python files"

    REQUIRED_PY_FILES=(
        "skill/__init__.py"
        "skill/client.py"
        "skill/api_server.py"
        "skill/executor.py"
        "skill/models.py"
    )

    for file in "${REQUIRED_PY_FILES[@]}"; do
        if [ ! -f "$SKILL_ROOT/$file" ]; then
            print_fail "Required Python file '$file' not found"
            return 1
        fi
    done

    # Check Python syntax
    for file in "${REQUIRED_PY_FILES[@]}"; do
        if ! python3 -m py_compile "$SKILL_ROOT/$file" 2>/dev/null; then
            print_fail "Python syntax error in $file"
            return 1
        fi
    done

    print_pass
}

validate_config_files() {
    print_check "Checking configuration files"

    if [ ! -f "$SKILL_ROOT/config/settings.yaml" ]; then
        print_fail "config/settings.yaml not found"
        return 1
    fi

    if [ ! -f "$SKILL_ROOT/config/schema.json" ]; then
        print_warn "config/schema.json not found (optional)"
    else
        # Check JSON syntax
        if ! python3 -c "import json; json.load(open('$SKILL_ROOT/config/schema.json'))" 2>/dev/null; then
            print_fail "config/schema.json has invalid JSON syntax"
            return 1
        fi
    fi

    print_pass
}

validate_dependencies() {
    print_check "Checking Python dependencies"

    if [ ! -f "$SKILL_ROOT/requirements.txt" ]; then
        print_warn "requirements.txt not found"
    else
        # Check if requests is available
        if ! python3 -c "import requests" 2>/dev/null; then
            print_fail "requests module not installed"
            return 1
        fi

        # Check if pyyaml is available
        if ! python3 -c "import yaml" 2>/dev/null; then
            print_fail "pyyaml module not installed"
            return 1
        fi
    fi

    print_pass
}

validate_documentation() {
    print_check "Checking documentation files"

    DOC_FILES=(
        "README.md"
        "VERSION"
        "CHANGELOG.md"
    )

    for file in "${DOC_FILES[@]}"; do
        if [ ! -f "$SKILL_ROOT/$file" ]; then
            print_warn "Documentation file '$file' not found"
        fi
    done

    print_pass
}

validate_environment() {
    print_check "Checking environment variables"

    if [ -z "$CLAWMOBILE_API_URL" ]; then
        print_warn "CLAWMOBILE_API_URL not set (using default from config)"
    fi

    if [ -z "$CLAWMOBILE_API_TOKEN" ]; then
        print_warn "CLAWMOBILE_API_TOKEN not set (required for production)"
    fi

    print_pass
}

validate_python_version() {
    print_check "Checking Python version"

    if ! command -v python3 &> /dev/null; then
        print_fail "Python 3 not found"
        return 1
    fi

    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
        print_fail "Python $PYTHON_VERSION not supported (requires 3.7+)"
        return 1
    fi

    print_pass
}

validate_adb() {
    print_check "Checking ADB"

    if ! command -v adb &> /dev/null; then
        print_warn "ADB not found in PATH (required for device connection)"
    else
        # Check if any devices are connected
        DEVICE_COUNT=$(adb devices | grep -v "List" | grep -c "device" || true)
        if [ "$DEVICE_COUNT" -eq 0 ]; then
            print_warn "No Android devices connected"
        else
            print_pass
        fi
    fi
}

validate_connection() {
    print_check "Testing API connection"

    if [ -z "$CLAWMOBILE_API_URL" ]; then
        # Try to load from config
        if [ -f "$SKILL_ROOT/config/settings.yaml" ]; then
            API_URL=$(grep "base_url:" "$SKILL_ROOT/config/settings.yaml" | awk '{print $2}' | tr -d '"')
        else
            API_URL="http://localhost:8765"
        fi
    else
        API_URL="$CLAWMOBILE_API_URL"
    fi

    # Test health endpoint
    if command -v curl &> /dev/null; then
        if curl -s -f "$API_URL/api/v1/health" > /dev/null 2>&1; then
            print_pass
        else
            print_warn "Cannot connect to API server at $API_URL"
        fi
    else
        print_warn "curl not available, skipping connection test"
    fi
}

validate_imports() {
    print_check "Checking Python module imports"

    cd "$SKILL_ROOT"

    # Try to import the skill module
    if ! python3 -c "import sys; sys.path.insert(0, '.'); from skill import client" 2>/dev/null; then
        print_fail "Cannot import skill.client module"
        return 1
    fi

    print_pass
}

# Print summary
print_summary() {
    print_header "Validation Summary"

    echo "Total Checks: $TOTAL_CHECKS"
    echo -e "${GREEN}Passed:${NC} $PASSED_CHECKS"
    echo -e "${YELLOW}Warnings:${NC} $WARNING_CHECKS"
    echo -e "${RED}Failed:${NC} $FAILED_CHECKS"
    echo ""

    if [ $FAILED_CHECKS -eq 0 ]; then
        echo -e "${GREEN}✓ All critical checks passed!${NC}"
        echo ""
        echo "The ClawMobile Skill is ready to use."
        return 0
    else
        echo -e "${RED}✗ Some checks failed${NC}"
        echo ""
        echo "Please fix the errors above before using the skill."
        return 1
    fi
}

# Main validation
main() {
    print_header "ClawMobile Skill Validation"

    # Run all validations
    validate_python_version
    validate_skill_md
    validate_skill_structure
    validate_python_files
    validate_config_files
    validate_dependencies
    validate_documentation
    validate_environment
    validate_adb
    validate_connection
    validate_imports

    # Print summary
    print_summary
    exit $?
}

# Run main
main "$@"
