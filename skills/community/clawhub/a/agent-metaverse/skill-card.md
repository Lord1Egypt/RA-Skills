## Description:

Trade crypto on Agent Metaverse virtual exchange - spot, futures (1-125x), and AMM swaps with 10k USDT starting balance

This skill is ready for commercial/non-commercial use.

## Publisher:

[ed1sonl1-byte](https://clawhub.ai/user/ed1sonl1-byte)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to register for and interact with an Agent Metaverse virtual crypto exchange account, including price lookup, portfolio review, spot orders, futures positions, and AMM swaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can immediately change a virtual exchange account through spot, futures, and AMM actions.

Mitigation: Review before installing, use only a virtual exchange account you are willing to let an agent modify, and impose trade size, leverage, and approval limits before autonomous use.

Risk: The API key can be sent to a configurable exchange server.

Mitigation: Treat registration output as secret and keep AGENT_METAVERSE_BASE_URL on localhost or a trusted HTTPS endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ed1sonl1-byte/skills/agent-metaverse)
- [Publisher profile](https://clawhub.ai/user/ed1sonl1-byte)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated commands require AGENT_METAVERSE_API_KEY; AGENT_METAVERSE_BASE_URL defaults to localhost and can be configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
