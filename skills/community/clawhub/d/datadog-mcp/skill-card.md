## Description:

Datadog MCP helps agents query Datadog observability data through Datadog's MCP Server, including logs, traces, metrics, monitors, incidents, dashboards, hosts, synthetics, and workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bcwilsondotcom](https://clawhub.ai/user/bcwilsondotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to connect an agent to Datadog for incident triage, production troubleshooting, monitor review, metric analysis, dashboard lookup, and related observability workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Datadog API and application keys can expose sensitive observability data if used with broad permissions or mishandled configuration.

Mitigation: Use least-privilege application keys, keep credentials in an approved secret store, and prefer read-only toolsets for normal troubleshooting.

Risk: An unvalidated DD_SITE value can send credentials to an unintended Datadog endpoint.

Mitigation: Use only documented Datadog site values and rotate keys if they may have been used with an untrusted site value.

Risk: The local stdio transport runs an npm package through npx and can introduce package supply-chain risk.

Mitigation: Prefer the Datadog-hosted remote MCP endpoint, or pin and review the npm package version before using local transport.

Risk: Workflow execution can change Datadog state when workflow toolsets are enabled.

Mitigation: Require explicit user approval before enabling or invoking workflow execution tools.

## Reference(s):

- [Datadog MCP Server documentation](https://docs.datadoghq.com/bits_ai/mcp_server/)
- [Datadog MCP ClawHub listing](https://clawhub.ai/bcwilsondotcom/skills/datadog-mcp)
- [Setup guide](artifact/docs/setup.md)
- [Architecture guide](artifact/docs/architecture.md)
- [API reference](artifact/references/api-reference.md)
- [Incident response runbook](artifact/references/incident-response.md)
- [Troubleshooting patterns](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DD_API_KEY and DD_APP_KEY; DD_SITE is optional for supported Datadog sites.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
