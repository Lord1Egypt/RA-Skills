## Description:

多平台内容分发器 v1.0。一次输入，自动适配小红书/知乎/公众号/抖音四种平台格式，直接输出可发布内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyjaixiao](https://clawhub.ai/user/hyjaixiao)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and marketing teams use this skill to turn one Chinese content topic and optional talking points into platform-specific drafts for Xiaohongshu, Zhihu, WeChat public accounts, and Douyin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forwards user topics, talking points, prompts, and the configured bearer token to the selected OpenAI-compatible API endpoint.

Mitigation: Use the default trusted OpenAI endpoint or a third-party endpoint you independently trust, and prefer a separate scoped API key with spending limits.

Risk: Generated social content can contain unsupported claims or platform-inappropriate messaging.

Mitigation: Review, fact-check, and edit generated drafts before publishing them externally.

Risk: Generated markdown files may store sensitive campaign drafts or personal topics locally.

Mitigation: Choose an appropriate output directory and apply normal local access controls or cleanup practices for sensitive drafts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hyjaixiao/skills/content-producer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown files with YAML front matter, plus command-line status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate one selected platform or all configured platforms; stores dated output files locally.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
