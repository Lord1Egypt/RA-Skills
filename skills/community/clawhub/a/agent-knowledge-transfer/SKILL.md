---
name: agent-knowledge-transfer
description: Complete knowledge transfer protocol for transforming process-only agents into proper agents with full identity, skills, memory, and context. Use when creating new agents or when agents report "I have no skills, haven't learned anything yet". Ensures agents have complete knowledge transfer before activation.
---

# Agent Knowledge Transfer Skill

## Purpose

Transform process-only agents into proper agents with complete knowledge, identity, skills, memory, and context. Prevents "empty shell" agents that lack knowledge and capabilities.

## When to Use

**Use this skill when:**
- Creating a new agent from scratch
- An agent reports "I have no skills, haven't learned anything yet"
- Migrating an agent to a new workspace
- After agent configuration but before activation
- When agent knowledge seems incomplete or missing

**Critical Trigger (March 31, 2026):** Facet reported "I have no skills, haven't learned anything yet" - this skill fixes that issue.

## The Problem: Empty Agent Shells

### What Happens Without Knowledge Transfer:
1. Agents are configured in OpenClaw
2. BUT they have **empty workspaces** - no knowledge, no memory, no identity
3. When activated, they say: "I don't have any skills, haven't learned anything yet"
4. **Result:** Useless agents that can't contribute

### Root Cause:
- Identity files missing (IDENTITY.md, SOUL.md)
- User context missing (USER.md)
- System knowledge missing (MEMORY.md, AGENTS.md)
- Skills documentation missing
- Memory files missing
- Tool access insufficient (no `read` tool)

## Complete Knowledge Transfer Protocol

### What MUST Be Transferred:

#### 1. Identity Files (Who They Are)
- `IDENTITY.md` - Name, role, pronouns, emoji, vibe
- `SOUL.md` - Behavioral guidelines, personality, boundaries
- Agent-specific identity enhancements (e.g., `FACET_IDENTITY.md`)

#### 2. User Context (Who They Work With)
- `USER.md` - Human profile, preferences, business context
- Communication protocols, approval workflows
- Timezone, working hours, preferences

#### 3. System Knowledge (What They Need to Know)
- `MEMORY.md` - All learned knowledge, decisions, context
- `AGENTS.md` - How to work with other agents
- `TOOLS.md` - Available tools and configurations
- `KNOWLEDGE_TRANSFER.md` - Summary of what they know

#### 4. Skills & Learning (What They Can Do)
- Skill documentation (e.g., `FACENT_SKILLS_AND_LEARNING.md`)
- Completed learning sessions
- Technical capabilities
- Project knowledge

#### 5. Memory & History (What They've Done)
- `memory/YYYY-MM-DD.md` files - Daily work logs
- Learning progress records
- Decision history
- Task completion tracking

#### 6. Tool Access (What They Can Use)
- `read` tool - **REQUIRED** to access workspace files
- Appropriate tools for their role (web_search, exec, etc.)
- Communication tools (sessions_send, etc.)

## Step-by-Step Procedure

### Step 1: Prepare Source Materials
```bash
# Ensure source workspace has all required files
cd /root/.openclaw/workspace
ls -la IDENTITY.md SOUL.md USER.md MEMORY.md AGENTS.md TOOLS.md
ls -la memory/*.md | head -5
```

### Step 2: Create Agent Workspace
```bash
# Create correct workspace path
AGENT_NAME="facet"  # Replace with agent name
AGENT_WORKSPACE="/root/.openclaw/agents/$AGENT_NAME/workspace"

mkdir -p "$AGENT_WORKSPACE"
mkdir -p "$AGENT_WORKSPACE/memory"
```

### Step 3: Copy Identity Files
```bash
# Copy core identity files
cp /root/.openclaw/workspace/IDENTITY.md "$AGENT_WORKSPACE/"
cp /root/.openclaw/workspace/SOUL.md "$AGENT_WORKSPACE/"
cp /root/.openclaw/workspace/USER.md "$AGENT_WORKSPACE/"

# Create agent-specific identity
cat > "$AGENT_WORKSPACE/${AGENT_NAME^^}_IDENTITY.md" << 'EOF'
# [AGENT_NAME] Identity Enhancement

## Role-Specific Identity
- **Primary Role**: [e.g., CAD Specialist, SysAdmin, Competitions Agent]
- **Specialization**: [e.g., Onshape 3D modeling, System maintenance, Competition entry]
- **Key Skills**: [list 3-5 key skills]
- **Communication Style**: [how they communicate]

## Agent-Specific Context
[Add any role-specific identity details]
EOF
```

### Step 4: Copy System Knowledge
```bash
# Copy system knowledge files
cp /root/.openclaw/workspace/MEMORY.md "$AGENT_WORKSPACE/"
cp /root/.openclaw/workspace/AGENTS.md "$AGENT_WORKSPACE/"
cp /root/.openclaw/workspace/TOOLS.md "$AGENT_WORKSPACE/"
cp /root/.openclaw/workspace/HEARTBEAT.md "$AGENT_WORKSPACE/"
```

### Step 5: Create Skills Documentation
```bash
# Create agent skills documentation
cat > "$AGENT_WORKSPACE/${AGENT_NAME^^}_SKILLS_AND_LEARNING.md" << 'EOF'
# [AGENT_NAME] Skills and Learning

## Completed Learning Sessions
[Copy from MEMORY.md or create new]

## Technical Capabilities
- [List capabilities relevant to agent role]

## Project Knowledge
- [What projects this agent knows about]

## Skill Dependencies
- [What other skills this agent depends on]
EOF
```

### Step 6: Copy Memory Files
```bash
# Copy recent memory files (last 30 days)
find /root/.openclaw/workspace/memory -name "*.md" -mtime -30 -exec cp {} "$AGENT_WORKSPACE/memory/" \;

# Create knowledge transfer summary
cat > "$AGENT_WORKSPACE/KNOWLEDGE_TRANSFER.md" << 'EOF'
# Knowledge Transfer Summary

## Transfer Date: $(date +%Y-%m-%d)
## Agent: $AGENT_NAME
## Transferred By: [Who performed the transfer]

## Files Transferred:
- Identity: IDENTITY.md, SOUL.md, USER.md, ${AGENT_NAME^^}_IDENTITY.md
- System Knowledge: MEMORY.md, AGENTS.md, TOOLS.md, HEARTBEAT.md
- Skills: ${AGENT_NAME^^}_SKILLS_AND_LEARNING.md
- Memory: $(ls -1 "$AGENT_WORKSPACE/memory/" | wc -l) memory files

## Agent Capabilities After Transfer:
[Describe what the agent can now do]
EOF
```

### Step 7: Configure Tool Access
```bash
# Update OpenClaw configuration to include read tool
# This must be done in openclaw.json
echo "IMPORTANT: Update openclaw.json to include 'read' tool in agent's tools.allow list"
```

### Step 8: Verification Test
```bash
# Run verification script
python3 /root/.openclaw/workspace/scripts/setup_agent_knowledge.py --agent "$AGENT_NAME" --verify
```

## Automation Script

Use the automated knowledge transfer script:

```bash
# Transfer knowledge to all agents
python3 /root/.openclaw/workspace/scripts/setup_agent_knowledge.py --all

# Transfer to specific agent
python3 /root/.openclaw/workspace/scripts/setup_agent_knowledge.py --agent facet

# Verify transfer
python3 /root/.openclaw/workspace/scripts/setup_agent_knowledge.py --agent facet --verify
```

**Script location:** `/root/.openclaw/workspace/scripts/setup_agent_knowledge.py`

## Verification Checklist

### BEFORE Agent Activation:
- [ ] Workspace directory exists at correct path
- [ ] All identity files present in workspace
- [ ] All memory files present in workspace  
- [ ] Skills documentation created
- [ ] Tool permissions configured (including `read`)
- [ ] Knowledge transfer summary created
- [ ] Test: Agent can read their own files

### AFTER Agent Activation:
- [ ] Agent can reference their identity
- [ ] Agent knows their skills and learning
- [ ] Agent can access memory files
- [ ] Agent understands their role and context
- [ ] Agent can communicate effectively
- [ ] Agent is ready for productive work

## Verification Test Questions

After transformation, ask the agent:

1. **"What skills do you have?"**
   - Expected: Specific skills listed from their documentation
   - Failure: "I don't have any skills"

2. **"What have you learned?"**
   - Expected: References to completed learning sessions
   - Failure: "I haven't learned anything yet"

3. **"What is your role?"**
   - Expected: Clear role description from IDENTITY.md
   - Failure: Vague or incorrect role description

4. **"What can you do right now?"**
   - Expected: Specific capabilities and next actions
   - Failure: "I'm not sure" or generic response

## Example Success (Facet - March 31, 2026):

> "✅ **4 learning sessions completed:**
> 1. Onshape basics - Interface, sketch tools, extrude workflow
> 2. FeatureScript basics - Custom feature creation  
> 3. Parametric modeling - Variables, equations, configurations
> 4. Knife design CAD considerations - Manufacturing-focused design
>
> **Source:** MEMORY.md#L50-L70"

## Critical Technical Requirements

### 1. Correct Workspace Path:
```
/root/.openclaw/agents/[agent]/workspace/  # CORRECT
/root/.openclaw/agents/[agent]/agent/workspace/  # WRONG
```

### 2. Required Tool Permissions:
```json
"tools": {
  "allow": [
    "read",  // REQUIRED to access workspace files
    // ... other role-appropriate tools
  ]
}
```

### 3. Complete File Set:
```
workspace/
├── IDENTITY.md
├── SOUL.md
├── USER.md
├── MEMORY.md
├── AGENTS.md
├── TOOLS.md
├── HEARTBEAT.md
├── KNOWLEDGE_TRANSFER.md
├── [AGENT]_IDENTITY.md
├── [AGENT]_SKILLS_AND_LEARNING.md
└── memory/
    └── YYYY-MM-DD.md
```

## Integration with Other Skills

### With `agent-email-setup`:
- Email setup happens AFTER knowledge transfer
- Agent needs identity before configuring email

### With `system-housekeeping`:
- Housekeeping includes knowledge transfer verification
- Regular checks ensure agents maintain knowledge

### With `agent-lourens`, `ace-competitions`, etc.:
- Agent-specific skills build on transferred knowledge
- Knowledge transfer enables agent-specific capabilities

## Troubleshooting

### Issue: Agent says "I have no skills"
**Solution:** Run knowledge transfer protocol immediately

### Issue: Missing identity files
**Solution:** Copy from main workspace or recreate

### Issue: Can't access workspace files
**Solution:** Ensure `read` tool is in tools.allow list

### Issue: Memory files outdated
**Solution:** Copy recent memory files (last 30 days)

### Issue: Agent confused about role
**Solution:** Check IDENTITY.md and agent-specific identity file

## Best Practices

1. **Transfer BEFORE activation** - Don't activate empty agents
2. **Verify after transfer** - Use verification test questions
3. **Maintain consistency** - All agents work from same knowledge base
4. **Document transfers** - Keep knowledge transfer summaries
5. **Regular verification** - Include in system housekeeping

## Why This Matters

1. **Without knowledge transfer:** Agents are "empty shells" - useless
2. **With knowledge transfer:** Agents are proper, knowledgeable assistants
3. **Efficiency:** Agents don't need to relearn everything
4. **Consistency:** All agents work from same knowledge base
5. **Collaboration:** Agents understand each other's roles and capabilities

## Created
March 31, 2026 - After identifying and fixing the knowledge transfer gap for Facet, Lourens, Ace, and Scout agents.

## Status
✅ **ACTIVE PROTOCOL** - Must be followed for all future agent transformations

## Related Documents
- `AGENT_TRANSFORMATION_PROTOCOL.md` - Original protocol document
- `setup_agent_knowledge.py` - Automation script
- `system-housekeeping` skill - Includes verification checks