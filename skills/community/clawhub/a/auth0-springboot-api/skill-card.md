## Description:

Helps developers secure Spring Boot REST APIs with Auth0 JWT access-token validation, scope-based authorization, and optional DPoP proof-of-possession using com.auth0:auth0-springboot-api.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auth0](https://clawhub.ai/user/auth0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Auth0-backed Spring Boot API authentication, authorization scopes, DPoP settings, and endpoint verification. It is intended for API services that receive access tokens from frontends, mobile apps, or machine clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated setup can create an Auth0 API resource and write application.yml in the user's project.

Mitigation: Require an explicit user choice before automated setup and review the generated Auth0 domain, audience, and Spring configuration before running the service.

Risk: Example token requests include client_secret fields that could lead users to paste real secrets into shared prompts, files, or logs.

Mitigation: Use only secrets from the user's own Auth0 tenant when requesting a test token, avoid storing them in examples, and prefer environment-specific secret handling.

Risk: Example error-handling code can return raw exception messages to API clients.

Mitigation: Review generated error responses and replace raw exception details with sanitized messages before production use.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Integration Guide](references/integration.md)
- [API Reference](references/api.md)
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills)
- [Auth0 Java Spring Security API Quickstart](https://auth0.com/docs/quickstart/backend/java-spring-security5)
- [Auth0 Auth Java SDK Repository](https://github.com/auth0/auth0-auth-java)
- [Spring Security Documentation](https://docs.spring.io/spring-security/reference/)
- [Auth0 Access Tokens Guide](https://auth0.com/docs/secure/tokens/access-tokens)
- [DPoP RFC 9449](https://datatracker.ietf.org/doc/html/rfc9449)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Java, YAML, properties, XML, Groovy, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Spring Boot configuration files when the user chooses automated setup.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
