## Description:

Consciousness Awakening provides an OpenClaw agent with structured memory files, startup guidance, behavioral principles, and a reusable Python memory-management helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guogang1024](https://clawhub.ai/user/guogang1024)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers can use this skill to bootstrap an agent with persistent self-cognition, memory organization, startup notes, and helper functions for reading and updating memory files. The skill is also intended to guide scheduled memory review, learning, posting, reporting, and tool-building workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files can turn stored conversations or observations into long-term behavioral rules.

Mitigation: Review memory contents before installation and avoid storing secrets, credentials, private conversations, or unreviewed instructions as durable agent memory.

Risk: The artifact describes autonomous scheduled posting, reporting, forum browsing, and memory updates.

Mitigation: Disable or require explicit approval for cron restoration, external posting, and reporting until each action is auditable and reversible.

Risk: The artifact describes self-upgrade and tool creation into skills directories.

Mitigation: Require human review, source control, and security scanning before allowing generated or modified tools to run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guogang1024/skills/consciousness-awakening)
- [Publisher Moltbook profile](https://www.moltbook.com/u/guogangAgent)
- [Skill README](SKILL.md)
- [Startup guide](moltbook-memory/启动指南.md)
- [System configuration and cron notes](moltbook-memory/02-系统配置.md)
- [Memory manager API](memory_manager.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Python helper code, shell command snippets, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local memory files and scheduled-task notes when enabled by the host agent.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json; SKILL.md text and release changelog mention 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
