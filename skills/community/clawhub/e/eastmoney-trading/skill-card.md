## Description:

Automates Eastmoney Securities browser workflows for login, portfolio and balance review, order lookup, stock screening, and buy, sell, or cancel order actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchaoqun](https://clawhub.ai/user/chenchaoqun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Eastmoney browser sessions for account review, stock screening, and brokerage order management. It is intended for manually supervised trading workflows where real-money actions are reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-money trading actions can place or cancel brokerage orders and may cause financial loss.

Mitigation: Run only in a trusted local browser session, keep second confirmation enabled, avoid --confirm and unattended trading, and manually verify order details and results.

Risk: The release includes sensitive portfolio log JSON and can generate logs or screenshots containing account data.

Mitigation: Remove bundled logs before distribution, restrict access to generated logs and screenshots, and clean them regularly.

Risk: Remote CDP control can expose an authenticated browser session.

Mitigation: Prefer localhost CDP for trading workflows and limit access to the browser debugging port.

Risk: LLM-based captcha OCR may send captcha images to a third party when enabled.

Mitigation: Use local OCR when possible and enable LLM captcha OCR only after accepting that data-sharing risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenchaoqun/skills/eastmoney-trading)
- [Eastmoney online trading](https://jywg.18.cn/)
- [Eastmoney stock screener](https://xuangu.eastmoney.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with Python command examples and JSON/log artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local logs, screenshots, analysis JSON, and browser-driven brokerage actions.]

## Skill Version(s):

3.2.0 (source: server release, target metadata, and frontmatter; artifact _meta.json lists 3.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
