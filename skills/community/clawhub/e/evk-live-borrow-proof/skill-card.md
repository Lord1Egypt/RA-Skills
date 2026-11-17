## Description:

Prove that a deployed Euler EVK market can really borrow against the intended collateral path with tiny live canaries or dry-run previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daav3](https://clawhub.ai/user/daav3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DeFi protocol operators use this skill to validate that an Euler EVK market can borrow against a configured collateral path after deployment. It supports preview-first checks and tiny live canaries for borrow vault cash, oracle pricing, EVC collateral/controller state, swaps, repayment cleanup, deposits, and final borrow proof reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can make irreversible on-chain financial changes, including spending gas, approving tokens, swapping assets, repaying debt, depositing collateral, changing collateral/controller settings, and borrowing.

Mitigation: Run preview first with tiny amounts, require explicit live intent, review the config carefully, and be prepared to recover manually from a partially completed sequence.

Risk: Weak swap and approval settings can increase slippage or token-spend exposure.

Mitigation: Use exact approvals where possible, opt in explicitly before unlimited approvals, and set realistic nonzero swap minimums from a fresh quote.

Risk: Full-balance deposits or partially completed operations can leave the account in a state different from the intended proof.

Mitigation: Avoid full-balance deposits unless intended, inspect preview and before/after state, and keep proof amounts small.

## Reference(s):

- [EVK live borrow checklist](references/live-borrow-checklist.md)
- [Arbitrum eUSDC-1 isolated example config](references/arbitrum-eusdc1-isolated-example.json)
- [Agentic lending project homepage](https://github.com/daav3/agentic-lending-project)
- [ClawHub skill page](https://clawhub.ai/daav3/skills/evk-live-borrow-proof)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Text]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include preview plans, before/after chain state summaries, transaction hashes for live operations, and unproven chain-specific conditions.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
