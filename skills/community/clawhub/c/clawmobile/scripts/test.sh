#!/usr/bin/env bash
#
# ClawMobile Skill Test Script
# Runs tests for the ClawMobile Skill

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0

# Functions
print_header() {
    echo ""
    echo "=========================================="
    echo "  $1"
    echo "=========================================="
    echo ""
}

print_test() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -e "${BLUE}[TEST $TOTAL_TESTS]${NC} $1"
}

print_pass() {
    PASSED_TESTS=$((PASSED_TESTS + 1))
    echo -e "  ${GREEN}✓ PASS${NC}"
}

print_fail() {
    FAILED_TESTS=$((FAILED_TESTS + 1))
    echo -e "  ${RED}✗ FAIL${NC}"
    echo "  Error: $1"
}

print_skip() {
    SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
    echo -e "  ${YELLOW}⊘ SKIP${NC} - $1"
}

# Test functions
test_python_imports() {
    print_test "Python module imports"

    cd "$SKILL_ROOT"

    if python3 -c "
import sys
sys.path.insert(0, '.')
from skill import client, api_server, executor, models
print('All modules imported successfully')
" 2>&1; then
        print_pass
    else
        print_fail "Failed to import modules"
        return 1
    fi
}

test_config_loading() {
    print_test "Configuration loading"

    if python3 -c "
import sys
import yaml
sys.path.insert(0, '.')

# Load config
with open('config/settings.yaml') as f:
    config = yaml.safe_load(f)

# Validate required sections
required_sections = ['api', 'server', 'auth']
for section in required_sections:
    if section not in config:
        raise ValueError(f'Missing required section: {section}')

print('Configuration loaded successfully')
print(f'API URL: {config[\"api\"][\"base_url\"]}')
print(f'Server port: {config[\"server\"][\"port\"]}')
" 2>&1; then
        print_pass
    else
        print_fail "Failed to load configuration"
        return 1
    fi
}

test_client_creation() {
    print_test "Client creation"

    if python3 -c "
import sys
sys.path.insert(0, '.')
from skill.client import ClawMobileClient

# Create client instance
client = ClawMobileClient()
print('Client created successfully')
print(f'Client type: {type(client).__name__}')
" 2>&1; then
        print_pass
    else
        print_fail "Failed to create client"
        return 1
    fi
}

test_api_health_check() {
    print_test "API health check"

    # Check if API server is running
    if ! command -v curl &> /dev/null; then
        print_skip "curl not available"
        return 0
    fi

    if [ -z "$CLAWMOBILE_API_URL" ]; then
        API_URL="http://localhost:8765"
    else
        API_URL="$CLAWMOBILE_API_URL"
    fi

    if curl -s -f "$API_URL/api/v1/health" > /dev/null 2>&1; then
        print_pass
    else
        print_skip "API server not running at $API_URL"
    fi
}

test_models() {
    print_test "Data models"

    if python3 -c "
import sys
sys.path.insert(0, '.')
from skill.models import Workflow, Task, Membership, Recording

# Test model creation
workflow = Workflow(
    workflow_id='test_001',
    workflow_name='Test Workflow',
    kernel_type='accessibility'
)
print(f'Workflow created: {workflow.workflow_name}')

task = Task(
    task_id='task_001',
    workflow_id='test_001',
    status='pending'
)
print(f'Task created: {task.task_id}')

membership = Membership(
    user_id='test_user',
    tier='free'
)
print(f'Membership created: {membership.tier}')

print('All models work correctly')
" 2>&1; then
        print_pass
    else
        print_fail "Failed to test models"
        return 1
    fi
}

test_redeem_code_validation() {
    print_test "Redeem code validation"

    if python3 -c "
import sys
sys.path.insert(0, '.')
from skill.membership import validate_redeem_code_format

# Test valid code
valid_code = 'C-VENDORCODE-24-01M-A1B2C3D4'
if not validate_redeem_code_format(valid_code):
    raise ValueError(f'Valid code rejected: {valid_code}')

# Test invalid codes
invalid_codes = [
    'INVALID',  # Too short
    'X-VENDORCODE-24-01M-A1B2C3D4',  # Invalid type
    'C-VENDORCODE-24-01M',  # Missing checksum
]

for code in invalid_codes:
    if validate_redeem_code_format(code):
        raise ValueError(f'Invalid code accepted: {code}')

print('Redeem code validation works correctly')
" 2>&1; then
        print_pass
    else
        print_fail "Failed to test redeem code validation"
        return 1
    fi
}

test_membership_tiers() {
    print_test "Membership tier permissions"

    if python3 -c "
import sys
sys.path.insert(0, '.')
from skill.membership import MEMBERSHIP_CONFIG

# Test tier configurations
tiers = ['free', 'vip', 'svip']

for tier in tiers:
    if tier not in MEMBERSHIP_CONFIG['daily_runs']:
        raise ValueError(f'Missing tier configuration: {tier}')

print(f'Free tier daily runs: {MEMBERSHIP_CONFIG[\"daily_runs\"][\"free\"]}')
print(f'VIP tier daily runs: {MEMBERSHIP_CONFIG[\"daily_runs\"][\"vip\"]}')
print(f'SVIP tier daily runs: {MEMBERSHIP_CONFIG[\"daily_runs\"][\"svip\"]}')

print('All tier configurations are valid')
" 2>&1; then
        print_pass
    else
        print_fail "Failed to test membership tiers"
        return 1
    fi
}

test_yaml_schema() {
    print_test "YAML schema validation"

    if [ ! -f "$SKILL_ROOT/config/schema.json" ]; then
        print_skip "schema.json not found"
        return 0
    fi

    if python3 -c "
import json
with open('config/schema.json') as f:
    schema = json.load(f)

if '\$schema' not in schema:
    raise ValueError('Missing \$schema in schema.json')

if 'properties' not in schema:
    raise ValueError('Missing properties in schema.json')

print('Schema validation passed')
print(f'Schema title: {schema.get(\"title\", \"N/A\")}')
" 2>&1; then
        print_pass
    else
        print_fail "Failed to validate schema"
        return 1
    fi
}

test_skill_md_format() {
    print_test "SKILL.md format validation"

    if [ ! -f "$SKILL_ROOT/SKILL.md" ]; then
        print_fail "SKILL.md not found"
        return 1
    fi

    # Check frontmatter
    if ! grep -q "^---" "$SKILL_ROOT/SKILL.md"; then
        print_fail "SKILL.md missing frontmatter delimiter"
        return 1
    fi

    # Check required fields
    REQUIRED_FIELDS=("name:" "description:" "version:")
    for field in "${REQUIRED_FIELDS[@]}"; do
        if ! grep -q "^$field" "$SKILL_ROOT/SKILL.md"; then
            print_fail "SKILL.md missing required field: $field"
            return 1
        fi
    done

    # Check for metadata section
    if ! grep -q "^metadata:" "$SKILL_ROOT/SKILL.md"; then
        print_fail "SKILL.md missing metadata section"
        return 1
    fi

    print_pass
}

test_version_file() {
    print_test "VERSION file validation"

    if [ ! -f "$SKILL_ROOT/VERSION" ]; then
        print_fail "VERSION file not found"
        return 1
    fi

    VERSION=$(cat "$SKILL_ROOT/VERSION")

    # Check semver format
    if ! echo "$VERSION" | grep -qE "^[0-9]+\.[0-9]+\.[0-9]+$"; then
        print_fail "VERSION does not follow semver format: $VERSION"
        return 1
    fi

    print_pass
}

test_readme_exists() {
    print_test "README.md exists"

    if [ ! -f "$SKILL_ROOT/README.md" ]; then
        print_fail "README.md not found"
        return 1
    fi

    print_pass
}

# Run integration tests if pytest is available
run_pytest_tests() {
    print_test "Pytest unit tests"

    if ! command -v pytest &> /dev/null; then
        if ! python3 -m pytest --version &> /dev/null 2>&1; then
            print_skip "pytest not available"
            return 0
        fi
    fi

    cd "$SKILL_ROOT"

    if [ -d "tests" ] && [ "$(ls -A tests/*.py 2>/dev/null)" ]; then
        if python3 -m pytest tests/ -v --tb=short 2>&1; then
            print_pass
        else
            print_fail "Some pytest tests failed"
            return 1
        fi
    else
        print_skip "No pytest tests found"
    fi
}

# Print summary
print_summary() {
    print_header "Test Summary"

    echo "Total Tests: $TOTAL_TESTS"
    echo -e "${GREEN}Passed:${NC} $PASSED_TESTS"
    echo -e "${YELLOW}Skipped:${NC} $SKIPPED_TESTS"
    echo -e "${RED}Failed:${NC} $FAILED_TESTS"
    echo ""

    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        echo ""
        echo "The ClawMobile Skill is working correctly."
        return 0
    else
        echo -e "${RED}✗ Some tests failed${NC}"
        echo ""
        echo "Please fix the errors above."
        return 1
    fi
}

# Main test execution
main() {
    print_header "ClawMobile Skill Tests"

    # Check if we're in the right directory
    if [ ! -f "$SKILL_ROOT/SKILL.md" ]; then
        echo "Error: SKILL.md not found. Please run this script from the skill root directory."
        exit 1
    fi

    # Run all tests
    test_python_imports
    test_config_loading
    test_client_creation
    test_api_health_check
    test_models
    test_redeem_code_validation
    test_membership_tiers
    test_yaml_schema
    test_skill_md_format
    test_version_file
    test_readme_exists
    run_pytest_tests

    # Print summary
    print_summary
    exit $?
}

# Run main
main "$@"
