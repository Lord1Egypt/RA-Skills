## Description:

Recommend optimal GCP Committed Use Discount portfolio (spend-based vs resource-based) with risk analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

External users, developers, and cloud cost engineers use this skill to analyze exported GCP billing and usage data and choose conservative, balanced, or aggressive CUD coverage for Compute Engine, GKE, and Cloud Run workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported GCP billing and usage data can reveal spend, project names, and workload structure.

Mitigation: Review and minimize pasted data before analysis, and do not include credentials, access keys, or secret keys.

Risk: Generated gcloud commands for CUD purchases can create financial commitments if run without review.

Mitigation: Treat generated commands as proposals and review them against current pricing, workload stability, and approval requirements before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with recommendation tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on user-provided GCP billing and usage data; no direct account access or credentials are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
