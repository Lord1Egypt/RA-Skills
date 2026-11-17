## Description:

REST API reference for 147 services, including authentication patterns, endpoints, rate limits, and common gotchas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbrown4123](https://clawhub.ai/user/mbrown4123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when integrating third-party APIs and need concise reference material for authentication, endpoints, pagination, rate limits, and common implementation mistakes. The skill is documentation-only and does not store credentials, make API calls automatically, or access external services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential examples may be copied into commands or code in ways that expose secrets, especially when credentials are placed in URLs or query strings.

Mitigation: Use environment variables or secret stores, prefer header-based authentication, avoid query-string credentials, and review generated commands before execution.

Risk: Some referenced APIs support write, delete, posting, payment, or crypto-transfer actions that can change external systems or move value.

Mitigation: Require explicit user approval, use least-privilege credentials, prefer sandbox or test modes, and confirm target account and environment before running commands.

Risk: Password-grant or broad credential examples may be inappropriate for general integrations.

Mitigation: Prefer provider-recommended OAuth, client-credentials, or scoped token flows and avoid password-grant examples unless the provider and user context explicitly require them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mbrown4123/skills/api-tmp)
- [Skill homepage](https://clawic.com/skills/api)
- [API skill overview](artifact/SKILL.md)
- [Setup guidance](artifact/setup.md)
- [Authentication traps](artifact/auth.md)
- [Credential naming](artifact/credentials.md)
- [Resilience patterns](artifact/resilience.md)
- [Webhook patterns](artifact/webhooks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reference guidance with API tables, credential naming conventions, and curl examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; examples should be adapted by the agent and run only with user-provided credentials and approval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
