## Description:

Verifies that a prepared AWS FIS experiment stack is already deployed, runs the experiment after explicit confirmation, monitors progress, and generates a results report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panlm](https://clawhub.ai/user/panlm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to execute already prepared AWS Fault Injection Simulator experiments, verify stack and resource readiness, collect logs, monitor impact, and create a post-experiment report. It is intended for controlled chaos testing workflows where infrastructure deployment has already happened.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can start real AWS fault-injection experiments that affect production resources.

Mitigation: Use explicit user confirmation, review affected resources and stop conditions before execution, and verify all targeted resources are healthy before starting.

Risk: The skill can use broad AWS and Kubernetes permissions to inspect EKS workloads and collect logs.

Mitigation: Run with least-privilege AWS IAM and Kubernetes RBAC, avoid Secret-read permissions where possible, and treat generated logs and reports as sensitive artifacts.

Risk: The workflow depends on the runtime-resolved app-service-log-analysis skill for application discovery and log analysis.

Mitigation: Review the resolved app-service-log-analysis skill before use and confirm its behavior is acceptable in the target environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/panlm/skills/aws-fis-experiment-execute)
- [CLI Commands Reference](references/cli-commands.md)
- [Experiment Results Report Template](references/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report, terminal guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a timestamped experiment results report in the prepared experiment directory and may reference collected log files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
