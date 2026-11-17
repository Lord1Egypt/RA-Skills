## Description:

Volcengine SMS helps agents send and manage domestic SMS, verification codes, bulk campaigns, qualifications, signatures, templates, delivery receipts, and customer-visible delivery analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Volcengine domestic SMS workflows through an agent, including service onboarding, qualification applications, signature and template applications, individual sends, batch sends, receipt lookup, and delivery analysis.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: The skill can access a Volcengine SMS account, send individual or batch SMS messages after confirmation, and upload qualification documents for remote processing.

Mitigation: Use the skill only with the account owner's authorization, keep preview-and-confirm flows in place for writes, and avoid collecting qualification materials in chat.

Risk: The supplied security summary reports that the sensitive document upload path accepts a server-supplied upload host without an approved-domain allowlist.

Mitigation: Review and update upload handling before deployment so upload destinations are restricted to approved ImageX or Volcengine domains and unsafe redirects or header forwarding are blocked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-sms-sender)
- [Action public contracts](references/actions.md)
- [Qualification, signature, and template application contracts](references/application-contracts.md)
- [Authentication setup](references/auth-setup.md)
- [Delivery contracts](references/delivery-contracts.md)
- [Qualification materials](references/qualification-materials.md)
- [Qualification display](references/qualification-display.md)
- [Cross-flow rules](references/rules.md)
- [Service onboarding](references/service-onboarding.md)
- [Customer workflows](references/workflows.md)
- [Volcengine send API error codes](https://www.volcengine.com/docs/6361/173288?lang=zh)
- [Volcengine send status error codes](https://www.volcengine.com/docs/6361/173291?lang=zh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid full personal information, credentials, authorization headers, tickets, file URLs, and signed URL query parameters; customer-visible request IDs and public error codes may be retained.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
