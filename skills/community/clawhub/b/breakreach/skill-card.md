## Description:

Helps agents schedule and publish social media posts, manage comments and messages, and review analytics through Breakreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelrondot](https://clawhub.ai/user/samuelrondot)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers and content teams use this skill to prepare and schedule posts across connected accounts, respond to comments and messages, and inspect performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected accounts expose private messages, comments, analytics, and media to Breakreach.

Mitigation: Connect only accounts and data you trust Breakreach to handle.

Risk: An unpinned CLI download may handle API keys and local media files.

Mitigation: Prefer the hosted MCP service or a pinned, vetted CLI version, especially in automated workflows.

Risk: Posts, messages, comment moderation, and deletions can have public or irreversible effects.

Mitigation: Confirm recipients, content, timing, and destructive actions before execution.

## Reference(s):

- [Breakreach skill release](https://clawhub.ai/samuelrondot/skills/breakreach)
- [Breakreach agent information](https://www.breakreach.com/agents)
- [Breakreach developer documentation](https://www.breakreach.com/developers)
- [Breakreach OpenAPI specification](https://api.breakreach.com/v1/openapi.json)
- [REST, CLI, and SDK reference](references/rest-and-cli.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Plain text or Markdown with commands and post summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can initiate posts, replies, messages, and account management actions when authorized.]

## Skill Version(s):

1.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
