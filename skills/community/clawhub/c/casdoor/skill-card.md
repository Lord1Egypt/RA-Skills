## Description:

Casdoor API Assistant helps agents identify Casdoor API endpoints, generate curl, JavaScript, and Python request examples, and debug Casdoor authentication, OIDC, and API issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y-victor](https://clawhub.ai/user/y-victor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose appropriate Casdoor REST, Swagger, OpenAPI, and OIDC endpoints, then produce request examples or troubleshoot authentication and API failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Casdoor requests may expose OAuth secrets, refresh tokens, passwords, or access tokens when copied into URLs or logs.

Mitigation: Review each generated request before use and keep real secrets in environment variables, secret stores, or request bodies where supported.

Risk: The skill covers privileged administrative endpoint families such as delete, payment, token, session, impersonation, MFA, and user-management operations.

Mitigation: Use generated examples for these endpoints only with explicit authorization and confirm the target deployment, tenant, and permissions before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/y-victor/skills/casdoor)
- [Endpoint Index](artifact/references/endpoint-index.md)
- [API Groups](artifact/references/api-groups.md)
- [Example Patterns](artifact/references/example-patterns.md)
- [Auth And Debugging](artifact/references/auth-and-debugging.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown with inline curl, JavaScript, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholders for deployment hosts, tokens, and tenant-specific values unless the user provides concrete values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
