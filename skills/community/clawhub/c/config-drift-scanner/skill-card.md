## Description: <br>
Detect configuration drift across environments (dev, staging, production). Compare config files, environment variables, feature flags, and secrets across deployments to find dangerous inconsistencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and operations teams use this skill to compare configuration across dev, staging, and production environments, identify dangerous drift, and prepare parity or remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration scans can expose sensitive values from config files, environment variables, secrets, temporary files, terminal output, or CI logs. <br>
Mitigation: Redact sensitive values by default, avoid raw .env or tfvars diffs in chat and CI logs, and delete temporary files containing configuration data after use. <br>
Risk: Kubernetes examples may inspect the wrong cluster or namespace or use broader access than needed. <br>
Mitigation: Verify the active cluster and namespaces before running commands and use read-only, narrowly scoped Kubernetes credentials. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include drift classifications, checklists, CI configuration snippets, and remediation recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
