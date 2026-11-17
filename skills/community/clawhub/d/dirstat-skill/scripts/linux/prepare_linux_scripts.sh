#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

for script in \
  "$REPO_ROOT/scripts/linux/verify_ncdu.sh" \
  "$REPO_ROOT/scripts/linux/install_ncdu.sh" \
  "$REPO_ROOT/scripts/linux/run_audit.sh" \
  "$REPO_ROOT/scripts/linux/show_latest_audit.sh" \
  "$REPO_ROOT/scripts/linux/find_safe_candidates.sh" \
  "$REPO_ROOT/scripts/linux/prepare_linux_scripts.sh"
do
  sed -i 's/\r$//' "$script"
  chmod +x "$script"
done

echo "prepared_linux_scripts=yes"
