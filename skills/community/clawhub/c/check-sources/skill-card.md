## Description:

Surveys connected health data sources and reports connection status plus record counts by type without clinical values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aks129](https://clawhub.ai/user/aks129)

### License/Terms of Use:

MIT-0

## Use Case:

External health users and their assisting agents use this skill to confirm which connected health services are available and how many records exist by type. It supports source-status review only, not clinical interpretation or record-detail review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reveal sensitive health-data metadata, including which services are connected and how many records exist by type.

Mitigation: Use step-up authentication for protected tenants and present only connection status, source names, and counts; do not expose diagnoses, lab values, medications, or other clinical details.

Risk: Connection summaries may mislead users if unsupported connections or records are implied.

Mitigation: Report only what sources_check returns, and explicitly state when a source is not connected or is connected with zero records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aks129/skills/check-sources)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Concise Markdown summary of connected sources and record counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports source names, connection status, and record counts only; no clinical values or record details.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
