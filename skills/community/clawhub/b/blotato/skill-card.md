## Description:

Helps agents publish, schedule, and manage social media content and interactions through Blotato.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blotato](https://clawhub.ai/user/blotato)

### License/Terms of Use:

MIT-0

## Use Case:

Social media teams and creators use this skill to draft and publish platform-specific posts, manage schedules, review analytics, respond to messages, and configure DM automations for connected accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Immediate publishing or outward-facing replies can make unreviewed content public.

Mitigation: Review platform-specific drafts and confirm with the user before publishing or sending messages.

Risk: Connected accounts and active automations can post or send DMs on the user's behalf.

Mitigation: Treat OAuth connections and API keys as sensitive; confirm the intended account and obtain approval before activating automations.

Risk: Deleting scheduled content or automations can be difficult to undo.

Mitigation: Show the item to the user and obtain explicit confirmation before deletion.

## Reference(s):

- [Blotato skill release](https://clawhub.ai/blotato/skills/blotato)
- [Blotato MCP setup](https://help.blotato.com/api/mcp/setup)
- [Blotato MCP tools](https://help.blotato.com/api/mcp/tools)
- [Blotato media publishing guide](https://help.blotato.com/api/publish-post/media)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions and platform-specific post drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authorized posting, scheduling, messaging, and account management through Blotato.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
