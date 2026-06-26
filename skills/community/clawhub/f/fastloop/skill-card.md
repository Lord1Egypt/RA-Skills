## Description: <br>
Trades Polymarket BTC/ETH/SOL 5-minute and 15-minute fast markets using CEX momentum, optional funding and order book confirmation, time-of-day filtering, volatility-adjusted sizing, win-rate calibration, and fee-aware EV math. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oryselias](https://clawhub.ai/user/oryselias) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External traders and agent operators use this skill to configure and run a paper-first or live Polymarket fast-market trading loop with calibration, position sizing, and market-filtering controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release declares a live-trading entrypoint, but the implementation file is not included in the artifact evidence. <br>
Mitigation: Install only when you already have and trust the exact fastloop_improved.py implementation, and review it before any live execution. <br>
Risk: The skill includes commands for unattended real-money trading loops. <br>
Mitigation: Start in paper mode, verify daily budget and position limits, add monitoring and a stop plan, and use a low-balance or limited-scope API key where possible. <br>
Risk: Fast prediction markets and fees can make small signal errors costly. <br>
Mitigation: Use the documented calibration flow before going live and review win-rate, P&L, signal breakdown, and market liquidity behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oryselias/fastloop) <br>
- [Publisher profile](https://clawhub.ai/user/oryselias) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and the simmer-sdk Python package; live execution depends on a trusted fastloop_improved.py implementation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
