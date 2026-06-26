## Description: <br>
Analyzes Binance USDT-margined perpetual futures using public market data and returns structured BUY, SELL, or HOLD strategy commentary without placing orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wqyblue3316](https://clawhub.ai/user/wqyblue3316) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to review Binance USDT perpetual futures setups, support and resistance, trend context, and risk plans. It is intended for analysis-only trading commentary and does not access private account APIs or place orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Leveraged futures recommendations may be mistaken for automated trading instructions. <br>
Mitigation: Treat outputs as informational analysis only; review recommendations independently before taking any trading action. <br>
Risk: Providing real balances or positions exposes sensitive financial context to the agent. <br>
Mitigation: Use default analysis assumptions unless real account context is intentionally needed for the analysis. <br>
Risk: The helper script contacts Binance public futures APIs and depends on external market data availability. <br>
Mitigation: Run it only in environments where outbound access to Binance public endpoints is acceptable, and prefer HOLD when data is incomplete or inconsistent. <br>


## Reference(s): <br>
- [Analysis Mode](references/analysis-mode.md) <br>
- [System Prompt Coverage](references/system-prompt-coverage.md) <br>
- [Binance USD-M Futures Public API Endpoint](https://fapi.binance.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Structured Chinese Markdown report by default; canonical JSON array when explicitly requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One report or decision object per requested symbol; recommendations are analysis-only and do not execute trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
