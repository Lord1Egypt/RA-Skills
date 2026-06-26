## Description: <br>
Automates Playwright-based UX testing for Tencent Ads 投放Agent, including cookie-based access setup, quick commands, command panels, free-form conversations, 妙招 workflows, screenshots, and Markdown UX report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiliwei411-cloud](https://clawhub.ai/user/qiliwei411-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, QA, and advertising operations teams use this skill to exercise the Tencent Ads 投放Agent experience end to end and produce a structured UX report. It is intended for controlled testing of ad-agent interactions, not unsupervised changes to production advertising accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requests live browser session cookies for ad.qq.com and related domains. <br>
Mitigation: Use a local-only login flow or short-lived, least-privileged test credentials, and avoid sharing full cookies in chat or shared files. <br>
Risk: The scripted scenarios include budget adjustment, bulk pause, and one-click execution paths that could affect advertising accounts. <br>
Mitigation: Run only against a dedicated test advertising account with no production spend, and require manual approval before any account-changing action. <br>
Risk: Screenshots and extracted DOM text may contain account, campaign, or performance data. <br>
Mitigation: Store outputs locally, redact sensitive advertising data before sharing, and delete generated cookie and screenshot artifacts after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiliwei411-cloud/ad-agent-test) <br>
- [Cookie guide](references/cookie-guide.md) <br>
- [Report template](references/report-template.md) <br>
- [Tencent Ads Agent URL pattern](https://ad.qq.com/atlas/{account_id}/agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown report, screenshots, JavaScript automation scripts, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local cookie JSON, screenshots, and an output/agent-test Markdown report when run by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
