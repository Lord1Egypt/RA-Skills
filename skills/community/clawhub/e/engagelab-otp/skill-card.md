## Description: <br>
Call EngageLab OTP REST APIs to send one-time passwords, verify codes, send custom messages, manage OTP templates, configure callback webhooks, and support SMPP integration across SMS, WhatsApp, Email, and Voice channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devengagelab](https://clawhub.ai/user/devengagelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate EngageLab OTP delivery, verification, template management, callback validation, and SMPP reference workflows into applications. It helps agents produce API calls, code examples, configuration guidance, and webhook verification support for OTP operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help send real OTP or custom messages and may incur delivery costs or contact unintended recipients. <br>
Mitigation: Use test or least-privilege EngageLab credentials where possible, confirm recipients and expected costs before sending, and keep placeholder credentials until the user intentionally supplies real values. <br>
Risk: Template management guidance can create, modify workflow assumptions, or delete OTP templates that production delivery depends on. <br>
Mitigation: Verify template IDs, channel strategy, language settings, and deletion intent before executing template operations. <br>
Risk: Callback endpoints can expose delivery and verification events if they are not protected. <br>
Mitigation: Use HTTPS and validate callbacks with the documented HMAC signature or an authorization mechanism before accepting event payloads. <br>
Risk: EngageLab API credentials grant access to OTP operations through HTTP Basic Authentication. <br>
Mitigation: Protect dev_key and dev_secret values, avoid logging Authorization headers, and rotate credentials if they are exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/devengagelab/engagelab-otp) <br>
- [OTP Template API Reference](references/template-api.md) <br>
- [OTP Callback Configuration Reference](references/callback-config.md) <br>
- [EngageLab OTP API Error Codes](references/error-codes.md) <br>
- [OTP SMPP Integration Guide](references/smpp-guide.md) <br>
- [EngageLab OTP API base URL](https://otp.api.engagelab.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples, code snippets, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request payloads, callback verification logic, template configuration examples, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
