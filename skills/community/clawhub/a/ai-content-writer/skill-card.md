## Description:

Generates platform-specific Chinese content drafts for channels such as WeChat, Xiaohongshu, Zhihu, LinkedIn, Twitter/X, Weibo, and Douyin, with optional hot-topic search when Tavily is configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft social, professional, and article-style content from a topic, style, tone, keywords, and length options. It is suited to assisted content drafting and should be reviewed before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The topic search path can execute shell commands unsafely when topic text is used to construct a shell command.

Mitigation: Review before installation and ask the publisher to replace shell command construction with argument-array execution and strict topic validation.

Risk: User topics and draft ideas can be sent to Tavily search when TAVILY_API_KEY is configured.

Mitigation: Do not provide confidential topics or unpublished ideas unless external search disclosure is acceptable.

Risk: A user-provided output path can overwrite an existing file.

Mitigation: Choose output destinations deliberately and review generated drafts before publication or downstream use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ryan-wuxl/skills/ai-content-writer)
- [Publisher Profile](https://clawhub.ai/user/ryan-wuxl)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown article printed to stdout or written to a user-provided output file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; TAVILY_API_KEY enables external hot-topic search; supported options include topic, platform style, tone, keywords, length, and output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
