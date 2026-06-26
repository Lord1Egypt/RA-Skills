## Description: <br>
APEX IA Pro scans Binance Futures markets across multiple timeframes for SMA 8/21, Pivot SuperTrend, RSI, volume, and confluence trading signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcusfranca12](https://clawhub.ai/user/marcusfranca12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External crypto traders and agent users use this skill to request Binance Futures scans and receive ranked trading setups with scores, targets, stop levels, and timeframe confluence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is advertised mainly as a Binance Futures scanner but also ships auto-trading scripts with embedded exchange credentials and default automatic order execution behavior. <br>
Mitigation: Install only after reviewing exactly which entrypoint OpenClaw will run; treat scanner use as separate from bundled trader scripts, revoke exposed Binance credentials, and run automatic trader or launcher scripts only after verifying account permissions, risk limits, stop behavior, and testnet/live mode. <br>
Risk: The skill produces trading signals for Binance Futures, which may be incorrect, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Use outputs as analysis support only, review signals manually before trading, and avoid treating generated targets or stop levels as financial advice. <br>


## Reference(s): <br>
- [APEX IA Pro ClawHub Release](https://clawhub.ai/marcusfranca12/apex-ia-pro) <br>
- [Binance Futures Klines API Endpoint](https://fapi.binance.com/fapi/v1/klines) <br>
- [Binance Futures Ticker Price API Endpoint](https://fapi.binance.com/fapi/v1/ticker/price) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted text with ranked trading signal summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Signals may include symbols, direction, quality, score, timeframe, RSI, volume ratio, targets, stop levels, risk/reward, and confluence.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
