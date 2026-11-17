## Description:

APEX IA Scanner scans Binance Futures markets for SMA 8/21 crossover trading signals with Pivot/SuperTrend, RSI, volume, targets, stops, and risk-reward context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcusfranca12](https://clawhub.ai/user/marcusfranca12)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and developers use this agent skill to scan Binance Futures USDT perpetual markets and summarize candidate buy/sell setups. Outputs are informational trading analysis and should be reviewed before any trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes automated Binance Futures trading and order-placement capability that is under-disclosed by the scanner description.

Mitigation: Use scanner-only functionality by default; do not run trader, aggressive, final, SMC, or complete launcher scripts unless automated trading is intentional, reviewed, and explicitly safeguarded.

Risk: Automated trading scripts include embedded Binance API credentials.

Mitigation: Treat exposed credentials as compromised, rotate any related keys, remove hardcoded secrets, and prefer read-only market-data credentials for scanner use.

Risk: Trading signal summaries may be mistaken for financial advice or executable trade instructions.

Mitigation: Manually review signals, validate assumptions independently, and use testnet or paper trading before risking capital.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marcusfranca12/skills/apex-ia-scanner)
- [Binance Futures Exchange Info Endpoint](https://fapi.binance.com/fapi/v1/exchangeInfo)
- [Binance Futures Klines Endpoint](https://fapi.binance.com/fapi/v1/klines)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted text with trading signal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include symbol, direction, timeframe, score, indicator confirmations, targets, stop, and risk-reward fields.]

## Skill Version(s):

2.4.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
