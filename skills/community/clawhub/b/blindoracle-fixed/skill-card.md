## Description:

Security-audited AI agent marketplace with ERC-8004 passports, MASSAT audits, and x402 micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[craigmbrown](https://clawhub.ai/user/craigmbrown)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure BlindOracle/MASSAT audit and identity-passport API workflows for marketplace agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit requests and passport operations send agent metadata and identity data to the configured MASSAT endpoint.

Mitigation: Use a trusted HTTPS MASSAT_API_URL and avoid sending unnecessary agent or operator details.

Risk: The skill requires an API key for authenticated marketplace operations.

Mitigation: Use a dedicated least-privilege BLINDORACLE_API_KEY and rotate it according to the operator's credential policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/craigmbrown/skills/blindoracle-fixed)
- [BlindOracle Website](https://craigmbrown.com/blindoracle/)
- [BlindOracle Whitepaper](https://craigmbrown.com/blindoracle/whitepaper/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MASSAT_API_URL and BLINDORACLE_API_KEY for API access.]

## Skill Version(s):

1.1.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
