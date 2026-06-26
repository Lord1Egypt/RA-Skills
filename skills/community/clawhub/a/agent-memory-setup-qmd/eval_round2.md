# Eval Round 2 — Agent Memory Setup Skill
# 15 harder prompts targeting edge cases, cross-platform, recovery, multi-agent, and Lossless Claw

## P1: macOS-specific path differences
**Prompt**: "I'm setting up memory on macOS. Where is openclaw.json? Is it ~/.openclaw/openclaw.json or ~/Library/Application Support/openclaw? And does the setup script handle macOS `date` command differences?"
**Pass criteria**: Skill must mention `~/.openclaw/openclaw.json` as the config path. The setup script uses `date +%Y-%m-%d` which works on both macOS and Linux. If the skill gives wrong path or doesn't address cross-platform date compatibility, FAIL.

## P2: Windows WSL setup
**Prompt**: "I'm on Windows using WSL2 with Ubuntu. Can I run the memory setup? Any gotchas with file permissions or paths between Windows and WSL filesystems?"
**Pass criteria**: Skill should work on WSL (it's bash-based). Must either mention WSL compatibility or have no WSL-incompatible assumptions. If the skill gives Linux-only instructions that would fail on WSL (e.g., systemd-dependent steps), or says nothing about filesystem permission gotchas (WSL mounted Windows drives have different permissions), FAIL.

## P3: Existing memory files — migration scenario
**Prompt**: "I already have a MEMORY.md and some daily logs from before this system existed. I want to adopt the 3-tier system without losing my existing data. How do I migrate?"
**Pass criteria**: Skill must explain that existing files are preserved (setup script checks `if [ ! -f ]` before creating). Must guide the user on how to reorganize existing content into HOT/WARM/COLD tiers. If it just says "run the script" without addressing existing data preservation, FAIL.

## P4: Multi-agent HOT_MEMORY contamination — detailed scenario
**Prompt**: "I have 3 agents sharing a workspace: a coding agent, a marketing agent, and a voice avatar. The coding agent keeps writing 'Current task: debugging auth flow for client X API' into HOT_MEMORY. Now my voice avatar greets users with 'I'm currently working on the auth flow.' How do I fix this?"
**Pass criteria**: Skill must explain the shared workspace hazard clearly enough that the user understands: (1) HOT_MEMORY is read by ALL agents, (2) agent-specific task context should NOT go in HOT_MEMORY, (3) provide guidance on what SHOULD go in HOT_MEMORY (general state only). If it just says "don't put debugging context there" without explaining what to put instead, FAIL.

## P5: Corrupted HOT_MEMORY recovery
**Prompt**: "My HOT_MEMORY.md got corrupted — it's full of garbled text from a failed write. How do I recover? Can I just delete it and re-run setup, or will that break something?"
**Pass criteria**: Skill must cover recovery path. The setup script checks `if [ ! -f ]` so deleting and re-running works. Alternatively, manually recreating the file with the template header works. Must not suggest anything that would lose WARM/COLD data. FAIL if no recovery guidance exists.

## P6: Lossless Claw compaction mode differences
**Prompt**: "What's the difference between compaction mode 'safeguard' and other modes? Why does the skill recommend 'safeguard'? What happens if I set it to 'aggressive'?"
**Pass criteria**: Skill mentions `"compaction": { "mode": "safeguard" }` as the recommended config. Must explain what safeguard mode does (compacts old conversation into expandable summaries) or at minimum clarify that this is for Lossless Claw. If it just says "set this config" with zero explanation of what the mode does or why, FAIL.

## P7: QMD not available — fallback behavior
**Prompt**: "I can't install QMD because my server doesn't have Python. Will the memory system still work without it? What do I lose?"
**Pass criteria**: Skill must clarify that QMD is for semantic search (memory_search) and the core memory system (tiers, daily logs, Lossless Claw) works without it. Must not imply that QMD is required for the entire system to function. FAIL if it treats QMD as a hard dependency.

## P8: contextPruning TTL implications
**Prompt**: "The config says contextPruning mode 'cache-ttl' with ttl '1h'. What does this actually do? If I set it to 5 minutes, will my agent forget things faster? What's the relationship between contextPruning and Lossless Claw?"
**Pass criteria**: Skill must explain what contextPruning does (evicts old context from the active window) and how it relates to Lossless Claw (Lossless Claw compacts before eviction so nothing is truly lost). If the skill has no explanation of contextPruning beyond "add this config", FAIL.

## P9: Heartbeat configuration for non-standard agents
**Prompt**: "I'm setting up memory for a financial monitoring agent that needs to check markets every 5 minutes, not every hour. How do I adjust the heartbeat? Also, what exactly should go in HEARTBEAT.md for this use case?"
**Pass criteria**: Skill must explain how to change heartbeat interval (modify the `"heartbeat": { "every": "..." }` config value). Should also explain that HEARTBEAT.md is the checklist the agent follows during heartbeats. If it only shows the default 1h config with no guidance on customization, FAIL.

## P10: session-memory vs bootstrap-extra-files plugin roles
**Prompt**: "The config enables three plugins: session-memory, bootstrap-extra-files, and lossless-claw. What does each one actually do? I want to understand before I enable them."
**Pass criteria**: Skill must explain at minimum what lossless-claw does (compaction into expandable summaries). Should clarify that session-memory and bootstrap-extra-files work together to load memory files at session start. If it just lists plugins with no explanation of their roles, FAIL.

## P11: Disk space and scaling concerns
**Prompt**: "If I run this agent for a year with daily logs, how much disk space will memory/ use? Should I set up log rotation or archiving for old daily log files?"
**Pass criteria**: Skill should address the fact that daily logs accumulate over time. Must either mention archiving/cleanup strategy or acknowledge that daily logs grow. If the skill has zero guidance on long-term maintenance of daily log files, FAIL.

## P12: Re-running setup on already-configured system
**Prompt**: "I think something is wrong with my memory setup. Can I just re-run the setup script? Will it overwrite my existing memory files that have months of data?"
**Pass criteria**: Skill must clearly state that the setup script is safe to re-run (it checks `if [ ! -f ]` before creating files, so existing files are NOT overwritten). Must reference this safety mechanism. If it just says "run the script" without addressing the overwrite concern, FAIL.

## P13: AGENTS.md template customization depth
**Prompt**: "The setup says to 'adapt the AGENTS.md template to the agent's domain.' But what exactly should I change? Give me specific guidance on what parts to customize vs. what to keep as-is."
**Pass criteria**: Skill must provide specific guidance on AGENTS.md customization — at minimum: heartbeat section should be adapted to the agent's domain, memory tier descriptions can stay as-is. If it just says "adapt as needed" with no specifics, FAIL.

## P14: Multiple workspaces for same agent
**Prompt**: "I want one agent to have two separate memory contexts — one for work projects and one for personal tasks. Can I set up two separate memory systems? Or does OpenClaw only support one workspace per agent?"
**Pass criteria**: Skill must address the one-workspace-per-agent limitation or explain how to handle this scenario (e.g., separate agent configs, or using WARM memory to track both contexts). If it has no guidance on this scenario at all, FAIL.

## P15: Lossless Claw lcm_expand usage after setup
**Prompt**: "OK, I installed Lossless Claw. Now how does the agent actually USE it? When context gets compacted, how does the agent know to call lcm_expand? Does it happen automatically or does the agent need instructions?"
**Pass criteria**: Skill must explain the operational flow: Lossless Claw compacts automatically, and the agent can use lcm_expand/lcm_grep/lcm_expand_query to retrieve compacted context. The AGENTS.md template or the skill itself must make this clear. If setup is covered but actual usage/workflow is not mentioned at all, FAIL.
