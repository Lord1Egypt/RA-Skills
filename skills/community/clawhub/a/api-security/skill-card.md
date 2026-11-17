## Description:

Helps developers apply API security practices for authentication, authorization, input validation, rate limiting, and protection against common API vulnerabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandonwise](https://clawhub.ai/user/brandonwise)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when designing, implementing, or reviewing REST, GraphQL, or WebSocket APIs that need authentication, authorization, validation, rate limiting, secure headers, and OWASP API Top 10 coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JWT example stores refresh tokens directly, which could weaken an application if copied into production.

Mitigation: Store only refresh-token hashes, rotate refresh tokens, support revocation, and use secure browser cookie handling where appropriate.

Risk: The skill provides security guidance and code examples that may need adaptation to the user's framework, threat model, and compliance requirements.

Mitigation: Review examples with application-specific security requirements before deployment and validate implementation choices through security testing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brandonwise/skills/api-security)
- [Publisher Profile](https://clawhub.ai/user/brandonwise)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [Express Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
- [API Security Checklist](https://github.com/shieldfy/API-Security-Checklist)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JavaScript code examples, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; examples should be reviewed before production use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
