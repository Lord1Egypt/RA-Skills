## Description:

Generates Docker Compose configuration for common local development services such as databases, caches, search, messaging, web servers, and Node.js.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to quickly draft Docker Compose files for local application infrastructure and development environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated services may expose default credentials and unauthenticated services on host ports.

Mitigation: Change database credentials, add Redis authentication, and limit port bindings before using the compose file on shared, public, or production hosts.

Risk: The bundled generator script can overwrite an existing file when given an output path.

Mitigation: Run it in a clean working directory or review the target output path before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/docker-compose-generator)

## Skill Output:

**Output Type(s):** [configuration, code, shell commands, guidance]

**Output Format:** [Text with Docker Compose YAML and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a docker-compose.yml file when the bundled shell script is executed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
