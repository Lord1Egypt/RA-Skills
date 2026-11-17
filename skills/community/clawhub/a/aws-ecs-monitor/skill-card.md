## Description:

AWS ECS production health monitoring with CloudWatch log analysis for ECS service health, ALB targets, SSL certificates, error categorization, restart detection, and production alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[briancolinger](https://clawhub.ai/user/briancolinger)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to monitor AWS ECS production services, inspect CloudWatch logs, diagnose unhealthy services, and produce health status or alert outputs from configured AWS environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports unsafe input handling that could allow crafted configuration or arguments to run commands in an AWS-enabled environment.

Mitigation: Review before installing, run only with trusted configuration and command arguments, and use least-privilege AWS read permissions.

Risk: The security guidance identifies unsafe Python interpolation, arithmetic parsing, and temporary-file handling.

Mitigation: Fix those implementation issues before use in shared, automated, or user-facing agent environments.

Risk: The scripts write status, alert, log, and analysis files to configured output paths.

Mitigation: Keep ECS_HEALTH_STATE and ECS_HEALTH_OUTDIR in protected directories and avoid locations writable by untrusted users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/briancolinger/skills/aws-ecs-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON health or log-analysis output from the bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes health state, alert, log, and analysis files under ECS_HEALTH_STATE or ECS_HEALTH_OUTDIR when the scripts are run.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
