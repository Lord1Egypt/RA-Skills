#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

required_files=(
  "SKILL.md"
  "README.md"
  "run_amath_cli.sh"
  "run_openclaw.sh"
  "requirements.txt"
  "CLAWHUB_PUBLISH_CHECKLIST.md"
  "COMMUNITY_POSTS.md"
)

missing=0
for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing required file: $file" >&2
    missing=1
  fi
done

if grep -RInE 'AMATH_ACCESS_TOKEN=.+|ghp_|github_pat_|BEGIN (RSA|OPENSSH) PRIVATE KEY|PRIVATE KEY-----' . >/dev/null 2>&1; then
  :
fi

if find . -maxdepth 2 -type f \( -name '.env' -o -name '*.env' \) -print0 | xargs -0 grep -nE '^[[:space:]]*AMATH_ACCESS_TOKEN=[^[:space:]#]+' >/dev/null 2>&1; then
  echo "Detected a populated AMATH_ACCESS_TOKEN in an env file. Remove it before publishing." >&2
  exit 1
fi

if grep -RInE --exclude='preflight_check.sh' 'ghp_|github_pat_|BEGIN (RSA|OPENSSH) PRIVATE KEY|PRIVATE KEY-----' . >/dev/null 2>&1; then
  echo "Potential secret material detected. Review before publishing." >&2
  exit 1
fi

if grep -RInE --exclude='preflight_check.sh' '/mnt/disk1|master-MS-|ThinkAI' . >/dev/null 2>&1; then
  echo "Machine-specific path or host marker detected. Review before publishing." >&2
  exit 1
fi

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

cat <<EOF
Preflight OK.
Suggested next steps:
1. clawhub login
2. ./publish_clawhub.sh
EOF
