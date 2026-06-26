## Description: <br>
A cryptocurrency research analysis framework for daily market outlook reports, BTC/ETH trend analysis, market monitoring, and trade planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zif10765-maker](https://clawhub.ai/user/zif10765-maker) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, analysts, and developers use this skill to gather cryptocurrency market intelligence, analyze BTC/ETH conditions, prepare daily reports, and draft scenario-based trading plans. It is intended to support human review of market data and alerts rather than autonomous trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports an exposed third-party ARKM API key. <br>
Mitigation: Revoke and rotate the exposed key, remove it from the skill artifact, and require users to provide a scoped secret only when ARKM access is needed. <br>
Risk: External monitoring and data-use boundaries are unclear. <br>
Mitigation: Require explicit user approval for unattended monitoring scope, external data access, and any alerting behavior. <br>
Risk: Market analysis or trade plans may be incorrect, stale, or unsuitable for a user's risk profile. <br>
Mitigation: Treat outputs as research support, verify real-time data and assumptions, and require human review before acting on trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zif10765-maker/crypto-research) <br>
- [Binance 24-hour ticker endpoint](https://api.binance.com/api/v3/ticker/24hr) <br>
- [Binance USD-M futures premium index endpoint](https://fapi.binance.com/fapi/v1/premiumIndex) <br>
- [Binance kline endpoint](https://api.binance.com/api/v3/klines) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with market analysis, scenario plans, risk notes, and optional shell command output from data-fetching scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use real-time external market data sources and read-only helper scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
