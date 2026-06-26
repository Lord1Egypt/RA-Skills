## Description: <br>
Use when adding login, logout, and user profile to a Flask web application using session-based authentication - integrates auth0-server-python for server-rendered apps with login/callback/profile/logout flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add Auth0-backed login, callback handling, logout, session storage, and profile routes to server-rendered Flask applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags unsafe admin-role guidance that could lead to overbroad authorization if copied into an application. <br>
Mitigation: Derive roles from verified claims or a server-side authorization store before using them for access control. <br>
Risk: The optional evaluation tooling can expose secrets if run in projects with real environment files or credentials. <br>
Mitigation: Avoid running the eval harness on projects with real .env files or secrets, and replace example secrets with placeholders. <br>
Risk: The setup material includes an Auth0 CLI installation path that relies on a remote shell installer. <br>
Mitigation: Prefer a pinned or package-manager Auth0 CLI installation before running setup commands. <br>


## Reference(s): <br>
- [Auth0 Flask Setup Guide](references/setup.md) <br>
- [Auth0 Flask Integration Patterns](references/integration.md) <br>
- [Auth0 Flask API Reference](references/api.md) <br>
- [Auth0 Agent Skills](https://github.com/auth0/agent-skills) <br>
- [auth0-server-python on PyPI](https://pypi.org/project/auth0-server-python/) <br>
- [Auth0 Flask Quickstart](https://auth0.com/docs/quickstart/webapp/python) <br>
- [Flask Documentation](https://flask.palletsprojects.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python, shell, and environment configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include changes to Flask application files and environment configuration guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
