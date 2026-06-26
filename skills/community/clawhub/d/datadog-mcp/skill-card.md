## Description: <br>
Datadog MCP connects agents to Datadog's official MCP Server to query logs, traces, metrics, monitors, incidents, dashboards, hosts, synthetics, and workflows using remote HTTP or local stdio transports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bcwilsondotcom](https://clawhub.ai/user/bcwilsondotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site reliability engineers, and incident responders use this skill to connect an agent to Datadog observability data, investigate production issues, correlate logs, traces, and metrics, check monitors, and review incident context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Datadog API and application keys can expose production observability data. <br>
Mitigation: Install only for trusted agents and environments, and use a dedicated least-privilege Datadog application key. <br>
Risk: Enabled workflow tooling may allow an agent to trigger Datadog automations. <br>
Mitigation: Enable only the Datadog MCP toolsets needed for the deployment and avoid workflow execution unless that behavior is intended. <br>
Risk: Returned logs, traces, host details, and incident data may contain sensitive operational information. <br>
Mitigation: Treat Datadog MCP responses as sensitive and limit sharing, retention, and downstream use according to the deployment's data-handling policy. <br>


## Reference(s): <br>
- [ClawHub Datadog MCP Skill](https://clawhub.ai/bcwilsondotcom/datadog-mcp) <br>
- [Datadog MCP Server Documentation](https://docs.datadoghq.com/bits_ai/mcp_server/) <br>
- [Datadog MCP Server Endpoint](https://mcp.datadoghq.com/api/unstable/mcp-server/mcp) <br>
- [Setup Guide](docs/setup.md) <br>
- [Architecture](docs/architecture.md) <br>
- [API Reference](references/api-reference.md) <br>
- [Incident Response Runbook](references/incident-response.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses may include Datadog query guidance, MCP setup commands, validation steps, and observability investigation summaries.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
