## Description:

Provides a structured workflow for updating and maintaining Docker-based CLI Proxy API deployments, including backups, test deployment, production replacement, validation, and rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jojo587](https://clawhub.ai/user/jojo587)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to plan and execute CLI Proxy API configuration changes, Docker image updates, production validation, and rollback steps while preserving configuration and authentication data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may deploy a mutable Docker image tag against live configuration and authentication mounts.

Mitigation: Replace mutable tags with a reviewed version and immutable digest, verify image provenance where possible, and test with non-production copies before production deployment.

Risk: Stopping, removing, or recreating containers can interrupt a production CLI Proxy API service or affect mounted data.

Mitigation: Confirm each stop, remove, recreate, and cleanup step with the operator, capture backups first, and keep a tested rollback path available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jojo587/skills/cpa-update)
- [CLI Proxy API Docker Hub Image](https://hub.docker.com/r/eceasy/cli-proxy-api)
- [CLI Proxy API GitHub Repository](https://github.com/router-for-me/Cli-Proxy-API)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown with inline shell commands and Docker configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance should be reviewed before execution because it can affect production Docker containers, mounted configuration, and authentication data.]

## Skill Version(s):

2.2.1 (source: server release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
