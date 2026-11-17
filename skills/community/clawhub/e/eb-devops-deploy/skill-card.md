## Description:

Deploy applications and set up infrastructure for solo founders using practical guidance for CI/CD, Docker, hosting, domains, SSL, monitoring, backups, and rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emersonbraun](https://clawhub.ai/user/emersonbraun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and solo founders use this skill to choose deployment platforms, define Docker and CI/CD setup, manage environment variables, configure domains and SSL, and plan monitoring, backups, and rollback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment examples include commands that can run unverified remote installers or unpinned global CLI installs.

Mitigation: Review commands before execution, prefer verified installers, and pin CLI versions where practical.

Risk: Backup deletion and database restore examples can remove data or affect the wrong environment if copied without checks.

Mitigation: Use dry-run deletion, private temporary files, explicit non-production restore targets, and confirmation before destructive operations.

## Reference(s):

- [Deployment Guides Reference](artifact/references/deployment-guides.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment commands and configuration examples that require user review before execution.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
