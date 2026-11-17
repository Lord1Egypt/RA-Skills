## Description:

Adapts original Markdown or plain text into platform-specific drafts for Xiaohongshu, WeChat Official Accounts, Zhihu, Weibo, Douyin, Bilibili, and Toutiao, adjusting length, formatting, emoji use, and tone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeliang2000](https://clawhub.ai/user/mikeliang2000)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and social media operators use this skill to turn one source draft into audience-appropriate versions for Chinese social and publishing platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags under-disclosed automatic analytics tied to a user identifier and publishing-platform metadata.

Mitigation: Review analytics behavior before installation, disclose it to users, and remove or disable tracking when user-linked analytics are not acceptable.

Risk: The security review notes that the installer may overwrite an existing content-adapter skill file and install shortened skill text with different publisher metadata.

Mitigation: Inspect the installer before running it, back up any existing skill, and prefer installing from the reviewed skill.md content when manual installation is possible.

Risk: The skill adapts user-provided content for public platforms, which can carry copyright, originality, or platform-policy risk if the source content is not cleared.

Mitigation: Use original or licensed source material and review final drafts against each target platform's rules before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikeliang2000/skills/content-adapter)
- [Publisher homepage](https://hermesai.ltd)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text platform-specific content drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform labels, hashtags, calls to action, formatting suggestions, and image suggestions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
