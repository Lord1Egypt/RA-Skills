## Description:

ClawMon checks MCP skills for multi-tier trust scores, staking, sybil resistance, and attestation signals to guide secure skill usage decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drewm33](https://clawhub.ai/user/drewm33)

### License/Terms of Use:


## Use Case:

Developers and agents use ClawMon to check MCP skill trust, staking, sybil-resistance, and attestation signals before deciding whether to use a skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trust lookups go to a publisher-operated ClawMon API and may reveal which skill IDs are queried.

Mitigation: Query only when a trust check is needed, limit requests to the requested skill IDs, and disclose the publisher-operated API dependency to users when relevant.

Risk: The optional feedback endpoint can send a skill ID, pseudonymous reviewer address, and numeric score.

Mitigation: Submit feedback only when the user explicitly requests it and use a pseudonymous identifier rather than personal or credential-like data.

## Reference(s):

- [ClawMon Skill Page](https://clawhub.ai/drewm33/skills/clawmon)
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [Monad](https://monad.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with HTTPS request examples and JSON field summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON returned by the ClawMon API when an agent performs a requested lookup.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
