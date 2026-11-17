## Description:

Check health of AWS EC2 instances and ECS clusters/services. Reports running/stopped counts, CPU/memory metrics, and unhealthy tasks. Use when the user asks about AWS instance health, ECS status, or infra monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yashgkar](https://clawhub.ai/user/yashgkar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to check AWS EC2 and ECS health, including instance state, service status, CPU and memory metrics, and unhealthy ECS tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires AWS credentials, which could expose cloud account access if long-lived or over-privileged credentials are used.

Mitigation: Use short-lived, least-privilege, read-only AWS credentials and avoid exposing credentials in chat or logs.

Risk: The security summary reports an unpinned tsx runtime dependency and a missing health-check script that cannot be reviewed in the artifact.

Mitigation: Do not run the skill until the missing script is packaged and the tsx dependency is pinned or controlled by a lockfile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yashgkar/skills/aws-health)
- [Publisher profile](https://clawhub.ai/user/yashgkar)
- [Source repository](https://github.com/yashgkar/aws-health)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown/text health report with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AWS credential environment variables and a Node/tsx runtime; supports EC2-only, ECS-only, and specific ECS cluster checks.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
