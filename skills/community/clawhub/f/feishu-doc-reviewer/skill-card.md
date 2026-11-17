## Description:

Provides Feishu document read-write tools for agents to export Markdown, inspect comments and paragraphs, write updates, reply to comments, and mark comments complete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jachian-lee](https://clawhub.ai/user/jachian-lee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to let an assistant review Feishu document comments, read the relevant text, draft edits, update document blocks, and reply or resolve comments after changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit, delete, reply to, and resolve live Feishu document content.

Mitigation: Use a test document first, restrict the Feishu app to intended documents, and require human review before any update, deletion, reply, or resolve action.

Risk: The CLI wrapper is identified by security evidence as unsafe for crafted input.

Mitigation: Avoid run-tool.sh until it is fixed; prefer reviewed MCP configuration or direct audited commands with controlled arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jachian-lee/skills/feishu-doc-reviewer)
- [Feishu Open Platform API base](https://open.feishu.cn/open-apis)
- [Feishu Open Platform app console](https://open.feishu.cn/app/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON tool responses, shell commands, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform authenticated Feishu API reads and writes when configured with app credentials and document access.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
