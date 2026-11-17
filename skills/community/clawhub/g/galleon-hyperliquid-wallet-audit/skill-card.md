## Description:

Audits a public Hyperliquid wallet's bounded activity, trading costs, open orders and current exposure, with reproducible local evidence and explicit coverage gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Traders, analysts and developers use this skill to review a public Hyperliquid account's observed outcomes, fees, funding and current exposure without connecting a wallet or placing trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected public wallet address and time window are sent to Hyperliquid's Info API, and captured activity is stored locally as sensitive financial metadata.

Mitigation: Use only the intended public account and window; restrict access to local captures and review them before sharing.

Risk: Limited history or excluded markets can make observed outcomes look like complete returns or full account exposure.

Mitigation: Preserve coverage gaps and excluded scope in the report; do not present observed subtotals as total profitability or portfolio returns.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/galleon-hyperliquid-wallet-audit)
- [Data scope and API limits](references/data-contract.md)
- [Output contract and interpretation](references/output-contract.md)
- [Hyperliquid Info API documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Files]

**Output Format:** [Markdown report, JSON report and capture, and local raw request/response evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports bounded or partial coverage and records local SHA256 evidence hashes; does not calculate complete portfolio returns.]

## Skill Version(s):

0.4.0 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
