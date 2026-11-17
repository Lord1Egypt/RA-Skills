## Description:

Use Bitquery GraphQL through UXC for onchain trades, transfers, token holder analysis, balances, and market structure queries across supported networks, with OAuth client_credentials authentication and query-first execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Bitquery GraphQL through UXC for onchain trades, transfers, token holder analysis, balances, and market structure. It guides OAuth client_credentials setup, schema inspection, query execution, and cautious subscription use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth client secrets may be exposed if pasted into shared terminals or agent transcripts.

Mitigation: Use a secure secret input method when available and rotate any secret that may have been logged.

Risk: Subscription file sinks can create persistent local records of streamed Bitquery data.

Mitigation: Store or delete subscription output according to local retention and access-control requirements.

Risk: Large or realtime GraphQL selections can return excessive data or unstable subscription behavior.

Mitigation: Start with narrow _select payloads, one network or asset at a time, and expand only after validating the response shape.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Bitquery GraphQL endpoint](https://streaming.bitquery.io/graphql)
- [Bitquery OAuth token endpoint](https://oauth2.bitquery.io/oauth2/token)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/bitquery-graphql-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell commands and JSON GraphQL payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on OAuth setup, help-first schema inspection, query-first execution, narrow selection sets, and subscription file sinks.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
