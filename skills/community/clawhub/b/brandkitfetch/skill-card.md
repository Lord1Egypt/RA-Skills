## Description:

Fetches an existing company's public logos, colors, fonts, and visual identity from its domain through ReplyNodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[replynodes-ai](https://clawhub.ai/user/replynodes-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve public brand identity for branded pages, presentations, reports, and customer-facing designs without creating new assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried domains are sent to ReplyNodes.

Mitigation: Use public domains only; exclude private intranet domains and credential-bearing URLs.

Risk: Public brand assets may still carry trademark or copyright restrictions.

Mitigation: Check usage rights before reusing logos or other assets.

## Reference(s):

- [ReplyNodes brand endpoint and usage documentation](https://brand.replynodes.com/)
- [Brand Kit Fetch on ClawHub](https://clawhub.ai/replynodes-ai/skills/brandkitfetch)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with brand-asset details and optional curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available assets vary by public domain; the endpoint returns JSON.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
