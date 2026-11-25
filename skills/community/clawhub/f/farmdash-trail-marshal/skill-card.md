## Description:

Use when composing multi-step DeFi workflows from FarmDash tools: plan, run, inspect supervised pipelines. Wallet steps stay policy-gated and zero-custody.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

External FarmDash users and OpenClaw agent developers use Trail Marshal to find named DeFi workflow recipes, check prerequisites and confirmation gates, and track guarded workflow plans. Separate execution skills handle any wallet actions under their own authorization rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional onboarding sends a public agent wallet address to FarmDash, and scanner coverage was partial.

Mitigation: Use onboarding only when you want to check setup or tier status, share only the listed public address, and review the skill and its separately installed execution skills before authorizing wallet actions.

## Reference(s):

- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [FarmDash Trail Marshal skill manual](https://www.farmdash.one/openclaw-skills/farmdash-trail-marshal/SKILL.md)
- [FarmDash agent integration documentation](https://www.farmdash.one/docs)
- [Live agent capability status](https://www.farmdash.one/api/v1/agent/status)
- [FarmDash OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash MCP discovery manifest](https://www.farmdash.one/.well-known/mcp.json)

## Skill Output:

**Output Type(s):** [Guidance, JSON, API calls]

**Output Format:** [Workflow catalog data, guarded plan and run records, and accompanying agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planning and run records do not execute wallet actions; execution is handled by separately installed skills.]

## Skill Version(s):

0.1.12 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
