## Description: <br>
中文技术博客写作助手。基于 blog-writer 方法论，产出高质量、有个人风格的技术文章。不需要外部依赖，专注于内容创作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liusaikang](https://clawhub.ai/user/liusaikang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and content creators use this skill to draft conversational Chinese technical blog posts, tutorials, troubleshooting notes, opinion pieces, comparisons, and news summaries. It guides the agent through topic intake, style calibration, drafting, user review, revision, and optional Markdown finalization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated articles may contain incorrect technical claims or misleading summaries, especially when based on user-provided links or rapidly changing topics. <br>
Mitigation: Review generated articles before publishing and verify technical claims, cited sources, code snippets, and news links. <br>
Risk: The skill can save a finalized Markdown article when the user confirms, so output may be written to an unintended path. <br>
Mitigation: Choose the save location intentionally and confirm the final filename before writing the article. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liusaikang/blog-generation) <br>
- [Chinese technical blog writing style guide](artifact/style-guide-cn.md) <br>
- [Example article: ReAct vs Plan-and-Execute](artifact/examples/2025-04-07-react-vs-plan-execute.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown drafts, revision guidance, and optional final article files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final drafts may include frontmatter, titles, tags, categories, code blocks, and source links when the article type calls for them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter declares 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
