#!/usr/bin/env bash

set -euo pipefail

NEED_IOS="${NEED_IOS:-yes}"         # yes|no
NEED_ANDROID="${NEED_ANDROID:-yes}" # yes|no

RED="$(printf '\033[31m')"
GREEN="$(printf '\033[32m')"
YELLOW="$(printf '\033[33m')"
RESET="$(printf '\033[0m')"

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  printf "${GREEN}PASS${RESET} - %s\n" "$1"
}

fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  printf "${RED}FAIL${RESET} - %s\n" "$1"
}

warn() {
  WARN_COUNT=$((WARN_COUNT + 1))
  printf "${YELLOW}WARN${RESET} - %s\n" "$1"
}

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

check_cmd() {
  local cmd="$1"
  local label="$2"
  if has_cmd "$cmd"; then
    pass "$label"
  else
    fail "$label (missing command: $cmd)"
  fi
}

check_env() {
  local key="$1"
  local expected="$2"
  local actual="${!key:-}"
  if [[ "$actual" == "$expected" ]]; then
    pass "$key is set to $expected"
  elif [[ -z "$actual" ]]; then
    fail "$key is not set"
  else
    warn "$key is '$actual' (expected '$expected')"
  fi
}

check_flutter_doctor() {
  if ! has_cmd flutter; then
    fail "flutter doctor check skipped (flutter not found)"
    return
  fi

  local doctor_output
  doctor_output="$(flutter doctor -v 2>&1 || true)"

  if printf '%s' "$doctor_output" | grep -q "No issues found!"; then
    pass "flutter doctor reports no issues"
    return
  fi

  # Android checks
  if [[ "$NEED_ANDROID" == "yes" ]]; then
    if printf '%s' "$doctor_output" | grep -Eq "Android toolchain .* [•✓]" \
      && ! printf '%s' "$doctor_output" | grep -Eq "Android toolchain .* ✗"; then
      pass "Android toolchain is available"
    else
      fail "Android toolchain has issues"
    fi
  fi

  # iOS checks
  if [[ "$NEED_IOS" == "yes" ]]; then
    if printf '%s' "$doctor_output" | grep -Eq "Xcode .* [•✓]" \
      && ! printf '%s' "$doctor_output" | grep -Eq "Xcode .* ✗"; then
      pass "Xcode toolchain is available"
    else
      fail "Xcode toolchain has issues"
    fi

    if printf '%s' "$doctor_output" | grep -Eq "CocoaPods .* [•✓]" \
      && ! printf '%s' "$doctor_output" | grep -Eq "CocoaPods .* ✗"; then
      pass "CocoaPods is available"
    else
      fail "CocoaPods has issues"
    fi
  fi
}

check_devices() {
  if ! has_cmd flutter; then
    fail "flutter devices check skipped (flutter not found)"
    return
  fi

  local devices_output
  devices_output="$(flutter devices 2>&1 || true)"

  if printf '%s' "$devices_output" | grep -q "No devices detected"; then
    warn "No runtime devices detected (emulator/simulator/physical)"
    return
  fi

  pass "At least one Flutter runtime device is detected"
}

print_summary() {
  printf "\n====================\n"
  printf "Validation Summary\n"
  printf "PASS: %s\n" "$PASS_COUNT"
  printf "WARN: %s\n" "$WARN_COUNT"
  printf "FAIL: %s\n" "$FAIL_COUNT"
  printf "====================\n"

  if [[ "$FAIL_COUNT" -eq 0 ]]; then
    printf "${GREEN}Result: READY for development${RESET}\n"
    exit 0
  else
    printf "${RED}Result: NOT READY${RESET}\n"
    printf "Fix FAIL items, then rerun this validator.\n"
    exit 1
  fi
}

main() {
  echo "Flutter CN environment validation"
  echo "NEED_ANDROID=$NEED_ANDROID NEED_IOS=$NEED_IOS"
  echo

  check_cmd flutter "Flutter CLI installed"
  check_cmd git "Git installed"
  check_cmd brew "Homebrew installed"

  check_env PUB_HOSTED_URL "https://pub.flutter-io.cn"
  check_env FLUTTER_STORAGE_BASE_URL "https://storage.flutter-io.cn"

  check_flutter_doctor
  check_devices
  print_summary
}

main "$@"
