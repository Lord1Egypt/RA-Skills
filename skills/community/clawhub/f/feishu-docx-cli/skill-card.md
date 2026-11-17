## Description:

Feishu Docx Cli helps agents manage Feishu documents from the command line, including creating, reading, overwriting, appending Markdown content, uploading images, and managing collaborator permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songofhawk](https://clawhub.ai/user/songofhawk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to operate Feishu document workflows from CLI scripts, including document creation, Markdown content updates, image insertion, and collaborator access changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The write workflow can overwrite existing Feishu document content.

Mitigation: Use overwrite commands only on documents intended for automation, and confirm the target document token before running them.

Risk: Permission commands can add, remove, or broaden collaborator access on shared or business-critical documents.

Mitigation: Double-check member IDs, permission levels, and document tokens before changing access.

Risk: The skill depends on Feishu app credentials with document, upload, and permission scopes.

Mitigation: Use a Feishu app and account dedicated to document automation, with only the permissions needed for the intended workflow.

## Reference(s):

- [Feishu Open Platform Documentation](https://open.feishu.cn/document/)
- [Feishu Open Platform](https://open.feishu.cn/)
- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [ClawHub skill page](https://clawhub.ai/songofhawk/skills/feishu-docx-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and command output such as document URLs, status messages, tables, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials configured through OpenClaw and valid document tokens, folder tokens, image paths, and member IDs for the selected operation.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
