#!/bin/bash
# init_debate.sh — one-click arena creation
# Usage: bash init_debate.sh <topic-slug>
# Example: bash init_debate.sh medlibya

set -e

TOPIC=${1:-}
if [ -z "$TOPIC" ]; then
  echo "Usage: bash init_debate.sh <topic-slug>"
  echo "  Example: bash init_debate.sh medlibya"
  exit 1
fi

# Sanitize: lowercase letters, digits, and hyphens only; max 32 chars; no leading/trailing hyphens; no consecutive hyphens
TOPIC=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9-')
TOPIC=$(echo "$TOPIC" | sed 's/^-*//;s/-*$//;s/--*/-/g')
if [ -z "$TOPIC" ] || [ "${#TOPIC}" -gt 32 ]; then
  echo "Error: invalid topic slug. Use 1-32 lowercase English letters, digits, and hyphens. No leading/trailing/consecutive hyphens."
  exit 1
fi

DATE=$(date +%Y%m%d)
ROOT="$HOME/.hermes/debates"
BASE="$ROOT/conclave-$DATE-$TOPIC"

# Handle name collision
if [ -d "$BASE" ]; then
  N=2
  while [ -d "$BASE-$N" ]; do
    N=$((N+1))
  done
  BASE="$BASE-$N"
fi

mkdir -p "$BASE"
cd "$BASE"

# Create directory structure
mkdir -p 00_preflight 01_brief 02_r1 03_r2 04_r3 05_r4 06_r5 07_verdicts 08_signoff 09_deliver

# Create starter files
NOW=$(date '+%Y-%m-%d %H:%M:%S')
cat > index.md << EOF
# Debate Index: conclave-$DATE-$TOPIC

- Created: $NOW
- Topic slug: $TOPIC
- Full path: $BASE

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| 00_preflight/ | Pre-flight pings |
| 01_brief/ | Brief + anonymity mapping + user constraints |
| 02_r1/ | R1 positioning |
| 03_r2/ | R2 rebuttals |
| 04_r3~06_r5/ | Convergence rounds (created on demand) |
| 07_verdicts/ | Chair synthesis per round |
| 08_signoff/ | Sign-off draft + individual votes |
| 09_deliver/ | Final report + meeting minutes |

## Timeline

| Time | Event | File |
|------|-------|------|
| $NOW | Arena created | This index |

## Key Decisions Quick-Reference

(To be filled after the debate concludes)
EOF

cat > 01_brief/brief.md << 'EOF'
# Brief

(To be filled: topic, background, constraints, and the decision(s) to be made)
EOF

cat > 01_brief/mapping.md << 'EOF'
# Anonymity Mapping

| Code | Real Identity | Notes |
|------|---------------|-------|
| A | (to be filled) | |
| B | (to be filled) | |
| C | (to be filled) | |
| D | (to be filled) | |
| E | Hermes | Chair & panelist |
EOF

cat > 01_brief/constraints.md << 'EOF'
# Clarification Constraints

(To be filled: user answers / rulings from the clarification phase, each annotated with how it shapes the outcome)
EOF

echo "✓ Arena created: $BASE"
echo "  Directory structure:"
find "$BASE" -maxdepth 1 -type d | sort | sed "s|$BASE/|    |"
echo ""
echo "  Next steps:"
echo "    1. Fill 01_brief/brief.md"
echo "    2. Fill 01_brief/mapping.md"
echo "    3. Run bash ~/.hermes/skills/conclave/scripts/preflight.sh $BASE"
echo "       (on a new machine or after CLI failures, first run scripts/install.sh)"
