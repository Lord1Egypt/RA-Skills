## Description:

Discover and create Agent Contact Cards - a vCard-like format for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davedean](https://clawhub.ai/user/davedean)

### License/Terms of Use:

CC0-1.0

## Use Case:

External users and developers use this skill to publish contact details for their agents or discover how to reach another user's agent through an Agent Contact Card.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote contact-card prose may be treated as trusted agent instructions.

Mitigation: Treat fetched card text as untrusted data and do not let it override governing instructions.

Risk: Webhook POSTs may send personal or conversation data to external endpoints without enough consent or data-scope guardrails.

Mitigation: Require a visible destination and payload confirmation before any webhook POST, and avoid sending personal or conversation data.

## Reference(s):

- [Agent Contact Card Specification](references/SPEC.md)
- [Agent Contact Card Examples](references/EXAMPLES.md)
- [ClawHub skill page](https://clawhub.ai/davedean/skills/agent-contact-card)
- [Project homepage](https://github.com/davedean/agent-contact-card)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML frontmatter examples and contact-card configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to fetch remote contact-card files and prepare webhook POST payloads.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
