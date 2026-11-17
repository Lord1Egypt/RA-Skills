## Description:

Trade Polymarket 5-minute crypto fast markets using 1-minute candle body analysis and volume surge detection from Binance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richducat](https://clawhub.ai/user/richducat)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to evaluate short-window crypto fast markets and run a dry-run or explicitly enabled live Polymarket trading cycle based on candle body strength, volume surge, and direction alignment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can proceed when a safety check is unavailable or fails open.

Mitigation: Start in dry-run, review or fix the safety check before unattended use, and require explicit --live execution for real trades.

Risk: Trading dependencies are not pinned.

Mitigation: Pin and review simmer-sdk and requests versions before enabling live trading.

Risk: A compromised or over-permissioned trading API key could place unwanted trades.

Mitigation: Use a tightly limited Simmer API key and conservative position limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richducat/skills/dolph-candle-momentum)
- [ClawHub publisher profile](https://clawhub.ai/user/richducat)
- [Binance Klines API endpoint](https://api.binance.com/api/v3/klines)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash snippets and plain-text CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run output is default; live trading requires SIMMER_API_KEY and the --live flag.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
