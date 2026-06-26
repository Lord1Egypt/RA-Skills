# AI Memory System Skill
## Auto-setup for the 3-layer OpenClaw memory architecture

### What It Does
Sets up the complete 3-layer memory system from the Zero-Human Company playbook:
- MEMORY.md (tacit knowledge and preferences)
- Daily notes (memory/YYYY-MM-DD.md)
- Nightly extraction cron job

### Setup Instructions
After installing, tell your AI: "Set up the memory system."

Your AI will:
1. Create MEMORY.md with a template
2. Create the memory/ directory
3. Set up a nightly extraction cron at 11pm your timezone
4. Create today's first daily note entry

### MEMORY.md Template

```markdown
# MEMORY.md — Long-Term Memory

## About [User]
- Name: 
- Timezone: 
- Communication preferences: 

## Working Style
- (Observe and update)

## Key Decisions
- (Log important decisions here)

## Lessons Learned
- (Capture mistakes and insights)

## Hard Rules
- (Non-negotiable boundaries)

## Action Log
- YYYY-MM-DD — [Action taken]
```

### Daily Note Template (memory/YYYY-MM-DD.md)

```markdown
# YYYY-MM-DD

## Key Events
- HH:MM — [What happened]

## Decisions Made
- [Decision and reasoning]

## Facts Extracted
- [Durable facts worth remembering]

## Pending
- [Open items to follow up]
```

### Nightly Extraction Cron

```bash
openclaw cron add \
  --name "nightly-extraction" \
  --cron "0 23 * * *" \
  --tz "[YOUR_TIMEZONE]" \
  --session isolated \
  --message "Review today's conversations. Extract durable facts (relationships, decisions, status changes, milestones). Skip small talk. Update memory/YYYY-MM-DD.md with timeline. Update MEMORY.md with new patterns or preferences." \
  --announce
```

### Memory Rules
1. If it matters, WRITE IT DOWN. Mental notes don't survive sessions.
2. Never delete facts — supersede them instead.
3. Update MEMORY.md when you notice new patterns about your user.
4. Daily notes are raw logs. MEMORY.md is curated wisdom.
5. Review and clean MEMORY.md weekly.

### Version
1.0 by TalonForge
