## Description: <br>
Send emails on behalf of agents and workflows. Supports plain text and HTML. Accepts freeform task strings or explicit fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent workflow operators use Email Bot to send notifications, reports, alerts, and workflow completion messages by providing explicit email fields or a freeform task string. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send outbound email from agent workflows, including from freeform instructions. <br>
Mitigation: Prefer explicit to, subject, and body fields and add a human or workflow confirmation step before each send. <br>
Risk: Recipient addresses, message content, and spend-token-backed requests are handled by AIProx and Resend. <br>
Mitigation: Use the skill only when those services are trusted for the intended data, and protect the AIPROX_SPEND_TOKEN as a paid credential. <br>
Risk: Untrusted pages or documents could supply freeform email instructions that cause unintended messages. <br>
Mitigation: Do not allow untrusted content to directly populate freeform email tasks; validate recipients and message content before sending. <br>


## Reference(s): <br>
- [AIProx](https://aiprox.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, HTML, JSON] <br>
**Output Format:** [Plain text or HTML email content with JSON delivery confirmation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIPROX_SPEND_TOKEN and either explicit to, subject, and body fields or a freeform task string.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
