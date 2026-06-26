## Description: <br>
Options trading strategy analysis and simulation tool that provides theoretical Black-Scholes pricing, Greeks, strategy P/L simulation, and risk-management guidance for educational use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate educational options strategies, compare theoretical risk/reward profiles, and understand Greeks and position sizing before making independent decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake educational options modeling for personalized financial advice or a trade instruction. <br>
Mitigation: Treat outputs as educational analysis only, verify assumptions independently, and do not rely on the skill as personalized financial advice. <br>
Risk: Theoretical Black-Scholes prices and historical volatility may differ from live option chains, bid-ask spreads, liquidity, early assignment risk, and earnings-driven volatility changes. <br>
Mitigation: Verify current quotes, liquidity, earnings dates, implied volatility, and contract terms with a broker or official market-data source before acting. <br>
Risk: Ticker symbols and related strategy queries may be sent to external market-data services such as FMP. <br>
Mitigation: Use the skill only if external market-data lookups are acceptable, configure API keys carefully, and never provide brokerage credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/einstein-research-options-dv) <br>
- [README](README.md) <br>
- [Black-Scholes pricing script](scripts/black_scholes.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Natural-language guidance with optional Markdown reports, JSON analysis, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use configured FMP market-data lookups for ticker prices, dividend yield, and historical volatility.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
