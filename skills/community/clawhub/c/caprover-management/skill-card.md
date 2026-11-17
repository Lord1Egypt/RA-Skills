## Description:

Manage CapRover PaaS instances through API-guided workflows for app creation, deployment, configuration, logs, volumes, ports, and Docker Swarm overrides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guim4dev](https://clawhub.ai/user/guim4dev)

### License/Terms of Use:


## Use Case:

Developers and infrastructure operators use this skill to deploy, configure, and diagnose applications on self-hosted CapRover servers. It is especially relevant for API-based app lifecycle work, Docker image or Dockerfile deployments, persistent volumes, TCP ports, runtime logs, and ARM64 deployment troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper and examples disable TLS certificate verification for CapRover API calls.

Mitigation: Enable certificate verification before use, preferably by trusting the CapRover server CA certificate.

Risk: The CLI usage accepts an admin password as a command-line argument and prints token material.

Mitigation: Pass credentials through a safer secret-handling path and avoid displaying, logging, or storing authentication tokens.

Risk: The skill can guide privileged infrastructure changes such as deployments, service overrides, app deletion, and volume deletion.

Mitigation: Require explicit user confirmation and review the target app, payload, and data-loss impact before executing destructive or deployment-changing actions.

## Reference(s):

- [CapRover API Reference](references/api.md)
- [CapRover Python Helper](scripts/caprover.py)
- [ClawHub Skill Page](https://clawhub.ai/guim4dev/skills/caprover-management)
- [Publisher Profile](https://clawhub.ai/user/guim4dev)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline Python, JSON, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privileged CapRover API actions and deployment instructions that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
