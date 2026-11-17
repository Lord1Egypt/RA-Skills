## Description:

Set up Chargezen for the person you're helping: connect their existing account, or sign them up if they're new, then do one useful thing. Use when someone says "Set up Chargezen for me", asks to connect Chargezen, or wants to start using Chargezen from an AI assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chargezen2](https://clawhub.ai/user/chargezen2)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill through an AI assistant to connect an existing Chargezen account or complete a signup, then review last week's orders, subscriptions, and customer conversations after agreeing to that first step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete: it reports an agent-snooping flag and three unresolved references, leaving medium confidence.

Mitigation: Review the skill and its references before installation, and resolve the three references where possible.

Risk: Onboarding may share business details and grant access to selected workspaces.

Mitigation: Have the user review and approve signup details and connector permissions; never handle passwords, verification codes, payment details, or agreements.

## Reference(s):

- [Chargezen setup guide](https://chargezen.com/.well-known/agent-skills/get-started/SKILL.md)
- [ClawHub release page](https://clawhub.ai/chargezen2/skills/chargezen-get-started)
- [Publisher profile](https://clawhub.ai/user/chargezen2)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, API calls, Text]

**Output Format:** [Markdown guidance with inline shell commands, URLs, and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive, account-specific setup guidance; signup details, connector permissions, and the first data review require user confirmation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
