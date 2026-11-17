## Description:

Adds Auth0 login, logout, callback handling, and session-based authentication guidance for Java Servlet web applications using com.auth0:mvc-auth-commons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Auth0 Regular Web Application login flows to Java Servlet apps, configure mvc-auth-commons, and generate servlet and filter code for login, callback, logout, protected routes, Organizations, and custom domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-paste authentication examples may create weaker login security if used without review.

Mitigation: Review generated authentication code before production use and require session ID rotation immediately after successful callback validation.

Risk: Callback and logout URLs derived from untrusted request data can lead to incorrect redirects or host-header related issues.

Mitigation: Derive callback and logout base URLs from trusted configuration and keep exact Auth0 callback and logout allowlists.

Risk: Auth0 client secrets may be written to local files during setup.

Mitigation: Write secrets only to user-approved locations, ensure .env is gitignored, and use production secret management outside local development.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Integration Guide](references/integration.md)
- [API Reference](references/api.md)
- [Auth0 Agent Skills Repository](https://github.com/auth0/agent-skills)
- [Auth0 Java MVC Common SDK Repository](https://github.com/auth0/auth0-java-mvc-common)
- [Auth0 Java Web App Quickstart](https://auth0.com/docs/quickstart/webapp/java)
- [Auth0 Universal Login](https://auth0.com/docs/authenticate/login/auth0-universal-login)
- [Authorization Code Flow](https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow)
- [Auth0 Organizations](https://auth0.com/docs/manage-users/organizations)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Java, XML, Gradle, Maven, properties, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dependency snippets, Auth0 CLI commands, environment variable configuration, servlet code, and security guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
