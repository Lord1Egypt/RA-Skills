## Description: <br>
Call EngageLab App Push REST APIs to send push notifications and in-app messages, manage tags and aliases, schedule or recall messages, query statistics, validate push requests, and configure callbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devengagelab](https://clawhub.ai/user/devengagelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare EngageLab App Push API requests, generate code or shell commands, manage devices and campaigns, and validate requests before sending notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare or invoke live sends, recalls, schedule changes, tag or alias mutations, and irreversible user deletion. <br>
Mitigation: Confirm the app, audience, identifiers, message content, and consequences before execution; prefer validation or read-only calls before live changes. <br>
Risk: EngageLab App Push uses AppKey and Master Secret credentials for Basic authentication. <br>
Mitigation: Keep the Master Secret out of prompts, logs, and generated files; use placeholders until the user intentionally supplies credentials in a trusted environment. <br>
Risk: Callbacks can affect analytics or automation if spoofed or replayed. <br>
Mitigation: Require HMAC-SHA256 verification of the X-CALLBACK-ID header and make callback handlers idempotent in production. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/devengagelab/engagelab-app-push) <br>
- [Callback API Reference](references/callback-api.md) <br>
- [App Push API Error Codes](references/error-codes.md) <br>
- [HTTP Status Code Reference](references/http-status-code.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare live EngageLab API requests that require credentials and human confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
