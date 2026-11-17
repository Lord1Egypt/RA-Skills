## Description:

Sends inline emoji images in Feishu chats by downloading selected images to OpenClaw media storage and preparing a message-tool send call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dearchenzj](https://clawhub.ai/user/dearchenzj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and Feishu/OpenClaw agent operators use this skill to find, download, and send emoji images as inline chat media for informal Feishu conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts fabiaoqing.com and related image CDNs to retrieve media.

Mitigation: Use it only for explicit user requests and restrict allowed image hosts before deployment.

Risk: Downloaded third-party media is saved into OpenClaw media storage and can be sent into Feishu chats.

Mitigation: Validate media type and size, sanitize filenames, and review image content before sending.

Risk: The helper script prints a message-tool call containing user-provided text and local media paths.

Mitigation: Treat printed tool-call text as guidance to review rather than text to execute automatically.

Risk: The artifact warns that internet-sourced emoji may not be suitable for commercial use.

Mitigation: Confirm rights for any selected emoji before business or public-channel use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dearchenzj/skills/feishu-emoji)
- [fabiaoqing.com emoji source](https://fabiaoqing.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash commands, Python usage examples, and message-tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local media paths, Feishu message text, and third-party image URLs.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
