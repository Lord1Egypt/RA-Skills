## Description:

步步为营 helps agents structure complex application development, CI/CD, and DevOps work with staged checklists, shell helpers, and monitoring templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smxtx](https://clawhub.ai/user/smxtx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and verify complex application delivery work, including scoped code changes, testing, builds, CI/CD release steps, rollback planning, and monitoring setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact build, dependency, deployment, rollback, and health-check actions can affect local projects or target environments if run without review.

Mitigation: Review each command before execution, run in a disposable or least-privileged environment, and verify the target project or deployment environment before build, release, or rollback actions.

Risk: Dependency commands such as npm install and npx can execute project-controlled code in untrusted projects.

Mitigation: Avoid dependency installation and npx execution on untrusted projects, or run them inside an isolated environment with least privilege.

Risk: Health checks can probe arbitrary hosts if parameters are supplied without validation.

Mitigation: Restrict health checks to known safe hosts and confirm host, port, and path values before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smxtx/skills/bu-bu-wei-ying)
- [Publisher profile](https://clawhub.ai/user/smxtx)
- [README](artifact/README.md)
- [English skill definition](artifact/SKILL-en.md)
- [Automation checklist script](artifact/scripts/checklist.sh)
- [Grafana alert template](artifact/templates/grafana-alerts.json)
- [Datadog alert template](artifact/templates/datadog-alerts.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON monitoring templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes executable DevOps helper commands and monitoring configuration templates; review commands before use.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
