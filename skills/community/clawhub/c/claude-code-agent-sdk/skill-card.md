## Description: <br>
Claude Agent SDK documentation — build production AI agents with Claude Code as a library in Python or TypeScript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as a Claude Code Agent SDK reference when building, configuring, or debugging Python and TypeScript agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples may involve powerful agent tool settings such as Bash access, MCP tool wildcards, or bypass-style permission modes. <br>
Mitigation: Prefer narrow allowlists, block risky tools by default, and use bypass-style modes only in isolated environments. <br>
Risk: SDK agents may require API tokens or other sensitive credentials. <br>
Mitigation: Store credentials in secret managers or environment variables, avoid hardcoding tokens, and limit credential scope and lifetime. <br>
Risk: Telemetry exports and session JSONL records can contain sensitive prompts, tool outputs, or file context. <br>
Mitigation: Treat logs and session files as sensitive records, restrict access, and redact or retain them according to policy. <br>
Risk: Guidance copied from reference examples can be misapplied in production agent deployments. <br>
Mitigation: Review configurations before use, set max turn and budget limits, and deploy agents in sandboxed or containerized environments. <br>


## Reference(s): <br>
- [SDK overview](references/overview.md) <br>
- [Quickstart](references/quickstart.md) <br>
- [Agent loop](references/agent-loop.md) <br>
- [Permissions](references/permissions.md) <br>
- [Custom tools](references/custom-tools.md) <br>
- [MCP integration](references/mcp.md) <br>
- [Sessions](references/sessions.md) <br>
- [Hosting and deployment](references/hosting.md) <br>
- [Cost tracking](references/cost-tracking.md) <br>
- [Python API reference](references/python.md) <br>
- [TypeScript API reference](references/typescript.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reference guidance with Python and TypeScript code examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no executable scripts are included in the artifact.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
