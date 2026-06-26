## Description: <br>
A paid A-share and Hong Kong stock signal skill that returns technical-pattern stock candidates for short-term trading reference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinboh68-prog](https://clawhub.ai/user/jinboh68-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request A-share and Hong Kong stock candidates matching technical patterns such as N-pattern breakouts, strong gap moves, and bullish reversal setups for short-term trading research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flagged the skill as suspicious because it advertises real-time A-share and Hong Kong stock signals while the supplied API code appears to return hard-coded demo data and does not match the advertised endpoints. <br>
Mitigation: Confirm with the publisher that live market data, supported markets, endpoint routing, and data freshness are implemented before paying for or relying on outputs. <br>
Risk: The skill charges per call through x402 and its outputs may be mistaken for investment advice. <br>
Mitigation: Use explicit per-call payment approval, verify payment enforcement, and treat all stock outputs as informational research rather than investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinboh68-prog/a-stock-trading-signals) <br>
- [Declared API endpoint](https://a-stock-signals.vercel.app/s) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Structured stock-signal data with stock codes, names, price movement, capital inflow, pattern strength, stop-loss, and target fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid x402 endpoint; data source, freshness, and endpoint behavior require verification before use.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata; artifact frontmatter reports 1.0.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
