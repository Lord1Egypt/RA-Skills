#!/bin/bash
# Agora Sentinel — Scan all installed OpenClaw skills
# Finds skills in ./skills/ directory and checks each against Sentinel

API="https://checksafe.dev/api/v1"
SKILLS_DIR="${OPENCLAW_SKILLS_DIR:-./skills}"

if [ ! -d "$SKILLS_DIR" ]; then
    # Try common locations
    for DIR in "./skills" "$HOME/.openclaw/skills" "$HOME/openclaw/skills"; do
        if [ -d "$DIR" ]; then
            SKILLS_DIR="$DIR"
            break
        fi
    done
fi

if [ ! -d "$SKILLS_DIR" ]; then
    echo "Could not find skills directory. Set OPENCLAW_SKILLS_DIR or run from workspace root."
    exit 1
fi

echo "Agora Sentinel — Installed Skills Audit"
echo "============================================"
echo "Scanning: ${SKILLS_DIR}"
echo ""

SLUGS=""
for SKILL_DIR in "$SKILLS_DIR"/*/; do
    if [ -f "${SKILL_DIR}SKILL.md" ]; then
        SLUG=$(basename "$SKILL_DIR")
        SLUGS="${SLUGS} ${SLUG}"
    fi
done

if [ -z "$SLUGS" ]; then
    echo "No skills found in ${SKILLS_DIR}"
    exit 0
fi

# Use batch check
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
bash "${SCRIPT_DIR}/check_batch.sh" $SLUGS
