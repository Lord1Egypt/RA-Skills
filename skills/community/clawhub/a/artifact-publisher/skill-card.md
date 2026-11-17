## Description:

Publish self-contained HTML to a stable share link and read page feedback via Artifact Publisher MCP. Use when the user wants a review/share URL for agent-made HTML, to update the same link, change access, pull comments, or style with built-in themes. Do not use for unrelated hosting, SPA/multi-file deploys, or package registries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angle-labs](https://clawhub.ai/user/angle-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agents use this skill to publish a self-contained HTML page for sharing, manage its access or versions, and retrieve optional reader feedback through Artifact Publisher MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published HTML is hosted externally, and anyone with an unlisted link can open it.

Mitigation: Choose suitable access settings and share links only with intended viewers.

Risk: A publisher key can authorize actions for the connected account.

Mitigation: Prefer OAuth where supported; otherwise keep the key in a client secret store or environment variable and never expose it in chat or artifacts.

Risk: The pack includes dry-run notes that affect release readiness.

Mitigation: Review the release readiness notes before using the pack.

## Reference(s):

- [Artifact Publisher MCP documentation](https://artifactpublisher.com/docs/mcp/)
- [Setup — OAuth vs publisher key](references/setup.md)
- [Live MCP tools](references/tools.md)

## Skill Output:

**Output Type(s):** [API calls, Guidance, Configuration instructions, Text]

**Output Format:** [Markdown guidance with MCP calls and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides an artifact share link and optional feedback summaries; the HTML is supplied or authored by the agent as input to publishing.]

## Skill Version(s):

0.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
