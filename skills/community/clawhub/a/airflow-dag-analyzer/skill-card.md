## Description:

Analyze Apache Airflow DAG definitions for quality, reliability, and operational best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data platform engineers use this skill to review Apache Airflow DAG files for operational quality, reliability, dependency structure, retry behavior, SLA coverage, sensor configuration, resource use, and production readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generic DAG trigger could activate the skill for unrelated graph or workflow code.

Mitigation: Use the skill only for Apache Airflow DAG directories or specific DAG files, and provide clear Airflow context when invoking it.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with findings, scores, remediation guidance, and inline code or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include health scores, category scores, critical issues, per-DAG findings, per-task findings, text dependency visualizations, remediation code, and priority matrices.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
