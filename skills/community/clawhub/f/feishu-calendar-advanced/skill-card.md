## Description:

Feishu calendar management via feishu-agent. View calendars, list events, create and delete events with conflict detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boyd4y](https://clawhub.ai/user/boyd4y)

### License/Terms of Use:


## Use Case:

Developers and Feishu or Lark workspace users use this skill to manage calendar workflows through feishu-agent: listing calendars and events, creating events with attendees and conflict detection, and deleting events by ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned external CLI that handles Feishu credentials and calendar access.

Mitigation: Install only from a trusted package source, prefer pinned package versions, and avoid exposing real app secrets in shell history.

Risk: The skill can delete calendar events by ID.

Mitigation: Verify event IDs before deletion and review proposed commands before running them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Feishu calendar CLI commands that require OAuth authorization and user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
