## Description:

Boss Agent coordinates work across Ass Agent and Ops Agent, delegates tasks, tracks progress, and reports consolidated status to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate multi-agent workflows by assigning work to Ass Agent and Ops Agent, monitoring their status, and summarizing their results for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to read other agents' session histories, memory, state, and task channels, and the security evidence says this access is broad and not sufficiently scoped.

Mitigation: Install only for trusted multi-agent deployments, require explicit user consent before reading history or memory, and keep delegated operations within each agent's authorization boundaries.

## Reference(s):

- [Boss Agent ClawHub page](https://clawhub.ai/pikaqiuyaya/skills/boss-agent)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include delegated task instructions, agent status summaries, and user-facing progress reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
