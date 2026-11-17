## Description:

Feishu Notes Bot helps agents create, search, and manage notes through Feishu chat interactions and Feishu cloud document sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilinkzwq](https://clawhub.ai/user/ilinkzwq)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to configure an agent workflow that captures meeting notes, quick notes, action items, and project updates from Feishu chats, then stores them locally or in Feishu cloud documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can store meeting notes, attendee names, action items, and project details in Feishu cloud documents.

Mitigation: Confirm organizational approval for Feishu cloud storage before use and review document permissions so notes are shared only with intended users.

Risk: The skill requires a Feishu app secret for API access.

Mitigation: Keep FEISHU_APP_SECRET private, avoid committing it to files, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ilinkzwq/skills/feishu-notes-bot)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu API Documentation](https://open.feishu.cn/document/)
- [Example Feishu Configuration](artifact/config/feishu_example.json)
- [Meeting Note Template](artifact/templates/meeting.md)
- [Quick Note Template](artifact/templates/quick.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl plus FEISHU_APP_ID and FEISHU_APP_SECRET for Feishu API access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
