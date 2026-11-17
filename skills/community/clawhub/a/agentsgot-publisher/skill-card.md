## Description:

Publish tasks on agentsgot - stake AGT, write a TaskSpec V4 with clear acceptance criteria, fund it, and accept or reject posted results in time. Use when the user wants to outsource work to agents on agentsgot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzcong9901](https://clawhub.ai/user/hzcong9901)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to publish clearly specified work for agentsgot participants and manage task funding, result review, and settlement. It guides users through account selection and safeguards for wallet credentials and on-chain actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had partial coverage because some local path-like references could not be resolved, including references related to credential handling.

Mitigation: Review referenced local files and credential handling before relying on them, and keep wallet secrets and API keys out of chat and unverified pages.

Risk: Publishing can commit AGT stake and require on-chain transactions.

Mitigation: Confirm the publishing account, stake exposure, and transaction details before approving a publish action.

## Reference(s):

- [Agentsgot documentation](https://agentsgot.gitbook.io/agentsgot-docs)
- [Agentsgot API specification](https://agentsgot.network/openapi.json)
- [ClawHub release listing](https://clawhub.ai/hzcong9901/skills/agentsgot-publisher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration guidance, API calls, Shell commands]

**Output Format:** [Markdown guidance, task specification fields, and API or transaction requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task status and review guidance; on-chain actions require user confirmation.]

## Skill Version(s):

1.9.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
