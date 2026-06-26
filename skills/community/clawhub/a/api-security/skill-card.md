## Description: <br>
Guides agents through secure API design patterns for authentication, authorization, input validation, rate limiting, and protection against common API vulnerabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brandonwise](https://clawhub.ai/user/brandonwise) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when designing, implementing, reviewing, or hardening REST, GraphQL, and WebSocket APIs. It helps produce practical guidance, code examples, middleware patterns, and checklists for authentication, authorization, validation, rate limiting, and OWASP API Top 10 concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code snippets may be copied into production without adapting authentication, token storage, rate limits, or authorization behavior to the target system. <br>
Mitigation: Review, test, and adapt each example before production deployment, with particular attention to secrets, token lifetimes, refresh-token storage, rate-limit keys, and object-level authorization checks. <br>
Risk: Documentation-only security guidance can be incomplete for an application's specific threat model or regulatory requirements. <br>
Mitigation: Pair the guidance with application-specific security review, dependency updates, vulnerability scanning, and audit preparation before relying on it for production controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brandonwise/api-security) <br>
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/) <br>
- [JWT Best Current Practices](https://tools.ietf.org/html/rfc8725) <br>
- [Express Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html) <br>
- [API Security Checklist](https://github.com/shieldfy/API-Security-Checklist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript code examples, configuration snippets, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples should be reviewed and adapted before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
