## Description: <br>
A-share short-term quantitative analysis skill for live market data, nine-factor screening, bull and bear debate, risk review, and recommendation tracking using free Sina Finance and Eastmoney market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhubohan190601-crypto](https://clawhub.ai/user/zhubohan190601-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch A-share market data, compute technical factors, compare bullish and bearish cases, generate risk-reviewed trade-support outputs, and track recommendations. It is decision support and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading decision-support outputs may be mistaken for verified investment advice. <br>
Mitigation: Treat recommendations, position limits, stop-loss and take-profit levels, and debate outcomes as unverified analysis requiring independent human review. <br>
Risk: Some Eastmoney market data requests use plaintext HTTP. <br>
Mitigation: Use trusted networks, verify market data against an independent source before acting, and avoid sending sensitive information through the skill. <br>
Risk: Executed scripts can write local reports, audit trails, trade logs, and tracking records. <br>
Mitigation: Run the skill in a controlled workspace and review generated files before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhubohan190601-crypto/finbot-stock) <br>
- [Sina Finance Market Data](https://finance.sina.com.cn) <br>
- [Eastmoney Market Data](https://data.eastmoney.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-like console output, and local report or tracking files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write reports, audit trails, trade logs, and tracking records under the skill directory when its scripts are executed.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
