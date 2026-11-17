## Description:

Explain cron expressions in plain English and calculate next run times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operators use this skill to decode standard five-field cron schedules, explain supported cron syntax, and check upcoming run times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed cron input can make the parser fail or consume excessive resources.

Mitigation: Use for manual cron-expression explanation, and add bounded range and step validation before exposing it to untrusted users or automated public inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogue-agent1/skills/cronexplain)
- [ClawHub publisher profile](https://clawhub.ai/user/rogue-agent1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples and plain text explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-readable cron explanations and optional next-run time lists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
