## Description:

Self-custodial Bitcoin and Lightning wallet guidance for AI agents that supports balances, receiving invoices, payments, and wallet operations through BreezClaw and Breez SDK Spark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robertclarkson](https://clawhub.ai/user/robertclarkson)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to configure and operate a self-custodial Bitcoin and Lightning wallet from an agent, including checking balances, generating receive requests, preparing sends with fees, and confirming payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and build remote code that can handle payments, API keys, and wallet secrets.

Mitigation: Review the repository and package scripts before installation, and prefer a pinned audited commit or signed release.

Risk: Using the skill may expose a Breez API key and self-custodial wallet authority to the agent environment.

Mitigation: Enable it only in trusted environments and restrict access to wallet data and credentials.

Risk: Mnemonic backup and mainnet send capability are highly sensitive.

Mitigation: Expose mnemonic material only on explicit request, show fees before sending, and require explicit user confirmation before payment execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/robertclarkson/skills/bitcoin-wallet)
- [BreezClaw Repository](https://github.com/onesandzeros-nz/BreezClaw)
- [Breez SDK](https://breez.technology/sdk/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet operation guidance, fee display before sends, and explicit confirmation before payment execution.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
