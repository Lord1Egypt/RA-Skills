## Description:

AI指网站改版助手 orchestrates end-to-end enterprise website redesigns, from site audit and strategy through information architecture, design planning, content migration, SEO/GEO, lead generation, preview, and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsqduron](https://clawhub.ai/user/hsqduron)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners, agencies, and developers use this skill to plan and execute redesigns of existing business websites while preserving content, conversion paths, and SEO considerations. It is suited to visual refreshes, information architecture restructuring, old-site content migration, and coordinated launch checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may add or call four third-party dependency skills before operating on a website redesign workflow.

Mitigation: Approve each dependency installation explicitly and prefer exact dependency versions or reviewed copies before use.

Risk: The skill may use website MCP credentials for real site changes.

Mitigation: Confirm the target site returned by MCP before writes and provide the least-privilege token that can complete the redesign.

Risk: Redesign, migration, cache clearing, or publishing actions can change a live site.

Mitigation: Back up target pages when requested, review previews on desktop and mobile, and require explicit approval before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hsqduron/skills/ai-website-gaiban)
- [Redesign templates](artifact/references/redesign-templates.md)
- [Yunzhi trial site](https://www.72e.net/autoweb/edition.aspx)
- [Jianzhan dependency skill](https://skillhub.cn/skills/org-b0bh4w8c/yunzhi-jian-zhan)
- [SEO dependency skill](https://skillhub.cn/skills/org-b0bh4w8c/yunzhi-seo-skill)
- [GEO dependency skill](https://skillhub.cn/skills/org-b0bh4w8c/yun-zhi-geo)
- [Lead generation dependency skill](https://skillhub.cn/skills/org-b0bh4w8c/yun-zhi-website-leadgen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown plans, checklists, reports, and implementation guidance with code or command snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before target-site writes and publishing.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
