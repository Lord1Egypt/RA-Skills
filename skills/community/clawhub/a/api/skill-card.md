## Description:

Helps agents integrate and debug third-party REST and GraphQL APIs, covering authentication, rate limits, pagination, webhooks, resilience patterns, and service-specific gotchas for 147 services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when consuming third-party APIs, diagnosing failed requests, selecting authentication and retry patterns, verifying webhooks, handling streaming or file transfers, and shaping safe example calls across common providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist inferred API preferences and context under ~/Clawic/data/api/, which can become sensitive or stale if users place account identifiers, credentials, or confidential request details there.

Mitigation: Review that directory periodically, keep credentials and confidential payloads out of stored preferences, and remove stale assumptions before relying on generated API guidance.

Risk: Copyable API examples can expose credentials through logs or trigger financial, public, deletion, posting, moderation, or crypto side effects if run against live services.

Mitigation: Use sandbox or scoped temporary credentials for examples, keep secrets in environment variables, avoid unredacted verbose logs, and require explicit confirmation before live side-effecting actions.

## Reference(s):

- [API / Application Programming Interface on ClawHub](https://clawhub.ai/ivangdavila/skills/api)
- [ivangdavila publisher profile](https://clawhub.ai/user/ivangdavila)
- [Clawic API skill homepage](https://clawic.com/skills/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples reference environment variables for credentials and may adapt to user preferences stored under ~/Clawic/data/api/.]

## Skill Version(s):

1.3.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
