## Description:

AB-Agents-Memory provides a long-term memory system for OpenClaw agents, including entity management, context summaries, an AB-Archivus memory agent, and Obsidian vault templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexburrstudio](https://clawhub.ai/user/alexburrstudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add persistent agent memory, organize people, companies, topics, and context summaries, and maintain an Obsidian-backed memory vault across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can create persistent nightly cron execution.

Mitigation: Use --skip-cron unless daily background processing is required, and inspect any generated cron entry before enabling it.

Risk: The memory vault can collect broad local context and personal or business information.

Mitigation: Choose a trusted fixed vault path and avoid storing secrets, credentials, private personal data, or regulated business data without access controls and retention rules.

Risk: Running setup as root can create files and scheduled jobs with elevated ownership.

Mitigation: Run setup as a regular user and review installed files, agent registration, and vault permissions after installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexburrstudio/skills/ab-agents-memory)
- [Project homepage from Clawdis metadata](https://github.com/alexburrstudio/ab-agents-memory)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration details, and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install or update local Obsidian vault files, OpenClaw agent files, and optional cron-based nightly processing.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
