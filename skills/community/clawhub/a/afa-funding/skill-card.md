## Description:

Discover Angels for Agents funding opportunities, assess an agent-led venture's readiness, prepare and validate an AFA pitch, submit an explicitly authorized application, or report an existing Proof Grant milestone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomrikert](https://clawhub.ai/user/tomrikert)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, AI agents, and accountable controllers use this skill to find Angels for Agents funding resources, prepare truthful pitches, validate eligibility, submit authorized applications, and report Proof Grant milestones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may submit funding applications or milestone reports to Angels for Agents.

Mitigation: Show the exact payload, destination, expected external effect, and relevant terms before obtaining explicit authorization in the current interaction.

Risk: Applications or reports could include credentials, regulated personal data, or confidential third-party information.

Mitigation: Review final submissions carefully and exclude credentials, identity documents, regulated personal data, private prompts, chain-of-thought, and confidential third-party information.

Risk: A validation pass, receipt, or referral code could be mistaken for acceptance, funding, or investment availability.

Mitigation: Describe validation and receipts only as readiness or delivery signals unless Angels for Agents' live response states a funding outcome.

## Reference(s):

- [Angels for Agents MCP server](https://angelsforagents.com/api/v1/mcp)
- [Angels for Agents agent-readable documentation](https://angelsforagents.com/llms.txt)
- [Angels for Agents OpenAPI specification](https://angelsforagents.com/openapi.json)
- [ClawHub skill page](https://clawhub.ai/tomrikert/skills/afa-funding)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Configuration]

**Output Format:** [Markdown guidance with structured API payloads and receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit controller authorization before consequential submissions or milestone reports.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
