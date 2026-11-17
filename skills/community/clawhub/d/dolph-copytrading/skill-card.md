## Description:

Mirror positions from top Polymarket traders using Simmer API with size-weighted aggregation across multiple wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richducat](https://clawhub.ai/user/richducat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect, simulate, and optionally execute copytrading strategies that mirror selected Polymarket wallets through the Simmer API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can exercise live financial trading authority when run with live execution.

Mitigation: Use dry-run first, prefer $SIM paper trading, and only connect a low-value trading account with tight max position and max trade limits.

Risk: Selling behavior and trade-safety boundaries are not disclosed or enforced clearly enough.

Mitigation: Explicitly disable whale exits with --no-whale-exits when buy-only behavior is required, then verify the planned trades before using --live.

Risk: Credentials or wallet authority may expose broader financial access than intended.

Mitigation: Protect SIMMER_API_KEY, avoid exposing a broad wallet private key, and scope any connected wallet to the minimum funds needed for the intended strategy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/richducat/skills/dolph-copytrading)
- [Simmer API](https://api.simmer.markets)
- [Simmer Dashboard](https://simmer.markets/dashboard)
- [predicting.top](https://predicting.top)
- [alphawhale.trade](https://alphawhale.trade)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style status reports with inline shell commands and configuration values.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report wallet counts, positions, skipped conflicts, proposed or executed trades, and portfolio status.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.8.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
