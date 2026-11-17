## Description:

Use when composing multi-step DeFi workflows from FarmDash tools: plan, run, inspect supervised pipelines. Wallet steps stay policy-gated, preview-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use named workflow recipes to plan multi-step DeFi tasks, check required skills and confirmations, and track supervised workflow runs. Any state-changing action is handed to a separately installed skill under its own authorization gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional setup can disclose a public wallet address, and optional installation analytics can correlate FarmDash skill usage.

Mitigation: Use setup only when needed and agreed; skip optional attribution when it is not wanted.

Risk: FarmDash API and session tokens can expose account capabilities if disclosed.

Mitigation: Protect API and session tokens, and do not treat session credentials as transaction authority.

Risk: A workflow may hand state-changing steps to companion skills, while this artifact review does not verify live backend safeguards.

Mitigation: Review the relevant execution skills and delegation grant separately, and rely on their authorization and confirmation checks.

## Reference(s):

- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical FarmDash Trail Marshal manual](https://www.farmdash.one/openclaw-skills/farmdash-trail-marshal/SKILL.md)
- [FarmDash agent integration documentation](https://www.farmdash.one/docs)
- [FarmDash OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)
- [FarmDash live agent capability status](https://www.farmdash.one/api/v1/agent/status)
- [FarmDash security and authority boundaries](https://www.farmdash.one/security)
- [ClawHub skill release page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-trail-marshal)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured workflow catalog, quality-gate plans, and run status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Named recipe metadata; wallet-changing actions remain with separately installed skills.]

## Skill Version(s):

0.1.11 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
