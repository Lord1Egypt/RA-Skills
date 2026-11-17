## Description:

Deliver locally generated office files back into Feishu chats as real attachments with streaming response support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu users use this skill when an agent creates local office files and needs the final Feishu reply to trigger real attachment upload. It guides the agent to save files locally, write a short caption, and list absolute file paths in an upload-friendly format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files listed in the final Feishu reply may be uploaded into the chat, including unintended local content if the path is wrong.

Mitigation: Before sending the final reply, verify that each absolute path exists and points only to the intended output file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wd041216-bit/skills/feishu-file-delivery)
- [Project homepage](https://github.com/wd041216-bit/openclaw-feishu-file-delivery)
- [OpenClaw documentation](https://openclaw.ai)
- [Feishu](https://www.feishu.cn)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown reply text with absolute local file paths on separate lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paths should be absolute, unformatted, one per line, and verified to point to intended output files before sending.]

## Skill Version(s):

2.0.0 (source: server release evidence, artifact _meta.json, artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
