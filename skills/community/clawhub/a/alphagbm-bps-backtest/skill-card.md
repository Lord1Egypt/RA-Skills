## Description: <br>
Runs a walk-forward Bull Put Spread backtest for a ticker, comparing FearScore-triggered entries with a no-signal control and returning performance metrics, trade ledger, equity curve, P&L distribution, and a plain-language summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders, analysts, and developers use this skill to compare a FearScore-driven bull put spread entry rule against a no-signal control for a selected ticker and parameter set. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial options-analysis output may be mistaken for guaranteed trading results. <br>
Mitigation: Use the backtest as research support only and verify methodology limits, assumptions, account requirements, and pricing before relying on results for real trades. <br>
Risk: Fresh analyses may call AlphaGBM's API and consume option-analysis credits. <br>
Mitigation: Confirm pricing and parameter choices before requesting new runs, and reuse cached results when appropriate. <br>


## Reference(s): <br>
- [AlphaGBM](https://alphagbm.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/clementgu/skills/alphagbm-bps-backtest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown prose with structured JSON backtest results and bilingual summary fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes side-by-side signal and no-signal results, key performance metrics, trade ledger, equity curve, and P&L distribution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
