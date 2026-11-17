## Description:

博客写作助手专业版 helps independent developers, enterprise teams, and automated workflows create marketing copy, blog content, optimized titles, and content-production workflows with brand voice, review, publishing, and SEO/readability support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and enterprise content teams use this skill to draft and optimize marketing copy, blog posts, titles, and content workflows. It supports brand voice management, collaborative review, content governance, publishing pipeline planning, batch operation examples, and SEO/readability scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad command, file, credential, API, and publishing authority.

Mitigation: Keep credentials narrowly scoped, avoid broad workspace access, and require explicit review before any publish, webhook, batch, or command-execution step.

Risk: Generated writing, SEO recommendations, or publishing guidance may be inaccurate, misleading, or unsuitable for the target brand.

Mitigation: Review drafts and workflow recommendations before publication, especially for factual claims, legal-sensitive content, and brand voice requirements.

Risk: File reads, file edits, shell commands, and environment inspection can expose sensitive data if used without constraints.

Mitigation: Limit the agent to the smallest necessary workspace, redact secrets from logs, and require user approval before inspecting credentials or modifying files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/blog-writer-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code, shell command examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce article drafts, review workflow guidance, configuration values, batch-processing examples, and publishing steps for an agent to execute after user review.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
