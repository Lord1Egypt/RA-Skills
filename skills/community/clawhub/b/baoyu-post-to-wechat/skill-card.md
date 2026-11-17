## Description:

Posts content to WeChat Official Account via API or Chrome CDP, supporting article posting from HTML, Markdown, or plain text and image-text posting with multiple images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to prepare and publish WeChat Official Account drafts from Markdown, HTML, plain text, or image collections. It supports local browser publishing, direct WeChat API publishing, remote API publishing through an allowlisted server, and multi-account configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat login sessions and AppSecrets during publishing workflows.

Mitigation: Install only when the publisher is trusted, keep AppSecrets in a protected secret store or locked-down local file, and avoid enabling Telegram QR forwarding unless the bot and chat are fully controlled.

Risk: Untrusted Markdown or image URLs could affect the content prepared for publication.

Mitigation: Review article inputs and image sources before publishing, and process only content from trusted sources.

Risk: Remote API publishing depends on SSH tunneling through a server whose IP is allowlisted by WeChat.

Mitigation: Use key-only SSH access, verify the remote host configuration, and confirm the allowlisted server is controlled by the operator.

Risk: Runtime installation through npx can execute a freshly resolved Bun runtime.

Mitigation: Prefer a preinstalled trusted Bun runtime over invoking npx to fetch Bun at execution time.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimliu/skills/baoyu-post-to-wechat)
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat)
- [API credential setup](references/api-setup.md)
- [Article posting](references/article-posting.md)
- [Image-text posting](references/image-text-posting.md)
- [Multi-account support](references/multi-account.md)
- [First-time setup](references/config/first-time-setup.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Text, Files]

**Output Format:** [Markdown guidance with inline shell commands and status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown drafts and preference files, and may trigger browser or WeChat API publishing workflows when the agent executes the skill.]

## Skill Version(s):

1.118.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
