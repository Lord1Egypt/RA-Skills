## Description:

Creates, reads, updates, and exports quotes, payment receipts, and delivery notes from user-provided transaction details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

People preparing business paperwork use this skill to create, review, revise, and export quotes, payment receipts, and delivery notes from their transaction facts. The platform returns document details and private PDF artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transaction facts, customer details, and document contents are sent to the AI Skills platform.

Mitigation: Use only with the user's authorization and avoid sharing private document links publicly.

Risk: Successful create, update, and export operations spend platform balance.

Mitigation: Explain charges before paid actions and avoid duplicate submissions when a result is uncertain.

Risk: A shared platform API key can grant broader access, and exposed keys can be misused.

Mitigation: Prefer the product-specific key when limiting access and keep full keys out of chats and logs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/youteacher/skills/business-documents)
- [Business Documents product](https://ai-skills.open-idea.net/skills/business-documents)
- [API key setup](https://ai-skills.open-idea.net/skill-docs/business-documents/API-KEY.md)
- [Document operations](https://ai-skills.open-idea.net/skill-docs/business-documents/OPERATIONS.md)
- [Request and task handling](https://ai-skills.open-idea.net/skill-docs/business-documents/HTTP-REQUESTS.md)
- [Behavior and error rules](https://ai-skills.open-idea.net/skill-docs/business-documents/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown with document details and private PDF artifact links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports partial or pending results separately; PDF links are shared only with the authorized user.]

## Skill Version(s):

1.4.0 (source: skill metadata and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
