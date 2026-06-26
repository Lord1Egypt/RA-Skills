#!/usr/bin/env bash
set -euo pipefail

# test-detection.sh
# Runs diagnose.sh against each of the 13 fixtures and asserts expected results.
# Exit 0 = all pass. Exit 1 = any fail.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURES_DIR="$SCRIPT_DIR/fixtures"
SCRIPTS_DIR="$SCRIPT_DIR/../scripts"
DIAGNOSE="$SCRIPTS_DIR/diagnose.sh"

PASS=0
FAIL=0

check() {
  local fixture="$1"
  local desc="$2"
  local must_detect="$3"    # comma-separated pattern_ids that MUST be present
  local must_not="$4"       # comma-separated pattern_ids that MUST NOT be present (or "none")

  local file="$FIXTURES_DIR/$fixture"
  if [ ! -f "$file" ]; then
    echo "FAIL [$fixture]: fixture file not found" >&2
    FAIL=$((FAIL + 1))
    return
  fi

  local findings
  findings=$(bash "$DIAGNOSE" "$file" 2>/dev/null)
  local detected_ids
  detected_ids=$(echo "$findings" | jq -r '[.[].pattern_id] | sort | @csv' 2>/dev/null || echo "")

  local ok=1

  # Check must-detect
  if [ "$must_detect" != "none" ]; then
    IFS=',' read -ra MUST <<< "$must_detect"
    for pid in "${MUST[@]}"; do
      pid="${pid// /}"  # trim spaces
      if ! echo "$findings" | jq -e --argjson p "$pid" 'any(.[]; .pattern_id == $p)' >/dev/null 2>&1; then
        echo "FAIL [$fixture]: expected pattern_id $pid but not detected (detected: [$detected_ids])"
        ok=0
      fi
    done
  fi

  # Check must-not-detect
  if [ "$must_not" != "none" ] && [ -n "$must_not" ]; then
    IFS=',' read -ra MUST_NOT <<< "$must_not"
    for pid in "${MUST_NOT[@]}"; do
      pid="${pid// /}"
      if echo "$findings" | jq -e --argjson p "$pid" 'any(.[]; .pattern_id == $p)' >/dev/null 2>&1; then
        echo "FAIL [$fixture]: pattern_id $pid should NOT be detected but was"
        ok=0
      fi
    done
  fi

  # Special case: fixture 12 must have ZERO findings
  if [ "$must_detect" = "none" ]; then
    local count
    count=$(echo "$findings" | jq 'length' 2>/dev/null || echo 1)
    if [ "$count" -ne 0 ]; then
      echo "FAIL [$fixture]: expected no findings (clean session) but got $count: [$detected_ids]"
      ok=0
    fi
  fi

  if [ "$ok" -eq 1 ]; then
    echo "PASS [$fixture]: $desc (detected: [$detected_ids])"
    PASS=$((PASS + 1))
  else
    FAIL=$((FAIL + 1))
  fi
}

# Helper for edge-case tests
check_edge() {
  local fixture="$1"
  local desc="$2"
  local expect="$3"   # should_return_empty_array

  local file="$FIXTURES_DIR/$fixture"
  if [ ! -f "$file" ]; then
    echo "FAIL [edge/$fixture]: fixture file not found"
    FAIL=$((FAIL + 1))
    return
  fi

  local findings
  findings=$(bash "$DIAGNOSE" "$file" 2>/dev/null)
  local count
  count=$(echo "$findings" | jq 'length' 2>/dev/null || echo "-1")

  if [ "$expect" = "should_return_empty_array" ]; then
    if [ "$count" -eq 0 ]; then
      echo "PASS [edge]: $desc"
      PASS=$((PASS + 1))
    else
      echo "FAIL [edge]: $desc — expected empty array, got $count finding(s)"
      FAIL=$((FAIL + 1))
    fi
  else
    echo "FAIL [edge]: $desc — unknown expectation: $expect"
    FAIL=$((FAIL + 1))
  fi
}

# Helper: test that diagnose.sh exits without crashing (exit 0 or 1 are both acceptable)
check_no_crash() {
  local fixture="$1"
  local desc="$2"

  local file="$FIXTURES_DIR/$fixture"
  if [ ! -f "$file" ]; then
    echo "FAIL [edge/$fixture]: fixture file not found"
    FAIL=$((FAIL + 1))
    return
  fi

  local exit_code=0
  bash "$DIAGNOSE" "$file" >/dev/null 2>&1 || exit_code=$?

  # Exit 0 or 1 are fine; anything else indicates a crash/unhandled error
  if [ "$exit_code" -le 1 ]; then
    echo "PASS [edge]: $desc (exit code: $exit_code)"
    PASS=$((PASS + 1))
  else
    echo "FAIL [edge]: $desc — unexpected exit code $exit_code (expected 0 or 1)"
    FAIL=$((FAIL + 1))
  fi
}

# Helper for unit tests
assert_unit() {
  local desc="$1"
  local result="$2"  # "pass" or "fail"
  if [ "$result" = "pass" ]; then
    echo "PASS [unit]: $desc"
    PASS=$((PASS + 1))
  else
    echo "FAIL [unit]: $desc"
    FAIL=$((FAIL + 1))
  fi
}

run_unit_tests() {
  echo ""
  echo "=== Unit tests ==="
  echo ""

  # Read expected version from VERSION file
  local EXPECTED_VERSION
  EXPECTED_VERSION=$(cat "$SCRIPT_DIR/../VERSION" 2>/dev/null | tr -d '[:space:]')
  EXPECTED_VERSION="${EXPECTED_VERSION:-1.0.0}"

  # 1. examine.sh --help exits 0
  if bash "$SCRIPTS_DIR/examine.sh" --help >/dev/null 2>&1; then
    assert_unit "examine.sh --help exits 0" "pass"
  else
    assert_unit "examine.sh --help exits 0" "fail"
  fi

  # 2. examine.sh --version outputs expected version and exits 0
  ver=$(bash "$SCRIPTS_DIR/examine.sh" --version 2>/dev/null)
  if [ "$ver" = "$EXPECTED_VERSION" ]; then
    assert_unit "examine.sh --version outputs $EXPECTED_VERSION" "pass"
  else
    assert_unit "examine.sh --version outputs $EXPECTED_VERSION" "fail"
  fi

  # 3. examine.sh on healthy session outputs valid JSON with required keys
  exam_out=$(bash "$SCRIPTS_DIR/examine.sh" "$FIXTURES_DIR/12-healthy-session.jsonl" 2>/dev/null)
  if echo "$exam_out" | jq -e 'has("sessionId") and has("turns") and has("total_cost") and has("tool_calls")' >/dev/null 2>&1; then
    assert_unit "examine.sh 12-healthy-session.jsonl outputs JSON with required keys" "pass"
  else
    assert_unit "examine.sh 12-healthy-session.jsonl outputs JSON with required keys" "fail"
  fi

  # 4. cost-waterfall.sh outputs valid JSON array
  cw_out=$(bash "$SCRIPTS_DIR/cost-waterfall.sh" "$FIXTURES_DIR/06-cost-spike.jsonl" 2>/dev/null)
  if echo "$cw_out" | jq -e 'type == "array"' >/dev/null 2>&1; then
    assert_unit "cost-waterfall.sh 06-cost-spike.jsonl outputs valid JSON array" "pass"
  else
    assert_unit "cost-waterfall.sh 06-cost-spike.jsonl outputs valid JSON array" "fail"
  fi

  # 5. prescribe.sh with empty array [] exits 0 and outputs "No issues detected"
  presc_out=$(echo "[]" | bash "$SCRIPTS_DIR/prescribe.sh" 2>/dev/null)
  presc_exit=$?
  if [ "$presc_exit" -eq 0 ] && echo "$presc_out" | grep -q "No issues detected"; then
    assert_unit "prescribe.sh with empty array exits 0 and outputs 'No issues detected'" "pass"
  else
    assert_unit "prescribe.sh with empty array exits 0 and outputs 'No issues detected'" "fail"
  fi

  # 6. history.sh on fixtures dir outputs valid JSON with sessions_analyzed key
  # Use a temp dir with only clean fixtures to avoid malformed file causing failure
  tmp_hist_dir=$(mktemp -d /tmp/clawdoc_hist_test.XXXXXX)
  trap 'rm -rf "$tmp_hist_dir"' RETURN
  cp "$FIXTURES_DIR/12-healthy-session.jsonl" "$tmp_hist_dir/"
  hist_out=$(bash "$SCRIPTS_DIR/history.sh" "$tmp_hist_dir" 2>/dev/null)
  if echo "$hist_out" | jq -e 'has("sessions_analyzed")' >/dev/null 2>&1; then
    assert_unit "history.sh outputs valid JSON with sessions_analyzed key" "pass"
  else
    assert_unit "history.sh outputs valid JSON with sessions_analyzed key" "fail"
  fi

  # 7 & 8. All 6 scripts respond to --help with exit 0 and --version with exit 0 and output "1.0.0"
  local all_scripts=("examine.sh" "diagnose.sh" "prescribe.sh" "cost-waterfall.sh" "history.sh" "headline.sh")

  for s in "${all_scripts[@]}"; do
    local spath="$SCRIPTS_DIR/$s"
    if [ ! -f "$spath" ]; then
      assert_unit "$s --help exits 0" "fail"
      assert_unit "$s --version exits 0 and outputs 1.0.0" "fail"
      continue
    fi

    # --help
    if bash "$spath" --help >/dev/null 2>&1; then
      assert_unit "$s --help exits 0" "pass"
    else
      assert_unit "$s --help exits 0" "fail"
    fi

    # --version
    s_ver=$(bash "$spath" --version 2>/dev/null)
    s_ver_exit=$?
    if [ "$s_ver_exit" -eq 0 ] && [ "$s_ver" = "$EXPECTED_VERSION" ]; then
      assert_unit "$s --version exits 0 and outputs $EXPECTED_VERSION" "pass"
    else
      assert_unit "$s --version exits 0 and outputs $EXPECTED_VERSION" "fail"
    fi
  done
}

run_integration_test() {
  echo ""
  echo "=== Integration test ==="
  echo ""

  # Full pipeline: examine → diagnose → prescribe
  result=$(bash "$DIAGNOSE" "$FIXTURES_DIR/01-infinite-retry.jsonl" 2>/dev/null | bash "$SCRIPTS_DIR/prescribe.sh" 2>/dev/null)

  local ok=1
  if ! echo "$result" | grep -q "Pattern 1"; then
    echo "FAIL [integration]: pipeline output missing 'Pattern 1'"
    ok=0
  fi
  if ! echo "$result" | grep -q "Diagnosis\|Prescription\|Findings"; then
    echo "FAIL [integration]: pipeline output missing 'Diagnosis' section"
    ok=0
  fi

  if [ "$ok" -eq 1 ]; then
    assert_unit "Full pipeline: diagnose | prescribe contains Pattern 1 and Diagnosis section" "pass"
  else
    assert_unit "Full pipeline: diagnose | prescribe contains Pattern 1 and Diagnosis section" "fail"
  fi
}

echo "=== clawdoc test-detection ==="
echo ""

# Fixture assertions per spec section 7
# Format: check <file> <description> <must_detect_pattern_ids> <must_not_detect_pattern_ids>
check "01-infinite-retry.jsonl"     "Infinite retry loop"              "1"       ""
check "02-non-retryable-error.jsonl" "Non-retryable error retried"     "2"       ""
check "03-tool-as-text.jsonl"       "Tool calls emitted as text"       "3"       ""
check "04-context-exhaustion.jsonl" "Context window exhaustion"        "4"       ""
check "05-subagent-replay.jsonl"    "Sub-agent replay storm"           "5"       ""
check "06-cost-spike.jsonl"         "Cost spike attribution"           "6"       ""
check "07-skill-miss.jsonl"         "Skill selection miss"             "7"       ""
check "08-model-routing-waste.jsonl" "Model routing waste"             "8"       ""
check "09-cron-accumulation.jsonl"  "Cron context accumulation"        "9"       ""
check "10-compaction-damage.jsonl"  "Compaction damage"                "10"      ""
check "11-workspace-overhead.jsonl" "Workspace token overhead"         "11"      ""
check "12-healthy-session.jsonl"    "Healthy session — no findings"    "none"    "1,2,3,4,5,6,7,8,9,10,11,12,13,14"
check "13-multi-pattern.jsonl"      "Multi-pattern (1 + 4 + 6)"        "1,4,6"   ""
check "17-task-drift-compaction.jsonl" "Task drift after compaction"    "12"      ""
check "18-task-drift-exploration.jsonl" "Exploration spiral"            "12"      ""
check "19-task-drift-negative.jsonl"   "No drift — stays on task"      "none"    "12"

echo ""
echo "=== Edge case tests (per-detector boundary) ==="
echo ""

# Edge-case fixtures: each sits just below the detection threshold
check "20-retry-edge-4x.jsonl"         "Retry 4x — below threshold (5)"           "none" "1"
check "21-non-retryable-edge-1x.jsonl" "Non-retryable 1x — below threshold (2)"   "none" "2"
check "22-tool-as-text-edge.jsonl"     "Tool names in text but not tool-as-text"   "none" "3"
check "23-context-edge-69pct.jsonl"    "Context 69% — below threshold (70%)"       "none" "4"
check "24-subagent-edge-2x.jsonl"      "Subagent replay 2x — below threshold (3)" "none" "5"
check "25-cost-edge-below.jsonl"       "Cost below thresholds (0.49/0.86)"         "none" "6"
check "26-skill-miss-edge.jsonl"       "Test failures — not skill-miss pattern"    "none" "7"
check "27-model-routing-edge.jsonl"    "Cron with cheap model — no waste"          "none" "8"
check "28-cron-accum-edge.jsonl"       "Cron tokens <2x growth — below threshold"  "none" "9"
check "29-compaction-edge.jsonl"       "Compaction but no repeated tools after"    "none" "10"
check "30-workspace-edge-14pct.jsonl"  "Workspace 14% — below threshold (15%)"    "none" "11"
check "31-task-drift-edge.jsonl"       "Same dirs post-compaction + 9 reads — no drift" "none" "12"

echo ""
echo "=== Pattern 13: Unbounded walk ==="
echo ""

check "32-unbounded-walk.jsonl"          "Unbounded walk — unscoped recursive cmds"    "13"   ""
check "33-unbounded-walk-negative.jsonl" "Scoped recursive cmds — no unbounded walk"   "none" "13"
check "34-unbounded-walk-edge.jsonl"     "Only 2 unscoped finds — below threshold (3)" "none" "13"

echo ""
echo "=== Pattern 14: Tool misuse ==="
echo ""

check "35-tool-misuse.jsonl"          "Redundant reads — same file 5x without edit"  "14"   ""
check "36-tool-misuse-negative.jsonl" "Read-edit-read cycle — no misuse"             "none" "14"
check "37-tool-misuse-edge.jsonl"     "Same file read 2x — below threshold (3)"      "none" "14"

echo ""
echo "=== Compaction threshold edge case ==="
echo ""

check "38-compaction-edge-35pct.jsonl" "35% token drop — below compaction threshold (40%)" "none" "10"

echo ""
echo "=== Edge case tests ==="
echo ""

# Section A: Edge case tests
check_edge "14-empty-session.jsonl" "Empty session (no messages)" should_return_empty_array
check_edge "16-single-turn.jsonl"   "Single-turn healthy session" should_return_empty_array
check_no_crash "15-malformed.jsonl" "Malformed JSONL does not crash diagnose"

# Section B: Unit tests
run_unit_tests

# Section C: Integration test
run_integration_test

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
exit 0
