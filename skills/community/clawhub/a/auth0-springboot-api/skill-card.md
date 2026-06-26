## Description: <br>
Helps developers secure Spring Boot REST API endpoints with Auth0 JWT bearer validation, scope-based authorization, and optional DPoP proof-of-possession support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Auth0 for Spring Boot REST APIs, add the Auth0 SDK dependency, define security filters, enforce scopes, and test protected endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated setup could create or configure an Auth0 API resource in the wrong tenant. <br>
Mitigation: Confirm the Auth0 CLI is logged into the intended tenant and review local configuration changes before using automated setup. <br>
Risk: Auth0 access tokens, client secrets, or tenant credentials could be exposed during setup or testing. <br>
Mitigation: Use placeholders in examples and keep real secrets out of source control, shell history, CI logs, screenshots, and chat transcripts. <br>
Risk: Incorrect endpoint or scope configuration could weaken API authorization. <br>
Mitigation: Review generated Spring Security configuration, verify audience and scope requirements, and test public and protected endpoints before deployment. <br>


## Reference(s): <br>
- [Auth0 Spring Boot API Setup Guide](artifact/references/setup.md) <br>
- [Auth0 Spring Boot API Integration Patterns](artifact/references/integration.md) <br>
- [API Reference & Testing](artifact/references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/auth0/auth0-springboot-api) <br>
- [OpenClaw Homepage](https://github.com/auth0/agent-skills) <br>
- [Auth0 SDK Repository](https://github.com/auth0/auth0-auth-java) <br>
- [Auth0 Java Spring Security API Quickstart](https://auth0.com/docs/quickstart/backend/java-spring-security5) <br>
- [Spring Security Documentation](https://docs.spring.io/spring-security/reference/) <br>
- [DPoP RFC 9449](https://datatracker.ietf.org/doc/html/rfc9449) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Java, YAML, XML, Groovy, properties, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Auth0 CLI commands and local Spring Boot configuration changes for the user's project.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
