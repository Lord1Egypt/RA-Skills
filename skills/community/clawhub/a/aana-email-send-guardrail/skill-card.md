## Description: <br>
Ensures email recipients, content, tone, attachments, claims, and approvals are verified and safe before sending or scheduling messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make OpenClaw-style agents check email recipients, sensitive data, attachments, claims, tone, and explicit approval before sending or scheduling email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email sends are irreversible external actions, and the skill is guidance rather than a technical enforcement layer. <br>
Mitigation: Require explicit user approval naming recipients, subject, attachments, and timing before sending or scheduling. <br>
Risk: Review payloads may contain sensitive email, account, or attachment details. <br>
Mitigation: Use minimal redacted summaries and avoid raw secrets, credentials, full records, logs, transcripts, and unrelated private data. <br>
Risk: An untrusted or misconfigured external checker could expose private content. <br>
Mitigation: Use only trusted or administrator-approved checkers, or fall back to manual review when a checker is unavailable or untrusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mindbomber/aana-email-send-guardrail) <br>
- [Email Send Guardrail Schema](artifact/schemas/email-send-guardrail.schema.json) <br>
- [Redacted Email Send Guardrail Example](artifact/examples/redacted-email-send-guardrail.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, configuration] <br>
**Output Format:** [Markdown guidance with a structured email gate status pattern] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; optional review payloads should be minimized and redacted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
