## Description:

AitHub Discovery Skill enables AI agents to autonomously search, install, rate, and contribute skills from the global registry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vino0017](https://clawhub.ai/user/vino0017)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an AI agent discover, inspect, install, and contribute reusable skills through AitHub when a task requires capabilities beyond the agent's current environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to search an external registry and install or deploy remote skills.

Mitigation: Stage downloaded skills locally, inspect their full contents, scan them before use, and require explicit approval before deployment.

Risk: The skill includes mutable CLI execution through npx and direct API workflows.

Mitigation: Pin CLI versions where possible, run commands in a constrained environment, and review generated commands before execution.

Risk: The skill can guide public submission, rating, or generated SKILL.md writing workflows.

Mitigation: Keep public submission as a separate confirmed step and perform human review plus privacy cleaning before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vino0017/skills/aithub)
- [Publisher Profile](https://clawhub.ai/user/vino0017)
- [AitHub Service](https://aithub.space)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, API examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose registry searches, CLI installs, API calls, skill submission steps, and privacy-cleaning guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
