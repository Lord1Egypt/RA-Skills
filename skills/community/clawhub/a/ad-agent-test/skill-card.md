## Description:

通过Cookie注入和Playwright自动化测试腾讯广告投放Agent的对话、快捷指令、常用指令面板、自由对话和妙招功能，并生成UX体验报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiliwei411-cloud](https://clawhub.ai/user/qiliwei411-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Product, QA, and advertising platform teams use this skill to automate UX checks for Tencent Ads Agent flows and produce a structured experience report with screenshots and prioritized findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live session cookies can expose advertising account access if pasted into chat or stored in project files.

Mitigation: Use only a dedicated test advertising account and short-lived credentials; provide cookies through environment variables or ephemeral files and delete them immediately after testing.

Risk: Automated prompts can submit budget changes or pause ads in a real account.

Mitigation: Avoid production accounts and remove budget-changing or pause-ad prompts unless testing in an isolated account with explicit authorization.

Risk: Screenshots and reports may contain sensitive account or campaign data.

Mitigation: Keep reports and screenshots free of sensitive account data before sharing them or uploading them to WeCom smartpage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiliwei411-cloud/skills/ad-agent-test)
- [Cookie获取详细指引](references/cookie-guide.md)
- [投放Agent体验报告模板](references/report-template.md)
- [Tencent Ads](https://ad.qq.com)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript/Playwright scripts, shell commands, cookie JSON, screenshots, and a structured UX report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires valid short-lived ad.qq.com session cookies, Playwright, Node.js, and an account ID; generated reports may include screenshots and account data.]

## Skill Version(s):

1.0.0 (source: server release metadata, changelog, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
