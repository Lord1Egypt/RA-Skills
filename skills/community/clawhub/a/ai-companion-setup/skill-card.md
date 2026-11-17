## Description:

Guides developers through setting up an OpenClaw AI companion agent with memory, Feishu text messaging, voice messages, generated selfies, and scheduled heartbeats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evan966890](https://clawhub.ai/user/evan966890)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to configure an OpenClaw companion workflow that keeps memory, rotates scheduled interactions, and sends Feishu text, voice, and image messages through local scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sets up autonomous scheduled outbound companion messages to Feishu contacts.

Mitigation: Require explicit recipient opt-in, disclose automation to recipients, and keep scheduled message frequency and quiet hours configurable.

Risk: The companion design uses persistent memory about the recipient.

Mitigation: Define where memory is stored, who can view it, and how the recipient can review or delete stored notes.

Risk: The workflow uses broad shell access and credentials for fal.ai and Feishu APIs.

Mitigation: Scope credentials to the minimum required permissions, store them in a secret mechanism, and narrow allowed tools before deployment.

Risk: The security summary notes instructions that hide automation context.

Mitigation: Remove or revise instructions that conceal automation and make the companion's automated nature clear to users and recipients.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evan966890/skills/ai-companion-setup)
- [fal.ai Grok Imagine image edit endpoint](https://fal.run/xai/grok-imagine-image/edit)
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload endpoint](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message send endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw and Feishu setup, command-line dependencies, and FAL_KEY for fal.ai image or paid TTS flows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
