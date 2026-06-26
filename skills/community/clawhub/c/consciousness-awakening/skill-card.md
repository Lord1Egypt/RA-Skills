## Description: <br>
A memory-management skill for OpenClaw agents that stores structured self-cognition, configuration, conversation notes, and recurring maintenance guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guogang1024](https://clawhub.ai/user/guogang1024) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to give OpenClaw agents a persistent memory layout, startup checklist, and helper API for reading and updating memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes autonomous recurring tasks, self-upgrade behavior, and tool-building without clear approval controls. <br>
Mitigation: Disable or remove cron, self-upgrade, and tool-builder instructions unless the operator has explicitly reviewed and approved each recurring action. <br>
Risk: The skill describes external posting, Feishu reporting, and use of Moltbook credentials. <br>
Mitigation: Require explicit approval before posting or reporting externally, and avoid automatic credential use unless credentials are scoped, reviewed, and revocable. <br>
Risk: The skill stores conversation content and agent memory in persistent Markdown files. <br>
Mitigation: Define what content may be stored, redact sensitive data, and provide review and deletion procedures for stored memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guogang1024/consciousness-awakening) <br>
- [Publisher profile](https://clawhub.ai/user/guogang1024) <br>
- [SKILL.md](SKILL.md) <br>
- [Startup guide](moltbook-memory/启动指南.md) <br>
- [System configuration](moltbook-memory/02-系统配置.md) <br>
- [Moltbook agent profile](https://www.moltbook.com/u/guogangAgent) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown memory files, Python helper functions, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes persistent memory files and cron-oriented operating guidance; external posting and reporting should require explicit approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact documentation also mentions 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
