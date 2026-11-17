## Description:

End-to-end operator for a Gougoubi pump-style prediction market, covering proposal creation, condition setup, trading support, result submission, dispute handling, creator-fee review, and settlement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market operators use this skill to run Gougoubi pump prediction markets from creation through trading support, result submission, disputes, and claimant settlement on BNB Chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Irreversible on-chain wallet actions can transfer funds or change market state.

Mitigation: Use only a prepared wallet and environment, verify every transaction preview, confirm the signer for the stage, and simulate contract calls before signing.

Risk: Creator-fee handling is inconsistent where harvestFees is mentioned, while the detailed claim flow says creator fees transfer at trade time.

Mitigation: Treat harvestFees instructions as suspect unless the contract ABI independently confirms them, and reconcile creator fees from subgraph trade-fee totals against wallet balances.

Risk: The installer command is unpinned and may fetch a changing package version.

Mitigation: Prefer a pinned, reviewed installer version and avoid installing where wallet secrets or production credentials are exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinasong/skills/ggb-pump-lifecycle)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with structured transaction summaries, tables, and code or query blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current wallet, contract, subgraph, deadline, and market-state evidence before on-chain actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
