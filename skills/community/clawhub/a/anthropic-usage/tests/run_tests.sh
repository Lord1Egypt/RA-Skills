#!/usr/bin/env bash
# =============================================================================
# run_tests.sh — Test suite for scripts/usage.sh
# =============================================================================
# Uses a curl stub (tests/stubs/curl) to simulate the Anthropic API without
# making real network calls. Fixtures live in tests/fixtures/*.json.
#
# Usage:
#   bash tests/run_tests.sh
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SCRIPT="${REPO_ROOT}/scripts/usage.sh"
STUBS_DIR="${SCRIPT_DIR}/stubs"

PASS=0
FAIL=0
SKIP=0

# --- Helpers -----------------------------------------------------------------

green()  { printf '\033[0;32m%s\033[0m\n' "$*"; }
red()    { printf '\033[0;31m%s\033[0m\n' "$*"; }
yellow() { printf '\033[0;33m%s\033[0m\n' "$*"; }

assert_contains() {
  local description="$1"
  local expected="$2"
  local actual="$3"

  if echo "$actual" | grep -qF -- "$expected"; then
    green "  PASS: ${description}"
    (( PASS++ )) || true
  else
    red "  FAIL: ${description}"
    echo "        expected to find: ${expected}"
    echo "        in output:        $(echo "$actual" | head -5)"
    (( FAIL++ )) || true
  fi
}

assert_not_contains() {
  local description="$1"
  local unexpected="$2"
  local actual="$3"

  if ! echo "$actual" | grep -qF -- "$unexpected"; then
    green "  PASS: ${description}"
    (( PASS++ )) || true
  else
    red "  FAIL: ${description}"
    echo "        expected NOT to find: ${unexpected}"
    echo "        in output:            $(echo "$actual" | head -5)"
    (( FAIL++ )) || true
  fi
}

assert_exit_nonzero() {
  local description="$1"
  local exit_code="$2"

  if [[ "$exit_code" -ne 0 ]]; then
    green "  PASS: ${description}"
    (( PASS++ )) || true
  else
    red "  FAIL: ${description} (expected non-zero exit, got 0)"
    (( FAIL++ )) || true
  fi
}

assert_exit_zero() {
  local description="$1"
  local exit_code="$2"

  if [[ "$exit_code" -eq 0 ]]; then
    green "  PASS: ${description}"
    (( PASS++ )) || true
  else
    red "  FAIL: ${description} (expected exit 0, got ${exit_code})"
    (( FAIL++ )) || true
  fi
}

# Run the script with the curl stub injected into PATH.
# Sets ANTHROPIC_ADMIN_API_KEY to a fake but valid-format key by default.
# Extra env vars can be passed as KEY=VALUE arguments before the script flags.
run_script() {
  local fixture="${STUB_CURL_FIXTURE:-response_ok}"
  STUB_CURL_FIXTURE="$fixture" \
    PATH="${STUBS_DIR}:${PATH}" \
    ANTHROPIC_ADMIN_API_KEY="${ANTHROPIC_ADMIN_API_KEY:-sk-ant-admin-test-fake-key-0000}" \
    bash "$SCRIPT" "$@" 2>&1
}

# Reset the page counter used by the paginated stub.
reset_page_counter() {
  rm -f "${TMPDIR:-/tmp}/.stub_curl_page_counter"
}

# --- Tests -------------------------------------------------------------------

echo ""
echo "Running tests for scripts/usage.sh"
echo "==================================="

# ---- Dependency checks ------------------------------------------------------

echo ""
echo "[ Pre-flight checks ]"

output=$(ANTHROPIC_ADMIN_API_KEY="" \
  PATH="${STUBS_DIR}:${PATH}" \
  bash "$SCRIPT" --weekly 2>&1) || true
assert_contains \
  "missing ANTHROPIC_ADMIN_API_KEY prints clear error" \
  "ANTHROPIC_ADMIN_API_KEY" \
  "$output"

output=$(ANTHROPIC_ADMIN_API_KEY="" \
  PATH="${STUBS_DIR}:${PATH}" \
  bash "$SCRIPT" --weekly 2>&1) || exit_code=$?
assert_exit_nonzero "missing key exits non-zero" "${exit_code:-1}"

output=$(ANTHROPIC_ADMIN_API_KEY="sk-not-an-admin-key" \
  PATH="${STUBS_DIR}:${PATH}" \
  bash "$SCRIPT" --weekly 2>&1) || true
assert_contains \
  "wrong key prefix prints format error" \
  "Invalid API key format" \
  "$output"

output=$(PATH="${STUBS_DIR}:${PATH}" \
  bash "$SCRIPT" --unknown-flag 2>&1) || true
assert_contains \
  "unknown flag prints error" \
  "Unknown option" \
  "$output"

# ---- --help -----------------------------------------------------------------

echo ""
echo "[ --help ]"

output=$(run_script --help 2>&1) || true
assert_contains "--help shows usage" "Usage:" "$output"
assert_contains "--help lists --weekly" "--weekly" "$output"
assert_contains "--help lists --breakdown" "--breakdown" "$output"

# ---- --check ----------------------------------------------------------------

echo ""
echo "[ --check ]"

output=$(STUB_CURL_FIXTURE=response_models_ok run_script --check 2>&1)
exit_code=$?
assert_exit_zero "--check exits 0 on HTTP 200" "$exit_code"
assert_contains "--check prints OK" "OK" "$output"

output=$(STUB_CURL_HTTP_CODE=401 STUB_CURL_FIXTURE=response_models_ok \
  PATH="${STUBS_DIR}:${PATH}" \
  ANTHROPIC_ADMIN_API_KEY="sk-ant-admin-test-fake-key-0000" \
  bash "$SCRIPT" --check 2>&1) || exit_code=$?
assert_exit_nonzero "--check exits non-zero on HTTP 401" "${exit_code:-1}"
assert_contains "--check 401 mentions invalid key" "Unauthorized" "$output"

output=$(STUB_CURL_HTTP_CODE=403 STUB_CURL_FIXTURE=response_models_ok \
  PATH="${STUBS_DIR}:${PATH}" \
  ANTHROPIC_ADMIN_API_KEY="sk-ant-admin-test-fake-key-0000" \
  bash "$SCRIPT" --check 2>&1) || exit_code=$?
assert_exit_nonzero "--check exits non-zero on HTTP 403" "${exit_code:-1}"
assert_contains "--check 403 mentions permissions" "Forbidden" "$output"

# ---- --weekly summary -------------------------------------------------------

echo ""
echo "[ --weekly summary ]"

output=$(STUB_CURL_FIXTURE=response_ok run_script --weekly 2>&1)
exit_code=$?
assert_exit_zero "--weekly exits 0" "$exit_code"
assert_contains "--weekly prints section header" "past 7 days" "$output"
assert_contains "--weekly prints table header" "Metric" "$output"
assert_contains "--weekly prints uncached input row" "Uncached input tokens" "$output"
assert_contains "--weekly prints output tokens row" "Output tokens" "$output"
assert_contains "--weekly prints total tokens row" "Total tokens" "$output"
assert_contains "--weekly prints web search row" "Web search requests" "$output"
assert_contains "--weekly aggregates uncached tokens correctly" "300,000" "$output"
assert_contains "--weekly aggregates output tokens correctly" "60,000" "$output"
assert_contains "--weekly aggregates web searches correctly" "10" "$output"

# ---- --daily summary --------------------------------------------------------

echo ""
echo "[ --daily summary ]"

output=$(STUB_CURL_FIXTURE=response_ok run_script --daily 2>&1)
exit_code=$?
assert_exit_zero "--daily exits 0" "$exit_code"
assert_contains "--daily prints today header" "Today" "$output"

# ---- --monthly summary ------------------------------------------------------

echo ""
echo "[ --monthly summary ]"

output=$(STUB_CURL_FIXTURE=response_ok run_script --monthly 2>&1)
exit_code=$?
assert_exit_zero "--monthly exits 0" "$exit_code"
assert_contains "--monthly prints 30 days header" "past 30 days" "$output"

# ---- --breakdown ------------------------------------------------------------

echo ""
echo "[ --breakdown ]"

output=$(STUB_CURL_FIXTURE=response_breakdown run_script --weekly --breakdown 2>&1)
exit_code=$?
assert_exit_zero "--breakdown exits 0" "$exit_code"
assert_contains "--breakdown prints model column header" "Model" "$output"
assert_contains "--breakdown lists claude-opus-4-5" "claude-opus-4-5" "$output"
assert_contains "--breakdown lists claude-haiku-3-5" "claude-haiku-3-5" "$output"
assert_contains "--breakdown shows opus input tokens (130,000)" "130,000" "$output"
assert_contains "--breakdown shows haiku input tokens (35,000)" "35,000" "$output"

# ---- Combining flags --------------------------------------------------------

echo ""
echo "[ Combining flags ]"

output=$(STUB_CURL_FIXTURE=response_ok run_script --daily --weekly --monthly 2>&1)
exit_code=$?
assert_exit_zero "combining --daily --weekly --monthly exits 0" "$exit_code"
assert_contains "combined output has Today section" "Today" "$output"
assert_contains "combined output has 7 days section" "past 7 days" "$output"
assert_contains "combined output has 30 days section" "past 30 days" "$output"

# ---- Default period (no flag) -----------------------------------------------

echo ""
echo "[ Default period ]"

output=$(STUB_CURL_FIXTURE=response_ok run_script 2>&1)
exit_code=$?
assert_exit_zero "no flags defaults to weekly, exits 0" "$exit_code"
assert_contains "no flags defaults to weekly output" "past 7 days" "$output"
assert_contains "no flags prints warning to stderr" "defaulting to --weekly" "$output"

# ---- Empty data -------------------------------------------------------------

echo ""
echo "[ Edge cases ]"

output=$(STUB_CURL_FIXTURE=response_empty run_script --weekly 2>&1)
exit_code=$?
assert_exit_zero "empty data response exits 0" "$exit_code"
assert_contains "empty data shows 0 for uncached tokens" "0" "$output"

# ---- Malformed response -----------------------------------------------------

output=$(STUB_CURL_FIXTURE=response_malformed run_script --weekly 2>&1) || exit_code=$?
assert_exit_nonzero "malformed response exits non-zero" "${exit_code:-1}"
assert_contains "malformed response prints clear error" "Malformed API response" "$output"

# ---- HTTP error codes -------------------------------------------------------

echo ""
echo "[ HTTP error codes ]"

output=$(STUB_CURL_HTTP_CODE=401 STUB_CURL_FIXTURE=response_ok \
  PATH="${STUBS_DIR}:${PATH}" \
  ANTHROPIC_ADMIN_API_KEY="sk-ant-admin-test-fake-key-0000" \
  bash "$SCRIPT" --weekly 2>&1) || exit_code=$?
assert_exit_nonzero "HTTP 401 exits non-zero" "${exit_code:-1}"
assert_contains "HTTP 401 prints Unauthorized" "Unauthorized" "$output"

output=$(STUB_CURL_HTTP_CODE=403 STUB_CURL_FIXTURE=response_ok \
  PATH="${STUBS_DIR}:${PATH}" \
  ANTHROPIC_ADMIN_API_KEY="sk-ant-admin-test-fake-key-0000" \
  bash "$SCRIPT" --weekly 2>&1) || exit_code=$?
assert_exit_nonzero "HTTP 403 exits non-zero" "${exit_code:-1}"
assert_contains "HTTP 403 prints Forbidden" "Forbidden" "$output"

output=$(STUB_CURL_HTTP_CODE=429 STUB_CURL_FIXTURE=response_ok \
  PATH="${STUBS_DIR}:${PATH}" \
  ANTHROPIC_ADMIN_API_KEY="sk-ant-admin-test-fake-key-0000" \
  bash "$SCRIPT" --weekly 2>&1) || exit_code=$?
assert_exit_nonzero "HTTP 429 exits non-zero" "${exit_code:-1}"
assert_contains "HTTP 429 prints rate limit message" "Too Many Requests" "$output"

output=$(STUB_CURL_HTTP_CODE=500 STUB_CURL_FIXTURE=response_ok \
  PATH="${STUBS_DIR}:${PATH}" \
  ANTHROPIC_ADMIN_API_KEY="sk-ant-admin-test-fake-key-0000" \
  bash "$SCRIPT" --weekly 2>&1) || exit_code=$?
assert_exit_nonzero "HTTP 500 exits non-zero" "${exit_code:-1}"
assert_contains "HTTP 500 prints server error message" "Server error" "$output"

# ---- Pagination -------------------------------------------------------------

echo ""
echo "[ Pagination ]"

reset_page_counter
output=$(STUB_CURL_PAGES=response_page1,response_page2 \
  PATH="${STUBS_DIR}:${PATH}" \
  ANTHROPIC_ADMIN_API_KEY="sk-ant-admin-test-fake-key-0000" \
  bash "$SCRIPT" --weekly 2>&1)
exit_code=$?
assert_exit_zero "paginated response exits 0" "$exit_code"
assert_contains "paginated response aggregates tokens across pages (300,000)" "300,000" "$output"

# ---- Key never appears in output --------------------------------------------

echo ""
echo "[ Security ]"

output=$(STUB_CURL_FIXTURE=response_ok run_script --weekly 2>&1)
assert_not_contains "API key does not appear in output" "sk-ant-admin" "$output"

# --- Summary -----------------------------------------------------------------

echo ""
echo "==================================="
total=$(( PASS + FAIL ))
if [[ "$FAIL" -eq 0 ]]; then
  green "All ${total} tests passed."
else
  red "${FAIL} of ${total} tests FAILED."
fi
echo ""

[[ "$FAIL" -eq 0 ]]
