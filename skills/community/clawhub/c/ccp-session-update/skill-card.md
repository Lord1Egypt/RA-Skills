## Description:

Context Continuity Protocol session update: the ops sequence Liv runs at the end of every significant session to update STATUS.md, post to Notion, sync an Obsidian vault, and create Plane issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to close significant work sessions by preserving project state across STATUS.md, Notion, Obsidian, and Plane so future agents can resume with minimal context loss.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can persist project summaries to local files, cloud services, and synced notes.

Mitigation: Review session content before sync and redact sensitive material from STATUS.md, Notion, and Obsidian outputs.

Risk: The workflow depends on access to a Notion credential and may interact with a password manager.

Mitigation: Use a narrowly scoped injected secret where possible and avoid exposing broad password-manager access to untrusted agents.

Risk: The workflow uses Docker access to mutate Plane issue data.

Mitigation: Run it only in trusted environments and prefer a supported Plane API or narrowly scoped helper for issue updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/ccp-session-update)
- [Publisher profile](https://clawhub.ai/user/nissan)
- [Notion pages API endpoint](https://api.notion.com/v1/pages)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker and NOTION_API_KEY; may write local files and call network services when executed by an agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
