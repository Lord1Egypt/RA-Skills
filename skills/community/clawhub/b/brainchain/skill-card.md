## Description:

Hand a scoped task to a graded worker on BrainChain and pay only if the result is accepted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usebrainchain](https://clawhub.ai/user/usebrainchain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use BrainChain to delegate scoped, public tasks for independent work and grading, then review the accepted result. The skill also provides setup guidance and a wallet readiness check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent shell may be able to read the payer key; a stolen key is outside the spending caps.

Mitigation: Keep little in the wallet and run the agent shell in the documented OpenClaw sandbox with only the needed BrainChain tools allowed.

Risk: Task briefs and accepted results are public, so private material could be disclosed if included.

Mitigation: Use only public, one-shot tasks and leave out secrets, private code, and personal data.

## Reference(s):

- [BrainChain agent documentation](https://docs.usebrainchain.com/agents)
- [BrainChain decisions](https://usebrainchain.com/decisions)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown instructions and task briefs; JSON wallet status; result format is specified per task]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One brief and one result per task; briefs and accepted results are public.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
