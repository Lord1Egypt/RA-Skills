## Description:

萃书——书籍精华萃取与信息图生成。输入书名，自动获取书籍素材，生成100字简介、3个核心观点、5条行动建议，并生成一张高质量信息图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xishaochen](https://clawhub.ai/user/xishaochen)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to quickly understand a real book by receiving a concise summary, three core ideas, five actionable suggestions, and a generated infographic. It is triggered by requests such as "萃书 + 书名" or requests to summarize, extract, or visualize a book's essence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells the agent to automatically send the generated image through POPO without waiting for confirmation.

Mitigation: Require explicit user confirmation and a visible recipient before any file transfer.

Risk: The security verdict is suspicious because automatic local file-transfer behavior can send generated files to an unintended recipient.

Mitigation: Review before installing and restrict or remove automatic transfer commands unless the deployment environment explicitly permits them.

## Reference(s):

- [萃书 ClawHub skill page](https://clawhub.ai/xishaochen/skills/cuishu)
- [Chinese Text Project](https://ctext.org/)
- [Project Gutenberg ebook search](https://www.gutenberg.org/ebooks/search/)
- [Douban Books](https://book.douban.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown summary with a generated infographic file and an attempted local file-transfer command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text output includes a book introduction, three core viewpoints, five action recommendations, source confidence labeling, and an image generation request for a 1024x1536 infographic.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
