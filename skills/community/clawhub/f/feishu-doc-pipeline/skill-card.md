## Description:

Complete pipeline for reading Feishu wiki documents and downloading embedded attachments with authorization guidance, node-type routing, and Windows path handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kooui](https://clawhub.ai/user/kooui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill when a user provides a Feishu/Lark wiki URL or token and needs to resolve the node, read document content, extract embedded file or image tokens, and download files locally with the correct lark-cli command path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to authorize persistent Feishu/Lark document read and file download scopes beyond what every task requires.

Mitigation: Authorize scopes only when the specific task needs them, download into a dedicated folder, and review how to revoke Feishu/Lark authorization after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kooui/skills/feishu-doc-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command decision paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require separate Feishu/Lark authorization flows and local file downloads.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
