## Description: <br>
Guides developers and agents through creating or modernizing DCC-MCP adapters for Nuke, Blender, 3ds Max, Unreal, ZBrush, Houdini, Maya, and custom studio tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build or modernize DCC-MCP adapter infrastructure, including server composition, host-thread dispatch, sidecar and gateway wiring, readiness, packaging, diagnostics, and cross-DCC verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or modified adapter code may affect host integrations, gateways, relay or mDNS discovery, or durable memory in production or privacy-sensitive environments. <br>
Mitigation: Review generated adapter code before running it, keep auth and TLS policy explicit for discovery or relay paths, and disable durable memory where privacy requirements demand it. <br>
Risk: Incorrect host-thread dispatch can run DCC APIs from unsafe worker threads or block host UI behavior. <br>
Mitigation: Use the documented dispatcher patterns, route host API calls through HostExecutionBridge, and add smoke tests that prove main-affinity calls run through the host dispatcher. <br>


## Reference(s): <br>
- [DCC-MCP Creator source](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/skills/dcc-mcp-creator/SKILL.md) <br>
- [Adapter Workflow](references/ADAPTER_WORKFLOW.md) <br>
- [Host Pattern Matrix](references/HOST_PATTERN_MATRIX.md) <br>
- [Core Escalation Checklist](references/CORE_ESCALATION_CHECKLIST.md) <br>
- [Testing And Release](references/TESTING_AND_RELEASE.md) <br>
- [RFC: add adapter skill-load transform hooks](https://github.com/dcc-mcp/dcc-mcp-core/issues/1204) <br>
- [RFC: expose public DccServerBase resource registration surface](https://github.com/dcc-mcp/dcc-mcp-core/issues/1205) <br>
- [RFC: add reusable adapter readiness binder](https://github.com/dcc-mcp/dcc-mcp-core/issues/1206) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code blocks, command examples, and configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces adapter design, implementation, testing, packaging, and release guidance for DCC-MCP infrastructure.] <br>

## Skill Version(s): <br>
0.19.2 (source: SKILL.md metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
