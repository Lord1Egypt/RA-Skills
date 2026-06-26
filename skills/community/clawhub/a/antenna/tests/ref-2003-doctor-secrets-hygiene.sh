#!/usr/bin/env bash
# REF-2003 regression test: `antenna doctor` surfaces secrets-directory
# hygiene problems.
#
# Section 6 of the existing doctor audits per-peer secrets *referenced
# from antenna-peers.json*. It says nothing about:
#   - orphan secret files whose peer ID is no longer in the registry
#     (the file-side counterpart to the pre-REF-1312 allowlist drift
#      for `nexus` / `bruce`)
#   - `.bak*` / `.backup*` / `~` / `.old` backup files whose perms drift
#     silently over time
#   - the permissions on secrets/ itself being too loose
#   - wholly unrecognized files sitting in secrets/
#
# This is the 6b section added by REF-2003.
#
# Cases covered:
#   1. Clean secrets/ (just known peer secrets + age bootstrap) → affirmative
#      pass lines, no warns.
#   2. Loose directory permissions (775) → warn.
#   3. Orphan peer secret (antenna-peer-<unknown>.secret) → warn + ID visible.
#   4. Orphan hooks token (hooks_token_<unknown>) → warn + ID visible.
#   5. Orphan `peer_secret_<unknown>` → warn + ID visible.
#   6. Backup file (`*.bak-*`) → warn + filename visible, not counted as orphan.
#   7. File with loose perms (644) → warn + filename + perm visible.
#   8. Unknown-shape file → warn + filename visible.
#   9. Missing secrets dir → info, never crashes.
#
# Isolated SKILL_DIR; does not touch the live registry.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"

TEST_ROOT="$(mktemp -d /tmp/antenna-ref2003-XXXXXX)"
trap 'rm -rf "$TEST_ROOT"' EXIT

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() {
  FAIL=$((FAIL + 1))
  printf '  \033[31m✗\033[0m %s\n' "$1"
  [[ -n "${2:-}" ]] && printf '      %s\n' "$2"
}

# ── Build an isolated SKILL_DIR ──────────────────────────────────────────
setup_skill_dir() {
  SKILL_DIR="$TEST_ROOT/skill-$1"
  rm -rf "$SKILL_DIR"
  mkdir -p "$SKILL_DIR/bin" "$SKILL_DIR/lib" "$SKILL_DIR/scripts" "$SKILL_DIR/secrets"
  cp "$SKILL_REPO/bin/antenna.sh" "$SKILL_DIR/bin/"
  cp -r "$SKILL_REPO/lib/." "$SKILL_DIR/lib/"
  cp -r "$SKILL_REPO/scripts/." "$SKILL_DIR/scripts/"
  chmod 700 "$SKILL_DIR/secrets"

  # Baseline peers file: valid self-peer + one known non-self peer.
  cat > "$SKILL_DIR/antenna-peers.json" <<'JSON'
{
  "testhost": {
    "self": true,
    "url": "https://testhost.example.com",
    "peer_secret_file": "secrets/antenna-peer-testhost.secret"
  },
  "alice": {
    "url": "https://alice.example.com",
    "token_file": "secrets/hooks_token_alice",
    "peer_secret_file": "secrets/antenna-peer-alice.secret"
  }
}
JSON

  # Minimal config (no drift) so 1b doesn't drown our output.
  cat > "$SKILL_DIR/antenna-config.json" <<'JSON'
{
  "self_id": "testhost",
  "allowed_inbound_peers": ["alice"],
  "allowed_outbound_peers": ["alice"],
  "inbox_auto_approve_peers": [],
  "allowed_inbound_sessions": []
}
JSON

  # Known peer secrets at 600 so section 6 passes cleanly.
  install -m 600 /dev/stdin "$SKILL_DIR/secrets/antenna-peer-testhost.secret" <<<"testhost-secret"
  install -m 600 /dev/stdin "$SKILL_DIR/secrets/antenna-peer-alice.secret"    <<<"alice-secret"
  install -m 600 /dev/stdin "$SKILL_DIR/secrets/hooks_token_alice"            <<<"alice-token"

  # Stub gateway config. If we point --gateway at a nonexistent path,
  # `jq empty` reports invalid JSON and doctor exits before section 6b runs
  # (see find_gateway_config — an explicit --gateway path is echoed verbatim,
  # existent or not). The file itself just needs to be valid JSON so the
  # outer gateway-validity branch continues into sections 3+.
  cat > "$SKILL_DIR/openclaw.json" <<'JSON'
{
  "hooks": { "enabled": true, "allowRequestSessionKey": true, "token": "stub" },
  "agents": {},
  "plugins": {}
}
JSON
}

run_doctor() {
  local out
  out="$(
    cd "$SKILL_DIR" && \
    SKILL_DIR="$SKILL_DIR" bash "$SKILL_DIR/scripts/antenna-doctor.sh" \
      --gateway "$SKILL_DIR/openclaw.json" 2>&1
  )" || true
  # Strip ANSI escapes so downstream section extraction and greps are
  # deterministic across color/no-color environments.
  printf '%s' "$out" | sed $'s/\x1b\\[[0-9;]*m//g'
}

extract_hygiene_section() {
  # Sections headers land as "6b. Secrets Directory Hygiene" and
  # "7. Connectivity (quick check)" once ANSI is stripped.
  sed -n '/6b\. Secrets Directory Hygiene/,/^7\. Connectivity/p' <<<"$1"
}

# ── Case 1: clean secrets/ ────────────────────────────────────────────────
echo "── REF-2003 case 1: clean secrets/ produces pass, no warn ─────────────"
setup_skill_dir case1

out="$(run_doctor)"
sec="$(extract_hygiene_section "$out")"

if grep -qF "secrets/ directory permissions OK" <<<"$sec"; then
  pass "clean dir perms produce affirmative pass line"
else
  fail "clean dir perms did not produce pass line" "$sec"
fi
if grep -qF "No orphan peer secrets in secrets/" <<<"$sec"; then
  pass "clean secrets/ produces 'no orphans' pass line"
else
  fail "clean secrets/ did not produce 'no orphans' pass line" "$sec"
fi
if grep -qF "No stale backup files in secrets/" <<<"$sec"; then
  pass "clean secrets/ produces 'no backups' pass line"
else
  fail "clean secrets/ did not produce 'no backups' pass line" "$sec"
fi
# Scope strictly to section 6b's own warn lines. Section 7 may still emit
# connectivity warnings in the isolated harness (peer URL is bogus), and
# those are not 6b's concern. Also: `No stale backup files` and
# `No orphan peer secrets` are pass lines whose substrings overlap the warn
# phrasing, so we match only the actual warn text which contains "(s)".
if grep -qE "orphan secret file\(s\) in secrets/|stale backup file\(s\) in secrets/|file\(s\) in secrets/ with loose permissions|unrecognized file\(s\) in secrets/" <<<"$sec"; then
  fail "clean secrets/ should not produce any 6b warn lines" "$sec"
else
  pass "clean secrets/ produced no 6b warn lines"
fi

# ── Case 2: loose dir perms ───────────────────────────────────────────────
echo ""
echo "── REF-2003 case 2: loose dir perms (775) produce warn ────────────────"
setup_skill_dir case2
chmod 775 "$SKILL_DIR/secrets"

out="$(run_doctor)"
sec="$(extract_hygiene_section "$out")"

if grep -qE "secrets/ directory permissions \(775\).*should be 700" <<<"$sec"; then
  pass "775 on secrets/ is called out"
else
  fail "775 on secrets/ was not warned" "$sec"
fi
chmod 700 "$SKILL_DIR/secrets"  # restore for further checks

# ── Case 3: orphan antenna-peer-<unknown>.secret ─────────────────────────
echo ""
echo "── REF-2003 case 3: orphan antenna-peer-<unknown>.secret ──────────────"
setup_skill_dir case3
install -m 600 /dev/stdin "$SKILL_DIR/secrets/antenna-peer-nexus.secret" <<<"x"

out="$(run_doctor)"
sec="$(extract_hygiene_section "$out")"

if grep -qF "orphan secret file(s) in secrets/: 1" <<<"$sec"; then
  pass "orphan antenna-peer-*.secret produces warn with count 1"
else
  fail "orphan antenna-peer-*.secret was not reported" "$sec"
fi
if grep -qE -- "- antenna-peer-nexus\.secret" <<<"$sec"; then
  pass "orphan filename appears in output"
else
  fail "orphan filename missing from output" "$sec"
fi

# ── Case 4: orphan hooks_token_<unknown> ─────────────────────────────────
echo ""
echo "── REF-2003 case 4: orphan hooks_token_<unknown> ──────────────────────"
setup_skill_dir case4
install -m 600 /dev/stdin "$SKILL_DIR/secrets/hooks_token_bruce" <<<"x"

out="$(run_doctor)"
sec="$(extract_hygiene_section "$out")"

if grep -qF "orphan secret file(s) in secrets/: 1" <<<"$sec"; then
  pass "orphan hooks_token produces warn with count 1"
else
  fail "orphan hooks_token was not reported" "$sec"
fi
if grep -qE -- "- hooks_token_bruce" <<<"$sec"; then
  pass "orphan hooks_token filename appears in output"
else
  fail "orphan hooks_token filename missing from output" "$sec"
fi

# ── Case 5: orphan peer_secret_<unknown> ─────────────────────────────────
echo ""
echo "── REF-2003 case 5: orphan peer_secret_<unknown> ──────────────────────"
setup_skill_dir case5
install -m 600 /dev/stdin "$SKILL_DIR/secrets/peer_secret_ghost" <<<"x"

out="$(run_doctor)"
sec="$(extract_hygiene_section "$out")"

if grep -qF "orphan secret file(s) in secrets/: 1" <<<"$sec"; then
  pass "orphan peer_secret_* produces warn with count 1"
else
  fail "orphan peer_secret_* was not reported" "$sec"
fi
if grep -qE -- "- peer_secret_ghost" <<<"$sec"; then
  pass "orphan peer_secret_* filename appears in output"
else
  fail "orphan peer_secret_* filename missing from output" "$sec"
fi

# ── Case 6: backup file ──────────────────────────────────────────────────
echo ""
echo "── REF-2003 case 6: backup file is flagged, not counted as orphan ─────"
setup_skill_dir case6
install -m 600 /dev/stdin "$SKILL_DIR/secrets/hooks_token_alice.bak-20260101-000000" <<<"x"

out="$(run_doctor)"
sec="$(extract_hygiene_section "$out")"

if grep -qF "stale backup file(s) in secrets/: 1" <<<"$sec"; then
  pass "backup file produces 'stale backup' warn with count 1"
else
  fail "backup file was not reported as backup" "$sec"
fi
if grep -qE -- "- hooks_token_alice\.bak-" <<<"$sec"; then
  pass "backup filename appears in output"
else
  fail "backup filename missing from output" "$sec"
fi
# Critically, a backup of a known peer should NOT be counted as an orphan.
if grep -qF "orphan secret file(s) in secrets/" <<<"$sec"; then
  fail "backup of a known peer must not be classified as an orphan" "$sec"
else
  pass "backup was not miscounted as an orphan"
fi

# ── Case 7: loose file perms ─────────────────────────────────────────────
echo ""
echo "── REF-2003 case 7: loose file perms (644) are flagged ────────────────"
setup_skill_dir case7
# Clean, registered peer secret but with perms 644 instead of 600.
install -m 644 /dev/stdin "$SKILL_DIR/secrets/hooks_token_alice" <<<"leaky"

out="$(run_doctor)"
sec="$(extract_hygiene_section "$out")"

if grep -qF "file(s) in secrets/ with loose permissions: 1" <<<"$sec"; then
  pass "644 file produces 'loose permissions' warn"
else
  fail "644 file was not reported as loose" "$sec"
fi
if grep -qE -- "- hooks_token_alice \(644\)" <<<"$sec"; then
  pass "loose-perm filename and mode appear in output"
else
  fail "loose-perm filename/mode missing from output" "$sec"
fi

# ── Case 8: unknown-shape file ───────────────────────────────────────────
echo ""
echo "── REF-2003 case 8: unknown-shape file is flagged ─────────────────────"
setup_skill_dir case8
install -m 600 /dev/stdin "$SKILL_DIR/secrets/notes.txt" <<<"hello"

out="$(run_doctor)"
sec="$(extract_hygiene_section "$out")"

if grep -qF "unrecognized file(s) in secrets/: 1" <<<"$sec"; then
  pass "unknown-shape file produces 'unrecognized' warn"
else
  fail "unknown-shape file was not flagged" "$sec"
fi
if grep -qE -- "- notes\.txt" <<<"$sec"; then
  pass "unknown-shape filename appears in output"
else
  fail "unknown-shape filename missing from output" "$sec"
fi
# It must not be miscounted as an orphan peer secret.
if grep -qF "orphan secret file(s) in secrets/" <<<"$sec"; then
  fail "unknown-shape file must not be classified as an orphan" "$sec"
else
  pass "unknown-shape file was not miscounted as an orphan"
fi

# ── Case 9: missing secrets dir ──────────────────────────────────────────
echo ""
echo "── REF-2003 case 9: missing secrets dir degrades gracefully ───────────"
setup_skill_dir case9
rm -rf "$SKILL_DIR/secrets"

out="$(run_doctor)"
sec="$(extract_hygiene_section "$out")"

if grep -qE "No secrets directory" <<<"$sec"; then
  pass "missing secrets/ dir produces info line, no crash"
else
  fail "missing secrets/ dir did not produce info line" "$sec"
fi
if grep -qE "^  .FAIL" <<<"$sec"; then
  fail "missing secrets/ dir should not produce a FAIL"
else
  pass "missing secrets/ dir did not escalate to FAIL"
fi

# ── Orphan warns are never fails ─────────────────────────────────────────
echo ""
echo "── REF-2003 invariant: orphans/backups are warns, never fails ─────────"
setup_skill_dir invariant
install -m 600 /dev/stdin "$SKILL_DIR/secrets/antenna-peer-nexus.secret" <<<"x"
install -m 600 /dev/stdin "$SKILL_DIR/secrets/hooks_token_alice.bak" <<<"x"

out="$(run_doctor)"
sec="$(extract_hygiene_section "$out")"

# Check for a FAIL line in the 6b section specifically.
if grep -qE "^\s+\S+\s+.FAIL" <<<"$sec" || grep -qE '✗' <<<"$sec"; then
  fail "hygiene issues must not escalate to FAIL in section 6b" "$sec"
else
  pass "hygiene issues stayed at warn severity"
fi

# ── Summary ──────────────────────────────────────────────────────────────
echo ""
echo "── REF-2003 summary ───────────────────────────────────────────────────"
echo "  passed: $PASS"
echo "  failed: $FAIL"
[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
