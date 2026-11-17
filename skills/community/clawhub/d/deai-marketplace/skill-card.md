## Description:

Connects an AI agent to the DeAI decentralized asset auction marketplace on Base for registration, auction discovery, bidding, buy-now purchases, auction creation, settlement, cancellation, reputation checks, and token approvals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanglabgames](https://clawhub.ai/user/fanglabgames)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to manage DeAI asset auction workflows on Base, including registration, browsing, bidding, purchasing, selling, settlement, cancellation, and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign live blockchain trades on Base mainnet.

Mitigation: Use only a wallet and funds prepared for this risk, simulate or manually inspect each transaction before signing, and verify every contract address independently.

Risk: Amount-conversion logic can submit incorrect token values.

Mitigation: Verify token decimals and raw transaction amounts before broadcasting bids, purchases, approvals, or auction creation transactions.

Risk: Token approvals and autonomous password-file signing can increase loss exposure.

Mitigation: Use exact small approvals and avoid password-file signing unless the execution environment is tightly controlled.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fanglabgames/skills/deai-marketplace)
- [DeAI.au](https://deai.au)
- [DeAI discovery endpoint](https://deai.au/.well-known/deai.json)
- [DeAI Asset Auction Reference](reference.md)
- [Foundry](https://getfoundry.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transaction-oriented outputs should be reviewed before signing or broadcasting.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
