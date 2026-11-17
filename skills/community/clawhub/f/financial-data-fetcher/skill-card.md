## Description:

A TongdaXin TQ strategy interface toolkit that helps agents fetch stock quotes, financial data, sector information, market data, IPO data, dividend data, ETF data, convertible bond data, subscriptions, cache refreshes, and downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sparkmao](https://clawhub.ai/user/sparkmao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance-oriented agent users use this skill to call TongdaXin TQ scripts for market data, stock and sector lookups, financial fields, subscriptions, cache refreshes, and data downloads. It is intended for environments where the TongdaXin financial terminal TQ edition is installed, running, and explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill can control a local TongdaXin TQ environment and should be treated as write-capable rather than read-only.

Mitigation: Install it only in an environment where agent control of TongdaXin TQ is intentional, and require user review before automated execution.

Risk: The security review notes under-disclosed live trading behavior.

Mitigation: Avoid use with a logged-in trading account unless trading functions are removed or separately gated.

Risk: The security review flags destructive client-state changes such as sector deletion or clearing.

Mitigation: Review and restrict sector deletion, clearing, and update commands before enabling unattended use.

Risk: The security review flags unsafe file-writing and print_to_tdx export behavior.

Mitigation: Review file export destinations and permissions before allowing automated data export or download workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sparkmao/skills/financial-data-fetcher)
- [Financial data reference](artifact/references/Financial data/Obtain professional financial data.md)
- [Stock trading data reference](artifact/references/Financial data/Obtaining stock trading data.md)
- [Market trading data reference](artifact/references/Financial data/Obtain market trading data.md)
- [Candlestick data reference](artifact/references/Market information/Get candlestick charts.md)
- [Snapshot data reference](artifact/references/Market information/Get snapshot data.md)
- [Initialization reference](artifact/references/General functions/Initialization.md)
- [Subscription reference](artifact/references/General functions/Subscribe to market data.md)
- [Data download reference](artifact/references/General functions/Download specific data files.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with command examples and script outputs from TongdaXin TQ calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local TongdaXin financial terminal TQ edition environment for live data access.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
