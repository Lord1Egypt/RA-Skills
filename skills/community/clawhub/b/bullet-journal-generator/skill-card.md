## Description:

Converts free-form natural-language notes into structured bullet journal entries, Obsidian daily logs, visual HTML cards, printable views, and JSON data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirutong](https://clawhub.ai/user/sirutong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal-productivity teams can use this skill to transform daily plans, work notes, and observations into standardized bullet journal records and Obsidian-ready logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill saves personal or work notes into persistent local files, generated HTML, JSON data, and backups.

Mitigation: Use it only with note content appropriate for local persistence, and review generated files and backup locations before sharing or syncing them.

Risk: Security evidence reports unsafe rendering and weak file-path controls around generated note content.

Mitigation: Avoid untrusted note text until HTML escaping and path constraints are reviewed and fixed.

Risk: Security evidence describes the interactive local-server workflow as incomplete.

Mitigation: Treat interactive task-status features as optional and review or constrain the local server before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sirutong/skills/bullet-journal-generator)
- [Publisher profile](https://clawhub.ai/user/sirutong)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, JSON, files]

**Output Format:** [Plain text, Markdown, HTML, printable HTML/PDF, and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dated journal content, Obsidian logs, generated cards, printable views, structured data, and backups to local disk.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
