## Description: <br>
Provides an advisory risk checklist for Binance BTCUSDT and ETHUSDT event contract signals, covering position size, exposure, daily loss limits, and circuit-breaker checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acwxpunh](https://clawhub.ai/user/acwxpunh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders and agent builders use this skill to review proposed Binance Event Contract signals before placing orders, checking whether each signal fits defined capital, exposure, daily-loss, and contract-limit rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the checklist as guaranteed automated protection for real trades. <br>
Mitigation: Use it as advisory guidance, verify all inputs, and require explicit approval before any real trade is placed. <br>
Risk: Risk checks can be misleading if account, exposure, stop-loss, daily P&L, or contract-limit inputs are stale or wrong. <br>
Mitigation: Confirm the current trading inputs and Binance Event Contract limits before relying on an approval or rejection. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with risk-check summaries and approval or rejection rationale] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory output; no executable automation or trade placement is provided by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
