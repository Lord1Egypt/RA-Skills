## Description:

Manages Fizzy boards, cards, steps, comments, and reactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[portavion](https://clawhub.ai/user/portavion)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect and manage Fizzy boards, cards, tasks, comments, reactions, users, tags, notifications, uploads, and workflow state through the Fizzy CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party Fizzy CLI.

Mitigation: Install only from a trusted Fizzy CLI source and verify the package before use.

Risk: The skill can modify or delete project data, including boards, cards, columns, comments, steps, reactions, notifications, and uploads.

Mitigation: Require explicit confirmation before delete, close, bulk read-all, upload, or update actions.

Risk: Broad Fizzy API credentials may expose more data or write access than a task requires.

Mitigation: Use the narrowest token permissions available and avoid storing tokens in world-readable files or logs.

## Reference(s):

- [Fizzy ClawHub Skill Listing](https://clawhub.ai/portavion/skills/fizzy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, jq patterns, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include command guidance for reading, creating, updating, uploading, closing, or deleting Fizzy resources.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
