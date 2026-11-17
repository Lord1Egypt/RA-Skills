## Description:

Evaluates data availability, quality, cost, and compliance, then produces a data acquisition strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyan521](https://clawhub.ai/user/shiyan521)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and data strategists use this skill to evaluate product data requirements and compare data sources across availability, quality, cost, compliance, and defensibility. It helps produce a Markdown data strategy document with collection approaches for APIs, web data, purchased datasets, UGC, and manual collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to discuss anti-scraping bypass strategy, which can create legal, terms-of-service, or access-control risk.

Mitigation: Review scraping-related recommendations before use, prefer official APIs, licensed datasets, permission-based access, rate limiting, and stop conditions when access controls are encountered.

Risk: Data acquisition guidance may rely on incomplete compliance assumptions for a specific data source or jurisdiction.

Mitigation: Require legal and terms-of-service review for proposed collection plans before implementation, especially for web scraping or third-party data reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shiyan521/skills/06-data-source-evaluator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown data strategy document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected filename pattern: {product name}-data-strategy.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
