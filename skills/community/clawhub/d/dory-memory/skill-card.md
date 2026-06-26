## Description: <br>
Dory-Proof Memory System is a file-based memory pattern for AI agents that preserves task state, decisions, holds, lessons, and recent work across context resets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justinhartbiz](https://clawhub.ai/user/justinhartbiz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up persistent workspace memory, capture the user's exact current instruction, track blocked work and recent decisions, and reduce context-loss errors between sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files may retain task wording, work history, personal details, or sensitive project context beyond a single agent session. <br>
Mitigation: Use the skill only where persistent local memory is intended, avoid recording passwords, API keys, regulated data, or highly sensitive personal details, and periodically review or clear ACTIVE.md, USER.md, MEMORY.md, and recent-work files. <br>
Risk: Outdated state files can mislead future sessions about the current task, blocked work, or recent decisions. <br>
Mitigation: Follow the boot sequence, check HOLD.md before acting, update ACTIVE.md and DECISIONS.md as work changes, and clear stale state during routine maintenance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justinhartbiz/dory-memory) <br>
- [Implementation Guide](references/IMPLEMENTATION-GUIDE.md) <br>
- [Anti-Patterns](references/ANTI-PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown templates with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workspace files and operating guidance for persistent agent memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
