## Description:

把对话转文章和贴图——把当前会话里用户与智能体的真实交互过程，整理成可直接发布的自媒体总结文章（.md）或竖版分享贴图（.png/.jpg）。当用户说"总结本次对话""总结会话""转成文章""生成贴图""生成分享卡片"时使用。要求会话已有可读取的历史对话记录，否则不启动并说明原因。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weikion](https://clawhub.ai/user/weikion)

### License/Terms of Use:

MIT-0

## Use Case:

People who want to turn a completed human–agent conversation into publishable content can use this skill to create a structured Markdown article, vertical share cards, or both. It requires accessible conversation history and bases the content on that record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A fallback session selection could include another project's conversation in the generated content.

Mitigation: Check that the selected session is the intended conversation, then review the article and cards and remove private details before sharing.

Risk: Transcript files may be written when record checks fail.

Mitigation: Confirm the record checks pass and inspect generated local files for sensitive content before sharing.

## Reference(s):

- [Chat-to-Content on ClawHub](https://clawhub.ai/weikion/skills/chat-to-content)
- [Article writing guide](artifact/references/article.md)
- [Share card layout guide](artifact/references/cards.md)
- [Conversation extraction guide](artifact/references/extraction.md)

## Skill Output:

**Output Type(s):** [Markdown, Image files, Guidance]

**Output Format:** [Markdown article (.md) and vertical share cards (.png or .jpg)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an article, share cards, or both from an accessible conversation record.]

## Skill Version(s):

0.1.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
