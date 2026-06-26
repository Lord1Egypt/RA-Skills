## Description: <br>
APEX IA Scanner scans Binance Futures USDT perpetual pairs across multiple timeframes and returns ranked SMA, Pivot SuperTrend, RSI, volume, and confluence-based trading signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcusfranca12](https://clawhub.ai/user/marcusfranca12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request informational Binance Futures market scans and review ranked candidate setups before doing their own analysis. It should not be used as financial advice or as an automated trading decision engine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-scan outputs can be misleading or fabricated, including mock/random signal paths noted in the security evidence. <br>
Mitigation: Treat outputs as informational, compare them with trusted live market data, and do not use this skill for automated or leveraged trading decisions. <br>
Risk: The package includes runtime installation behavior, local history writers, and a bundled web application that expand the execution and data-writing surface. <br>
Mitigation: Review before installing, run in a restricted environment, and remove or disable runtime npm install fallback, local persistence, and webapp components unless explicitly needed. <br>


## Reference(s): <br>
- [APEX IA Scanner on ClawHub](https://clawhub.ai/marcusfranca12/apex-ia) <br>
- [Publisher profile: marcusfranca12](https://clawhub.ai/user/marcusfranca12) <br>
- [Binance Futures kline endpoint used by artifact](https://fapi.binance.com/fapi/v1/klines) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with ranked market-scan summaries and signal entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include symbol, timeframe, direction, score, RSI, volume ratio, targets, stop, risk/reward, and confluence fields.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
