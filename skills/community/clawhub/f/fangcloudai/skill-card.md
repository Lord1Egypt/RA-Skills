## Description:

Fangcloud AI integrates with the Fangcloud open platform for file search, upload, download, sharing, collaboration invites, knowledge-base chat, and agent interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiema123](https://clawhub.ai/user/jiema123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Fangcloud files and collaboration workflows from an agent, including finding recent documents, creating share links, uploading or downloading files, organizing folders, and using Fangcloud knowledge-base chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs platform-specific Fangcloud CLI binaries whose release integrity is not pinned in the skill evidence.

Mitigation: Install only after administrator review, require signed or pinned binary verification, and prefer auditable CLI source before deployment.

Risk: The skill can perform broad file, sharing, collection, upload, download, delete, and tenant-wide operations when supplied with privileged tokens.

Mitigation: Use least-privilege user tokens, withhold FANGCLOUD_ADMIN_TOKEN unless admin actions are intentionally needed, and require explicit confirmation before public sharing, collection links, upload/download, delete, or tenant-wide actions.

Risk: Security evidence reports hard-coded bearer tokens in documentation.

Mitigation: Rotate or remove exposed bearer tokens before installation and avoid reusing tokens shown in bundled examples.

## Reference(s):

- [Fangcloud API Endpoint Analysis](references/openapi.md)
- [Fangcloud CLI Release README](cli/release/README.md)
- [Fangcloud Skill Page](https://clawhub.ai/jiema123/skills/fangcloudai)
- [Fangcloud CLI Release Downloads](https://app.fangcloud.com/sync/vv25/knowclaw/release/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke platform-specific Fangcloud CLI binaries and Fangcloud API operations when configured with user or admin tokens.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
