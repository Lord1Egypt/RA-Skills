## Description:

GEO搜索占位架构师 helps agents optimize SEO/GEO content by adding JSON-LD structured data, generating FAQ schema and llms.txt summaries, and scoring content with a five-dimension GEO gate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams, SEO specialists, and developers use this skill to prepare article, how-to, FAQ, and product content for AI search visibility. It produces structured data, FAQ suggestions, llms.txt-style summaries, GEO score details, and optimization guidance for human review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad command, file, API, and credential use could modify content or expose secrets if the skill is run with excessive permissions.

Mitigation: Keep agent permissions constrained and require confirmation before file writes, shell commands, external API calls, batch processing, or API-key use.

Risk: Generated SEO/GEO suggestions, JSON-LD, FAQs, or scores could introduce inaccurate or misleading public-facing content.

Mitigation: Require human review of optimized content, structured data, FAQ entries, llms.txt summaries, and GEO scores before publication.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/thcjp/skills/geo-rank-architect)
- [Schema.org structured data vocabulary](https://schema.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and JSON-LD snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optimized content, GEO scores, score breakdowns, JSON-LD, FAQ schema entries, llms.txt-style summaries, retry counts, and optimization notes.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
