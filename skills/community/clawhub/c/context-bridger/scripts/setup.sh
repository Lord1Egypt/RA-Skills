#!/bin/bash
# Context Bridge Setup Script
# Creates and populates all required registry files

set -e

echo "=== Context Bridge Setup ==="
echo ""

# Create directories
echo "Creating directories..."
mkdir -p ~/.openclaw/model-agnostic-memory
mkdir -p ~/.openclaw/agents/defaults
mkdir -p ~/.openclaw/workspace/skills
mkdir -p ~/.openclaw/scripts
mkdir -p ~/.openclaw/agents

NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# ============================================================================
# SCAN FOR EXISTING SKILLS
# ============================================================================
echo ""
echo "Scanning for existing skills..."

SKILLS_JSON="{}"
SKILLS_LIST="[]"

# Scan workspace skills
if [ -d ~/.openclaw/workspace/skills ]; then
    for skill_dir in ~/.openclaw/workspace/skills/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            skill_file="${skill_dir}SKILL.md"
            
            # Extract info from SKILL.md if it exists
            if [ -f "$skill_file" ]; then
                # Get first header as name
                skill_display_name=$(grep -m1 "^# " "$skill_file" 2>/dev/null | sed 's/^# //' || echo "$skill_name")
                # Get emoji if present
                skill_emoji=$(grep -o "emoji.*" "$skill_file" 2>/dev/null | head -1 | cut -d'"' -f2 || echo "📦")
                # Get description from first paragraph
                skill_desc=$(grep -m1 "^[^#]" "$skill_file" 2>/dev/null | head -1 | sed 's/^[[:space:]]*//' || echo "No description")
            else
                skill_display_name="$skill_name"
                skill_emoji="📦"
                skill_desc="Local workspace skill"
            fi
            
            # Add to skills JSON
            SKILLS_JSON=$(echo "$SKILLS_JSON" | jq --arg name "$skill_name" --arg display "$skill_display_name" --arg emoji "$skill_emoji" --arg desc "$skill_desc" --arg path "~/.openclaw/workspace/skills/$skill_name" --arg now "$NOW" '
                .[$name] = {
                    "name": $display,
                    "emoji": $emoji,
                    "location": $path,
                    "description": $desc,
                    "installed": $now,
                    "status": "active"
                }
            ')
            
            # Add to discovery list
            SKILLS_LIST=$(echo "$SKILLS_LIST" | jq --arg id "$skill_name" --arg name "$skill_display_name" --arg emoji "$skill_emoji" --arg desc "$skill_desc" '
                . + [{
                    "id": $id,
                    "name": $name,
                    "emoji": $emoji,
                    "status": "active",
                    "setupRequired": false,
                    "description": $desc
                }]
            ')
            
            echo "  ✓ Found: $skill_emoji $skill_name"
        fi
    done
fi

# Scan system skills
if [ -d ~/.openclaw/skills ]; then
    for skill_dir in ~/.openclaw/skills/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            skill_file="${skill_dir}SKILL.md"
            
            # Skip if already in workspace
            if echo "$SKILLS_JSON" | jq -e "has(\"$skill_name\")" >/dev/null 2>&1; then
                continue
            fi
            
            # Extract info from SKILL.md if it exists
            if [ -f "$skill_file" ]; then
                skill_display_name=$(grep -m1 "^# " "$skill_file" 2>/dev/null | sed 's/^# //' || echo "$skill_name")
                skill_emoji=$(grep -o "emoji.*" "$skill_file" 2>/dev/null | head -1 | cut -d'"' -f2 || echo "📦")
                skill_desc=$(grep -m1 "^[^#]" "$skill_file" 2>/dev/null | head -1 | sed 's/^[[:space:]]*//' || echo "System skill")
            else
                skill_display_name="$skill_name"
                skill_emoji="📦"
                skill_desc="System skill"
            fi
            
            SKILLS_JSON=$(echo "$SKILLS_JSON" | jq --arg name "$skill_name" --arg display "$skill_display_name" --arg emoji "$skill_emoji" --arg desc "$skill_desc" --arg path "~/.openclaw/skills/$skill_name" --arg now "$NOW" '
                .[$name] = {
                    "name": $display,
                    "emoji": $emoji,
                    "location": $path,
                    "description": $desc,
                    "installed": $now,
                    "status": "active"
                }
            ')
            
            SKILLS_LIST=$(echo "$SKILLS_LIST" | jq --arg id "$skill_name" --arg name "$skill_display_name" --arg emoji "$skill_emoji" --arg desc "$skill_desc" '
                . + [{
                    "id": $id,
                    "name": $name,
                    "emoji": $emoji,
                    "status": "active",
                    "setupRequired": false,
                    "description": $desc
                }]
            ')
            
            echo "  ✓ Found: $skill_emoji $skill_name (system)"
        fi
    done
fi

SKILL_COUNT=$(echo "$SKILLS_JSON" | jq 'length')
echo "  → Total skills found: $SKILL_COUNT"

# ============================================================================
# SCAN FOR EXISTING CRONS
# ============================================================================
echo ""
echo "Scanning for existing cron jobs..."

CRONS_JSON="{}"
CRON_COUNT=0

if command -v openclaw &>/dev/null; then
    # Get cron list from openclaw if available
    CRON_LIST=$(openclaw cron list --json 2>/dev/null || echo "[]")
    
    if [ "$CRON_LIST" != "[]" ] && [ -n "$CRON_LIST" ]; then
        CRONS_JSON=$(echo "$CRON_LIST" | jq --arg now "$NOW" 'map({(.id // .name): {
            "schedule": .schedule,
            "payload": .payload,
            "enabled": (.enabled // true),
            "created": (.created // $now),
            "lastRun": .lastRun
        }}) | add // {}')
        CRON_COUNT=$(echo "$CRONS_JSON" | jq 'length')
    fi
else
    echo "  ⚠️ openclaw CLI not available, skipping cron scan"
fi

echo "  → Total crons found: $CRON_COUNT"

# ============================================================================
# SCAN FOR EXISTING AGENTS
# ============================================================================
echo ""
echo "Scanning for existing agents..."

AGENTS_JSON="{}"
AGENT_COUNT=0

if command -v openclaw &>/dev/null; then
    AGENT_LIST=$(openclaw agents list --json 2>/dev/null || echo "[]")
    
    if [ "$AGENT_LIST" != "[]" ] && [ -n "$AGENT_LIST" ]; then
        AGENTS_JSON=$(echo "$AGENT_LIST" | jq --arg now "$NOW" 'map({(.id // .agentId): {
            "name": (.name // .id),
            "status": (.status // "active"),
            "workspace": .workspace,
            "created": (.created // $now)
        }}) | add // {}')
        AGENT_COUNT=$(echo "$AGENTS_JSON" | jq 'length')
    fi
else
    echo "  ⚠️ openclaw CLI not available, skipping agent scan"
fi

# Also check for agent directories directly
if [ -d ~/.openclaw/agents ]; then
    for agent_dir in ~/.openclaw/agents/*/; do
        if [ -d "$agent_dir" ]; then
            agent_id=$(basename "$agent_dir")
            if ! echo "$AGENTS_JSON" | jq -e "has(\"$agent_id\")" >/dev/null 2>&1; then
                AGENTS_JSON=$(echo "$AGENTS_JSON" | jq --arg id "$agent_id" --arg now "$NOW" '
                    .[$id] = {
                        "name": $id,
                        "status": "active",
                        "discovered": $now
                    }
                ')
                AGENT_COUNT=$((AGENT_COUNT + 1))
                echo "  ✓ Found agent: $agent_id"
            fi
        fi
    done
fi

echo "  → Total agents found: $AGENT_COUNT"

# ============================================================================
# CREATE/UPDATE REGISTRY FILES
# ============================================================================

# Create skills-registry.json
echo ""
echo "Creating skills-registry.json..."
cat > ~/.openclaw/skills-registry.json << EOF
{
  "version": "1.0",
  "lastUpdated": "$NOW",
  "skills": $SKILLS_JSON,
  "missing": {},
  "rules": {
    "beforeCreatingSkill": [
      "Check this registry - does skill already exist?",
      "If exists: UPDATE existing, don't create duplicate",
      "If not exists: CREATE new, then ADD to this registry",
      "Use canonical naming: {agent}-{purpose}"
    ],
    "namingConvention": "lowercase-with-hyphens",
    "examples": [
      "marketing-ga4-reporter",
      "fleet-reporter",
      "systems-engineer"
    ]
  }
}
EOF
echo "  ✓ Created skills-registry.json ($SKILL_COUNT skills)"

# Create cron-registry.json
echo "Creating cron-registry.json..."
cat > ~/.openclaw/cron-registry.json << EOF
{
  "version": "1.0",
  "lastUpdated": "$NOW",
  "crons": $CRONS_JSON,
  "rules": {
    "beforeCreatingCron": [
      "Check this registry for existing cron with same purpose/name",
      "If exists: UPDATE existing, don't create duplicate",
      "If not exists: CREATE new, then ADD to this registry",
      "Use canonical naming: {agent}-{purpose}"
    ],
    "namingConvention": "{agent-name}-{purpose-or-time}"
  }
}
EOF
echo "  ✓ Created cron-registry.json ($CRON_COUNT crons)"

# Create skills-discovery.json
echo "Creating skills-discovery.json..."
cat > ~/.openclaw/skills-discovery.json << EOF
{
  "version": "1.0",
  "lastUpdated": "$NOW",
  "discoveryMethod": "Auto-discovered on Context Bridge setup",
  "skills": $SKILLS_LIST,
  "usageInstructions": {
    "forModels": "On session start, read this file and acknowledge available skills",
    "forUsers": "Say 'what skills do we have' to see current capabilities",
    "forSetup": "Skills marked 'setupRequired: true' need configuration before use"
  }
}
EOF
echo "  ✓ Created skills-discovery.json ($SKILL_COUNT skills)"

# Create model-handoff.md if missing
echo "Creating model-handoff.md..."
if [ ! -f ~/.openclaw/model-agnostic-memory/model-handoff.md ]; then
cat > ~/.openclaw/model-agnostic-memory/model-handoff.md << 'EOF'
# Model Handoff Log

**Purpose:** Track context between model sessions to prevent "starting from zero"

---

## Latest Session

**Model:** (current model)  
**Started:** (timestamp)  
**Previous Model:** (previous model)

**Context:**
- (Add context here)

**Active Projects:**
- (Add projects here)

**Recent Actions:**
- (Add actions here)

---

## How to Update

After each session, append:
```
### TIMESTAMP - MODEL_NAME
**Actions:**
- What was done

**Context for next model:**
- What they should know
```

EOF
echo "  ✓ Created model-handoff.md"
else
    echo "  ✓ model-handoff.md already exists"
fi

# Create session-start-hook.md if missing
echo "Creating session-start-hook.md..."
if [ ! -f ~/.openclaw/agents/defaults/session-start-hook.md ]; then
cat > ~/.openclaw/agents/defaults/session-start-hook.md << 'EOF'
# Session Start Hook

**Purpose:** Auto-load shared context on every session start

---

## Auto-Load Sequence

On EVERY session start (`/new`, model switch, restart):

1. READ: ~/.openclaw/skills-discovery.json
2. READ: ~/.openclaw/model-agnostic-memory/model-handoff.md
3. READ: ~/.openclaw/cron-registry.json
4. READ: ~/.openclaw/skills-registry.json
5. CHECK: Recent memory files

## Output Format

If loaded successfully:
```
[Context Loaded]
📧 Skills available: (list)
🔁 Crons active: (count)
📋 Projects: (active)

Ready.
```

If auto-load FAILS:
```
[Session Started]
⚠️ Auto-context load failed
📋 Manual load: Say "load context"

Ready.
```
EOF
echo "  ✓ Created session-start-hook.md"
else
    echo "  ✓ session-start-hook.md already exists"
fi

# Create load-context.sh if missing
echo "Creating load-context.sh..."
if [ ! -f ~/.openclaw/scripts/load-context.sh ]; then
cat > ~/.openclaw/scripts/load-context.sh << 'EOF'
#!/bin/bash
# load-context.sh - Manual context loader

echo "=== Loading Session Context ==="
echo ""

echo "1. Skills Discovery..."
cat ~/.openclaw/skills-discovery.json 2>/dev/null | jq '.skills[].id' 2>/dev/null || echo "  (discovery file empty)"

echo ""
echo "2. Model Handoff..."
cat ~/.openclaw/model-agnostic-memory/model-handoff.md 2>/dev/null | head -30 || echo "  (handoff file empty)"

echo ""
echo "3. Active Crons..."
cat ~/.openclaw/cron-registry.json 2>/dev/null | jq '.crons | keys' 2>/dev/null || echo "  (cron registry empty)"

echo ""
echo "4. Installed Skills..."
cat ~/.openclaw/skills-registry.json 2>/dev/null | jq '.skills | keys' 2>/dev/null || echo "  (skills registry empty)"

echo ""
echo "=== Context Loaded ==="
EOF
chmod +x ~/.openclaw/scripts/load-context.sh
echo "  ✓ Created load-context.sh"
else
    echo "  ✓ load-context.sh already exists"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "📊 Summary:"
echo "  • Skills registered: $SKILL_COUNT"
echo "  • Crons registered: $CRON_COUNT"
echo "  • Agents discovered: $AGENT_COUNT"
echo ""
echo "Registry files auto-populated with existing data!"
echo ""
echo "Next steps:"
echo "1. Update AGENTS.md to require Context Bridge files on startup"
echo "2. Test manual load: ~/.openclaw/scripts/load-context.sh"
echo ""
