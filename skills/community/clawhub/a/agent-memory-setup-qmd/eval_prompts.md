# Eval Prompts for agent-memory-setup Skill

## Scoring: Pass (1) / Fail (0) per prompt. Metric = % pass rate.

### P1: Trigger — Direct request
**Prompt:** "Set up the memory system for my new agent"
**Pass criteria:** Skill clearly activates. SKILL.md description/triggers match this phrasing.

### P2: Trigger — Indirect/synonym
**Prompt:** "I just installed OpenClaw, how do I configure agent memory?"
**Pass criteria:** Skill description covers "configure agent memory" as a trigger scenario.

### P3: Trigger — Negative (should NOT trigger)
**Prompt:** "How do I back up my agent's memory files to S3?"
**Pass criteria:** SKILL.md does NOT cover backup/export — nothing misleading that would make an agent think this skill handles backup.

### P4: Setup — Complete directory structure
**Prompt:** "Run the setup for workspace /home/agent/.openclaw/workspace"
**Pass criteria:** SKILL.md + script create ALL required dirs (memory/, memory/hot/, memory/warm/) and ALL files (HOT_MEMORY.md, WARM_MEMORY.md, MEMORY.md, daily log, heartbeat-state.json).

### P5: Setup — Existing workspace (idempotency)
**Prompt:** "I already have memory/ with some files. Will this overwrite them?"
**Pass criteria:** SKILL.md or script explicitly handles existing files (skip/preserve, not overwrite). Clear guidance on idempotency.

### P6: Setup — QMD installation guidance
**Prompt:** "How do I install QMD for semantic search?"
**Pass criteria:** SKILL.md provides specific install commands (pip install qmd or equivalent) AND explains what QMD does in the memory context.

### P7: Setup — Lossless Claw installation guidance
**Prompt:** "How do I install Lossless Claw?"
**Pass criteria:** SKILL.md provides the exact install command (openclaw plugins install @martian-engineering/lossless-claw) AND explains what it does (compaction into expandable summaries).

### P8: Setup — openclaw.json configuration completeness
**Prompt:** "What config changes do I need in openclaw.json?"
**Pass criteria:** SKILL.md lists ALL required config: memorySearch, compaction, contextPruning, heartbeat settings, AND all plugin enables (session-memory, bootstrap-extra-files, lossless-claw).

### P9: Edge case — Missing openclaw CLI
**Prompt:** "I don't have the openclaw CLI installed yet. Can I still set up memory?"
**Pass criteria:** SKILL.md or script handles the case where openclaw CLI is not available — provides fallback or clear prerequisite message.

### P10: AGENTS.md template — Quality and completeness
**Prompt:** "What instructions should I put in AGENTS.md for the agent to use the memory system?"
**Pass criteria:** SKILL.md references the AGENTS_TEMPLATE.md AND the template covers: session startup routine (read SOUL/USER/daily logs), memory tiering explanation, when to update each tier, write-it-down principle, heartbeat guidance.

### P11: AGENTS.md template — Customization guidance
**Prompt:** "I'm setting up a CFO agent, not a marketing agent. How do I customize the memory template?"
**Pass criteria:** SKILL.md explicitly mentions adapting/customizing the AGENTS.md template to the agent's domain (e.g., what to check on heartbeats).

### P12: Verification — Post-setup validation
**Prompt:** "How do I verify everything was set up correctly?"
**Pass criteria:** SKILL.md includes verification steps: check qmd --version, check plugin list, verify directories/files exist. Clear checklist format.

### P13: Architecture — Tier explanation clarity
**Prompt:** "What's the difference between HOT, WARM, and COLD memory?"
**Pass criteria:** SKILL.md clearly explains all 3 tiers with: file location, purpose, update frequency, and concrete examples of what goes in each.

### P14: Edge case — Multiple agents sharing workspace
**Prompt:** "I have two agents sharing the same workspace. Any gotchas?"
**Pass criteria:** SKILL.md mentions the shared workspace hazard (HOT_MEMORY read by all agents) and provides guidance on what NOT to put in HOT_MEMORY.

### P15: Troubleshooting — Common issues
**Prompt:** "I set everything up but the agent doesn't seem to be using memory. What went wrong?"
**Pass criteria:** SKILL.md includes troubleshooting guidance OR a checklist of common issues (plugin not enabled, config not applied, gateway not restarted, etc.).
