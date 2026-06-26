#!/usr/bin/env bash
# REF-603 regression test: plaintext bootstrap bundle JSON must never leak to
# /tmp, and any decrypted plaintext must be cleaned up on every exit path.
#
# Layers under test:
#   1. Encrypt path hardening: build_plaintext_bundle_stdout writes to stdout
#      (not a temp file); run_bundle_command pipes directly into age. No
#      plaintext temp file is ever created during encrypt, so there is
#      nothing to leak on failure.
#   2. Decrypt path hardening: import_bundle installs a RETURN/EXIT/INT/TERM
#      trap immediately after decrypt_bundle_to_json, so the plaintext temp
#      file is removed even when validate_* or print_import_preview call die.
#   3. Legacy temp-file pattern on encrypt is gone (no mktemp/jq->file then
#      age(file) sequence in run_bundle_command).
#
# This test is structural + seam-level. It does not require a running gateway.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
EXCHANGE="$SKILL_REPO/scripts/antenna-exchange.sh"

TEST_ROOT="$(mktemp -d /tmp/antenna-ref603-XXXXXX)"
trap 'rm -rf "$TEST_ROOT"' EXIT

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf '  \033[31m✗\033[0m %s\n' "$1"; [[ -n "${2:-}" ]] && printf '      %s\n' "$2"; }

echo "── REF-603 regression ──"

# ─── T1: encrypt-side helper writes plaintext to stdout, not a temp file ────
if awk '/^build_plaintext_bundle_stdout\(\) \{/,/^\}$/' "$EXCHANGE" \
  | grep -Eq '^\s*jq -n '; then
  # The new helper should NOT call mktemp or redirect to a file.
  if awk '/^build_plaintext_bundle_stdout\(\) \{/,/^\}$/' "$EXCHANGE" \
    | grep -Eq 'mktemp|bundle_json=\$\(mktemp\)|> *"\$bundle_json"'; then
    fail "T1: build_plaintext_bundle_stdout streams to stdout" \
         "found mktemp/temp-file write inside the helper"
  else
    pass "T1: build_plaintext_bundle_stdout streams to stdout (no mktemp)"
  fi
else
  fail "T1: build_plaintext_bundle_stdout streams to stdout" \
       "helper not found or does not build with jq"
fi

# ─── T2: encrypt-side wrapper takes plaintext from stdin, not a file arg ────
if awk '/^encrypt_bundle_from_stdin\(\) \{/,/^\}$/' "$EXCHANGE" \
  | grep -Eq 'age .* -o "\$output_file" -[[:space:]]*$'; then
  pass "T2: encrypt_bundle_from_stdin invokes age with stdin input"
else
  fail "T2: encrypt_bundle_from_stdin invokes age with stdin input" \
       "helper missing or does not use stdin"
fi

# ─── T3: legacy encrypt path (jq -> tempfile -> age file) is gone ───────────
if awk '/^run_bundle_command\(\) \{/,/^}$/' "$EXCHANGE" \
  | grep -Eq 'bundle_json="\$\(build_plaintext_bundle '; then
  fail "T3: legacy temp-file encrypt path removed from run_bundle_command" \
       "found legacy build_plaintext_bundle call"
else
  pass "T3: legacy temp-file encrypt path removed from run_bundle_command"
fi

# Also: run_bundle_command must actually pipe stdout into encrypt_bundle_from_stdin.
if awk '/^run_bundle_command\(\) \{/,/^}$/' "$EXCHANGE" \
  | grep -Eq 'build_plaintext_bundle_stdout .* \| encrypt_bundle_from_stdin '; then
  pass "T3b: run_bundle_command pipes plaintext straight into age"
else
  fail "T3b: run_bundle_command pipes plaintext straight into age" \
       "expected pipe 'build_plaintext_bundle_stdout ... | encrypt_bundle_from_stdin ...' not found"
fi

# ─── T4: import_bundle installs a cleanup trap before any validate step ────
IMPORT_BODY="$(awk '/^import_bundle\(\) \{/,/^\}$/' "$EXCHANGE")"
DECRYPT_LINE=$(printf '%s\n' "$IMPORT_BODY" | grep -n 'bundle_json="\$(decrypt_bundle_to_json ' | cut -d: -f1 | head -n1)
TRAP_LINE=$(printf '%s\n' "$IMPORT_BODY" | grep -nE '^[[:space:]]*trap .*bundle_json' | cut -d: -f1 | head -n1)
VALIDATE_LINE=$(printf '%s\n' "$IMPORT_BODY" | grep -nE '^[[:space:]]*validate_bundle_json ' | cut -d: -f1 | head -n1)
if [[ -n "$DECRYPT_LINE" && -n "$TRAP_LINE" && -n "$VALIDATE_LINE" \
      && "$DECRYPT_LINE" -lt "$TRAP_LINE" && "$TRAP_LINE" -lt "$VALIDATE_LINE" ]]; then
  pass "T4: import_bundle installs cleanup trap between decrypt and validate"
else
  fail "T4: import_bundle installs cleanup trap between decrypt and validate" \
       "expected decrypt -> trap -> validate ordering in import_bundle"
fi

# ─── T5: import_bundle trap covers SIGINT and SIGTERM, not just RETURN ─────
if printf '%s\n' "$IMPORT_BODY" | grep -Eq 'trap .*bundle_json.* (RETURN|EXIT).*(INT|TERM)'; then
  pass "T5: import_bundle cleanup trap covers INT/TERM"
else
  fail "T5: import_bundle cleanup trap covers INT/TERM" \
       "trap should cover RETURN EXIT INT TERM"
fi

# ─── T6: redundant `rm -f \"\$bundle_json\"` removed from happy path ─────────
# With a proper trap, manual rm calls are redundant. Two places used to have
# them (self-peer refuse branch and end of function). They should be gone or
# at minimum not be the only line of defense.
RM_COUNT=$(printf '%s\n' "$IMPORT_BODY" | grep -cE '^\s*rm -f "\$bundle_json"\s*$' || true)
if [[ "$RM_COUNT" -eq 0 ]]; then
  pass "T6: redundant rm -f \"\$bundle_json\" calls removed in favour of trap"
else
  fail "T6: redundant rm -f \"\$bundle_json\" calls removed in favour of trap" \
       "still found $RM_COUNT manual rm call(s); trap should be sufficient"
fi

# ─── T7: LIVE seam — failed validate does not leak plaintext ────────────────
# Simulate the validate-step failure path: hand decrypt_bundle_to_json a
# plaintext file, then call validate_bundle_json on malformed JSON and assert
# the temp file is cleaned up by the trap. We model this by literally
# exercising the trap behaviour in an isolated harness that mirrors
# import_bundle's trap shape.

PLAINTEXT="$TEST_ROOT/plaintext-bundle.json"
echo '{"not":"a real bundle"}' > "$PLAINTEXT"

HARNESS="$TEST_ROOT/harness.sh"
cat > "$HARNESS" <<'BASH'
#!/usr/bin/env bash
# Mirrors the trap shape installed in import_bundle after REF-603.
set -euo pipefail

die() { echo "$1" >&2; exit "${2:-1}"; }

# Stand-in for decrypt_bundle_to_json: just prints the pre-staged path.
decrypt_bundle_to_json() { printf '%s\n' "$1"; }

# Stand-in for validate_bundle_json that always fails via die().
validate_bundle_json() { die "validate failed"; }

simulated_import() {
  local bundle_json
  bundle_json="$(decrypt_bundle_to_json "$1")"
  # Exactly the REF-603 trap shape, copied verbatim from import_bundle.
  # shellcheck disable=SC2064
  trap "rm -f '$bundle_json' 2>/dev/null || true" RETURN EXIT INT TERM
  validate_bundle_json "$bundle_json"
}

simulated_import "$1"
BASH
chmod +x "$HARNESS"

set +e
"$HARNESS" "$PLAINTEXT" >/dev/null 2>&1
set -e

if [[ ! -e "$PLAINTEXT" ]]; then
  pass "T7: plaintext temp file cleaned up after validate-step die()"
else
  fail "T7: plaintext temp file cleaned up after validate-step die()" \
       "file still exists: $PLAINTEXT"
fi

# ─── T8: LIVE seam — happy path also cleans up via RETURN trap ─────────────
PLAINTEXT2="$TEST_ROOT/plaintext-bundle-2.json"
echo '{"ok":true}' > "$PLAINTEXT2"

HARNESS2="$TEST_ROOT/harness-ok.sh"
cat > "$HARNESS2" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail
decrypt_bundle_to_json() { printf '%s\n' "$1"; }
simulated_import() {
  local bundle_json
  bundle_json="$(decrypt_bundle_to_json "$1")"
  # shellcheck disable=SC2064
  trap "rm -f '$bundle_json' 2>/dev/null || true" RETURN EXIT INT TERM
  # Happy path: no die. Function returns normally; RETURN trap should fire.
  return 0
}
simulated_import "$1"
BASH
chmod +x "$HARNESS2"

"$HARNESS2" "$PLAINTEXT2" >/dev/null 2>&1
if [[ ! -e "$PLAINTEXT2" ]]; then
  pass "T8: plaintext temp file cleaned up on happy-path RETURN"
else
  fail "T8: plaintext temp file cleaned up on happy-path RETURN" \
       "file still exists: $PLAINTEXT2"
fi

# ─── T9: LIVE seam — SIGTERM mid-flow still cleans up ──────────────────────
PLAINTEXT3="$TEST_ROOT/plaintext-bundle-3.json"
echo '{"secret":"nope"}' > "$PLAINTEXT3"

HARNESS3="$TEST_ROOT/harness-sigterm.sh"
cat > "$HARNESS3" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail
decrypt_bundle_to_json() { printf '%s\n' "$1"; }
simulated_import() {
  local bundle_json
  bundle_json="$(decrypt_bundle_to_json "$1")"
  # shellcheck disable=SC2064
  trap "rm -f '$bundle_json' 2>/dev/null || true" RETURN EXIT INT TERM
  # Simulate a long-running step that reacts directly to TERM.
  python3 - <<'PY'
import signal, time
signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(SystemExit(143)))
while True:
    time.sleep(1)
PY
}
simulated_import "$1"
BASH
chmod +x "$HARNESS3"

setsid "$HARNESS3" "$PLAINTEXT3" >/dev/null 2>&1 &
BG_PID=$!
# Give the bash trap and the python signal handler time to install.
sleep 0.5
# Send SIGTERM to the whole process group so the python child actually receives it.
kill -TERM -- -"$BG_PID" 2>/dev/null || true
# Belt-and-suspenders: also target any python child of the harness directly.
for child in $(pgrep -P "$BG_PID" 2>/dev/null); do
  kill -TERM "$child" 2>/dev/null || true
done
kill -TERM "$BG_PID" 2>/dev/null || true
# Bounded wait so a misbehaving harness can't hang the whole suite.
for _ in 1 2 3 4 5 6 7 8 9 10; do
  kill -0 "$BG_PID" 2>/dev/null || break
  sleep 0.2
done
kill -KILL -- -"$BG_PID" 2>/dev/null || true
kill -KILL "$BG_PID" 2>/dev/null || true
wait "$BG_PID" 2>/dev/null || true

if [[ ! -e "$PLAINTEXT3" ]]; then
  pass "T9: plaintext temp file cleaned up on SIGTERM"
else
  fail "T9: plaintext temp file cleaned up on SIGTERM" \
       "file still exists: $PLAINTEXT3"
fi

# ─── T10: CHANGELOG Unreleased mentions REF-603 ────────────────────────────
if grep -q 'REF-603' "$SKILL_REPO/CHANGELOG.md"; then
  pass "T10: CHANGELOG references REF-603"
else
  fail "T10: CHANGELOG references REF-603" "no REF-603 entry found"
fi

echo
echo "── Summary ──"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"

[[ $FAIL -eq 0 ]]
