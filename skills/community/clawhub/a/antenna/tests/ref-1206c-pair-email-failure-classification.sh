#!/usr/bin/env bash
# REF-1206c regression test: pair wizard must classify email-send failure
# as a hard failure rather than printing "Press Enter once you've sent it off"
# as if delivery had succeeded.
#
# Structural coverage only. Validates that scripts/antenna-pair.sh:
#   1. captures the exit status of the send subprocess (no bare `|| true`),
#   2. tracks BUNDLE_EMAIL_ATTEMPTED / BUNDLE_EMAIL_DELIVERED flags,
#   3. on delivery success: skips the "sent it off" prompt,
#   4. on delivery failure: emits an explicit "Email delivery failed" message
#      and asks for manual-delivery ack rather than soft-confirming,
#   5. preserves the original "sent it off" prompt only on the
#      no-email-attempted path.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
PAIR="$SKILL_REPO/scripts/antenna-pair.sh"

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf '  \033[31m✗\033[0m %s\n' "$1"; [[ -n "${2:-}" ]] && printf '      %s\n' "$2"; }

echo "── REF-1206c regression ──"

# T1: the old soft-success pattern (`|| true` on the antenna send call) must
#     be gone. That was the core bug: the pair wizard discarded the exit
#     code and then presented "sent it off" to the operator.
if grep -n 'EMAIL_OUTPUT=\$(bash "\$ANTENNA" "\${EMAIL_ARGS\[@\]}" 2>&1) || true' "$PAIR" >/dev/null; then
  fail "T1: no `|| true` on the antenna send invocation" \
       "found legacy soft-success capture that masked real delivery failures"
else
  pass "T1: no \`|| true\` on the antenna send invocation"
fi

# T2: the new code must capture the exit status into a dedicated variable.
if grep -q 'EMAIL_EXIT=\$?' "$PAIR"; then
  pass "T2: exit status of send is captured"
else
  fail "T2: exit status of send is captured" \
       "expected EMAIL_EXIT=\$? capture after the antenna invocation"
fi

# T3: BUNDLE_EMAIL_ATTEMPTED must be set before the send subprocess runs so
#     the later branching logic can distinguish "no email tried" from
#     "email tried and failed".
if grep -q 'BUNDLE_EMAIL_ATTEMPTED="y"' "$PAIR"; then
  pass "T3: email-attempted state flips before the send call"
else
  fail "T3: email-attempted state flips before the send call" \
       "expected BUNDLE_EMAIL_ATTEMPTED=\"y\" before the antenna send invocation"
fi

# T4: BUNDLE_EMAIL_DELIVERED must only flip to "y" on exit 0.
if grep -q 'if \[\[ \$EMAIL_EXIT -eq 0 \]\]; then' "$PAIR" \
   && grep -q 'BUNDLE_EMAIL_DELIVERED="y"' "$PAIR"; then
  pass "T4: delivery flag gated on EMAIL_EXIT == 0"
else
  fail "T4: delivery flag gated on EMAIL_EXIT == 0" \
       "expected BUNDLE_EMAIL_DELIVERED=\"y\" only inside an EMAIL_EXIT -eq 0 guard"
fi

# T5: on explicit failure the wizard must say so clearly. No soft-confirm.
if grep -q 'Email delivery failed — bundle was NOT sent.' "$PAIR"; then
  pass "T5: explicit failure message present"
else
  fail "T5: explicit failure message present" \
       "expected 'Email delivery failed — bundle was NOT sent.' on the failure branch"
fi

# T6: after a failure the wizard should ask the operator to confirm manual
#     delivery rather than unconditionally moving on with a success-toned
#     prompt.
if grep -q 'Did you deliver it out of band?' "$PAIR"; then
  pass "T6: manual-delivery ack prompt present on failure path"
else
  fail "T6: manual-delivery ack prompt present on failure path" \
       "expected 'Did you deliver it out of band?' prompt on the failure branch"
fi

# T7: the legacy "Press Enter once you've sent it off" prompt must now be
#     reachable only on the no-email-attempted branch. We check that it is
#     inside an else after the attempted/delivered checks, i.e. gated by
#     BUNDLE_EMAIL_ATTEMPTED being "n".
#     Implementation check: the only remaining `wait_for_enter "Press Enter
#     once you've sent it off"` line must sit inside an `else` branch.
awk '
  /wait_for_enter "Press Enter once you'\''ve sent it off"/ {
    target_line = NR
    print NR
  }
' "$PAIR" > /tmp/ref-1206c-pair.lines

pair_lines="$(cat /tmp/ref-1206c-pair.lines)"
count_lines=$(printf '%s\n' "$pair_lines" | grep -c '.' || true)
rm -f /tmp/ref-1206c-pair.lines

if [[ "$count_lines" -ne 1 ]]; then
  fail "T7: exactly one legacy 'sent it off' prompt remains" \
       "found $count_lines occurrences; expected exactly 1 (on the no-email-attempted path)"
else
  # Confirm that an `else` appears within the 10 lines preceding that prompt,
  # which is how the new branching guards it.
  target_line=$(printf '%s\n' "$pair_lines" | tr -d '[:space:]')
  start=$(( target_line - 10 ))
  (( start < 1 )) && start=1
  preceding_block="$(awk -v s="$start" -v e="$target_line" 'NR>=s && NR<=e' "$PAIR")"
  if printf '%s\n' "$preceding_block" | grep -q '^[[:space:]]*else'; then
    pass "T7: legacy 'sent it off' prompt is gated by an else branch"
  else
    fail "T7: legacy 'sent it off' prompt is gated by an else branch" \
         "did not see an else clause immediately guarding the prompt"
  fi
fi

echo ""
printf 'Result: \033[32m%s passed\033[0m, \033[31m%s failed\033[0m\n' "$PASS" "$FAIL"

if (( FAIL > 0 )); then
  exit 1
fi
