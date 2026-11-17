## Description:

Docker container lifecycle management, health checks, log analysis, cleanup, compose orchestration, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill with Codex to inspect Docker state, debug containers and services, analyze logs, clean up unused Docker resources, and follow Docker Compose operating patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker cleanup and volume-removal guidance can delete data if used without confirming the target resources.

Mitigation: Use dry-run mode and explicit confirmation before cleanup, and avoid `docker compose down -v` unless volume deletion is intended.

Risk: Docker group or sudo guidance can grant persistent root-equivalent host access.

Mitigation: Require administrator approval before changing Docker group membership or running privileged Docker operations.

Risk: Copied Compose templates can expose services or rely on weak placeholder secrets.

Mitigation: Replace sample credentials with managed secrets and review public database port exposure before deployment.

## Reference(s):

- [Docker Compose Patterns](references/compose-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, YAML, and Dockerfile code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational commands and cleanup guidance that should be reviewed before execution.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
