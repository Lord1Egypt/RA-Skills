## Description:

Analyzes public BBB complaint narratives, business responses, statuses, and reporting-window totals through Crawlora to support sourced comparisons with clear coverage limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and consumer analysts compare complaint themes and response processes for selected BBB business profiles while preserving attribution, reporting windows, and sample limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Crawlora API receives the API key and research queries.

Mitigation: Use a dedicated key kept in the environment, never paste it into prompts or logs, and limit queries to the needed businesses and time window.

Risk: Incomplete complaint lists or mismatched reporting windows can make comparisons misleading.

Mitigation: Separate itemized sample counts from aggregate totals, disclose missing detail and date filters, and compare only matching measures.

Risk: Complaint allegations or redacted details can be mistaken for verified findings or exposed identities.

Mitigation: Attribute each allegation and response to its source, preserve redactions, and avoid unsupported conclusions about business misconduct.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/business-complaint-pattern-analysis)
- [Crawlora BBB endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown with evidence tables and sourced analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies business profiles, complaint themes and statuses, source dates, sample sizes, reporting windows, and unresolved questions.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
