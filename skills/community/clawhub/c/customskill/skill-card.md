## Description:

Enforces mandatory use of a designated backend tool for financial transactions and prevents an agent from directly executing or simulating trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsr0705](https://clawhub.ai/user/tsr0705)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial workflow operators use this skill to require a backend tool for buy, sell, or other asset-modifying requests while avoiding tool use for analysis-only or ambiguous requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route requests toward real financial execution without clear confirmation safeguards.

Mitigation: Use only with a trusted, verified financial tool and require separate user confirmation showing asset, side, quantity, account, estimated cost, fees, and order state before any real transaction is submitted.

Risk: The tool input schema asks for agent reasoning, which may expose unnecessary private reasoning.

Mitigation: Minimize or omit private reasoning in tool payloads and retain only the transaction details needed for authorization, audit, and compliance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsr0705/skills/customskill)
- [Publisher profile](https://clawhub.ai/user/tsr0705)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown instructions with a JSON tool input schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to route financial execution requests through a named backend tool.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
