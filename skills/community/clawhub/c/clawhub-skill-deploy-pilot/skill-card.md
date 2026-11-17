## Description:

Automates versioned Docker Compose and Proxmox LXC deployments with health checks, blue-green updates, chat approvals, and rollback workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure operators use this skill to plan and run container deployment workflows for Docker Compose stacks and Proxmox LXC containers, including health checks, version tracking, rollback, hooks, and approval steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make production-impacting deployment changes through Docker, SSH, and related deployment access.

Mitigation: Review the skill and deployment configuration before installing or running it, test changes outside production first, and run with the least privileges possible.

Risk: Untrusted stack configuration, health-check scripts, or deployment hooks can execute commands or affect services and host data.

Mitigation: Use only trusted stack configuration and avoid script health checks or hooks from untrusted sources.

Risk: Advertised approval and rollback behavior may not be sufficient as the only production safeguard.

Mitigation: Keep independent change review, monitoring, backups, and rollback procedures in place instead of relying solely on the skill's approval or rollback flow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mariusfit/skills/clawhub-skill-deploy-pilot)
- [Publisher Profile](https://clawhub.ai/user/mariusfit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate deployment commands, health-check configuration, hook configuration, and operational guidance for Docker Compose and LXC workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
