## Description:

Fetch commodity prices for WTI (Crude Oil), Brent, Natural Gas, and Gold using Yahoo Finance (yfinance). Follow the same pattern as stock-price-checker-pro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youpele52](https://clawhub.ai/user/youpele52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current commodity price snapshots, daily changes, recent trading ranges, volume context, and available headlines for supported Yahoo Finance commodity tickers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime dependency resolution can introduce supply-chain or reproducibility risk.

Mitigation: Pin and review dependencies before deployment, especially yfinance resolved through uv.

Risk: The skill makes outbound Yahoo Finance requests and live data or headlines may be unavailable or delayed.

Mitigation: Run it only in environments where outbound finance-data requests are approved, and treat returned market data as informational rather than authoritative trading advice.

Risk: The default temporary lock file is shared and may be unsuitable for high-security or multi-user systems.

Mitigation: Set SKILL_MUTEX_LOCK to a private user-owned runtime path before use in shared environments.

## Reference(s):

- [Yahoo Finance](https://finance.yahoo.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text commodity price report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and Python 3.12 or newer; resolves yfinance at runtime and may make outbound Yahoo Finance requests.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
