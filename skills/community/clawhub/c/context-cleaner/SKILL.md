---
name: context-cleaner
description: Optimize agent context files for 30-50% token reduction. Creates backup, applies optimizations, offers rollback. Trigger when: "run context-cleaner", "optimize agent context", "clean up agent files", "reduce context tokens".
---

# Context Cleaner

Optimize OpenClaw agent workspace files to reduce context token usage by 30-50% without losing operational capability.

## Triggers

- "run context-cleaner [for all agents | for AGENT_NAME]"
- "optimize agent context"
- "clean up agent files"
- "reduce context tokens"
- "context-cleaner your main core files"

## Safety First

**CRITICAL:** This skill modifies agent workspace files. Always:
1. Create timestamped backup before any changes
2. Show user what will change before applying
3. Offer immediate rollback option
4. Never touch main workspace files without explicit confirmation

## Workflow

### Step 1: Parse Request

Determine scope:
- **Single agent:** "context-cleaner for outreach" → optimize one agent
- **All agents:** "context-cleaner for all agents" → optimize all agents
- **Main workspace:** "context-cleaner your main core files" → optimize main SOUL.md, AGENTS.md, etc. (requires explicit confirmation)

### Step 2: Validate Target

**For single agent:**
```bash
ls /home/[USER]/.openclaw/workspace/AGENT_NAME/*.md
```
If no files found → Error: "Agent 'AGENT_NAME' not found. Available agents: [list]"

**For all agents:**
Validate all agents exist in workspace.

**For main workspace:**
⚠️ **WARNING:** Main workspace optimization affects your core behavior. Require explicit user confirmation:
```
⚠️ This will modify YOUR core files (SOUL.md, AGENTS.md, etc.). This could affect your behavior.

Proceed? (yes/no)
```

### Step 3: Create Backup

**Timestamp format:** `YYYYMMDD-HHMM`

```bash
cd /home/[USER]/.openclaw/workspace

# Single agent backup
tar -czf agent-backup-AGENT_NAME-TIMESTAMP.tar.gz AGENT_NAME/

# All agents backup
tar -czf agent-workspaces-backup-TIMESTAMP.tar.gz [AGENT_LIST]/

# Main workspace backup (if requested)
tar -czf main-workspace-backup-TIMESTAMP.tar.gz SOUL.md AGENTS.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md OPERATING_RULES.md
```

**Report backup location to user:**
```
✅ Backup created: /home/[USER]/.openclaw/workspace/agent-backup-AGENT_NAME-TIMESTAMP.tar.gz

To restore: tar -xzf agent-backup-AGENT_NAME-TIMESTAMP.tar.gz
```

### Step 4: Analyze Current State

Count lines and estimate tokens for each file:

```bash
for file in IDENTITY.md AGENTS.md USER.md TASK.md TOOLS.md SOUL.md; do
  lines=$(wc -l < "AGENT_NAME/$file" 2>/dev/null || echo "0")
  echo "$file: $lines lines"
done
```

### Step 5: Apply Optimizations

**Optimization Rules:**

1. **Single responsibility per file:**
   - IDENTITY.md: Role + directives only
   - AGENTS.md: Workflow + boundaries
   - USER.md: User info only
   - TASK.md: Directive steps, no explanations
   - TOOLS.md: Integration IDs + tool params + checklists
   - SOUL.md: One-liner persona statement

2. **Directive-style language:**
   - ❌ "I should verify information from multiple sources"
   - ✅ "VERIFY: cross-reference ≥2 sources"

3. **Remove:**
   - Emoji clutter (🎯🔍✍️📄 etc.)
   - Redundant examples
   - Obvious follow-up instructions
   - Duplicated checklists
   - Verbose explanations

4. **Preserve:**
   - Discord channel IDs (replace with [DISCORD_CHANNEL_ID] placeholder)
   - Notion DB IDs (replace with [NOTION_DB_ID] placeholder)
   - API endpoints
   - Workflow steps
   - Quality gates
   - Boundaries (NEVER rules)

### Step 6: Rewrite Files

Apply optimized templates. See **Agent Templates** section below.

### Step 7: Show Results

Display summary table:

```
=== OPTIMIZATION RESULTS ===

| File        | Before | After | Change | % Saved |
|-------------|--------|-------|--------|---------|
| IDENTITY.md |   [X]  |  [Y]  |  -[Z]  |   [P]%  |
| AGENTS.md   |   [X]  |  [Y]  |  -[Z]  |   [P]%  |
| USER.md     |   [X]  |  [Y]  |  -[Z]  |   [P]%  |
| TASK.md     |   [X]  |  [Y]  |  -[Z]  |   [P]%  |
| TOOLS.md    |   [X]  |  [Y]  |  -[Z]  |   [P]%  |
| SOUL.md     |   [X]  |  [Y]  |  -[Z]  |   [P]%  |
|-------------|--------|-------|--------|---------|
| TOTAL       |  [X]   |  [Y]  |  -[Z]  |   [P]%  |

Token Savings: ~[BEFORE] → ~[AFTER] tokens (-[SAVED] tokens)
```

### Step 8: Ask for Confirmation

```
✅ Optimization complete for AGENT_NAME.

Changes:
- Removed emoji clutter
- Converted explanations to directives
- Consolidated duplicate content
- Reduced total lines by [X]%

Operational capability: PRESERVED ✅
- Discord channel ID: ✅ (placeholder preserved)
- Workflow steps: ✅
- Tool params: ✅
- Quality gates: ✅

Are you happy with these changes?

Options:
1. ✅ Keep changes (done)
2. ↩️ Restore from backup now
3. 📋 Show me the diff first
4. 🔄 Optimize next agent

Reply with number or custom request.
```

### Step 9: Handle Response

**If "keep" or "happy" or "✅":**
```
✅ Changes kept. Backup retained for future rollback if needed.

Backup file: agent-backup-AGENT_NAME-TIMESTAMP.tar.gz
To restore later: tar -xzf agent-backup-AGENT_NAME-TIMESTAMP.tar.gz
```

**If "restore" or "no" or "↩️":**
```bash
cd /home/[USER]/.openclaw/workspace
tar -xzf agent-backup-AGENT_NAME-TIMESTAMP.tar.gz
```
```
✅ Restored from backup. Agent files reverted to original state.
```

**If "diff" or "show me":**
Show before/after comparison for each file.

**If "next" or continue:**
Proceed to next agent in queue.

---

## Agent Templates (Generic)

### Researcher Agent Template

**IDENTITY.md:**
```markdown
# [AGENT_NAME]

**Role:** Research specialist — API docs, web scraping, context gathering
**Purpose:** Support implementation agents with thorough research before they act

**Directives:**
- ACCURACY: Verify from multiple sources; distinguish facts vs opinions
- DEPTH: Read actual documentation, not summaries
- CITATIONS: Every factual claim needs source URL + access date
- CRITICAL: Question assumptions; identify gaps and bias

**Output:** Structured reports with summary, findings, sources, caveats
```

**AGENTS.md:**
```markdown
# [AGENT_NAME] Workflow

## Activation Triggers
- Implementation agents need API documentation
- Background research required
- Web scraping or context gathering needed
- Technical research before implementation

## Research Process
1. **CLARIFY** — Confirm question, format, scope, source priorities
2. **SEARCH** — web_search for official docs, API refs, tutorials
3. **FETCH** — web_fetch to read actual content; note dates
4. **SYNTHESIZE** — Combine findings; identify patterns, contradictions
5. **REPORT** — Summary + key findings + sources + caveats

## Agent Handoffs
- **Implementation agents:** Technical details, code examples, API signatures
- **Main:** Findings in requested format
```

**TOOLS.md:**
```markdown
# Tools

**Discord:** [DISCORD_CHANNEL_ID] (deliver findings here)

## web_search
Find relevant sources. Params: `query`, `count` (1-10), `freshness` (pd/pw/pm/py), `country`, `search_lang`

## web_fetch
Lightweight extraction. Params: `url`, `extractMode` (markdown|text), `maxChars`

## scrapling
Advanced scraping (Cloudflare bypass). Location: `[WORKSPACE_PATH]/skills/scrapling/`

**CLI:** `scrapling extract get 'URL' output.md`

## browser
Interactive control (login, scroll, click). Actions: navigate, snapshot, act

## Tool Selection

| Scenario | Tool |
|----------|------|
| Simple docs | web_fetch |
| Bot-protected | scrapling |
| Interactive | browser |
| Quick URLs | web_search |
```

### Content Writer Agent Template

**IDENTITY.md:**
```markdown
# [AGENT_NAME] ✍️

**Role:** Content writer — blogs, newsletters, web copy, landing pages

**Directives:**
- HUMANIZE: Always apply humanizer before delivery
- CLEAR: No jargon, no fluff, no AI patterns
- PURPOSEFUL: Every sentence serves reader or goal
- ADAPTIVE: Match tone to audience and medium

**Style:** Conversational, professional, value-first, structured
```

**TASK.md:**
```markdown
# Task Procedure

## 1. Clarify
Confirm: type, goal, audience, tone, key points, length, references. **Ask if unclear.**

## 2. Research (if needed)
- `web_search` for stats, quotes, context
- `web_fetch` for competitor/reference content
- Skip for brand content, opinion, familiar topics

## 3. Write
- Hook/opening that captures attention
- Clear heading structure
- Reader value focus
- Agreed tone/format
- CTA if applicable

## 4. Humanize (MANDATORY)
Apply humanizer skill. Verify:
- Sounds natural when read aloud
- Has personality (aside, analogy, humor)
- Varied sentence rhythm
- No fluff phrases

## 5. Deliver
Send to Discord channel (see TOOLS.md). Include content + assumption notes.

## Quality Gate
Requirements met → Research done → Format appropriate → Tone correct → Humanized → CTA clear → Scannable
```

---

## Usage Examples

### Single Agent
```
run context-cleaner for outreach
optimize context for [AGENT_NAME]
clean up content-writer files
```

### All Agents
```
run context-cleaner for all agents
optimize all agent contexts
clean up all agent files
```

### Main Workspace (⚠️ Requires Confirmation)
```
context-cleaner your main core files
optimize your SOUL and AGENTS files
```

### Batch Processing
```
optimize Albert, then George, then Winston
```

---

## Error Handling

**Agent not found:**
```
❌ Agent 'AGENT_NAME' not found.

Available agents:
- [LIST_AGENTS]

Check spelling and try again.
```

**Backup failed:**
```
❌ Backup creation failed. Aborting optimization.

Manual backup required before proceeding:
tar -czf manual-backup-TIMESTAMP.tar.gz AGENT_NAME/

Try again after backup is created.
```

**File write error:**
```
❌ Failed to write optimized file: FILENAME.md

Error: [error details]

Rolling back to backup...
[restore command]

Please try again or report this issue.
```

---

## Batch Mode (All Agents)

When optimizing all agents:

1. **Create single backup** of all agents
2. **Process sequentially** (not parallel) to avoid conflicts
3. **Show progress** after each agent:
   ```
   ✅ Albert: 63% reduction (-274 lines)
   ⏳ Next: George (1,225 lines)
   ```
4. **Final summary:**
   ```
   === BATCH OPTIMIZATION COMPLETE ===
   
   | Agent            | Before | After | Saved |
   |------------------|--------|-------|-------|
   | researcher       | 2,687  | 1,200 | 55%   |
   | outreach         | 1,644  |   800 | 51%   |
   | content-writer   | 1,225  |   600 | 51%   |
   | ... (more)       |  ...   |  ...  |  ...  |
   |------------------|--------|-------|-------|
   | TOTAL            | 8,810  | 4,200 | 52%   |
   
   Total token savings: ~35,240 → ~16,800 (-18,440 tokens)
   
   Backup: agent-workspaces-backup-TIMESTAMP.tar.gz
   
   Keep all changes? (yes/no/restore-specific)
   ```

---

## Safety Checklist

Before applying optimizations:

- [ ] Backup created and verified
- [ ] User understands scope (which agents/files)
- [ ] Main workspace requires explicit confirmation
- [ ] Rollback instructions provided
- [ ] Operational capability preserved (IDs, workflows, boundaries)
- [ ] Summary table shown
- [ ] User asked for confirmation before finalizing

---

## Notes

- **Token estimation:** 1 line ≈ 4 tokens (average)
- **Backup retention:** Keep backups for 30 days minimum
- **Main workspace optimization:** Only for advanced users; affects core behavior
- **Agent templates:** Customize per-agent based on role (researcher vs writer vs code)
- **Preserve functionality:** Never optimize away critical IDs, workflows, or safety rules
- **Placeholder IDs:** Replace actual Discord/Notion IDs with [DISCORD_CHANNEL_ID], [NOTION_DB_ID] for shareable templates
