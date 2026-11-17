## Description:

Guides an AI agent through sending one human-approved outbound email via Sendmux and reporting the actual outcome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendmux.ai](https://clawhub.ai/user/sendmux.ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to prepare, approve, send, and reconcile a single outbound email through an existing Sendmux connection. Bulk and batch sending are outside its scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unapproved or incorrect email could be sent to external recipients.

Mitigation: Require explicit human approval of the exact sender, recipients, subject, body, and attachments before sending.

Risk: Overbroad credentials or exposed secrets could permit unauthorized sending.

Mitigation: Use an existing connection with scoped Sendmux sending authorization; do not request secrets in chat or use root keys.

Risk: Retrying an uncertain send could produce duplicate email.

Mitigation: Keep the same idempotency key and identical approved payload; reconcile uncertain outcomes before sending again.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sendmux.ai/skills/email-for-ai-agents)
- [Skill homepage (listed in metadata)](https://github.com/Sendmux/skills)
- [Sendmux connection setup](https://sendmux.ai/docs/ai-integrations/mcp)
- [Sendmux HTTP sending](https://sendmux.ai/docs/sending/http)
- [Sendmux idempotency](https://sendmux.ai/docs/sending/idempotency)
- [Sendmux delegated agent access](https://sendmux.ai/docs/ai-integrations/agent-access)
- [Sendmux attachments](https://sendmux.ai/docs/sending/attachments)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with optional JSON and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposed message for approval and actual send result, including message ID and status or an uncertain outcome.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
