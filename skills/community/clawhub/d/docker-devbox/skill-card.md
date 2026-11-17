## Description:

Devbox creates one-command Docker development environments by detecting project types and local runtime versions, generating Docker Compose configuration, managing ports, attaching optional database services, and isolating dependencies and build caches in named volumes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nciae-zyh](https://clawhub.ai/user/nciae-zyh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Devbox to generate isolated Docker Compose development environments for local projects, including framework-specific runtime images, port mapping, named volumes for dependencies and caches, and optional database services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Docker Compose files can expose development services and databases on host ports with default credentials.

Mitigation: Review docker-compose.dev.yml before running it, bind services to localhost or avoid publishing database ports, and replace default database and MinIO credentials.

Risk: The Bun package-manager path installs Bun through an unpinned remote shell installer.

Mitigation: Avoid the Bun path unless the installer is pinned, replaced with a trusted package source, or reviewed in the target environment.

Risk: The target project source tree and optional env_file are mounted into containers, which can expose local secrets to container processes.

Mitigation: Inspect mounted paths and environment files before use, and avoid running Devbox against projects containing sensitive secrets.

## Reference(s):

- [Docker Compose Templates](references/docker-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/nciae-zyh/skills/docker-devbox)

## Skill Output:

**Output Type(s):** [shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with bash commands and generated Docker Compose YAML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a docker-compose.dev.yml file in the target project and may update .gitignore entries.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
