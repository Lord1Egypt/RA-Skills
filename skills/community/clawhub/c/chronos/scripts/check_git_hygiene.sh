#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"

if git ls-files | grep -E '(^|/)(__pycache__/|.*\.pyc$)' >/dev/null; then
  echo "Tracked Python cache artifacts found. Remove them from git index before committing."
  git ls-files | grep -E '(^|/)(__pycache__/|.*\.pyc$)'
  exit 1
fi

echo "Git hygiene OK"
