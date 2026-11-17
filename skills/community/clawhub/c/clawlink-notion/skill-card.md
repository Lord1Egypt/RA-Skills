## Description:

Search pages and databases, update content, and manage Notion workspace data from chat. Use this skill when users want to read, create, or modify Notion pages, query databases, manage sections, or automate Notion workflows via the Notion API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect OpenClaw to Notion through ClawLink, then search, read, create, update, and manage Notion pages and databases from chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an external OAuth-backed ClawLink plugin that can remain available in future OpenClaw chats.

Mitigation: Install only when the user trusts ClawLink, review Notion permissions during authorization, and remove or disable the plugin when it is no longer needed.

Risk: Connected Notion access may expose or modify pages, databases, and workspace content within the authorized scope.

Mitigation: Share only the Notion pages or databases needed, use read/list/search calls before writes, and require explicit confirmation before create, update, or delete operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hith3sh/skills/notion-pages)
- [Notion API Documentation](https://developers.notion.com/)
- [Notion Integration Guide](https://www.notion.so/help/guides)
- [ClawLink](https://claw-link.dev)
- [ClawLink OpenClaw docs](https://docs.claw-link.dev/openclaw)
- [ClawLink verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes setup, OAuth connection management, live tool discovery, confirmation before writes, and troubleshooting.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
