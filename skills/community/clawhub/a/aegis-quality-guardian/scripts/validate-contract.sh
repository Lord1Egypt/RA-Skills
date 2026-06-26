#!/usr/bin/env bash
# validate-contract.sh — Validate contract consistency
#
# Usage: bash validate-contract.sh /path/to/project
#
# Checks:
#   1. contracts/api-spec.yaml exists and is valid YAML
#   2. contracts/shared-types.ts exists
#   3. contracts/errors.yaml exists and is valid YAML
#   4. (Optional) OpenAPI validation if npx available

set -euo pipefail

PROJECT="${1:-.}"
CONTRACTS="$PROJECT/contracts"
ERRORS=0

echo "🛡️  Aegis Contract Validation: $PROJECT"
echo "──────────────────────────────────────"

# Check file existence
check_file() {
  local file="$1"
  local desc="$2"
  if [[ -f "$file" ]]; then
    echo "  ✅ $desc: $file"
  else
    echo "  ❌ $desc: $file (MISSING)"
    ERRORS=$((ERRORS + 1))
  fi
}

check_file "$CONTRACTS/api-spec.yaml" "API Spec"
check_file "$CONTRACTS/shared-types.ts" "Shared Types"
check_file "$CONTRACTS/errors.yaml" "Error Codes"

# Validate YAML syntax
validate_yaml() {
  local file="$1"
  if [[ -f "$file" ]]; then
    if command -v python3 &>/dev/null; then
      if python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
        echo "  ✅ YAML valid: $file"
      else
        echo "  ❌ YAML invalid: $file"
        ERRORS=$((ERRORS + 1))
      fi
    fi
  fi
}

echo ""
echo "YAML Syntax:"
validate_yaml "$CONTRACTS/api-spec.yaml"
validate_yaml "$CONTRACTS/errors.yaml"

# Optional: OpenAPI validation
echo ""
if command -v npx &>/dev/null && [[ -f "$CONTRACTS/api-spec.yaml" ]]; then
  echo "OpenAPI Validation:"
  if npx --yes @redocly/cli lint "$CONTRACTS/api-spec.yaml" --skip-rule no-unused-components 2>/dev/null; then
    echo "  ✅ OpenAPI spec is valid"
  else
    echo "  ⚠️  OpenAPI validation had warnings/errors (non-blocking)"
  fi
else
  echo "OpenAPI Validation: skipped (npx or spec not available)"
fi

echo ""
echo "──────────────────────────────────────"
if [[ $ERRORS -eq 0 ]]; then
  echo "🛡️  All checks passed!"
  exit 0
else
  echo "❌ $ERRORS issue(s) found."
  exit 1
fi
