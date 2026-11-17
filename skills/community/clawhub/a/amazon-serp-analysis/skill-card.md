## Description:

Analyzes an Amazon niche from a seed keyword by scraping SERP data, expanding related keywords, scoring competition intensity, estimating demand, and producing a go/no-go recommendation with entry strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbeihanda](https://clawhub.ai/user/linbeihanda)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and market analysts use this skill to evaluate an Amazon product niche from a seed keyword, compare SERP competition and demand signals, and decide whether to enter the track.

### Deployment Geography for Use:

Global; the workflow evidence focuses on Amazon.com and US marketplace data.

## Known Risks and Mitigations:

Risk: The workflow sends Amazon search URLs and keywords to a configured scraper.

Mitigation: Use the skill only for approved market-analysis queries and require confirmation before scraping ambiguous or sensitive keywords.

Risk: Optional marketplace and database tools can expose broader data access than the analysis requires.

Mitigation: Scope ClickHouse and marketplace credentials to read-only access and the minimum datasets needed for the niche analysis.

Risk: The workflow may run a local listing-grader script using ASIN input.

Mitigation: Validate ASINs as exactly ten alphanumeric characters before script execution.

Risk: Go/no-go market recommendations can be misleading when based on incomplete scraper results or inferred keyword expansion.

Mitigation: Keep source labels in the output, call out omitted unavailable tools, and review conclusions before using them for investment decisions.

## Reference(s):

- [Amazon Serp Analysis on ClawHub](https://clawhub.ai/linbeihanda/skills/amazon-serp-analysis)
- [linbeihanda ClawHub Profile](https://clawhub.ai/user/linbeihanda)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables, labeled data sources, scoring, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SERP and product metrics, competition scoring, demand estimates, entry-angle candidates, go/no-go verdict, and data source labels.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
