## Description:

Duanshipinjiexi helps an agent parse supported Douyin, Kuaishou, Xiaohongshu, and Pipixia links, retrieve watermark-free media where available, manage identity-code usage, and guide status or payment flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kangleizhui](https://clawhub.ai/user/kangleizhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to process shared short-video links from supported Chinese content platforms, return downloadable media or fallback links, and track remaining quota tied to an identity code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic fallback can send user video links and identity codes to an unverified replacement service.

Mitigation: Disable fallback or require administrator approval before switching endpoints; use the skill only with links and identity codes acceptable for third-party processing.

Risk: The identity code may be saved and reused for quota and purchases.

Mitigation: Treat the identity code like an account token and avoid exposing it in shared logs, public chats, or unrelated workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kangleizhui/skills/duanshipinjiexi)
- [API Docs](artifact/references/api-docs.md)
- [Field Map](artifact/references/field-map.md)
- [Key Rules](artifact/references/key-rules.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [URL Fallback](artifact/references/url-fallback.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with command snippets, media links, status details, and user-facing guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include direct media URLs, remaining quota information, payment-status guidance, and fallback instructions.]

## Skill Version(s):

1.7.6 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
