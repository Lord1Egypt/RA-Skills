#!/usr/bin/env sh
set -eu

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

TARGETS="SKILL.md scripts references assets tests requirements.txt requirements-dev.txt"
PATTERN='(AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]{10,}|sk-[A-Za-z0-9]{20,}|-----BEGIN (RSA|EC|OPENSSH|DSA|PGP) PRIVATE KEY-----|/home/[A-Za-z0-9._-]+/\.openclaw|/home/[A-Za-z0-9._-]+/Documents/Vault)'

if grep -RInE "$PATTERN" $TARGETS >/tmp/book_capture_security_scan.txt 2>/dev/null; then
  echo "Security scan failed. Potential sensitive strings found:"
  cat /tmp/book_capture_security_scan.txt
  exit 1
fi

echo "Security scan passed"
