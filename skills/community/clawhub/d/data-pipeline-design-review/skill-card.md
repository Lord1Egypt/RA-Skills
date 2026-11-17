## Description:

Use when a data engineer needs a structured design review of a proposed data pipeline, ETL/ELT flow, or dbt/SQL model before it ships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to pressure-test data pipeline, ETL/ELT, streaming, and dbt/SQL designs before release. It produces severity-rated reliability, data-quality, schema-evolution, observability, and cost findings with a remediation checklist and go/no-go recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pipeline design reviews may include internal system names, schemas, operational details, or credentials if users paste them into the prompt.

Mitigation: Share only the design details needed for review and redact secrets, credentials, and unnecessary sensitive identifiers before use.

Risk: The skill's findings are design-review guidance and may miss issues when source, orchestration, failure, or consumer-SLA details are absent.

Mitigation: Treat missing context as assumptions, review the generated assumptions and findings, and confirm recommendations with the responsible data platform owner before release.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review report with severity-rated findings, assumptions, dimension coverage, remediation checklist, and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask targeted follow-up questions when key pipeline design details are missing.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
