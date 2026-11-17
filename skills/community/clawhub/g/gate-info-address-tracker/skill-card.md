## Description:

Tracks and summarizes on-chain wallet addresses using Gate-Info read-only data, with optional transaction history and fund-flow tracing when warranted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to inspect an on-chain address, review labels, balances, risk indicators, DeFi positions, and follow significant transactions or fund flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gate-Info MCP receives submitted wallet addresses and may return enriched blockchain intelligence.

Mitigation: Use the skill only when address sharing with Gate-Info MCP is acceptable for the user's context.

Risk: Basic address lookups may automatically expand into transaction and fund-flow tracing for labeled, high-balance, or risk-flagged addresses.

Mitigation: Ask explicitly for profile-only results when deeper tracing is not desired.

Risk: The reviewed package references shared runtime rule files that are not bundled in the artifact.

Mitigation: Bundle or pin the shared runtime rules before treating the release as low-risk.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-info-address-tracker)
- [Gate Address Tracker MCP Specification](references/mcp.md)
- [Scenarios and Prompt Examples](references/scenarios.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports with address profile, holdings, DeFi, PnL, transaction history, fund-flow, and risk-warning sections as available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Gate-Info MCP results are summarized with missing-data and uncertainty notes when data or tools are unavailable.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
