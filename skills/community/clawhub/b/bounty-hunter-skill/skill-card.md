## Description:

Helps agents operate the Niuma Bounty task platform on XLayer testnet by querying bounty data and preparing task, submission, review, bidding, balance, allowance, and unsigned transaction workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futeyaoshi](https://clawhub.ai/user/futeyaoshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to inspect Niuma bounty tasks, check balances and allowances, and prepare XLayer testnet transactions for bounty creation, participation, submission, review, bidding, and token approval workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can require users to handle a raw wallet private key for write operations.

Mitigation: Prefer the unsigned build-tx workflow with an external wallet; do not paste or export a production private key, and use only a dedicated low-value test wallet.

Risk: Dependency sourcing is weak in the shipped lockfile.

Mitigation: Regenerate the lockfile from the official HTTPS npm registry before relying on the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/futeyaoshi/skills/bounty-hunter-skill)
- [Niuma Bounty Platform](https://task.niuma.works)
- [XLayer Testnet Explorer](https://www.oklink.com/xlayer-test)
- [Contract Addresses](references/contracts.json)
- [Contract ABIs](references/abis.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations return JSON; build-tx returns unsigned transaction data for external wallet signing.]

## Skill Version(s):

1.0.5 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
