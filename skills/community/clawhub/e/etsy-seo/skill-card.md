## Description:

Etsy SEO analyzer and optimizer that helps improve listing search visibility with title optimization, tag analysis, description scoring, keyword suggestions, SEO scoring, and prioritized action plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers and agents use this skill to evaluate Etsy listing metadata and generate practical optimization guidance for titles, tags, descriptions, attributes, images, and next actions. The reports are best treated as local heuristic SEO guidance rather than live marketplace, competitor, trend, or search-volume research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guidance uses an unpinned global npx command.

Mitigation: Install only from a trusted package source, avoid administrator privileges, and prefer a pinned installer version when available.

Risk: The skill can overstate keyword research, competitor, trend, or search-volume capabilities because the artifact performs local heuristic analysis.

Mitigation: Treat reports as optimization suggestions and verify marketplace demand, competitor behavior, and search-volume claims with authoritative Etsy or analytics data before making business decisions.

Risk: The CLI behavior in the artifact may not analyze arbitrary listing data as fully as the usage examples imply.

Mitigation: Validate the analyzer with representative listings before operational use and update the invocation flow if structured listing input is required.

## Reference(s):

- [ClawHub Etsy Seo Skill Page](https://clawhub.ai/phheng/skills/etsy-seo)
- [phheng Publisher Profile](https://clawhub.ai/user/phheng)
- [Nexscope AI](https://www.nexscope.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style SEO analysis report with scores, suggested tags, keyword guidance, and prioritized action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local heuristic analysis; no API key is required.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
