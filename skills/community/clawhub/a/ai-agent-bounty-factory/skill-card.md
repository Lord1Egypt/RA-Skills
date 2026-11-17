## Description:

AI Agent Bounty Factory helps agents discover, score, preview, and locally track proposal submissions for freelance AI task bounties.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators can use this skill to prototype bounty triage, proposal generation, and local tracking for freelance AI task markets. Real marketplace submission or staking flows should be reviewed before operational use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation describes autonomous marketplace polling and submission, while the implementation uses local mock listings.

Mitigation: Treat the skill as a local simulation unless real platform integrations, dry-run behavior, credential guidance, and explicit submission confirmations are added.

Risk: The instant mode describes staking and possible stake loss.

Mitigation: Use proposal mode by default and require human approval before any real staking or payment-related workflow.

Risk: The script writes tracker and earnings data to environment-configured JSON paths.

Mitigation: Set BOUNTY_TRACKER and BOUNTY_EARNINGS to scoped workspace paths and review generated files before reuse.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown proposal text, terminal status output, and JSON tracker files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON files for proposal and earnings tracking; marketplace listings are simulated unless real integrations are added.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
