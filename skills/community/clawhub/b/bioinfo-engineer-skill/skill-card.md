## Description: <br>
Guides agents through bioinformatics engineering workflows with environment management, secrets isolation, Git and DVC versioning, relative paths, and reusable pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biociao](https://clawhub.ai/user/biociao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bioinformatics developers and analysis teams use this skill to plan, review, and standardize reproducible analysis projects. It helps agents produce environment setup guidance, Git and DVC workflows, pipeline templates, report structures, and security-conscious handling of project paths and credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example credential-loading and logging patterns could expose secrets if copied directly into real projects. <br>
Mitigation: Use scoped credential loading, keep .env files out of Git, and redact sensitive values before writing logs. <br>
Risk: DVC remote configuration and data push commands can move sensitive bioinformatics data to unintended storage. <br>
Mitigation: Review DVC remote targets, access controls, and data sensitivity before running dvc push. <br>
Risk: Generated workflow commands may modify local environments, Git state, or project data. <br>
Mitigation: Review proposed commands before execution and run them in project-specific environments with version control or backups. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose project files such as environment manifests, pipeline definitions, reports, and Git/DVC commands for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
