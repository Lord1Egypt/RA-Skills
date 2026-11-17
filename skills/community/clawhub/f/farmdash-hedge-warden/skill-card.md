## Description:

Use when sizing a hedge for existing DeFi exposure: delta-neutral recommendations with explicit bounds and risk notes. Advisory only; never trades itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and DeFi users use the skill to size a hedge for existing spot exposure, review funding and basis risks, and prepare a plan for a separate execution workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio exposure may be sent to FarmDash when requesting a hedge recommendation.

Mitigation: Review FarmDash's security information and share only exposure details you are comfortable disclosing.

Risk: The security scan was partial, so some references were not covered.

Mitigation: Review the linked security information and unresolved references before installation.

Risk: Funding, basis, liquidity, and venue risks can leave a hedge ineffective or costly.

Mitigation: Check existing positions, instrument correlation, funding, and liquidity; verify fills and residual exposure and define an unwind for failed legs.

Risk: A hedge recommendation could be mistaken for execution approval or authority.

Mitigation: Treat the output as advisory and require the separate futures workflow's research and applicable human approval or owner grant before execution.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-hedge-warden)
- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical FarmDash Hedge Warden manual](https://www.farmdash.one/openclaw-skills/farmdash-hedge-warden/SKILL.md)
- [FarmDash integration documentation](https://www.farmdash.one/docs)
- [FarmDash OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [FarmDash security and authority boundaries](https://www.farmdash.one/security)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Text]

**Output Format:** [Structured hedge recommendation with per-asset legs, checks, and handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory only; the skill does not sign or submit orders.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
