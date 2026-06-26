## Description: <br>
ClawMem Pro installs and guides a file-based memory system that lets OpenClaw agents persist daily notes, curated memory, heartbeat state, and optional scheduled extraction across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marc69-69](https://clawhub.ai/user/marc69-69) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up persistent local workspace memory for OpenClaw agents, including MEMORY.md, daily notes, cron inbox files, heartbeat state, and optional cron or scheduled-task automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory files can accumulate sensitive personal, work, or secret-adjacent information over time. <br>
Mitigation: Use the skill only in trusted direct sessions, avoid storing secrets, tokens, personal data, or exact secret locations, and treat MEMORY.md and daily notes as sensitive workspace data. <br>
Risk: Optional cron jobs or scheduled tasks can continue reading and writing workspace memory after setup. <br>
Mitigation: Review the created files, scripts, and schedules before enabling background jobs, and enable them only for the intended local workspace. <br>


## Reference(s): <br>
- [ClawMem Pro on ClawHub](https://clawhub.ai/marc69-69/clawmem-pro) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Tests README](artifact/tests/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and PowerShell commands plus generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local MEMORY.md, HEARTBEAT.md, memory/*.md, and heartbeat-state.json files; optional cron or scheduled tasks can update those files over time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
