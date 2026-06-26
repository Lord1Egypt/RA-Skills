#!/usr/bin/env bash
# REF-616 regression test: himalaya From: address must resolve from
# ~/.config/himalaya/config.toml (or $HIMALAYA_CONFIG), and the script must
# never silently fall back to antenna@localhost. Interactive From
# confirmation is selection-only — no free-text account entry.
#
# Structural coverage. Loads antenna-exchange.sh's helper functions without
# firing main(), then exercises them against synthetic himalaya config files
# and greps the code for the hardened invariants.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
EXCHANGE="$SKILL_REPO/scripts/antenna-exchange.sh"

PASS=0
FAIL=0
pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf '  \033[31m✗\033[0m %s\n' "$1"; [[ -n "${2:-}" ]] && printf '      %s\n' "$2"; }

echo "── REF-616 regression ──"

# T1: destructive fallback is gone from both send paths.
if grep -nE 'from_addr="antenna@localhost"' "$EXCHANGE" >/dev/null; then
  fail "T1: antenna@localhost fallback removed" "still present in $EXCHANGE"
else
  pass "T1: antenna@localhost fallback removed"
fi

# T2: wrong-source probe is gone (himalaya account list | jq .email).
if grep -nE 'himalaya account list -a .* -o json.*\.email' "$EXCHANGE" >/dev/null; then
  fail "T2: legacy '.email from account list -o json' probe removed" "still present"
else
  pass "T2: legacy '.email from account list -o json' probe removed"
fi

# T3: new helpers exist.
for fn in himalaya_config_path himalaya_account_email himalaya_accounts_list select_himalaya_account confirm_from_account; do
  if grep -qE "^${fn}\\(\\)" "$EXCHANGE"; then
    pass "T3.${fn}: helper defined"
  else
    fail "T3.${fn}: helper defined" "missing function ${fn}"
  fi
done

# T4: send_bundle_email hard-fails on unresolved email via die (no silent fallback).
if awk '/^send_bundle_email\(\)/,/^}/' "$EXCHANGE" | grep -q 'die "Could not resolve email address for himalaya account'; then
  pass "T4: send_bundle_email dies when email cannot be resolved"
else
  fail "T4: send_bundle_email dies when email cannot be resolved"
fi

# T5: send_pubkey_email hard-fails on unresolved email via die (no silent fallback).
if awk '/^send_pubkey_email\(\)/,/^}/' "$EXCHANGE" | grep -q 'die "Could not resolve email address for himalaya account'; then
  pass "T5: send_pubkey_email dies when email cannot be resolved"
else
  fail "T5: send_pubkey_email dies when email cannot be resolved"
fi

# T6: interactive bundle path no longer free-text-prompts for account name.
if awk '/run_bundle_command\(\)/,/^decrypt_bundle_to_json/' "$EXCHANGE" | grep -q 'prompt interactive_account "Himalaya account name"'; then
  fail "T6: bundle interactive path removed free-text account prompt" "still present"
else
  pass "T6: bundle interactive path removed free-text account prompt"
fi

# T7: interactive pubkey path no longer free-text-prompts for account name.
if awk '/cmd_pubkey\(\)/,/^cmd_initiate_or_reply/' "$EXCHANGE" | grep -q 'prompt interactive_account "Himalaya account name"'; then
  fail "T7: pubkey interactive path removed free-text account prompt" "still present"
else
  pass "T7: pubkey interactive path removed free-text account prompt"
fi

# T8: interactive paths now route through the selection-only confirm helper.
# Note: awk | grep -q under `set -o pipefail` can spuriously fail when grep -q
# short-circuits and awk gets SIGPIPE (141). Avoid that by materializing awk's
# full output first, then grepping without -q.
_bundle_region="$(awk '/run_bundle_command\(\)/,/^decrypt_bundle_to_json/' "$EXCHANGE")"
if printf '%s\n' "$_bundle_region" | grep -F 'confirm_from_account ' >/dev/null; then
  pass "T8.bundle: interactive bundle path uses confirm_from_account"
else
  fail "T8.bundle: interactive bundle path uses confirm_from_account"
fi
_pubkey_region="$(awk '/cmd_pubkey\(\)/,/^cmd_initiate_or_reply/' "$EXCHANGE")"
if printf '%s\n' "$_pubkey_region" | grep -F 'confirm_from_account ' >/dev/null; then
  pass "T8.pubkey: interactive pubkey path uses confirm_from_account"
else
  fail "T8.pubkey: interactive pubkey path uses confirm_from_account"
fi

# Load helpers for live probes by materializing the script with SCRIPT_DIR/SKILL_DIR
# pinned and main() call stripped.
TMPSH=$(mktemp --suffix=.sh)
sed \
  -e "s|SCRIPT_DIR=\"\$(cd \"\$(dirname \"\$0\")\" && pwd)\"|SCRIPT_DIR=\"$SKILL_REPO/scripts\"|" \
  -e "s|SKILL_DIR=\"\$(dirname \"\$SCRIPT_DIR\")\"|SKILL_DIR=\"$SKILL_REPO\"|" \
  -e 's|^main "\$@"$|# main stripped|' \
  "$EXCHANGE" > "$TMPSH"
# shellcheck disable=SC1090
source "$TMPSH"
rm -f "$TMPSH"

# Build a synthetic himalaya config and point $HIMALAYA_CONFIG at it.
FAKE_CFG=$(mktemp)
cat > "$FAKE_CFG" <<'TOML'
[accounts.alpha]
email = "alpha@example.com"
backend = "imap"

[accounts.beta]
# no email key on purpose
backend = "smtp"

[accounts.gamma]
email = "gamma@example.com"
TOML
export HIMALAYA_CONFIG="$FAKE_CFG"

# T9: $HIMALAYA_CONFIG override is honored.
out="$(himalaya_config_path)"
if [[ "$out" == "$FAKE_CFG" ]]; then
  pass "T9: \$HIMALAYA_CONFIG override honored"
else
  fail "T9: \$HIMALAYA_CONFIG override honored" "got '$out' expected '$FAKE_CFG'"
fi

# T10: email lookup for a configured account returns the real address.
out="$(himalaya_account_email alpha)"
if [[ "$out" == "alpha@example.com" ]]; then
  pass "T10: himalaya_account_email returns the configured address"
else
  fail "T10: himalaya_account_email returns the configured address" "got '$out'"
fi

# T11: account with no email key returns empty (hard-fail trigger for callers).
out="$(himalaya_account_email beta || true)"
if [[ -z "$out" ]]; then
  pass "T11: missing email key returns empty (no fallback)"
else
  fail "T11: missing email key returns empty (no fallback)" "got '$out'"
fi

# T12: unknown account returns empty.
out="$(himalaya_account_email noSuchAccount || true)"
if [[ -z "$out" ]]; then
  pass "T12: unknown account returns empty"
else
  fail "T12: unknown account returns empty" "got '$out'"
fi

# T13: $HIMALAYA_CONFIG pointing at a missing file falls back to default path
# resolution (not a crash).
export HIMALAYA_CONFIG=/tmp/nonexistent-ref616-himalaya.toml
out="$(himalaya_account_email alpha || true)"
if [[ -z "$out" ]]; then
  pass "T13: missing \$HIMALAYA_CONFIG file does not crash"
else
  fail "T13: missing \$HIMALAYA_CONFIG file does not crash" "got '$out'"
fi

# T14: no free-text email prompt anywhere in the From-account flow.
# (Guards against regressing the selection-only decision.)
if awk '/confirm_from_account\(\)/,/^select_himalaya_account/' "$EXCHANGE" | grep -qE 'prompt[[:space:]]+[a-z_]+[[:space:]]+"(From|Email|email|address|From address)'; then
  fail "T14: confirm_from_account does not prompt for free-text email" "free-text prompt found inside helper"
else
  pass "T14: confirm_from_account does not prompt for free-text email"
fi

# T15: select_himalaya_account uses strict numeric validation.
if awk '/^select_himalaya_account\(\)/,/^confirm_from_account/' "$EXCHANGE" | grep -qE '\[\[ "\$choice" =~ \^\[0-9\]\+\$ \]\]'; then
  pass "T15: select_himalaya_account rejects non-numeric input"
else
  fail "T15: select_himalaya_account rejects non-numeric input"
fi

rm -f "$FAKE_CFG"

echo
echo "Passed: $PASS"
echo "Failed: $FAIL"
[[ "$FAIL" -eq 0 ]]
