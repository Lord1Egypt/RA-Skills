## Description:

Guide for setting up an OpenClaw AI companion agent with memory that can send Feishu text messages, voice messages, selfies, and shared content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evan966890](https://clawhub.ai/user/evan966890)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill as a practical setup guide for creating an OpenClaw companion agent that maintains memories, runs scheduled heartbeats, and sends Feishu messages, voice, and generated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes an autonomous scheduled companion that can repeatedly send messages and generated media.

Mitigation: Require recipient opt-in, clearly disclose automation and AI-generated media, and add stop commands, quotas, or expiration for scheduled jobs before deployment.

Risk: The setup uses broad local authority, shell commands, and service credentials.

Mitigation: Restrict Bash and credential access, store secrets safely, and review generated scripts before use.

Risk: The companion pattern can involve personal memories or likeness-like generated images.

Mitigation: Avoid sensitive memories and personal likenesses unless everyone involved has clearly consented.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/evan966890/skills/clawgirl)
- [ClawHub Publisher Profile](https://clawhub.ai/user/evan966890)
- [fal.ai Grok Imagine Image Edit Endpoint](https://fal.run/xai/grok-imagine-image/edit)
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu File Upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu Message Send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and setup checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu messaging, scheduled OpenClaw heartbeats, memory files, voice generation, and generated image setup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
