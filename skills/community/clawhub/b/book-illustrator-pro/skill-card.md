## Description:

Book Illustrator Pro helps publishing teams manage book illustration workflows, including batch requirement planning, style libraries, illustrator collaboration, progress boards, review automation, and asset archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External publishers, illustration studios, editors, art directors, project coordinators, and rights teams use this skill to plan, assign, track, review, archive, and report on book illustration work. It supports operational coordination and traceability rather than replacing human creative judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If connected to a real CLI, the skill could perform broad file and command operations across project directories.

Mitigation: Use a dedicated workspace, verify the CLI source separately, and avoid broad project directories until file access is scoped.

Risk: Local databases and illustration asset or style libraries could retain sensitive project, rights, or creative materials.

Mitigation: Confirm storage paths, limit sensitive data, and apply appropriate local access controls and retention practices.

Risk: Callback URLs, email notifications, remote mode, or publishing-system API synchronization could send project data outside the local environment.

Mitigation: Enable integrations only after confirming endpoints, data flows, HTTPS use, credential handling, and approval from the relevant project owner.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/book-illustrator-pro)
- [Detailed Reference](artifact/references/detail.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include status, result data, execution logs, and error fields; the artifact itself does not include executable code.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
