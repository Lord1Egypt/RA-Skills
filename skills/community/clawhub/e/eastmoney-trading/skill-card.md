## Description: <br>
Eastmoney Trading automates Eastmoney Securities login, holdings and balance queries, portfolio analysis, stock screening, buy and sell order entry, order cancellation, and order lookup through a CDP-connected browser with OCR-assisted CAPTCHA handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchaoqun](https://clawhub.ai/user/chenchaoqun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate an Eastmoney brokerage account, inspect balances and orders, analyze holdings, screen stocks, and place or cancel trades. It is intended only for users who deliberately want agent-assisted brokerage automation involving real financial accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a real Eastmoney brokerage account, including buy, sell, and cancel actions involving real funds. <br>
Mitigation: Install only when this behavior is intentional, keep the default confirmation flow for buy, sell, and cancel commands, and avoid the --confirm bypass unless the trade has been independently reviewed. <br>
Risk: The skill attaches to a browser through CDP and can reuse an authenticated brokerage session. <br>
Mitigation: Use a dedicated local browser profile, keep CDP bound to localhost, and avoid exposing the debugging port to a network. <br>
Risk: Optional third-party OCR providers may receive CAPTCHA images when API keys are configured. <br>
Mitigation: Leave third-party OCR API keys unset unless sending CAPTCHA images to that provider is acceptable. <br>
Risk: Generated logs and screenshots may contain account balances, holdings, orders, or CAPTCHA images. <br>
Mitigation: Store outputs only in a trusted local environment and regularly delete generated logs and screenshots. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenchaoqun/eastmoney-trading) <br>
- [Eastmoney online trading site](https://jywg.18.cn/) <br>
- [Eastmoney stock screening site](https://xuangu.eastmoney.com) <br>
- [Artifact README](README.md) <br>
- [Artifact skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files] <br>
**Output Format:** [Command-line text with optional JSON output, Markdown-style analysis reports, log files, and screenshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include sensitive account balances, holdings, orders, CAPTCHA images, logs, screenshots, and generated trading suggestions.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
