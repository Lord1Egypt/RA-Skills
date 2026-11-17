## Description:

APEX IA Scanner scans Binance Futures USDT perpetual pairs across multiple timeframes and returns ranked analysis signals based on SMA crosses, Pivot SuperTrend, RSI, volume, and confluence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcusfranca12](https://clawhub.ai/user/marcusfranca12)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request Binance Futures market scans and review ranked trading-analysis signals. Outputs should be treated as analysis hints, not financial advice or automated trade instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner behavior and documentation may be inconsistent, including randomized mock-signal behavior called out by security evidence.

Mitigation: Review the package before installation and require the author to remove or clearly separate mock scanning behavior and align the documentation with the calculations.

Risk: Users may mistake market-analysis signals for financial advice or instructions for real trades.

Mitigation: Treat outputs as analysis hints only, require human review, and avoid connecting the skill to real or automated trading workflows.

Risk: Local file writes, web server exposure, runtime package installation, and dependency issues require review before deployment.

Mitigation: Document local files and web exposure, remove runtime package installation, and update vulnerable dependencies before production use.

## Reference(s):

- [APEX IA Scanner ClawHub listing](https://clawhub.ai/marcusfranca12/skills/apex-ia)
- [Binance Futures klines endpoint used by the scanner](https://fapi.binance.com/fapi/v1/klines)
- [ClawHub publisher profile for marcusfranca12](https://clawhub.ai/user/marcusfranca12)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted text containing ranked market-analysis signal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include symbols, timeframes, score, signal direction, RSI, volume, targets, stop values, and confluence notes.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
