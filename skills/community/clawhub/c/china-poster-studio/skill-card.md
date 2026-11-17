## Description:

社交海报生成器。一键将文字/文章生成精美海报，支持朋友圈、小红书、抖音等平台。粘贴内容即可生成，无需设计技能。适合运营人员、自媒体、普通用户。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, social media operators, creators, and general users use this skill to turn pasted Chinese text, article content, short prompts, or public article URLs into social poster content for WeChat Moments, Xiaohongshu, Douyin, and similar channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted text may be summarized or transformed into poster content.

Mitigation: Avoid providing private or sensitive material unless it is intended to appear in, or be summarized for, the generated poster.

Risk: Optional URL mode asks the agent to fetch and process user-provided article URLs, which may fail or expose untrusted page content to the workflow.

Mitigation: Use URL mode only with public pages the user trusts, and review extracted content before publishing the poster.

Risk: Local poster generation depends on Pillow and Chinese font assets when the agent implements image output.

Mitigation: Confirm required local dependencies and font files are available before expecting PNG output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/china-poster-studio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown or text guidance with optional Python/Pillow implementation details and PNG poster output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports square, 3:4, and 9:16 poster layouts; local image generation may require Pillow and Chinese font assets.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
