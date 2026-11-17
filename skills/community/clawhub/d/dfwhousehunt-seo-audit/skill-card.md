## Description:

Crawl any website and get a 0-100 SEO score with 50+ checks across Technical, On-Page, Schema, Social, and Compliance categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, and site operators use this skill to audit websites for SEO quality, industry compliance issues, quick wins, competitor gaps, and article-generation opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented Python script is not present in the submitted artifact, so advertised commands may fail.

Mitigation: Confirm the implementation is included and runnable before release or installation.

Risk: The skill declares unpinned Python dependencies and premium use requires an Anthropic API key.

Mitigation: Review and pin dependencies before deployment, and provide API keys only after implementation review.

Risk: Website crawling may send requests to external or sensitive URLs supplied by a user.

Mitigation: Avoid auditing sensitive internal URLs unless the execution environment and implementation have been reviewed.

## Reference(s):

- [Project homepage](https://github.com/dfw-area-house-hunt/openclaw-skills)
- [ClawHub skill page](https://clawhub.ai/drivenautoplex1/skills/dfwhousehunt-seo-audit)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown or JSON audit results, with optional generated article content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a weighted SEO score, category-level findings, prioritized quick wins, competitor gap analysis, compliance flags, or generated article text.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
