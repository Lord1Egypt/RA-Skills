## Description:

Automate DolphinDB Docker deployment with auto architecture detection (ARM64/x86_64), smart memory allocation (50% rule), and full data persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate commands and guidance for deploying DolphinDB in Docker on macOS or Linux, including architecture selection, memory sizing, persistent data setup, and basic validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the deployment gives the container broad writable access to host system configuration.

Mitigation: Review and modify the deployment before real use; remove the full /etc mount or replace it with minimal read-only license files.

Risk: The security guidance notes that Docker image selection is under-scoped.

Mitigation: Pin and verify Docker image digests before running generated deployment commands.

Risk: The deployment exposes DolphinDB service ports and makes host and Docker changes.

Mitigation: Bind ports to localhost unless remote access is intentional, restrict the data directory to a dedicated path, and avoid elevated privileges.

## Reference(s):

- [DolphinDB Docker Skill on ClawHub](https://clawhub.ai/ugpoor/skills/dolphindb-docker)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [DolphinDB Documentation](https://dolphindb.cn/)
- [DolphinDB Docker Hub](https://hub.docker.com/u/dolphindb)
- [DolphinDB GitHub](https://github.com/dolphindb)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, Docker, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Docker image tags, host data paths, memory limits, exposed ports, and validation commands.]

## Skill Version(s):

1.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
