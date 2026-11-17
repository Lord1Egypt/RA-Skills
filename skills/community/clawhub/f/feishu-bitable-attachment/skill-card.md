## Description:

Uploads files from local paths, URLs, or Feishu messages to Feishu Bitable attachment fields using the Bitable material upload flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyjbazinga-stack](https://clawhub.ai/user/gyjbazinga-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to attach files to Feishu or Lark Bitable records without hardcoding a table, field, or record. It supports updating existing records, lookup-based targeting, and new record creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged Feishu credentials can write to any Bitable available to the app.

Mitigation: Use a least-privilege Feishu app limited to the intended Bitables and review the target app, table, field, and record before execution.

Risk: The configurable Feishu base URL and URL source mode can send requests or download content from unintended locations.

Mitigation: Pin FEISHU_BASE_URL to official Feishu or Lark origins and avoid untrusted URL sources.

Risk: Local copies, downloaded files, logs, and temporary paths may contain sensitive attachment data.

Mitigation: Treat logs and temporary directories as sensitive and avoid caller-supplied filenames when handling untrusted inputs.

Risk: Replace mode can overwrite existing Bitable attachment field contents.

Mitigation: Use replace mode only when overwriting existing attachments is intended; otherwise keep append mode enabled.

## Reference(s):

- [Feishu API Implementation Notes](artifact/references/feishu-api-notes.md)
- [Feishu Open Platform](https://open.feishu.cn)
- [ClawHub Skill Page](https://clawhub.ai/gyjbazinga-stack/skills/feishu-bitable-attachment)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON status output with concise success or error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials and a JSON input file describing source file, Bitable target, and append or replace behavior.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
