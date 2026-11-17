## Description:

Guides agents and developers in authorizing Mailtrap API requests by selecting the right auth header and token scope, storing tokens safely, and resolving Mailtrap account IDs before generating API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailtrap](https://clawhub.ai/user/mailtrap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and AI agents use this skill before creating Mailtrap API calls to choose safe authentication headers, token scopes, secret storage practices, and account-scoped endpoint identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commands could run against live Mailtrap email-sending endpoints or use the wrong token scope.

Mitigation: Review generated commands before execution, keep sandbox and live tokens separate, and use the narrowest token scope that works.

Risk: Mailtrap API tokens could be exposed if copied into prompts, source files, shell history, or logs.

Mitigation: Use environment variables or managed secret stores, never hardcode or echo literal tokens, and rotate any token that is exposed.

## Reference(s):

- [Mailtrap API Tokens Documentation](https://docs.mailtrap.io/email-api-smtp/setup/api-tokens.md)
- [Mailtrap Accounts API](https://docs.mailtrap.io/developers/account-management/accounts)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses environment-variable placeholders for sensitive values and separates sandbox from live sending credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
