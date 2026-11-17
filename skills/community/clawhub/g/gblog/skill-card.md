## Description:

Blogger API CLI for managing blog posts: post, edit, delete, list, search, schedule, and monitor Blogger activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saiteja007-mv](https://clawhub.ai/user/saiteja007-mv)

### License/Terms of Use:

MIT

## Use Case:

Developers, content operators, and external users can use this skill to manage Google Blogger posts through an assistant or command line, including publishing HTML posts, editing content, listing posts, deleting posts, and monitoring blog updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes TechRex-specific scripts that can publish or overwrite Blogger posts and insert promotional content without clear scoping or confirmation.

Mitigation: Prefer the main gblog.py commands with explicit blog and post IDs; review generated HTML, back up existing posts, and avoid update-blogger-full.py or generator scripts unless hard-coded paths and branding are removed or intentionally accepted.

Risk: The skill stores Google OAuth credentials and refresh tokens under the local gblog configuration directory.

Mitigation: Use a limited Blogger account or OAuth client, restrict file permissions on credentials and tokens, and revoke or rotate access if the workspace is shared or compromised.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/saiteja007-mv/skills/gblog)
- [Google Blogger API v3 Reference](https://developers.google.com/blogger/docs/3.0/reference)
- [Google Cloud Console](https://console.cloud.google.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration paths, and HTML content examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cause Blogger API side effects such as creating, editing, deleting, or bulk updating posts when commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
