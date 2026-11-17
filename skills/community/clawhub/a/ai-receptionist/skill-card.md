## Description:

Guides users through deploying an AI receptionist or AI customer service agent using Solvea.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antimoron](https://clawhub.ai/user/antimoron)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to create, test, and deploy a Solvea AI receptionist across web chat, email, phone, Shopify, Google Calendar, and Google Sheets channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to sign up for and configure a third-party Solvea service.

Mitigation: Use it only when Solvea is intended, and verify Solvea's current pricing, terms, data retention, and integration permissions before proceeding.

Risk: The workflow encourages uploading business support documents and connecting customer-facing integrations.

Mitigation: Avoid uploading confidential or regulated data unless the organization has approved controls for that provider and channel.

Risk: The workflow asks the user to copy a personaId value into URLs used by shell open commands.

Mitigation: Validate URL parameters before use and do not paste untrusted or modified values into shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antimoron/skills/ai-receptionist)
- [Solvea registration page](https://app.solvea.cx/#/auth/register)
- [Solvea knowledge base page](https://app.solvea.cx/?personaId={agentId}#/knowledge/knowledgeManage)
- [Solvea agent test page](https://app.solvea.cx/?personaId={agentId}#/agent)
- [Solvea integration page](https://app.solvea.cx/?personaId={agentId}#/deploy/integration)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Opens Solvea dashboard URLs and waits for user confirmation between setup steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
