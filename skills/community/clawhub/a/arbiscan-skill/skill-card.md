## Description: <br>
Comprehensive crypto market scanner across Binance, OKX, Bybit, and Bitget. 12 scan types covering arbitrage (funding rate, basis, spot spread, futures spread), market monitoring (open interest, price movers, volume anomaly, stablecoin depeg, funding extreme), and trading signals (funding trend, long/short ratio, new listing detection). Read-only - no trading, no API keys needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZadAnthony](https://clawhub.ai/user/ZadAnthony) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use ArbiScan to scan public crypto market data for arbitrage candidates, market anomalies, and trading signals across major exchanges. It reports opportunities for review and does not execute trades or require API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading signals may be incomplete, stale, or unsuitable for execution. <br>
Mitigation: Treat outputs as informational only and require explicit review, sizing, liquidity, slippage, and confirmation checks before any trade. <br>
Risk: Some exchange endpoints or symbols may be unavailable, causing partial scan results. <br>
Mitigation: Review which exchanges returned data and avoid relying on a scan result unless the relevant market coverage is sufficient. <br>
Risk: The scanner composes with trading or executor skills, which could amplify market-risk decisions if used without human oversight. <br>
Mitigation: Keep ArbiScan read-only and require a separate user decision before invoking any exchange or executor skill. <br>


## Reference(s): <br>
- [ArbiScan ClawHub Release](https://clawhub.ai/ZadAnthony/arbiscan-skill) <br>
- [ZadAnthony ClawHub Profile](https://clawhub.ai/user/ZadAnthony) <br>
- [README.md](artifact/README.md) <br>
- [Sample Output](artifact/examples/sample_output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown tables, JSON, or terminal tables depending on the requested scan mode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only market-data reports; standalone CLI supports table, markdown, and JSON output formats.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
