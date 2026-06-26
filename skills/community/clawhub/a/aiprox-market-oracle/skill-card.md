## Description: <br>
Get trading signals for single or batch Polymarket markets. Supports timeframe framing ranked by edge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External prediction-market researchers and Polymarket users use this skill to request single-market or batch market analysis, compare ranked edge estimates, and frame recommendations over short, medium, or long timeframes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-query details and an AIPROX spend token are sent to aiprox.dev. <br>
Mitigation: Install only if that network use is acceptable, keep the spend token private, and monitor paid usage. <br>
Risk: Generated trading signals may be wrong or misleading. <br>
Mitigation: Treat signals as research support rather than financial advice and verify decisions independently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unixlamadev-spec/aiprox-market-oracle) <br>
- [AIProx homepage](https://aiprox.dev) <br>
- [AIProx orchestration endpoint](https://aiprox.dev/api/orchestrate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-market output includes signal, edge, confidence, reasoning, and timeframe; batch output ranks up to five markets by opportunity.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
