## Description:

博客/公众号文章润色改写专家，可将现有文章进行深度润色改写，在保持核心事实不变的前提下大幅降低文本相似度，同时提升内容吸引力和传播力，并支持链接内容抓取、AI 痕迹消除、HTML 封面设计和事实核实。

This skill is ready for commercial/non-commercial use.

## Publisher:

[javastarboy](https://clawhub.ai/user/javastarboy)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and content operators use this skill to rewrite Chinese blog or public-account articles, reduce textual similarity, remove AI-like phrasing, verify questionable facts, replace promotional copy, generate alternate titles, and create a screenshot-ready HTML cover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private, paywalled, or logged-in URLs may be opened and processed when a user asks the skill to rewrite linked content.

Mitigation: Use only content the user is authorized to process, and avoid private or logged-in URLs unless the user explicitly accepts that processing.

Risk: Rewritten articles may include inaccurate or misleading factual claims if source material is stale, ambiguous, or only partially verified.

Mitigation: Review the final article and any facts marked as unverified before publication.

Risk: Cover generation writes local HTML files that may later be opened or shared outside the workspace.

Mitigation: Inspect generated HTML files before opening, publishing, or distributing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/javastarboy/skills/blog-rewriter)
- [AI 痕迹识别与优化指南](artifact/references/ai-detection-patterns.md)
- [HTML 封面设计模板](artifact/references/html-cover-templates.md)
- [文章改写操作指南](artifact/references/rewriting-guidelines.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown article rewrite with title suggestions, a rewrite report, and HTML cover code or a local HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local 1200x900 HTML cover file in the workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
