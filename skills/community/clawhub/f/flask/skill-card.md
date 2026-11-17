## Description:

Avoid common Flask mistakes - context errors, circular imports, session configuration, and production gotchas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as a quick reference for avoiding common Flask context, import, session, SQLAlchemy, and production deployment mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Developers may apply development-only Flask settings in production.

Mitigation: Review production configuration before deployment, especially debug mode, SECRET_KEY, SESSION_COOKIE_SECURE, and SESSION_COOKIE_HTTPONLY.

Risk: Reference guidance may not match every Flask application version or deployment environment.

Mitigation: Validate the generated advice against the target application's Flask, extension, and hosting configuration before making changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/flask)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with inline Flask code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution; concise reference guidance for Flask development and production settings.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-02-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
