## Description:

Google Analytics 4, Search Console, and Indexing API toolkit for analyzing website traffic, page performance, user demographics, real-time visitors, search queries, SEO metrics, URL indexing status, and re-indexing requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamkristopher](https://clawhub.ai/user/adamkristopher)

### License/Terms of Use:


## Use Case:

Developers, site operators, and analytics teams use this skill to query GA4, Search Console, and Google Indexing APIs, then save structured results and produce human-readable summaries for traffic, SEO, content, conversion, and indexing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broadly scoped Google service account could expose more GA4, Search Console, or Indexing API access than the intended property or site requires.

Mitigation: Use a least-privilege Google service account limited to the target GA4 property and Search Console site.

Risk: Index removal functionality can request removal of URLs from Google indexing.

Mitigation: Avoid invoking removeFromIndex unless the operator explicitly intends to remove the URL from Google indexing.

Risk: Saved analytics and Search Console results may contain sensitive business or traffic data.

Mitigation: Keep the results directory private and control access to generated JSON and Markdown summaries.

Risk: The skill includes npm dependencies that may change over time or require security review before use with sensitive analytics data.

Mitigation: Audit and update npm dependencies before installation in sensitive or production environments.

## Reference(s):

- [API Reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are saved as timestamped JSON files under results/ by category; summaries may be written as Markdown.]

## Skill Version(s):

1.0.0 (source: server release metadata, scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
