## Description:

Connects agents to 100+ third-party APIs through Maton's managed OAuth API gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larry-at](https://clawhub.ai/user/larry-at)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to make native API calls to supported SaaS and productivity services through Maton's gateway after the user has authorized the relevant service connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broker broad API authority across many connected services.

Mitigation: Use it only where Maton is trusted, grant the narrowest OAuth or API scopes possible, and require explicit confirmation before destructive or administrative actions.

Risk: Credential, authorization header, connection response, or connect-session URL exposure could leak access.

Mitigation: Do not print, paste, log, or share MATON_API_KEY values, Authorization headers, raw connection responses, or connect.maton.ai session URLs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/larry-at/skills/api-gateway-1-0-64)
- [Maton Homepage](https://maton.ai)
- [Maton API Reference](https://www.maton.ai/docs/api-reference)
- [Provider Routing Guides](artifact/references/)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; results depend on user-authorized third-party OAuth connections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
