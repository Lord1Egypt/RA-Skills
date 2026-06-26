# Step 2 — Contradiction Patterns

This is the core detection engine. For each agent, systematically check every pair of instruction sources against these patterns.

## Priority order (when two files conflict)

1. **Cron inline prompt** — always wins at runtime (it's what actually executes)
2. **HEARTBEAT.md** — beats AGENTS.md for periodic task behavior
3. **AGENTS.md** — beats SOUL.md for behavioral rules
4. **SOUL.md** — persona defaults, lowest priority for behavioral rules
5. **Skills** — contextual; win when triggered but may conflict with agent-level rules

---

## Pattern 1: Format Duplication (HIGH RISK)

**What**: The same output format (report structure, message template) defined in two or more files independently.

**Why it's dangerous**: When format is defined in both AGENTS.md and a cron prompt, updating one doesn't update the other. The cron prompt wins at runtime, making the AGENTS.md change invisible. This is the most common real-world contradiction.

**How to detect**:
- Search for structural keywords across all files for the same agent: "format", "structure", "template", "report", "message", numbered lists defining output sections
- Compare: do two files define the same output independently?
- Even if currently aligned, flag as a latent risk if defined in more than one place

**Fix**: Keep format in exactly ONE file. All others should reference it: "Follow AGENTS.md format exactly."

**Real example**: Weather bot AGENTS.md defined report structure (greeting → recommendation → clothing → forecast). Cron payload defined the same structure independently. Both were aligned, but next format change would only hit one file.

---

## Pattern 2: Cron Prompt Override (HIGH RISK)

**What**: A cron job's inline prompt contains behavioral instructions that supersede HEARTBEAT.md.

**Why it's dangerous**: The cron prompt is what actually runs. If it contains old instructions while HEARTBEAT.md has been updated, the agent follows the cron. Fixes to HEARTBEAT.md appear to do nothing.

**How to detect**:
- For each cron job with an inline prompt: does it contain behavioral instructions beyond "run your heartbeat" or "follow HEARTBEAT.md"?
- Compare the cron prompt's instructions against HEARTBEAT.md — any divergence?
- Look for stale instructions that were updated in HEARTBEAT.md but not in the cron

**Fix**: Keep cron prompts minimal — ideally just "Follow your HEARTBEAT.md exactly." Move all behavioral details to HEARTBEAT.md as the single source of truth.

---

## Pattern 3: Routing Mismatch (HIGH RISK)

**What**: Different files specify different targets for the same type of output (sessions_send targets, group IDs, channel routing).

**Why it's dangerous**: Agent sends reports/data to the wrong destination, or sends to multiple destinations causing duplicates.

**How to detect**:
- Search all files for `sessions_send`, session keys, group IDs, channel identifiers
- For each output type (reports, alerts, data relay): is the target consistent across all files?
- Check both the sending agent's files AND the receiving agent's files

**Fix**: Define routing in one place per agent. Use session key constants.

**Real example**: Moltbook was sending reports directly to the user AND to agent:main:main. Instructions needed to explicitly say "send to agent:main:main only — never directly to the user."

---

## Pattern 4: Persona/Tone Conflict (MEDIUM RISK)

**What**: SOUL.md defines one communication style while AGENTS.md or HEARTBEAT.md implies another.

**Why it's dangerous**: Agent oscillates between styles across sessions depending on file read order.

**How to detect**:
- Compare tone descriptors: concise vs verbose, formal vs casual, emoji use, language
- Check if AGENTS.md says "include full context" while SOUL.md says "be concise"
- Check language: does SOUL.md specify Hebrew while AGENTS.md examples are in English?

**Fix**: SOUL.md owns persona/tone. AGENTS.md should not re-specify tone unless overriding for a specific task.

---

## Pattern 5: Trigger/Schedule Mismatch (MEDIUM RISK)

**What**: HEARTBEAT.md says one frequency/trigger while cron schedule says another.

**Why it's dangerous**: Agent either runs too often (cost, spam) or too rarely (stale data).

**How to detect**:
- Compare cron schedule expression against HEARTBEAT.md timing references
- Check for conflicting thresholds (e.g., "report if >5 upvotes" in one file, ">3" in another)

**Fix**: Cron schedule is the runtime truth for timing. HEARTBEAT.md should match or not specify timing.

---

## Pattern 6: Memory Routing Conflict (MEDIUM RISK)

**What**: Two files route the same type of data to different memory locations or formats.

**Why it's dangerous**: Data gets split across locations, causing incomplete context in future sessions.

**How to detect**:
- Search for memory write instructions: "log to", "update", "append to", "save to"
- Check if the same data type is routed to different files (e.g., corrections → MEMORY.md in one file, corrections → ~/self-improving/corrections.md in another)

**Fix**: Define memory routing in one place (typically AGENTS.md). Remove duplicates.

---

## Pattern 7: Dead/Orphaned Rules (MEDIUM RISK)

**What**: A rule exists in one file that another file has superseded, but the old rule was never removed.

**Why it's dangerous**: The agent may follow the old rule in sessions where files are read in a different order.

**How to detect**:
- Look for rules that contradict each other across files with no indication of which wins
- Check MEMORY.md for "from now on" statements that contradict AGENTS.md
- Check if a skill's instructions conflict with the agent's AGENTS.md

**Fix**: Remove the superseded rule. Keep the authoritative version only.

---

## Pattern 8: Cross-Agent Assumption Mismatch (MEDIUM RISK)

**What**: Agent A assumes Agent B will do X, but Agent B's instructions say to do Y.

**Why it's dangerous**: Relay chains break silently. The sending agent thinks the job is done, the receiving agent does something different.

**How to detect**:
- For each sessions_send or cross-agent relay, read BOTH agents' instructions
- Does the sender's expectation match the receiver's instructions?
- Check format expectations: does the sender format data one way while the receiver expects another?

**Fix**: Align both agents' instructions. The sender should match the receiver's expected input, or vice versa.

---

## Pattern 9: Implicit vs Explicit Behavior (LOW-MEDIUM RISK)

**What**: A behavior is implied by one file but not explicitly stated, while another file implies the opposite.

**Why it's dangerous**: The agent fills gaps with defaults that may conflict.

**How to detect**:
- Look for missing explicit instructions where behavior matters: "What happens if the API fails?" "What language should the output be in?"
- Compare across agents doing similar tasks — are there gaps in one that the other fills?

**Fix**: Make implicit behavior explicit in the authoritative file.

---

## Pattern 10: Skill-Agent Instruction Conflict (LOW-MEDIUM RISK)

**What**: A skill's SKILL.md gives instructions that conflict with the agent's AGENTS.md or SOUL.md.

**Why it's dangerous**: When the skill triggers, its instructions may override agent-level rules for that task.

**How to detect**:
- For each installed skill, compare its instructions against the agent's AGENTS.md
- Check: does the skill tell the agent to do something the agent's own rules prohibit?
- Check: does the skill assume a persona, format, or routing that conflicts?

**Fix**: Skills should complement, not override, agent-level rules. Add explicit boundaries in the skill or the agent's AGENTS.md.

---

## Pattern 11: Stale MEMORY.md Directives (LOW RISK)

**What**: MEMORY.md contains "from now on" or behavioral directives that have been superseded by AGENTS.md changes.

**Why it's dangerous**: MEMORY.md is loaded into context and can re-activate old behavior.

**How to detect**:
- Scan MEMORY.md for imperative language: "always", "never", "from now on", "must"
- Compare each directive against current AGENTS.md and HEARTBEAT.md
- Flag any that contradict current instructions

**Fix**: Remove behavioral directives from MEMORY.md. It should contain facts and decisions, not rules. Move rules to AGENTS.md.

---

## Pattern 12: Environment/Config Assumption Drift (LOW RISK)

**What**: Instructions reference environment details (paths, API endpoints, model names) that have changed.

**Why it's dangerous**: Agent uses wrong paths, calls wrong APIs, or references non-existent resources.

**How to detect**:
- Extract all referenced paths, URLs, model names, environment variables from instruction files
- Verify they exist / are current
- Check for hardcoded values that should be dynamic

**Fix**: Update references or make them dynamic.

---

## Audit checklist per agent

For each agent, check all applicable pattern pairs:

- [ ] AGENTS.md ↔ SOUL.md (Patterns 4, 7)
- [ ] AGENTS.md ↔ HEARTBEAT.md (Patterns 1, 5, 6, 7)
- [ ] AGENTS.md ↔ Cron prompts (Patterns 1, 2, 3, 5)
- [ ] HEARTBEAT.md ↔ Cron prompts (Patterns 1, 2, 5)
- [ ] AGENTS.md ↔ Skills (Pattern 10)
- [ ] MEMORY.md ↔ AGENTS.md (Patterns 7, 11)
- [ ] Cross-agent relay pairs (Patterns 3, 8)
- [ ] All files ↔ Environment (Pattern 12)
