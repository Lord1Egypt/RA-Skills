## Description:

Builds, debugs, and hardens FastAPI services, including async endpoints, Pydantic models, dependencies, auth, testing, deployment, and production troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, review, debug, test, secure, and deploy FastAPI applications with guidance for common framework, database, async, auth, and production issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated FastAPI code or dependency recommendations may not match the target application's production constraints.

Mitigation: Review generated app-specific code, dependency choices, security behavior, and deployment settings before applying them in production.

Risk: The skill may use a local preference file under ~/Clawic/data/fastapi/config.yaml.

Mitigation: Treat stored preferences as non-secret configuration and avoid placing credentials or sensitive project data in that file.

## Reference(s):

- [ClawHub FastAPI Skill Page](https://clawhub.ai/ivangdavila/skills/fastapi)
- [Clawic FastAPI Skill Page](https://clawic.com/skills/fastapi)
- [FastAPI Skill Guide](artifact/SKILL.md)
- [FastAPI Security Guide](artifact/security.md)
- [FastAPI Deployment Guide](artifact/deployment.md)
- [FastAPI Testing Guide](artifact/testing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, configuration, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a local preference file at ~/Clawic/data/fastapi/config.yaml; generated app-specific code and dependency choices should be reviewed before production use.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
