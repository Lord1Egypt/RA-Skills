## Description:

Enables an agent to collaborate in Feishu or Lark documents by reacting to document edit events, reading structured in-document messages, and appending replies inline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongweiii](https://clawhub.ai/user/dongweiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using Feishu or Lark use this skill to turn shared documents into structured human-agent collaboration spaces. It supports in-document chat routing, status-based response control, and optional Bitable task board workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill patches trusted OpenClaw monitor code, which can be fragile across OpenClaw or extension updates.

Mitigation: Review the patch before installation, keep backups of modified monitor files, reapply after updates, and prefer a supported extension mechanism when available.

Risk: Shared Feishu document edits can trigger authenticated agent actions and document or Bitable writes.

Mitigation: Limit deployment to approved documents and bases, use the narrowest OAuth scopes available, avoid exposing unrelated tools to hook-triggered sessions, and add audit logging and approval gates for writes.

Risk: Frequent autosave and Bitable change events can trigger duplicate agent sessions and excessive token use.

Mitigation: Keep the per-file debounce enabled, monitor gateway logs for repeated triggers, and scope event subscriptions to the collaboration workflows that need automation.

## Reference(s):

- [Feishu Doc Chat Protocol Template](artifact/assets/DOC_PROTOCOL_TEMPLATE.md)
- [Bitable Task Board Protocol](artifact/references/bitable-task-protocol.md)
- [Feishu App Setup Guide](artifact/references/feishu-app-setup.md)
- [Manual Patching Guide](artifact/references/manual-patch.md)
- [Feishu Open Platform](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and protocol templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a patch script, a patched monitor reference file, Feishu setup guidance, and document/task protocol templates.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
