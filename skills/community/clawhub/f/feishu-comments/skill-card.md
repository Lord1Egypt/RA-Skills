## Description:

Read comments from Feishu documents for document review and collaboration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadblue22](https://clawhub.ai/user/deadblue22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document collaborators use this skill to fetch Feishu/Lark document comments, quoted text, replies, and comment status during document review cycles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that the skill is advertised as read-only while bundled scripts can close comments.

Mitigation: Use read-only Feishu/Lark credentials for comment-reading workflows and run the resolver script only when comment closure is intended.

Risk: The release evidence reports unsafe Python interpolation that could execute code from document content.

Mitigation: Fix the unsafe interpolation before using the skill on documents editable by untrusted collaborators.

Risk: The skill reads Feishu/Lark app credentials from local OpenClaw configuration.

Mitigation: Grant only the minimum Feishu/Lark permissions required for the planned workflow and avoid comment-write permission for read-only use.

## Reference(s):

- [Feishu Open API](https://open.feishu.cn)
- [Lark Open API](https://open.larksuite.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text terminal output with optional Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Comment output may include comment IDs, status, scope, quoted text, replies, user IDs, and active/orphaned/resolved summary counts.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
