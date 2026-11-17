## Description:

Enhanced Docker with Dockerfile templates, multi-stage builds, security hardening, production best practices, Docker Compose patterns, and troubleshooting guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to draft Dockerfiles, Docker Compose configurations, hardening practices, production container guidance, and troubleshooting commands for containerized applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential examples in Dockerfile or Docker Compose snippets could be copied into real systems and expose secrets.

Mitigation: Use Docker or platform secrets, runtime injection, and unique credentials instead of copying example credentials into production configuration.

Risk: Broad cleanup commands such as docker system prune -af can remove Docker resources destructively.

Mitigation: Verify the active Docker context and confirm resources are disposable before running destructive cleanup commands.

## Reference(s):

- [Docker Plus ClawHub page](https://clawhub.ai/534422530/skills/docker-plus)
- [Source skill artifact](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Dockerfile, YAML, and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable Dockerfile templates, Compose examples, security guidance, best practices, and troubleshooting tables.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
