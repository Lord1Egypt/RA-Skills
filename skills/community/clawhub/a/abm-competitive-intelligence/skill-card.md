## Description:

Performs competitive intelligence by researching competitors and analyzing their online presence using web search and site scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, product, sales, and strategy teams use this skill to research competitors, compare positioning, pricing, and features, and synthesize actionable competitive intelligence reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided competitor names or URLs could be inserted into shell command templates unsafely.

Mitigation: Pass search terms and URLs as structured tool arguments when available; otherwise validate and quote user-provided values before execution.

Risk: Competitive intelligence findings can be misleading when search results or scraped pages are stale, incomplete, or unverifiable.

Mitigation: Cross-reference search results with scraped source pages and explicitly flag pricing, feature, or company details that could not be verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariokarras/skills/abm-competitive-intelligence)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes executive summary, competitor profiles, feature comparison matrix, messaging analysis, and gaps and opportunities; findings should flag information gaps.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
