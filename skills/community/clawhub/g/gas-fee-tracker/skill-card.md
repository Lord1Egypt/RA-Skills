## Description:

Track live EVM gas fees across Ethereum, Base, Polygon, and Arbitrum using free public RPC endpoints with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, blockchain operators, and automation builders use this skill to check current gas prices, log gas snapshots, and gate on-chain activity when gas falls below configured thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public RPC endpoints may time out, rate-limit requests, or observe gas price queries.

Mitigation: Run the skill in an environment where outbound RPC calls are expected, handle per-chain errors, and substitute approved endpoints if required.

Risk: The --log option appends gas snapshots to the file path supplied by the user.

Mitigation: Use an intended log path with appropriate permissions and review generated JSONL files before sharing them.

Risk: The requests dependency is not pinned by the artifact.

Mitigation: Install in a virtual environment and pin requests to an approved version before operational use.

## Reference(s):

- [Gas Fee Tracker README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/ssidharhubble/skills/gas-fee-tracker)

## Skill Output:

**Output Type(s):** [text, json, shell commands, files, guidance]

**Output Format:** [Plain text table or JSON, with optional JSONL log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return per-chain errors and may use exit status as an alert gate when --alert-below is provided.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
