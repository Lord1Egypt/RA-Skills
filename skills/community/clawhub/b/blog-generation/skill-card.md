## Description:

中文技术博客写作助手，基于 blog-writer 方法论，产出高质量、有个人风格的技术文章。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liusaikang](https://clawhub.ai/user/liusaikang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and external ClawHub users use this skill to draft conversational Chinese technical blog posts, including tutorials, incident writeups, opinion pieces, comparisons, and news summaries. The skill helps collect topic details, apply a Chinese writing style guide, draft Markdown, iterate on feedback, and optionally save a final article.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafted technical or news content may contain factual errors, outdated claims, or incorrect links.

Mitigation: Review facts, code, and original news links before approving or publishing the article.

Risk: Generated code examples may be incomplete or unsuitable for the reader's environment.

Mitigation: Test code snippets and adjust prerequisites, versions, and commands before publication.

Risk: The skill may save a final Markdown article to an unintended path after user approval.

Mitigation: Confirm the target filename and save location before allowing the final write.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liusaikang/skills/blog-generation)
- [Chinese technical blog writing style guide](artifact/style-guide-cn.md)
- [Example article: ReAct vs Plan-and-Execute](artifact/examples/2025-04-07-react-vs-plan-execute.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance, Files]

**Output Format:** [Markdown prose with optional code blocks and article frontmatter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include iterative draft revisions and an optional final Markdown file when the user approves saving.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
