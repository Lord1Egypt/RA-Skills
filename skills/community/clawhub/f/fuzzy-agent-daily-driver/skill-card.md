## Description: <br>
The 6 core workflows every OpenClaw agent uses every day: recall, spawn, schedule, research, delegate, and monitor-update. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill as a daily-driver workflow reference for memory recall, subagent spawning, scheduling, research, delegation, and progress monitoring in OpenClaw-style agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory notes and workspace files may capture sensitive details if used carelessly. <br>
Mitigation: Keep secrets out of MEMORY.md, USER.md, TOOLS.md, and daily notes; review what is written before preserving it. <br>
Risk: Scheduled jobs, spawned sessions, and background processes can keep acting after the initial turn. <br>
Mitigation: Review cron jobs, spawned sessions, and running processes regularly, and remove jobs that are no longer needed. <br>
Risk: Web lookups and outbound messages may expose sensitive topics or send updates to the wrong audience. <br>
Mitigation: Require confirmation before sensitive web searches or external channel messages. <br>


## Reference(s): <br>
- [Memory Patterns](references/memory-patterns.md) <br>
- [Session Patterns](references/session-patterns.md) <br>
- [ClawHub release page](https://clawhub.ai/fuzzyb33s/fuzzy-agent-daily-driver) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JavaScript-style tool-call examples, checklists, and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow reference; no executable scripts or detected credential variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
