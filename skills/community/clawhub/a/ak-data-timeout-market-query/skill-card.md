## Description:

Query timeout status and market timeout ranking for any single job type on huge sharded job tables (job_a~job_d) without index changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leehoo29](https://clawhub.ai/user/leehoo29)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to generate read-only, single-job-type timeout diagnostics for AK Data job shards, including timeout totals, market rankings, duration statistics, representative samples, and chart-ready report sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may expose operational identifiers such as req_ssn.

Mitigation: Run the skill only for users with legitimate read access to the referenced job tables and handle report outputs according to internal data-access controls.

Risk: Large sharded job-table queries can create operational load if scope limits are ignored.

Mitigation: Keep execution read-only, use one jobType at a time, limit each SQL query to a single-day window, and rely on the documented existing index strategy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leehoo29/skills/ak-data-timeout-market-query)

## Skill Output:

**Output Type(s):** [Markdown, Code, JSON, Guidance]

**Output Format:** [Markdown report with SQL templates and chart-ready JSON blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single job type and single-day query windows; recent requests are split into two single-day runs before application-level aggregation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
