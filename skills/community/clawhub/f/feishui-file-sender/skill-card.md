## Description:

Send files via Feishu channel using message tool with filePath parameter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephyb97](https://clawhub.ai/user/josephyb97)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to package local files or skill folders and send them to Feishu groups or users through an OpenClaw Feishu channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send local files through Feishu, which could disclose secrets, credentials, private workspace data, or proprietary content if the wrong file or chat ID is used.

Mitigation: Before sending, verify the target chat ID and confirm the selected file is intended for that Feishu recipient and contains no sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephyb97/skills/feishui-file-sender)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides Feishu message parameters including action, channel, filePath, message, and target.]

## Skill Version(s):

1.0.0 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
