## Description:

Implement secure API design patterns including authentication, authorization, input validation, rate limiting, and protection against common API vulnerabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when designing, securing, or reviewing APIs across authentication, authorization, input validation, rate limiting, data protection, monitoring, and common API vulnerability controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The refresh-token example stores raw refresh tokens directly, which could create replayable session tokens if copied into a real application.

Mitigation: Review and revise refresh-token implementations before use; prefer hashed or HMACed opaque refresh tokens, token rotation, revocation, and replay detection.

Risk: The skill provides general API security guidance that may not fully fit a specific production threat model or compliance environment.

Mitigation: Treat the guidance as a starting checklist and validate controls through application-specific security review, testing, and audit requirements.

## Reference(s):

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [Express Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
- [Node.js Security Checklist](https://blog.risingstack.com/node-js-security-checklist/)
- [API Security Checklist](https://github.com/shieldfy/API-Security-Checklist)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration, shell commands]

**Output Format:** [Markdown guidance with inline JavaScript, configuration examples, shell commands, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes security review checklists and implementation examples for REST, GraphQL, and WebSocket APIs.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
