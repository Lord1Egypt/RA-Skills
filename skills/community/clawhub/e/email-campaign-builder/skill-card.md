## Description:

Builds a single-send email campaign brief with the subject line, preheader, body and CTA, and marks the CAN-SPAM and bulk sender elements it must carry. Use when the user asks for email campaign builder, can-spam compliant email template, email subject line and preheader. For US lifecycle marketers and ecommerce teams that send email from their own sending domain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US lifecycle marketers and ecommerce teams use this skill to draft and check a single-send campaign brief before preparing the email in their own sending platform. It highlights content limits and compliance elements, but the generated report does not replace manual review of the copy or sending-platform settings.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The generated report can misread template limits as supplied copy and does not perform a complete compliance check.

Mitigation: Manually inspect the campaign copy and sending-platform settings, including required disclosures, postal address, unsubscribe handling, and delivery configuration; do not treat the report as proof of compliance.

Risk: The optional Windows toolkit is an unsigned application and is not reviewed as part of the bundled Python workflow.

Mitigation: Assess the separate download independently, verify its archive hash against the value in the skill documentation, and avoid running it with administrator privileges unless necessary.

## Reference(s):

- [Email legal basics](references/email-legal-basics.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/email-campaign-builder)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown campaign-brief report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks subject, preheader, body, and CTA presence and character limits; does not send or schedule email.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
