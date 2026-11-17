## Description:

Browse, search, upload, download, and manage files and folders in Dropbox, powered by ClawLink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an OpenClaw agent to Dropbox through ClawLink so the agent can browse, search, read, upload, share, and manage Dropbox files and folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party ClawLink integration that routes Dropbox credentials and actions.

Mitigation: Review ClawLink's publisher, privacy terms, token storage, and revocation controls before installation.

Risk: Dropbox actions can modify access, create public links, upload files, remove collaborators, delete contacts, or permanently delete files and folders.

Mitigation: Require explicit user confirmation before uploads, sharing changes, member removals, contact deletion, public link creation, and delete operations.

Risk: Broad Dropbox access can expose sensitive folders and files.

Mitigation: Use the narrowest Dropbox permissions available and avoid highly sensitive folders unless approved by the organization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hith3sh/skills/dropbox-files)
- [Publisher profile](https://clawhub.ai/user/hith3sh)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=dropbox-files)
- [ClawLink Dropbox connection](https://claw-link.dev/dashboard?add=dropbox)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Code]

**Output Format:** [Markdown with inline shell commands and JavaScript API-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill routes Dropbox operations through ClawLink and includes safe, confirmation-required, and high-impact Dropbox actions.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
