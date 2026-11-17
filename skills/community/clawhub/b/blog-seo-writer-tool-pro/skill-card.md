## Description:

企业级 SEO 内容营销辅助工具，支持竞品分析、长尾关键词矩阵、多语言生成、批量操作及团队协作自动化发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External content marketers, bloggers, and enterprise teams use this skill to plan and draft SEO-focused blog and product-page content, including keyword clusters, meta descriptions, FAQ sections, Schema.org suggestions, and CMS publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad command, file, API, webhook, and CMS publishing authority for a writing workflow.

Mitigation: Run it in a restricted workspace, require confirmation before file writes or publishing actions, and grant only the integrations needed for the current task.

Risk: Credential handling and environment inspection examples may expose sensitive API key or token names in agent context.

Mitigation: Avoid production credentials, prefer scoped test credentials, and keep secret values out of prompts, logs, drafts, and generated configuration.

Risk: Generated SEO drafts, schema suggestions, and CMS publishing steps may be inaccurate, off-brand, or unsuitable for external release.

Mitigation: Review generated content, metadata, structured data, and publishing actions before using them on public sites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/blog-seo-writer-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON examples, and inline shell or code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated SEO article drafts, keyword matrices, metadata, execution logs, and publishing configuration examples.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
