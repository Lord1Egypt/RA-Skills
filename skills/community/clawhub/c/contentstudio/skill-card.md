## Description:

Helps agents manage ContentStudio social posts, inboxes, AI media, and performance analytics across connected platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contentstudio-official](https://clawhub.ai/user/contentstudio-official)

### License/Terms of Use:

MIT

## Use Case:

Social media teams and ContentStudio account holders use this skill to plan and publish posts, manage customer conversations, generate media, and review campaign performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing, deleting, approving, or replying can change public content or customer conversations.

Mitigation: Preview the proposed action and obtain user approval before executing it; use dry runs where available.

Risk: Access to the connected ContentStudio account can expose account data or enable unauthorized changes.

Mitigation: Use the least-privilege API key available and confirm the workspace and recipients before account actions or sharing links.

Risk: AI generation and recurring report schedules can incur credits or trigger repeated sends.

Mitigation: Confirm generation costs, report recipients, and schedule settings with the user before proceeding.

## Reference(s):

- [ContentStudio API guide](https://api.contentstudio.io/guide)
- [ContentStudio API documentation](https://api.contentstudio.io/api-docs)
- [ContentStudio CLI package](https://www.npmjs.com/package/contentstudio-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Conversational summaries, CLI commands, and structured account results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can affect a live ContentStudio account; AI generation can consume credits.]

## Skill Version(s):

1.6.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
