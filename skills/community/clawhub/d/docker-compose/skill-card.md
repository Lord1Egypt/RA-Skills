## Description:

Define multi-container applications with proper dependency handling, networking, and volume management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill for Docker Compose guidance covering service readiness, health checks, volume handling, resource limits, build context hygiene, override files, profiles, and environment variable precedence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Docker Compose guidance may include destructive volume commands such as docker compose down -v, which can delete application data.

Mitigation: Review volume-related commands before use and confirm backups or disposable data before removing volumes.

Risk: Compose and Docker build guidance can accidentally include secrets or large local directories in image contexts or base compose files.

Mitigation: Use a .dockerignore file, keep secrets out of images and base compose files, and review resolved configuration with docker compose config.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/docker-compose)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker Compose tooling through either docker-compose or docker.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
