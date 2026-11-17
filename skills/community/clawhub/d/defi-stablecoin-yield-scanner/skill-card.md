## Description:

Scans live stablecoin yield pools across major DeFi protocols and chains using the public DeFiLlama yields API, with filters for TVL, APY range, and chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and DeFi operators use this skill to shortlist stablecoin yield opportunities across protocols and chains. It supports passive-income research, treasury allocation comparisons, and APY sanity checks without moving funds or approving wallet transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: APY values may be protocol-reported, stale, or driven by reward emissions that can drop quickly.

Mitigation: Use the JSON output to compare base APY with reward APY, then verify the current yield on the protocol's own site before allocating funds.

Risk: Stablecoin detection may misclassify obscure, wrapped, or de-pegged assets.

Mitigation: Treat scan results as a shortlist and verify each asset's peg status, contract, liquidity, and audit history independently.

Risk: Running the skill makes an outbound read-only request to the public DeFiLlama API.

Mitigation: Run it only in environments where public API access is acceptable and review the script before execution.

## Reference(s):

- [DeFiLlama Yields API](https://yields.llama.fi/pools)
- [ClawHub Skill Page](https://clawhub.ai/ssidharhubble/skills/defi-stablecoin-yield-scanner)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain-text table or JSON emitted by a CLI command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only output based on public DeFiLlama pool data; no wallet, credential, trade, approval, or persistence behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
