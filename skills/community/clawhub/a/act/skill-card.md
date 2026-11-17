## Description:

Act lets an agent search Shenzhen-area activities, view activity details and schedules, and create public activity listings through the fore.vip MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onsoul](https://clawhub.ai/user/onsoul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users connect this skill to an MCP-capable assistant to find Shenzhen-area activities, inspect details and schedules, and publish single or batch public activity records when they provide an API key.

### Deployment Geography for Use:

Shenzhen, China (CN-SZ)

## Known Risks and Mitigations:

Risk: The skill can publish multiple public activity listings from web-sourced details and images without a clear final per-item approval flow.

Mitigation: Review each candidate, source, image rights, address, and time before creation; require explicit approval for each item in bulk publishing flows.

Risk: The creation API key authorizes publishing public activity records through the fore.vip service.

Mitigation: Install only when the fore.vip service is trusted, request the API key only for the current creation flow, and avoid storing it.

Risk: Activity detail lookups increment view counts.

Mitigation: Avoid repeated detail calls unless the user needs a fresh activity detail response.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/onsoul/skills/act)
- [Publisher profile](https://clawhub.ai/user/onsoul)
- [MCP service](https://mcp.fore.vip)
- [MCP server endpoint](https://mcp.fore.vip/act/mcp)
- [fore.vip project site](https://fore.vip)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with MCP tool-call results, progress summaries, activity links, and installation commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Activity creation requires an X-API-Key and a public cover image URL; detail lookups increment activity view counts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
