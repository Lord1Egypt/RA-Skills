#!/usr/bin/env bash
# setup-evolution.sh — Initialize self-evolution file structure
# Usage: bash setup-evolution.sh [workspace_dir]
# Default workspace: current directory

set -euo pipefail

WORKSPACE="${1:-.}"
MEMORY_DIR="$WORKSPACE/memory"

echo "🧬 Setting up self-evolution system in: $WORKSPACE"

# Create memory directory
mkdir -p "$MEMORY_DIR"

# --- evolution-log.md ---
if [ ! -f "$MEMORY_DIR/evolution-log.md" ]; then
  cat > "$MEMORY_DIR/evolution-log.md" << 'EOF'
# Evolution Log 🧬

Chronicle of every evolution event.

## Format
```
### [YYYY-MM-DD HH:MM] Evolution Type
- **Trigger**: What triggered this evolution
- **Changes**: What was improved
- **Expected effect**: What improvement is expected
```

---

### [$(date +%Y-%m-%d)] System Initialized
- **Trigger**: Self-evolution system setup
- **Changes**: Created evolution file structure
- **Expected effect**: Enable continuous learning and improvement

EOF
  # Fix the date placeholder
  sed -i "s/\$(date +%Y-%m-%d)/$(date +%Y-%m-%d)/" "$MEMORY_DIR/evolution-log.md"
  echo "  ✅ Created evolution-log.md"
else
  echo "  ⏭️  evolution-log.md already exists, skipping"
fi

# --- evolution-metrics.json ---
if [ ! -f "$MEMORY_DIR/evolution-metrics.json" ]; then
  cat > "$MEMORY_DIR/evolution-metrics.json" << EOF
{
  "initialized": "$(date +%Y-%m-%d)",
  "total_evolutions": 0,
  "daily_evolutions": 0,
  "weekly_evolutions": 0,
  "skills_improved": 0,
  "code_fixes_applied": 0,
  "skills_created": 0,
  "mistakes_recorded": 0,
  "mistakes_resolved": 0,
  "knowledge_entries_added": 0,
  "memory_updates": 0,
  "soul_updates": 0,
  "last_daily_evolution": null,
  "last_weekly_evolution": null,
  "history": [
    {
      "date": "$(date +%Y-%m-%d)",
      "type": "system_init",
      "desc": "Self-evolution system initialized"
    }
  ]
}
EOF
  echo "  ✅ Created evolution-metrics.json"
else
  echo "  ⏭️  evolution-metrics.json already exists, skipping"
fi

# --- mistakes-learned.md ---
if [ ! -f "$MEMORY_DIR/mistakes-learned.md" ]; then
  cat > "$MEMORY_DIR/mistakes-learned.md" << 'EOF'
# Mistakes & Lessons 🎓

Record every mistake to avoid repeating it.

## Format
```
### Category
- **Short description**: Root cause → Fix/Prevention
```

## Lessons

<!-- Add your first lesson after making your first mistake! -->

---
EOF
  echo "  ✅ Created mistakes-learned.md"
else
  echo "  ⏭️  mistakes-learned.md already exists, skipping"
fi

# --- skill-improvements.md ---
if [ ! -f "$MEMORY_DIR/skill-improvements.md" ]; then
  cat > "$MEMORY_DIR/skill-improvements.md" << 'EOF'
# Skill & Code Improvements 🔧

Queue improvements here. Daily evolution cron will execute them.

## Queued

<!-- Format:
- [ ] target: <file/skill> | issue: <description> | fix: <proposed solution>
-->

## Completed

<!-- Completed items move here with date:
- [x] target: <file/skill> | issue: <what> | fix: <done> ✅ (YYYY-MM-DD)
-->

---
EOF
  echo "  ✅ Created skill-improvements.md"
else
  echo "  ⏭️  skill-improvements.md already exists, skipping"
fi

echo ""
echo "🎉 Self-evolution system ready!"
echo ""
echo "Next steps:"
echo "  1. Set up daily cron job (e.g. every night at 23:00)"
echo "  2. Set up weekly cron job (e.g. Sunday at 10:00)"
echo "  3. Add real-time capture hooks to AGENTS.md"
echo "  4. See SKILL.md for full instructions"
