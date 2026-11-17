## Description:

Monitor current Ethereum gas prices across Slow, Standard, Fast, and Instant tiers with Gwei values, estimated confirmation times, gas alerts, JSON output, and public API fallbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check Ethereum network gas conditions, compare fee tiers, request machine-readable gas data, or script gas threshold checks before non-urgent transaction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alert mode can report success even when standard gas is above the configured threshold, which may mislead scripts that depend on process exit status.

Mitigation: Do not use the alert exit status for trading, swapping, or transaction submission decisions until the alert behavior is fixed; inspect the printed gas value or JSON output instead.

Risk: Gas tiers and estimated confirmation times are derived from public API data and local tier heuristics, so they may be stale, unavailable, or only approximate.

Mitigation: Treat results as informational and cross-check current network conditions before submitting time-sensitive or high-value transactions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fuzzyb33s/skills/gas-tracker)
- [Ethereum PublicNode RPC](https://ethereum.publicnode.com)
- [Blockscout Gas Oracle API](https://api.blockscout.com/api/v1/gasOracle)
- [ethgas.info API](https://ethgas.info/api/ethgas)
- [ethgas.watch API](https://api.ethgas.watch/api/gas)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [CLI text report or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports gas tiers, estimated confirmation times, source, timestamp, block number, base fee when available, and threshold alert messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
