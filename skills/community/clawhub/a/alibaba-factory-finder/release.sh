#!/bin/bash
set -e

SKILL_NAME="alibaba-factory-finder"
VERSION="1.0.0"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Publishing $SKILL_NAME..."

cd "$SKILL_DIR"

# Repackage
rm -f $SKILL_NAME.skill 2>/dev/null || true
python3 scripts/package_skill.py .
mv .skill $SKILL_NAME.skill

# Publish
clawdhub publish . --version $VERSION --tags latest --changelog "Initial release"

echo "✓ Published to ClawHub!"
echo "📦 https://clawhub.ai/skills/$SKILL_NAME"
