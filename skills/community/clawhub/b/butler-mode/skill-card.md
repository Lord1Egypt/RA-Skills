## Description:

Butler Mode turns an agent into a manager that plans, delegates work to teammate agents, monitors progress, and reviews results instead of doing substantive work directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[csuwl](https://clawhub.ai/user/csuwl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Butler Mode to coordinate multi-agent work by having one agent decompose tasks, assign work to teammate agents, monitor status, and review outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates work to other agents and asks for broad worker authority, including permission-bypass patterns.

Mitigation: Install it only when supervised delegation is intended, and enforce least-privilege permissions outside the skill before using it on sensitive repositories or accounts.

Risk: Delegated agents may produce incorrect guidance, code, commands, or configuration changes.

Mitigation: Review teammate outputs and scan proposed changes before execution or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/csuwl/skills/butler-mode)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include agent task plans, delegation prompts, status summaries, shell command examples, and configuration guidance.]

## Skill Version(s):

1.2.2 (source: server release evidence, created 2026-04-16T13:13:59Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
