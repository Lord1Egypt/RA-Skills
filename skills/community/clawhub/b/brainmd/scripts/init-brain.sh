#!/bin/bash
# Initialize a blank BRAIN.md structure
# Usage: ./init-brain.sh [path]

BRAIN_DIR="${1:-./brain}"

echo "🧠 Initializing BRAIN.md at: $BRAIN_DIR"

mkdir -p "$BRAIN_DIR"/{reflexes,habits,skills,weights,cortex,mutations}

# Create blank pathways file
cat > "$BRAIN_DIR/weights/pathways.json" << 'EOF'
{
  "version": 1,
  "created": "",
  "description": "Pathway strength tracker. Higher weight = more reinforced behavior.",
  "pathways": {}
}
EOF

# Stamp creation time
sed -i "s/\"created\": \"\"/\"created\": \"$(date -Iseconds)\"/" "$BRAIN_DIR/weights/pathways.json"

# Create blank preferences
cat > "$BRAIN_DIR/habits/preferences.json" << 'EOF'
{
  "version": 1,
  "description": "Learned preferences. Evolves with each interaction.",
  "communication": {},
  "lifestyle": {},
  "technical": {}
}
EOF

# Copy cortex engine
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
if [ -f "$SCRIPT_DIR/scripts/cortex-review.js" ]; then
  cp "$SCRIPT_DIR/scripts/cortex-review.js" "$BRAIN_DIR/cortex/review.js"
  chmod +x "$BRAIN_DIR/cortex/review.js"
fi

# Copy reflex templates
if [ -f "$SCRIPT_DIR/scripts/reflex-timing.js" ]; then
  cp "$SCRIPT_DIR/scripts/reflex-timing.js" "$BRAIN_DIR/reflexes/timing.js"
  chmod +x "$BRAIN_DIR/reflexes/timing.js"
fi

# Create README
cat > "$BRAIN_DIR/README.md" << 'EOF'
# BRAIN.md

*Self-modifying file system mimicking neuroplasticity.*

See SKILL.md for full documentation.

## Quick Commands

```bash
# Record an outcome
node cortex/review.js record "reflex:my-pattern" true "What happened"

# Run self-review
node cortex/review.js review

# Check status
node cortex/review.js status
```

## Getting Started

1. Observe your agent's behavior for a session
2. Identify patterns that worked or failed
3. Record them as pathways
4. Wire cortex review into your heartbeat/cron
5. Let it evolve
EOF

echo "✅ BRAIN.md initialized"
echo ""
echo "Next steps:"
echo "  1. Seed pathways: node $BRAIN_DIR/cortex/review.js record 'reflex:my-pattern' true 'Description'"
echo "  2. Run review:    node $BRAIN_DIR/cortex/review.js review"
echo "  3. Check status:  node $BRAIN_DIR/cortex/review.js status"
