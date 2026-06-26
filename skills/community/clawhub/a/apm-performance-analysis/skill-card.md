## Description: <br>
APM performance analysis skill that connects to Tencent Cloud APM through ApmClient.SendMCPMessage to support system lookup, trace analysis, flame graph review, and Span latency analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doycc](https://clawhub.ai/user/doycc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operations engineers use this skill to inspect Tencent Cloud APM systems, discover available APM MCP operations, call selected tools, and interpret performance data such as traces, flame graphs, and Span timing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Tencent Cloud credentials and network access to Tencent Cloud APM. <br>
Mitigation: Use a least-privilege Tencent Cloud subaccount, provide credentials through environment variables, and do not paste secrets into chat. <br>
Risk: Error logs may contain operational details from failed APM requests. <br>
Mitigation: Use the documented error log location intentionally, redirect it with APM_ERROR_LOG_DIR when needed, and review log handling for sensitive operational data. <br>
Risk: Remote APM tool calls can return or analyze production telemetry depending on the selected tool and parameters. <br>
Mitigation: Confirm the tool name and arguments before execution and limit calls to the intended business system, time range, and region. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/doycc/apm-performance-analysis) <br>
- [Cloud API guide](references/cloud_api_guide.md) <br>
- [Credential guide](references/credential_guide.md) <br>
- [Error log guide](references/error_log_guide.md) <br>
- [Interaction guide](references/interaction_guide.md) <br>
- [Mobile compatibility guide](references/mobile_compat_guide.md) <br>
- [Tencent Cloud API key management](https://console.cloud.tencent.com/cam/capi) <br>
- [Tencent Cloud APM MCP service role authorization](https://console.cloud.tencent.com/cam/role/grant?roleName=APM_QCSLinkedRoleInApmMcp&serviceLinkedRole=1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-formatted APM results when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Tencent Cloud request IDs, discovered tool schemas, parsed APM responses, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
