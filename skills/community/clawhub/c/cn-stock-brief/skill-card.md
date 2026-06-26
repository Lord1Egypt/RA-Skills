## Description: <br>
Generates concise daily A-share market briefs from public Eastmoney market data, including major indices, sector performance, top gainers, and top losers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch public Chinese A-share market data and generate a readable daily market brief or machine-readable JSON for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Eastmoney for market data. <br>
Mitigation: Install only when outbound requests to Eastmoney are acceptable in the target environment. <br>
Risk: Generated stock briefs can be mistaken for investment advice. <br>
Mitigation: Treat the output as informational market data and verify it before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-stock-brief) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>
- [AISoBrand](https://aisobrand.com) <br>
- [AISoBrand free diagnosis](https://aisobrand.com/free-diagnosis.html) <br>
- [Eastmoney public market data endpoint](https://push2.eastmoney.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [Plain text market brief or JSON emitted by a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches live public market data from Eastmoney; non-trading days may show the previous trading day's data.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
