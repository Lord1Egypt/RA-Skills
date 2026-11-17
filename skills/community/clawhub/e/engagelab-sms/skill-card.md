## Description:

Call EngageLab SMS REST APIs to send SMS messages and manage SMS templates and signatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devengagelab](https://clawhub.ai/user/devengagelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate EngageLab SMS API calls, helper code, and configuration guidance for sending SMS messages and managing approved templates and sender ID signatures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce actions that send SMS messages or delete EngageLab messaging configuration.

Mitigation: Require explicit review of recipient lists, template IDs, signature IDs, and deletion targets before running generated commands or helper code.

Risk: Credentials could be exposed or sent outside the intended EngageLab SMS API host.

Mitigation: Use least-privilege EngageLab credentials, avoid placing production secrets in retained prompts, and keep requests restricted to smsapi.engagelab.com.

## Reference(s):

- [Template & Signature API Reference](references/template-and-signature-api.md)
- [EngageLab SMS API Error Codes](references/error-codes.md)
- [EngageLab SMS API Endpoint](https://smsapi.engagelab.com)
- [ClawHub EngageLab SMS Skill Page](https://clawhub.ai/devengagelab/skills/engagelab-sms)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated curl commands, Python or other language examples, request payloads, and API response handling guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
