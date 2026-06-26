## Description: <br>
Docker and container security anti-pattern analyzer that detects Dockerfile issues, missing health checks, resource limit gaps, privileged containers, insecure networking, and orchestration anti-patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to scan Dockerfiles, compose files, and container-related configuration for security and reliability anti-patterns. It can produce local scan findings, scores, and remediation guidance for development or CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: License keys are sensitive and can be supplied through environment variables, local configuration, or command-line flags. <br>
Mitigation: Use the CONTAINERLINT_LICENSE_KEY environment variable or local config file, avoid passing keys on the command line, and use only trusted license keys. <br>
Risk: Optional hook installation can modify repository hook configuration and run scans during commit or push workflows. <br>
Mitigation: Review the lefthook.yml changes before installing hooks and confirm the team accepts commit-time and push-time scans. <br>
Risk: The artifact executes local shell scripts over repository files. <br>
Mitigation: Review the scripts before deployment and start with the free local scan path on a non-sensitive repository when evaluating the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suhteevah/containerlint) <br>
- [ContainerLint homepage](https://containerlint.pages.dev) <br>
- [ContainerLint hooks documentation](https://containerlint.pages.dev/docs/hooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text, JSON, HTML, and Markdown reports with inline shell commands and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local scanner output may include file paths, line numbers, severity, check IDs, scores, grades, and category summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
