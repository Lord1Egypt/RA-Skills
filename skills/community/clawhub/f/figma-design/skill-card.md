## Description:

Read files, manage comments, extract design tokens, download images, and create webhooks in Figma via the Figma REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use this skill to inspect Figma design files, retrieve comments and assets, extract design tokens, generate Tailwind CSS configuration, and manage Figma webhooks through a connected Figma account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party OAuth plugin with broad access to Figma files and actions available to the connected account.

Mitigation: Install only when the publisher and ClawLink service are trusted, and revoke the Figma OAuth connection and remove the plugin when it is no longer needed.

Risk: Write-capable operations can create, update, or delete Figma comments, reactions, and webhooks.

Mitigation: Confirm the target resource and intended effect before each write or destructive action.

## Reference(s):

- [Figma API Overview](https://www.figma.com/developers/api)
- [Figma REST API Reference](https://www.figma.com/developers/api/rest)
- [Figma Webhooks](https://www.figma.com/developers/api/webhooks)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=figma-design)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/figma-design)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Code, Configuration, Files]

**Output Format:** [Markdown with inline shell commands, JSON tool parameters, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce downloaded image files, Figma JSON, design-token data, Tailwind CSS configuration, comments, webhook configuration, or operational guidance depending on the requested Figma task.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
