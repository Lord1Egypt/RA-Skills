## Description: <br>
Fetches the current Crypto Fear & Greed Index with BTC price movement and concise market sentiment analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyiyuleyuli-cloud](https://clawhub.ai/user/yuyiyuleyuli-cloud) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and trading-oriented agents use this skill to fetch current or recent crypto sentiment data, BTC price movement, and simple sentiment commentary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running a script can attempt to charge a SkillPay account before market data is returned. <br>
Mitigation: Require explicit user approval for paid runs, use narrowly scoped SkillPay credentials when available, and avoid unattended automation. <br>
Risk: The skill produces simple crypto sentiment commentary that may be mistaken for investment advice. <br>
Mitigation: Present the output as market-sentiment context only and pair it with independent review before any trading decision. <br>


## Reference(s): <br>
- [Alternative.me Crypto Fear & Greed Index API](https://alternative.me/crypto/fear-and-greed-index/) <br>
- [ClawHub Skill Page](https://clawhub.ai/yuyiyuleyuli-cloud/fear-greed-index) <br>
- [Publisher Profile](https://clawhub.ai/user/yuyiyuleyuli-cloud) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted terminal text with sentiment values, BTC price movement, and brief analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scripts require a user id and SkillPay credential; paid calls are billed at 0.001 USDT per invocation.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
