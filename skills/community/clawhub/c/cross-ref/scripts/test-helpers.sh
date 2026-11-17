#!/usr/bin/env bash
# Smoke tests for approval gates and input validation. Makes no GitHub requests.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

pass() { echo "  ✓ $1"; }
fail() { echo "  ✗ $1" >&2; exit 1; }

bash -n "$SCRIPT_DIR/post-comments.sh" && pass "post-comments.sh syntax"
bash -n "$SCRIPT_DIR/fetch-data.sh" && pass "fetch-data.sh syntax"

if "$SCRIPT_DIR/post-comments.sh" ../etc/passwd "$TMP_DIR" >/dev/null 2>&1; then
  fail "reject path traversal repo"
else
  pass "reject path traversal repo"
fi

printf '%s\n' '[]' > "$TMP_DIR/approved-comments.json"
if "$SCRIPT_DIR/post-comments.sh" owner/repo "$TMP_DIR" >/dev/null 2>&1; then
  fail "reject legacy array queue"
else
  pass "reject legacy array queue"
fi

printf '%s\n' '{"approved":false,"approved_at":"2026-01-01T00:00:00Z","comments":[]}' > "$TMP_DIR/approved-comments.json"
if "$SCRIPT_DIR/post-comments.sh" owner/repo "$TMP_DIR" >/dev/null 2>&1; then
  fail "reject unapproved queue"
else
  pass "reject unapproved queue"
fi

printf '%s\n' '{"approved":true,"approved_at":"2026-01-01T00:00:00Z","comments":[{"target_number":123,"type":"issue_link","body":"reviewed"}]}' > "$TMP_DIR/approved-comments.json"
OUTPUT=$("$SCRIPT_DIR/post-comments.sh" owner/repo "$TMP_DIR")
if [[ "$OUTPUT" == *"Mode: dry-run (no GitHub writes)"* ]] && [[ "$OUTPUT" == *"#123"* ]]; then
  pass "approved queue defaults to dry-run"
else
  fail "approved queue defaults to dry-run"
fi

echo "All smoke tests passed."
