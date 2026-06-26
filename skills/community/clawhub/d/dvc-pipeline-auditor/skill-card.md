## Description: <br>
Audits DVC (Data Version Control) pipelines for reproducibility, storage efficiency, and tracking correctness across pipeline definitions, lock files, tracked data, remotes, parameters, metrics, and stage dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and ML engineers use this skill to review DVC project setup, validate reproducibility, identify tracking or storage issues, and generate prioritized remediation guidance for data and model pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DVC configuration files and project paths may expose storage locations or operational details when shared with an agent. <br>
Mitigation: Point the skill only at projects intended for inspection and avoid sharing credential files, secrets, or real access keys. <br>
Risk: Suggested DVC commands such as push, pull, add, remote modify, repro, or gc may change local or remote project state if executed without review. <br>
Mitigation: Review generated remediation commands before running them and apply them in an appropriate working branch or controlled environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/dvc-pipeline-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with issue annotations, scores, and remediation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes pipeline graph review, lock-file integrity findings, data tracking audit, remote storage review, parameter and metrics checks, reproducibility score, health score, and prioritized remediation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
