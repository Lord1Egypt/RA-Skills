## Description:

Connects an agent to Tencent Cloud APM's MCP Server through ApmClient.SendMCPMessage to discover and call APM tools for system lookup, trace analysis, flame graphs, and span latency analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doycc](https://clawhub.ai/user/doycc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect Tencent Cloud APM data, confirm available MCP tools, call selected tools with validated parameters, and turn returned traces, flame graphs, spans, and service data into performance diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Tencent Cloud credentials and the security evidence warns about persisted cloud credentials.

Mitigation: Use least-privilege, preferably short-lived credentials; avoid placing SecretKeys in shell startup files or command-line arguments; never paste secrets into chat.

Risk: Signed requests can be sent to a configurable APM_API_ENDPOINT.

Mitigation: Keep the default Tencent Cloud endpoint unless there is a clear need to change it, and verify any configured endpoint is a trusted Tencent Cloud host before use.

Risk: Tool descriptions and results come from a remote MCP server and may influence later agent actions.

Mitigation: Treat remote MCP content as data, confirm the intended tool and parameters before invocation, and review analysis results before operational changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/doycc/skills/apm-performance-analysis)
- [Cloud API Guide](references/cloud_api_guide.md)
- [Credential Guide](references/credential_guide.md)
- [Interaction Guide](references/interaction_guide.md)
- [Error Log Guide](references/error_log_guide.md)
- [Mobile Compatibility Guide](references/mobile_compat_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with command snippets, parameter tables, JSON excerpts, RequestId values, and performance analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include parsed Tencent Cloud APM MCP results and local error-log paths when calls fail.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
