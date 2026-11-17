## Description:

Exact arithmetic for AI agents - zero hallucination math via 62 tools covering integer arithmetic, fractions, units, calculus, and financial calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrningslo](https://clawhub.ai/user/lrningslo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Arithym to route math-sensitive tasks to a hosted MCP service for exact arithmetic, unit conversion, calculus, financial calculations, and physics constants when approximation would be unacceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calculation inputs are sent to Arithym's hosted MCP service.

Mitigation: Use the skill only when sending those inputs to a third-party service is acceptable, and avoid confidential financial or business data unless that use has been approved.

Risk: The skill requires an ARITHYM_API_KEY in the MCP environment.

Mitigation: Store the API key in the agent or MCP secret-management path and avoid hard-coding it in shared configuration.

## Reference(s):

- [Arithym homepage](https://arithym.xyz)
- [Arithym source repository](https://github.com/Arithym-io/arithym)
- [ClawHub skill page](https://clawhub.ai/lrningslo/skills/arithym-io-arithym)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Text]

**Output Format:** [Markdown with MCP configuration JSON and tool-selection guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARITHYM_API_KEY and sends calculation inputs to the hosted Arithym MCP service.]

## Skill Version(s):

1.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
