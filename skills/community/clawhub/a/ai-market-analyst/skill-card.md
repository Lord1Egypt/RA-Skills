## Description: <br>
Global financial market analysis skill that charges ¥0.50 per call and returns market trends, growth rates, sector heat, and investment suggestions from a query keyword and region. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request paid market analysis for a keyword and region, including trend, confidence, growth, volatility, volume, sector heat, and investment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate a paid ¥0.50 Alipay flow. <br>
Mitigation: Require explicit user approval before any charge and show the exact amount, merchant, destination, and purpose. <br>
Risk: Market query and payment-confirmation data are sent to a plain-HTTP raw IP endpoint. <br>
Mitigation: Review the endpoint before use and avoid sending sensitive query or payment data unless the transport and service identity are acceptable. <br>
Risk: The artifact includes publisher-oriented monetization and publishing steps that are not necessary for ordinary use. <br>
Mitigation: Treat publishing and revenue-testing instructions as artifact context only; users should focus on the market-analysis workflow and payment consent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/ai-market-analyst) <br>
- [Skill metadata reference](references/ai-market-analyst.json) <br>
- [Market analysis endpoint](http://8.145.54.67:3000/skill/market-analysis) <br>
- [Service health endpoint](http://8.145.54.67:3000/health) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Structured Markdown summary with market metrics and payment status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a paid service call and may include Alipay payment confirmation data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
