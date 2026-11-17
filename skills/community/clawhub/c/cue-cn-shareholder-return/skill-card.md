## Description:

将 A 股分红、回购、减持和质押公告整理成八项带原文引用与出处锚点的逐字卡，并列明缺失项；判断留给人工。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

供分析 A 股公告的用户使用，将分红、回购、减持及质押披露整理为八项可回查的原文记录，并标出缺失信息；不提供投资判断或代办服务。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The channel parsing workflow may send user-provided URLs or paths to an external service, and ClawScan reports unrelated external catalog requests; the scan evidence is partial.

Mitigation: Before using the channel path, confirm the endpoint and service are trusted. Avoid private links, credential-bearing URLs, or local paths until data handling is clear, and review the missing referenced path when assessing the partial scan.

## Reference(s):

- [股东回报条目页面](https://clawhub.ai/huhoo/skills/cue-cn-shareholder-return)
- [股东回报名词与项目定义](references/sh-return-terms.md)
- [Cue MCP 服务目录](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured note with eight verbatim items, source anchors, and a missing-data list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records filing language and sources; investment judgments remain with a human.]

## Skill Version(s):

0.1.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
