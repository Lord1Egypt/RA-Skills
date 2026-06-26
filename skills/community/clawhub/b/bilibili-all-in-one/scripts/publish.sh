#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Release helper for the `bilibili-all-in-one` skill.
#
# What it does:
#   1. Reads the current `version` field from skill.json.
#   2. Computes the next version based on the first CLI arg:
#        - "patch"           -> x.y.(z+1)   (default)
#        - "minor"           -> x.(y+1).0
#        - "major"           -> (x+1).0.0
#        - explicit "1.2.3"  -> use that exact version
#   3. Writes the new version back into skill.json (keeps formatting minimal).
#   4. Runs:  clawhub publish <project_root> --version <new_version>
#
# This script itself is excluded from the published package via .clawignore,
# so it will NOT be shipped to end users of the skill.
#
# Usage:
#   ./scripts/publish.sh                 # bumps patch version and publishes
#   ./scripts/publish.sh patch
#   ./scripts/publish.sh minor
#   ./scripts/publish.sh major
#   ./scripts/publish.sh 1.0.22          # publish exactly 1.0.22
# ---------------------------------------------------------------------------
set -euo pipefail

# Resolve absolute project root (parent of this script's directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_JSON="${PROJECT_ROOT}/skill.json"

if [[ ! -f "${SKILL_JSON}" ]]; then
    echo "ERROR: skill.json not found at ${SKILL_JSON}" >&2
    exit 1
fi

# --- 1. Read current version -------------------------------------------------
CURRENT_VERSION="$(python3 -c '
import json, sys
with open(sys.argv[1], "r", encoding="utf-8") as f:
    print(json.load(f)["version"])
' "${SKILL_JSON}")"

echo "Current version: ${CURRENT_VERSION}"

# --- 2. Compute next version -------------------------------------------------
BUMP="${1:-patch}"

SEMVER_RE='^[0-9]+\.[0-9]+\.[0-9]+$'
if [[ "${BUMP}" =~ ${SEMVER_RE} ]]; then
    NEW_VERSION="${BUMP}"
else
    IFS='.' read -r MAJOR MINOR PATCH <<< "${CURRENT_VERSION}"
    case "${BUMP}" in
        major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
        minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
        patch|"") PATCH=$((PATCH + 1)) ;;
        *)
            echo "ERROR: unknown bump level or version: '${BUMP}'" >&2
            echo "       expected one of: patch | minor | major | X.Y.Z" >&2
            exit 1
            ;;
    esac
    NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
fi

echo "New version:     ${NEW_VERSION}"

# --- 3. Write version back to skill.json -------------------------------------
# Preserve the file's original formatting as much as possible by only
# rewriting the single `version` field in-place with sed. We anchor the regex
# loosely so it works whether the line starts with a tab or spaces.
python3 - "${SKILL_JSON}" "${NEW_VERSION}" <<'PY'
import json, sys, io, re

path, new_version = sys.argv[1], sys.argv[2]
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

new_text, n = re.subn(
    r'("version"\s*:\s*")[^"]+(")',
    lambda m: f'{m.group(1)}{new_version}{m.group(2)}',
    text,
    count=1,
)
if n != 1:
    print(f"ERROR: failed to locate version field in {path}", file=sys.stderr)
    sys.exit(2)

with open(path, "w", encoding="utf-8") as f:
    f.write(new_text)
PY

echo "Updated ${SKILL_JSON} -> version ${NEW_VERSION}"

# --- 4. Publish via clawhub --------------------------------------------------
if ! command -v clawhub >/dev/null 2>&1; then
    echo "ERROR: 'clawhub' CLI not found on PATH." >&2
    echo "       Install it first, then re-run this script." >&2
    exit 1
fi

echo "Running: clawhub publish ${PROJECT_ROOT} --version ${NEW_VERSION}"
clawhub publish "${PROJECT_ROOT}" --version "${NEW_VERSION}"

echo "Done. Published bilibili-all-in-one@${NEW_VERSION}"
