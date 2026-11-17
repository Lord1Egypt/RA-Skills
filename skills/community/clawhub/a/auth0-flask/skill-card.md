## Description:

Use when adding login, logout, and user profile to a Flask web application using session-based authentication with auth0-server-python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Auth0 session-based authentication to server-rendered Flask applications, including login, callback, profile, logout, protected routes, and session storage patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automated setup path can install the Auth0 CLI through a shell installer and append Auth0 values to environment files.

Mitigation: Review setup steps manually, install the Auth0 CLI from a pinned and verified release or package manager path, require explicit confirmation before env-file writes, and ensure credential files are excluded from version control.

Risk: The bundled evaluation runner can read project source files, including credential-like files, and send selected content to an external model through the Claude CLI.

Mitigation: Run evaluations only on sanitized workspaces, exclude .env and other secret-bearing files, and avoid using the eval runner on projects containing real credentials.

Risk: Using insecure session cookie settings in production can expose session cookies over non-HTTPS connections.

Mitigation: Set SESSION_COOKIE_SECURE=True for production deployments, use HTTPS, and review Flask session settings before release.

Risk: Cookie-based sessions have size and logout limitations, including unsupported backchannel logout in the provided stateless pattern.

Mitigation: Use Redis-backed Flask-Session or another server-side session store when sessions may exceed cookie limits or federated logout behavior is required.

## Reference(s):

- [Auth0 Flask Setup Guide](references/setup.md)
- [Auth0 Flask Integration Patterns](references/integration.md)
- [Auth0 Flask API Reference](references/api.md)
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills)
- [auth0-server-python on PyPI](https://pypi.org/project/auth0-server-python/)
- [Auth0 Flask Quickstart](https://auth0.com/docs/quickstart/webapp/python)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [auth0-server-python GitHub](https://github.com/auth0/auth0-server-python)
- [Flask-Session Documentation](https://flask-session.readthedocs.io/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes application code patterns, environment variable examples, setup commands, and testing guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
