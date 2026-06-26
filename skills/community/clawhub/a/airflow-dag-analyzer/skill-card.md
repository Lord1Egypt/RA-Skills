## Description: <br>
Analyze Apache Airflow DAG definitions for quality, reliability, and operational best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and platform teams use this skill to audit Apache Airflow DAGs for operational quality, reliability risks, dependency structure, retry behavior, sensor configuration, resource usage, and production readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Airflow DAG code and related configuration, which may expose secrets or sensitive infrastructure details if broad paths are provided. <br>
Mitigation: Point the agent only at intended DAG files or DAG directories, and avoid including secrets or unrelated repository areas. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with findings, scores, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include health scores, category scores, critical issues, per-DAG findings, dependency visualization, remediation code, and prioritized recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
