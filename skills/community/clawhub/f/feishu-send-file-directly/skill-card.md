## Description:

飞书消息直接发送文件附件技能。当用户需要直接通过飞书消息发送文件附件（而不是文档链接）时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gongjieliu](https://clawhub.ai/user/gongjieliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send local files as direct Feishu message attachments, including single files, batches, and files with custom display names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent may send local files externally through Feishu without sufficient review of recipients, paths, or file contents.

Mitigation: Before use, verify the recipient or channel, the exact file paths, and the contents of every file or archive being sent.

Risk: Batch sends or compressed archives may include sensitive, confidential, personal, or unauthorized material.

Mitigation: Inspect batch file lists and archive contents before sending, and use the skill only where Feishu file sending is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gongjieliu/skills/feishu-send-file-directly)
- [OpenClaw message tool documentation](https://docs.openclaw.ai/tools/message)
- [OpenClaw write tool documentation](https://docs.openclaw.ai/tools/write)
- [OpenClaw workspace management](https://docs.openclaw.ai/guides/workspace)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with JavaScript-style tool call examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on Feishu message sends that use local file paths, optional display filenames, and pre-send file checks.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata, released 2026-04-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
