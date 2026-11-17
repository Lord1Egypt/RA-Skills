## Description:

Generates operational runbooks from project files by scanning Dockerfiles, Docker Compose files, systemd units, Makefiles, package.json, environment files, and nginx configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and operations engineers use this skill to generate first-draft deployment, lifecycle, rollback, troubleshooting, and monitoring runbooks from infrastructure files in a project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads infrastructure and environment files in the target project, including .env metadata.

Mitigation: Run it only on trusted project directories and review generated environment-variable details before sharing or committing output.

Risk: Generated runbooks may include privileged or disruptive systemctl, Docker, and deployment commands.

Mitigation: Treat generated commands as procedures for human review and obtain separate approval before running privileged or destructive operations.

Risk: Generated operational guidance can be incomplete or misleading because parsing is heuristic and based only on detected files.

Mitigation: Validate runbooks against the actual deployment environment and fill in contacts, health checks, rollback, and monitoring details before production use.

## Reference(s):

- [Runbook Generator Skill Source](artifact/SKILL.md)
- [Runbook Generator Status](artifact/STATUS.md)
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/cm-runbook-generator)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown runbook by default, or structured JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write output to a selected file with -o; generated operational commands require review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
