## Description:

Bounty Hunter Agent scans GitHub, Algora, and Opire for bounty issues, scores opportunities by payout and competition, ranks them, and supports automated pull request workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanxevo3](https://clawhub.ai/user/lanxevo3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill to discover paid open-source issues, compare bounty opportunities, and prioritize work based on payout, freshness, and visible competition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an authenticated GitHub CLI context, so scans may use the installer's GitHub account permissions.

Mitigation: Run it with an account and repository access scope appropriate for bounty discovery, and review GitHub CLI authentication before execution.

Risk: The skill advertises autonomous fix sessions and automatic pull request submission without clear user controls.

Mitigation: Require explicit confirmation and clear repository boundaries before enabling fix-session or pull request workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanxevo3/skills/bounty-hunter-agent)
- [Publisher profile](https://clawhub.ai/user/lanxevo3)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable terminal summary and ranked JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local bounties.json state file in the configured state directory.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact SKILL.md lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
