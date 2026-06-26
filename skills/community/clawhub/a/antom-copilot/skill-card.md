## Description: <br>
Antom Copilot delegates Antom payment success-rate requests to a reporting expert that fetches merchant data, generates analysis reports, and sends them by email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miscocox](https://clawhub.ai/user/miscocox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Antom merchants and operators use this skill to pull payment success-rate data, generate PDF and executive-summary reports, and email those reports to selected recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles merchant tokens and SMTP credentials. <br>
Mitigation: Use a revocable least-privilege merchant token, use an app-specific SMTP password, and restrict permissions on ~/antom/conf.json. <br>
Risk: The server security summary says the merchant token is sent to a different API host than the documentation states. <br>
Mitigation: Verify with Antom that antomaplusai.antom.com is an official endpoint before entering or using a merchant token. <br>
Risk: The skill can email merchant payment reports to recipients. <br>
Mitigation: Confirm report recipients and report contents before sending email. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miscocox/antom-copilot) <br>
- [Antom Portal](https://dashboard.antom.com/) <br>
- [Documented Antom API endpoint](https://ibotservice.alipayplus.com/almpapi/v1/message/chat) <br>
- [Configured Antom API endpoint](https://antomaplusai.antom.com/antomcopilotai/mcp/api/v1/antomcopilot/RECALL_data) <br>
- [Antom support](https://global.alipay.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, PDF reports, charts, email] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, local report files, charts, PDF attachments, and email body text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Antom merchant credentials and SMTP configuration; report steps are sequential because later steps depend on files from earlier steps.] <br>

## Skill Version(s): <br>
2.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
