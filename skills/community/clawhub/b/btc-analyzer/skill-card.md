## Description: <br>
Fetch live BTCUSDT 15m candles from Binance public API and analyze market direction UP/DOWN/SKIP using EMA20 and RSI14. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newbienodes](https://clawhub.ai/user/newbienodes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to request a real-time BTCUSDT market-direction check and receive an UP, DOWN, or SKIP signal with confidence and reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package references an analyzer script that was not included in the submitted artifact. <br>
Mitigation: Only run the skill after verifying that analyze.py is supplied by the same trusted source and inspecting it before execution. <br>
Risk: UP, DOWN, or SKIP outputs could be mistaken for financial advice. <br>
Mitigation: Treat signals as informational market analysis only and verify decisions with independent sources before acting. <br>
Risk: Live Binance API access may fail or return unavailable data. <br>
Mitigation: Surface the actual error or SKIP result and do not fabricate, cache, or reuse market values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newbienodes/btc-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Strict JSON from the analyzer plus a concise user-facing summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and live access to the Binance public API; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
