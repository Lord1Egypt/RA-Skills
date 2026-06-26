## Description: <br>
Manage and update Airflow DAG Python files through GitHub pull requests with strict path, repository, and content restrictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kansodata](https://clawhub.ai/user/kansodata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data platform engineers use this skill to read existing Airflow DAG Python files and submit single-file DAG updates through human-reviewed GitHub pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Airflow DAG edits can affect production workflows if repository, path, or content guardrails are not enforced by the connected GitHub tools. <br>
Mitigation: Verify the tool allowlist and least-privilege GitHub access before installation, and require human review before merging pull requests. <br>
Risk: A generated update could introduce unsafe or invalid DAG content. <br>
Mitigation: Restrict operations to a single allowlisted .py DAG file, require DAG-like content, reject dangerous patterns, and use pull request review before merge. <br>
Risk: A merged DAG change may need to be undone after review or deployment. <br>
Mitigation: Use the documented rollback posture: close unmerged pull requests, delete created branches, or revert the merge commit after merge. <br>


## Reference(s): <br>
- [Airflow DAG Git on ClawHub](https://clawhub.ai/kansodata/airflow-dag-git) <br>
- [kansodata publisher profile](https://clawhub.ai/user/kansodata) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with tool calls, Python DAG content, and pull request instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to stay within allowlisted repositories and DAG paths and to create human-reviewed pull requests rather than direct production changes.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
