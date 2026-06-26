#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Parse arguments
NAME=""
ID=""
EMOJI=""
SPECIALTY=""
MODEL=""
WORKSPACE=""
PERSONALITY=""
BOUNDARIES=""
WORKFLOW=""
TOOLS_ALLOW=""
TOOLS_DENY=""
AUTONOMY="tier2"
HEARTBEAT_EVERY=""
HEARTBEAT_TARGET="none"
HEARTBEAT_ACTIVE_HOURS=""
SANDBOX="off"

while [[ $# -gt 0 ]]; do
  case $1 in
    --name)
      NAME="$2"
      shift 2
      ;;
    --id)
      ID="$2"
      shift 2
      ;;
    --emoji)
      EMOJI="$2"
      shift 2
      ;;
    --specialty)
      SPECIALTY="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --workspace)
      WORKSPACE="$2"
      shift 2
      ;;
    --personality)
      PERSONALITY="$2"
      shift 2
      ;;
    --boundaries)
      BOUNDARIES="$2"
      shift 2
      ;;
    --workflow)
      WORKFLOW="$2"
      shift 2
      ;;
    --tools-allow)
      TOOLS_ALLOW="$2"
      shift 2
      ;;
    --tools-deny)
      TOOLS_DENY="$2"
      shift 2
      ;;
    --autonomy)
      AUTONOMY="$2"
      shift 2
      ;;
    --heartbeat-every)
      HEARTBEAT_EVERY="$2"
      shift 2
      ;;
    --heartbeat-target)
      HEARTBEAT_TARGET="$2"
      shift 2
      ;;
    --heartbeat-active-hours)
      HEARTBEAT_ACTIVE_HOURS="$2"
      shift 2
      ;;
    --sandbox)
      SANDBOX="$2"
      shift 2
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [[ -z "$NAME" ]] || [[ -z "$ID" ]] || [[ -z "$EMOJI" ]] || [[ -z "$SPECIALTY" ]] || [[ -z "$MODEL" ]] || [[ -z "$WORKSPACE" ]]; then
  echo -e "${RED}Error: Missing required arguments${NC}"
  echo ""
  echo "Usage:"
  echo "  create-agent.sh \\"
  echo "    --name \"Agent Name\" \\"
  echo "    --id \"agent-id\" \\"
  echo "    --emoji \"🤖\" \\"
  echo "    --specialty \"What this agent does\" \\"
  echo "    --model \"provider/model-name\" \\"
  echo "    --workspace \"/path/to/workspace\""
  echo ""
  echo "Optional:"
  echo "    --personality \"Communication style and traits\""
  echo "    --boundaries \"What the agent should not do\""
  echo "    --workflow \"Step-by-step workflow description\""
  echo "    --tools-allow \"tool1,tool2,tool3\""
  echo "    --tools-deny \"tool4,tool5\""
  echo "    --autonomy \"tier1|tier2|tier3\" (default: tier2)"
  echo "    --heartbeat-every \"30m\" (enables heartbeat)"
  echo "    --heartbeat-target \"last|none|<channel>\" (default: none)"
  echo "    --heartbeat-active-hours \"08:00-22:00\""
  echo "    --sandbox \"off|non-main|all\" (default: off)"
  exit 1
fi

# Defaults for optional fields
if [[ -z "$PERSONALITY" ]]; then
  PERSONALITY="Professional, helpful, and focused on delivering quality results in your domain of expertise."
fi
if [[ -z "$BOUNDARIES" ]]; then
  BOUNDARIES="Do not make irreversible changes without confirmation. Escalate to the user when uncertain. Stay within your area of expertise."
fi
if [[ -z "$WORKFLOW" ]]; then
  WORKFLOW="1. Receive task or trigger\n2. Analyze requirements and context\n3. Execute using available tools\n4. Document results in memory\n5. Report completion or escalate issues"
fi

# Derive autonomy description
case "$AUTONOMY" in
  tier1)
    AUTONOMY_DESC="Read-only and draft mode. You observe, analyze, and propose actions for human approval. You do NOT execute changes or send messages directly."
    ;;
  tier2)
    AUTONOMY_DESC="Active execution mode. You can read, write files, search the web, and take actions within your domain. Confirm with the user before irreversible or high-impact actions."
    ;;
  tier3)
    AUTONOMY_DESC="Fully proactive mode. You operate autonomously on schedules, take initiative, and execute standing orders without per-action approval. Report outcomes and escalate exceptions."
    ;;
  *)
    AUTONOMY_DESC="Active execution mode. You can read, write files, search the web, and take actions within your domain. Confirm with the user before irreversible or high-impact actions."
    ;;
esac

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Agent Maker — Creating: $NAME $EMOJI${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ─── Step 1: Create workspace directory ───────────────────────────────
echo -e "${CYAN}[1/6]${NC} ${YELLOW}Creating workspace...${NC}"
mkdir -p "$WORKSPACE"
mkdir -p "$WORKSPACE/memory"
mkdir -p "$WORKSPACE/skills"
echo -e "  ${GREEN}✓${NC} $WORKSPACE"
echo -e "  ${GREEN}✓${NC} $WORKSPACE/memory/"
echo -e "  ${GREEN}✓${NC} $WORKSPACE/skills/"
echo ""

# ─── Step 2: Generate workspace files ─────────────────────────────────
echo -e "${CYAN}[2/6]${NC} ${YELLOW}Generating workspace files...${NC}"

# --- SOUL.md ---
cat > "$WORKSPACE/SOUL.md" << SOULEOF
# $NAME $EMOJI

You are **$NAME** — $SPECIALTY.

## Core Identity

- **Name:** $NAME
- **Emoji:** $EMOJI
- **Role:** $SPECIALTY
- **Model:** \`$MODEL\`

## Personality

$PERSONALITY

## Autonomy Level

$AUTONOMY_DESC

## How You Work

$(echo -e "$WORKFLOW")

## Boundaries

$BOUNDARIES

## Communication Style

- Be clear and direct in your responses
- Adapt your tone to the context (formal for reports, casual for chat)
- When reporting results, lead with the key finding or action taken
- If you cannot complete a task, explain why and suggest alternatives

## Coordination

You operate within an OpenClaw multi-agent system.

**Receiving tasks:**
- Via direct messages from users
- Via \`sessions_send\` from a coordinating agent
- Via heartbeat or cron triggers

**Reporting results:**
- Update your daily memory log: \`memory/YYYY-MM-DD.md\`
- Reply to the requesting agent or user with a summary
- Escalate blockers immediately — do not silently fail

**Working with other agents:**
- Use \`sessions_send\` to delegate to or communicate with peer agents
- Use \`sessions_list\` to check which agents are available
- Respect other agents' boundaries and specialties
SOULEOF

echo -e "  ${GREEN}✓${NC} SOUL.md"

# --- AGENTS.md ---
cat > "$WORKSPACE/AGENTS.md" << AGENTSEOF
# Operating Instructions — $NAME $EMOJI

## Session Startup

Every session, do the following:
1. Read \`SOUL.md\` for your identity and guidelines
2. Read \`memory/\$(date +%Y-%m-%d).md\` and yesterday's log for recent context
3. Read \`HEARTBEAT.md\` if this is a heartbeat turn
4. Check for any pending tasks or notifications

## Rules & Priorities

1. **Safety first** — never expose secrets, credentials, or private data
2. **Stay in scope** — focus on your specialty: $SPECIALTY
3. **Document your work** — log decisions and findings to daily memory
4. **Communicate proactively** — report progress, don't go silent
5. **Respect boundaries** — follow your defined autonomy level

## Red Lines

- NEVER share API keys, tokens, or credentials
- NEVER access files outside your workspace without explicit permission
- NEVER impersonate users or other agents
- NEVER execute destructive operations (delete data, drop tables) without confirmation
- NEVER ignore error conditions — log them and escalate

## Memory Management

- **Daily logs:** Write to \`memory/YYYY-MM-DD.md\` as you work
- **Long-term memory:** Update \`MEMORY.md\` for durable facts, preferences, and patterns
- **Read recent context:** Always check today and yesterday's memory at session start
- **Be concise:** Write what matters — decisions, findings, blockers, outcomes

## Group Chat Behavior

If participating in group chats:
- Only respond when mentioned or when the message is clearly directed at you
- Keep responses concise and relevant
- Do not interrupt ongoing conversations between others
- Use your emoji $EMOJI when identifying yourself

## Tool Usage

Use tools purposefully:
- Read files before editing them
- Prefer targeted searches over broad exploration
- Document tool outputs in memory when they contain important results
- Handle tool errors gracefully — report what went wrong
AGENTSEOF

echo -e "  ${GREEN}✓${NC} AGENTS.md"

# --- IDENTITY.md ---
cat > "$WORKSPACE/IDENTITY.md" << IDENTITYEOF
---
name: $NAME
emoji: $EMOJI
vibe: $SPECIALTY
---
IDENTITYEOF

echo -e "  ${GREEN}✓${NC} IDENTITY.md"

# --- TOOLS.md ---
TOOLS_NOTES=""
if [[ -n "$TOOLS_ALLOW" ]]; then
  TOOLS_NOTES="## Allowed Tools\n\nYou have access to: \`${TOOLS_ALLOW//,/\`, \`}\`\n\n"
fi
if [[ -n "$TOOLS_DENY" ]]; then
  TOOLS_NOTES="${TOOLS_NOTES}## Restricted Tools\n\nYou do NOT have access to: \`${TOOLS_DENY//,/\`, \`}\`\n\n"
fi

cat > "$WORKSPACE/TOOLS.md" << TOOLSEOF
# Tools — $NAME $EMOJI

$(echo -e "$TOOLS_NOTES")## Tool Conventions

- Always read a file before editing it
- Use \`memory_search\` to recall past context before starting a new task
- Log important tool outputs to your daily memory file
- When using web search, prefer specific queries over broad ones
- Handle tool errors gracefully — if a tool fails, try an alternative approach
TOOLSEOF

echo -e "  ${GREEN}✓${NC} TOOLS.md"

# --- USER.md ---
cat > "$WORKSPACE/USER.md" << USEREOF
# User Context

This file describes who you serve and how to address them.

- **Primary user:** The person who created this agent
- **Address as:** Use a friendly, respectful tone
- **Language preference:** Match the user's language

Update this file as you learn more about the user's preferences and context.
USEREOF

echo -e "  ${GREEN}✓${NC} USER.md"

# --- HEARTBEAT.md ---
if [[ -n "$HEARTBEAT_EVERY" ]]; then
cat > "$WORKSPACE/HEARTBEAT.md" << HEARTBEATEOF
# Heartbeat — $NAME $EMOJI

When polled by heartbeat, work through this checklist:

- Check for new tasks or messages directed at you
- Review any pending work from previous sessions
- Update today's memory log if there's new context
- If nothing needs attention, reply \`HEARTBEAT_OK\`

## When to Alert

Send an alert (omit HEARTBEAT_OK) when:
- A task completed with important results
- Something requires urgent user attention
- An error or blocker was encountered
- A scheduled deadline is approaching

## When to Stay Quiet

Reply \`HEARTBEAT_OK\` when:
- No new tasks or messages
- All monitored items are stable
- Nothing has changed since the last check
HEARTBEATEOF
else
cat > "$WORKSPACE/HEARTBEAT.md" << HEARTBEATEOF
# Heartbeat — $NAME $EMOJI

Heartbeat is not currently configured for this agent.

To enable periodic heartbeat, update the gateway config:
\`\`\`json5
{
  agents: {
    list: [
      {
        id: "$ID",
        heartbeat: {
          every: "30m",
          target: "none",
          activeHours: { start: "08:00", end: "22:00" }
        }
      }
    ]
  }
}
\`\`\`
HEARTBEATEOF
fi

echo -e "  ${GREEN}✓${NC} HEARTBEAT.md"

# --- Initial memory file ---
TODAY=$(date +%Y-%m-%d)
cat > "$WORKSPACE/memory/$TODAY.md" << MEMEOF
# $TODAY — $NAME $EMOJI

## Created

Agent **$NAME** was created today.

- **Specialty:** $SPECIALTY
- **Model:** $MODEL
- **Autonomy:** $AUTONOMY
- **Workspace:** \`$WORKSPACE\`

## Notes

Agent is ready for initial testing and customization.
MEMEOF

echo -e "  ${GREEN}✓${NC} memory/$TODAY.md"
echo ""

# ─── Step 3: Get current config & build agent entry ───────────────────
echo -e "${CYAN}[3/6]${NC} ${YELLOW}Building gateway configuration...${NC}"

CURRENT_CONFIG=$(openclaw gateway config.get --format json 2>/dev/null || echo "{}")
EXISTING_AGENTS=$(echo "$CURRENT_CONFIG" | jq -c '.agents.list // []')

# Check if agent ID already exists
EXISTING_CHECK=$(echo "$EXISTING_AGENTS" | jq --arg id "$ID" '[.[] | select(.id == $id)] | length')
if [[ "$EXISTING_CHECK" -gt 0 ]]; then
  echo -e "  ${YELLOW}!${NC} Agent with ID '$ID' already exists in config — updating..."
  EXISTING_AGENTS=$(echo "$EXISTING_AGENTS" | jq --arg id "$ID" '[.[] | select(.id != $id)]')
fi

# Build new agent JSON object
NEW_AGENT_JSON="{
  \"id\": \"$ID\",
  \"name\": \"$NAME\",
  \"workspace\": \"$WORKSPACE\""

# Add model
NEW_AGENT_JSON="$NEW_AGENT_JSON,
  \"model\": {
    \"primary\": \"$MODEL\"
  }"

# Add identity
NEW_AGENT_JSON="$NEW_AGENT_JSON,
  \"identity\": {
    \"name\": \"$NAME\",
    \"emoji\": \"$EMOJI\"
  }"

# Add sandbox if not off
if [[ "$SANDBOX" != "off" ]]; then
  NEW_AGENT_JSON="$NEW_AGENT_JSON,
  \"sandbox\": {
    \"mode\": \"$SANDBOX\",
    \"scope\": \"agent\"
  }"
fi

# Add tools allow/deny
if [[ -n "$TOOLS_ALLOW" ]] || [[ -n "$TOOLS_DENY" ]]; then
  TOOLS_JSON="\"tools\": {"
  if [[ -n "$TOOLS_ALLOW" ]]; then
    ALLOW_ARRAY=$(echo "$TOOLS_ALLOW" | jq -R 'split(",")')
    TOOLS_JSON="$TOOLS_JSON \"allow\": $ALLOW_ARRAY"
    if [[ -n "$TOOLS_DENY" ]]; then
      TOOLS_JSON="$TOOLS_JSON,"
    fi
  fi
  if [[ -n "$TOOLS_DENY" ]]; then
    DENY_ARRAY=$(echo "$TOOLS_DENY" | jq -R 'split(",")')
    TOOLS_JSON="$TOOLS_JSON \"deny\": $DENY_ARRAY"
  fi
  TOOLS_JSON="$TOOLS_JSON }"
  NEW_AGENT_JSON="$NEW_AGENT_JSON,
  $TOOLS_JSON"
fi

# Add heartbeat if configured
if [[ -n "$HEARTBEAT_EVERY" ]]; then
  HEARTBEAT_JSON="\"heartbeat\": {
    \"every\": \"$HEARTBEAT_EVERY\",
    \"target\": \"$HEARTBEAT_TARGET\""
  if [[ -n "$HEARTBEAT_ACTIVE_HOURS" ]]; then
    HB_START=$(echo "$HEARTBEAT_ACTIVE_HOURS" | cut -d'-' -f1)
    HB_END=$(echo "$HEARTBEAT_ACTIVE_HOURS" | cut -d'-' -f2)
    HEARTBEAT_JSON="$HEARTBEAT_JSON,
    \"activeHours\": { \"start\": \"$HB_START\", \"end\": \"$HB_END\" }"
  fi
  HEARTBEAT_JSON="$HEARTBEAT_JSON
  }"
  NEW_AGENT_JSON="$NEW_AGENT_JSON,
  $HEARTBEAT_JSON"
fi

# Close the agent object
NEW_AGENT_JSON="{ $NEW_AGENT_JSON }"

# Validate JSON
echo "$NEW_AGENT_JSON" | jq . > /dev/null 2>&1 || {
  echo -e "  ${RED}Error: Invalid agent JSON generated${NC}"
  echo "$NEW_AGENT_JSON"
  exit 1
}

# Merge with existing agents
ALL_AGENTS=$(echo "$EXISTING_AGENTS" | jq --argjson new "$(echo "$NEW_AGENT_JSON" | jq .)" '. + [$new]')

echo -e "  ${GREEN}✓${NC} Agent config prepared"
echo ""

# ─── Step 4: Apply config patch ───────────────────────────────────────
echo -e "${CYAN}[4/6]${NC} ${YELLOW}Applying gateway config...${NC}"

CONFIG_PATCH=$(cat <<EOF
{
  "agents": {
    "list": $ALL_AGENTS
  }
}
EOF
)

# Show config being applied
echo -e "  ${BLUE}Config patch:${NC}"
echo "$CONFIG_PATCH" | jq . | sed 's/^/    /'
echo ""

TEMP_CONFIG=$(mktemp)
echo "$CONFIG_PATCH" > "$TEMP_CONFIG"
openclaw gateway config.patch --raw "$(cat "$TEMP_CONFIG")" --note "Add $NAME agent via agent-maker skill"
rm "$TEMP_CONFIG"

echo -e "  ${GREEN}✓${NC} Gateway config updated"
echo ""

# ─── Step 5: Optional cron job setup ──────────────────────────────────
echo -e "${CYAN}[5/6]${NC} ${YELLOW}Automation setup...${NC}"

if [[ -n "$HEARTBEAT_EVERY" ]]; then
  echo -e "  ${GREEN}✓${NC} Heartbeat configured: every $HEARTBEAT_EVERY"
  if [[ -n "$HEARTBEAT_ACTIVE_HOURS" ]]; then
    echo -e "  ${GREEN}✓${NC} Active hours: $HEARTBEAT_ACTIVE_HOURS"
  fi
  echo ""
fi

echo "Would you like to set up a daily memory consolidation cron job?"
echo "This creates a nightly job that reviews and summarizes the day's activity."
echo ""
read -p "Create daily memory cron? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo ""
  echo "What time should the daily memory update run? (24-hour format, e.g., 23:30)"
  read -p "Time (HH:MM): " MEMORY_TIME

  HOUR=$(echo "$MEMORY_TIME" | cut -d: -f1)
  MINUTE=$(echo "$MEMORY_TIME" | cut -d: -f2)

  echo ""
  echo "What timezone? (e.g., America/New_York, Asia/Ho_Chi_Minh, Europe/London)"
  read -p "Timezone: " TIMEZONE

  openclaw cron add \
    --name "$NAME Daily Memory" \
    --cron "$MINUTE $HOUR * * *" \
    --tz "$TIMEZONE" \
    --session "$ID" \
    --system-event "End of day memory update: Review today's activity and conversations. Update $WORKSPACE/memory/\$(date +%Y-%m-%d).md with a summary of: what you worked on, decisions made, progress on tasks, things learned, and important context for tomorrow. Be thorough but concise. After updating, reply HEARTBEAT_OK." \
    --wake now

  echo -e "  ${GREEN}✓${NC} Daily memory cron created ($MEMORY_TIME $TIMEZONE)"
  echo ""
fi

# ─── Step 6: Summary ─────────────────────────────────────────────────
echo ""
echo -e "${CYAN}[6/6]${NC} ${GREEN}Agent creation complete!${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  $NAME $EMOJI — Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  ${CYAN}ID:${NC}         $ID"
echo -e "  ${CYAN}Name:${NC}       $NAME $EMOJI"
echo -e "  ${CYAN}Specialty:${NC}  $SPECIALTY"
echo -e "  ${CYAN}Model:${NC}      $MODEL"
echo -e "  ${CYAN}Autonomy:${NC}   $AUTONOMY"
echo -e "  ${CYAN}Sandbox:${NC}    $SANDBOX"
echo -e "  ${CYAN}Workspace:${NC}  $WORKSPACE"
echo ""
echo -e "  ${CYAN}Files created:${NC}"
echo "    SOUL.md        — Personality & guidelines"
echo "    AGENTS.md      — Operating instructions"
echo "    IDENTITY.md    — Name & emoji"
echo "    TOOLS.md       — Tool conventions"
echo "    USER.md        — User context"
echo "    HEARTBEAT.md   — Periodic checklist"
echo "    memory/        — Daily memory logs"
echo "    skills/        — Agent-specific skills"
echo ""
if [[ -n "$HEARTBEAT_EVERY" ]]; then
  echo -e "  ${CYAN}Heartbeat:${NC}  Every $HEARTBEAT_EVERY → $HEARTBEAT_TARGET"
fi
if [[ -n "$TOOLS_ALLOW" ]]; then
  echo -e "  ${CYAN}Tools (allow):${NC} $TOOLS_ALLOW"
fi
if [[ -n "$TOOLS_DENY" ]]; then
  echo -e "  ${CYAN}Tools (deny):${NC}  $TOOLS_DENY"
fi
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Review & customize SOUL.md and AGENTS.md"
echo "  2. Set up channel bindings if needed:"
echo "     openclaw gateway config.patch --raw '{"
echo "       \"bindings\": [{"
echo "         \"agentId\": \"$ID\","
echo "         \"match\": { \"channel\": \"<channel>\", \"accountId\": \"<account>\" }"
echo "       }]"
echo "     }'"
echo "  3. Test the agent:"
echo "     openclaw agent --agent $ID --message \"Hello! Introduce yourself.\""
echo "  4. Add agent-specific skills to $WORKSPACE/skills/"
echo ""
