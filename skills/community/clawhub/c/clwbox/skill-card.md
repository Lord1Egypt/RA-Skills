## Description:

Use the ClawBox CLI to upload, download, organize, search, and share files on ClawBox or a self-hosted ClawBox server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bennyoooo](https://clawhub.ai/user/bennyoooo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage files through the ClawBox CLI, including upload, download, folder organization, semantic search, sharing links, token setup, and storage checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can install CLI code from a local checkout or cloned repository before the user has reviewed the source.

Mitigation: Install only from a pinned or reviewed source, preferably in an isolated environment.

Risk: The skill handles external file uploads, downloads, semantic search, and share links through ClawBox or a self-hosted server.

Mitigation: Avoid uploading sensitive files unless the server, token, quota, and sharing model are understood.

Risk: Share links, drop codes, and bearer tokens can grant access to stored files.

Mitigation: Treat tokens, share links, and drop codes as secrets and revoke sharing links when they are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bennyoooo/skills/clwbox)
- [ClawBox API Reference](artifact/references/api.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [ClawBox Service](https://clawbox.ink)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file IDs, download paths, share links, status summaries, and configuration details returned by the ClawBox CLI.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
