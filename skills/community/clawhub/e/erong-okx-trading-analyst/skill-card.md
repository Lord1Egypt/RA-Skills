## Description: <br>
OKX Trading Analyst fetches OKX cryptocurrency market data, calculates technical indicators, and generates trading signal reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erongcao](https://clawhub.ai/user/erongcao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze OKX cryptocurrency pairs across multiple timeframes, inspect technical indicators, and receive formatted buy, sell, or watch signals. It is an analysis aid and does not place trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags unsafe and under-disclosed local code execution paths. <br>
Mitigation: Review the included scripts before installation, avoid the Node wrapper unless it is needed and trusted, and prefer running the Python analyzer directly with explicit arguments. <br>
Risk: The analyzer asks for OKX API credentials and could expose unnecessary account risk if privileged keys are used. <br>
Mitigation: Use read-only OKX credentials at most, never provide trading or withdrawal permissions, and do not paste secrets into chat. <br>
Risk: News collection can invoke separate local news integrations that are not fully disclosed by the skill documentation. <br>
Mitigation: Run with --no-news unless those local news scripts and external news providers have been reviewed and approved. <br>
Risk: Trading signals and suggested levels can be wrong or misleading in volatile crypto markets. <br>
Mitigation: Treat output as technical analysis only, verify against current market data, and do not use it as financial advice or automated trading authorization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erongcao/erong-okx-trading-analyst) <br>
- [OKX market API base](https://www.okx.com) <br>
- [NS3 news feed API](https://api.ns3.ai/feed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console and Markdown-style technical analysis reports with optional Python module output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include price data, indicator values, signal strength, suggested stop and target levels, news summaries, and local state for quick-change checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
