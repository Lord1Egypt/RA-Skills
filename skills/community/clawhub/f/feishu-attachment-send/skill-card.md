## Description:

Provides a reliable workflow for sending files to Feishu users by staging attachments in allowed paths and sending explanatory text separately from media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujunyanyanya](https://clawhub.ai/user/yujunyanyanya)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents handling Feishu conversations use this skill to deliver generated or edited files reliably and troubleshoot missing attachments in Feishu DMs or groups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Allowing the whole /tmp directory as a Feishu attachment source could expose unintended local files.

Mitigation: Use a dedicated, access-controlled staging directory under the OpenClaw workspace and avoid adding system-wide /tmp to mediaLocalRoots unless the disclosure risk is explicitly accepted.

Risk: Combining explanatory text and an attachment in one Feishu outbound message can make the attachment unreliable for recipients.

Mitigation: Send a short text message first when needed, then send the attachment as a separate media-only message.

## Reference(s):

- [Feishu file sending notes](references/feishu-file-sending-notes.md)
- [ClawHub skill page](https://clawhub.ai/yujunyanyanya/skills/feishu-attachment-send)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown prose with ordered workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file-path checks, workspace staging guidance, and separate Feishu message-send steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
