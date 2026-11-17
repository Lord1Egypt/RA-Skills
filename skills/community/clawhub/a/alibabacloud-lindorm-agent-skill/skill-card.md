## Description:

Guides agents through Alibaba Cloud Lindorm development and operations, including SQL, search, AI workflows, instance management, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to plan and troubleshoot Lindorm applications and instances, including connectivity, access control, data management, and SQL or search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud operations can change or delete resources, alter access, or incur charges.

Mitigation: Require human approval before creating, scaling, releasing, or changing billing, whitelists, security groups, users, or permissions.

Risk: Credential and installation examples may expose secrets or encourage unsafe execution.

Mitigation: Do not paste access keys or passwords into chat or shell history; avoid curl-to-shell installation commands.

Risk: Connections may expose credentials or model inputs.

Mitigation: Prefer private, TLS-protected endpoints when transmitting credentials or model inputs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-lindorm-agent-skill)
- [Skill homepage](https://clawhub.ai/sdk-team/alibabacloud-lindorm-agent-skill)
- [Lindorm quick start](references/01-dev/quick-start-guide.md)
- [Instance lifecycle](references/02-ops/instance-lifecycle.md)
- [Network access control](references/02-ops/network-access-control.md)
- [Lindorm CLI guide](references/03-ref/lindorm-cli-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review cloud-changing commands before execution.]

## Skill Version(s):

0.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
