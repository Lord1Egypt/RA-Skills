## Description:

A website SEO audit and optimization assistant that crawls or analyzes site HTML, scores SEO health across key dimensions, and produces risk-graded recommendations for review and implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsqduron](https://clawhub.ai/user/hsqduron)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and site operators use this skill to audit public websites they own or are authorized to assess, generate SEO scores, and plan or apply reviewed SEO improvements. It supports generic website audits and CMS-oriented workflows when the user provides appropriate access credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can crawl arbitrary URLs and may follow redirects or links from the execution network.

Mitigation: Use it only on public sites the user owns or is authorized to audit, and avoid networks that can reach sensitive internal services until URL validation and redirect controls are confirmed.

Risk: CMS Bearer tokens can enable site changes.

Mitigation: Request tokens only when the user intends write operations, never echo or store them, and require explicit review of each proposed write before execution.

Risk: Some CMS guidance discusses bypassing normal write controls when host validation blocks an operation.

Mitigation: Prefer documented SEO MCP tools, keep changes minimal and SEO-scoped, preserve pre-change snapshots, and proceed only with clear site-operator approval.

Risk: SEO recommendations can affect site visibility, ranking, or page semantics.

Mitigation: Treat generated changes as proposals, separate low-risk metadata updates from high-risk structural changes, and require confirmation before high-risk edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hsqduron/skills/ai-seo-assistant)
- [SEO metrics reference](references/seo-metrics.md)
- [SEO scoring model](references/scoring-model.md)
- [Risk classification and confirmation rules](references/risk-classification.md)
- [CMS write-back mapping](references/cms-writeback.md)
- [SEO MCP tool reference](references/mcp-tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON audit reports, and code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SEO scores, per-dimension findings, and low/high risk recommendation lists for human review.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
