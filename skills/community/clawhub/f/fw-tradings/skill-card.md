## Description:

FW-trading helps agents manage Fosun Wealth OpenAPI credentials and route Hong Kong and U.S. stock account, cash, holdings, market data, and order operations across real and simulated trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fosunwealth](https://clawhub.ai/user/fosunwealth)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading workflow operators use this skill to prepare Fosun Wealth OpenAPI credentials, inspect account and market information, and submit confirmed real or simulated Hong Kong and U.S. stock order actions through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys and trading credential files.

Mitigation: Treat fosun.env and its backups as sensitive trading credentials and restrict access to systems and users that need them.

Risk: Real trading authority can affect live accounts.

Mitigation: Require the user to explicitly choose real trading and confirm order creation, modification, or cancellation before running those actions.

Risk: The installer and SDK source are review-worthy supply-chain surfaces.

Mitigation: Audit or harden the installer first, prefer preinstalling uv, verify the Fosun SDK source, and use custom SDK or base URLs only when you control them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fosunwealth/skills/fw-tradings)
- [Credential management flow](fosun-env-setup/reference/credential-management-flow.md)
- [uv documentation](https://docs.astral.sh/uv/)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured script-output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may guide credential setup and trading workflows, including operations that require explicit user confirmation.]

## Skill Version(s):

2.0.3 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
