## Description: <br>
Use when adding Auth0 login, logout, and callback handling to Java Servlet web applications - integrates com.auth0:mvc-auth-commons SDK for server-side Java apps using javax.servlet with session-based authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Auth0 Regular Web Application login, logout, callback handling, and session-based route protection to Java Servlet web applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to handle Auth0 domains, client IDs, client secrets, and OAuth-related credentials. <br>
Mitigation: Keep provider secrets in environment variables or managed secret stores, ensure generated .env files are ignored by version control, and review outputs before committing. <br>
Risk: The skill may propose Auth0 CLI actions, dependency changes, and environment variable writes. <br>
Mitigation: Review package installs, provider CLI commands, application URI changes, and configuration writes before approving execution. <br>


## Reference(s): <br>
- [Auth0 Java MVC Common Skill](https://clawhub.ai/auth0/auth0-java-mvc-common) <br>
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills) <br>
- [Auth0 Java Web App Quickstart](https://auth0.com/docs/quickstart/webapp/java) <br>
- [Auth0 Java MVC Common SDK Repository](https://github.com/auth0/auth0-java-mvc-common) <br>
- [Auth0 Universal Login](https://auth0.com/docs/authenticate/login/auth0-universal-login) <br>
- [Authorization Code Flow](https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow) <br>
- [Auth0 Organizations](https://auth0.com/docs/manage-users/organizations) <br>
- [Setup Guide](references/setup.md) <br>
- [Integration Guide](references/integration.md) <br>
- [API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Java, XML, Gradle, properties, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Auth0 CLI actions and environment variable changes that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
