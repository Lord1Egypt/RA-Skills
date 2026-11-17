## Description:

Extracts structured data from websites and APIs into clean CSV and JSON datasets with pagination, deduplication, and enrichment support for business intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreataide86](https://clawhub.ai/user/andreataide86)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and data operators use this skill to scope permitted web or API extraction requests, define schemas, collect bounded datasets, clean and deduplicate records, and deliver business intelligence outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on the unpinned cashclaw npm package, so behavior depends on the installed package version and publisher.

Mitigation: Install only from a trusted publisher, pin and audit the package version before use, and run it in a constrained environment.

Risk: Scraping can violate robots.txt, website terms, or privacy expectations, especially when business contact data is collected.

Mitigation: Use only permitted sources, respect robots.txt and terms of service, keep record limits narrow, apply rate limits, and avoid personal contact data outside a legitimate business context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andreataide86/skills/cashclaw-data-scraper)
- [CashClaw npm package](https://www.npmjs.com/package/cashclaw)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files, Markdown]

**Output Format:** [Markdown guidance with inline JSON, YAML, CSV, and bash examples; final extraction deliverables are CSV, JSON, and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and curl; examples invoke the cashclaw npm package.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
