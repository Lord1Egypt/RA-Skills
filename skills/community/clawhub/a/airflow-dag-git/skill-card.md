## Description:

Manage and update Airflow DAG Python files through GitHub pull requests with strict path and content restrictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kansodata](https://clawhub.ai/user/kansodata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to read and update allowlisted Airflow DAG Python files through GitHub pull requests with human review before merge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Airflow DAG changes can affect scheduled production workflows.

Mitigation: Install only where the named GitHub tools are configured with the documented allowlists, and review every generated pull request before merging.

Risk: Out-of-scope repository or file changes could bypass intended workflow control.

Mitigation: Restrict operations to allowlisted owners, repositories, and DAG paths, and keep updates to a single .py file.

Risk: Unsafe or invalid DAG content could be proposed for review.

Mitigation: Require DAG-like content checks and inspect the generated pull request diff before merge.

## Reference(s):

- [Airflow DAG Git on ClawHub](https://clawhub.ai/kansodata/skills/airflow-dag-git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, API Calls, Guidance]

**Output Format:** [Markdown guidance with Python DAG content and pull request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single allowlisted Python DAG file changes are submitted through a GitHub pull request for human review.]

## Skill Version(s):

0.1.1 (source: server evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
