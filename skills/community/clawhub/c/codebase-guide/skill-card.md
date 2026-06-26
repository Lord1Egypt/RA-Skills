## Description: <br>
Use for every task involving this project; it covers running Ganglion, CLI commands, the HTTP bridge API, pipeline execution, knowledge queries, configuration, and operational workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tensorlink-dev](https://clawhub.ai/user/tensorlink-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to administer Ganglion projects, run local or remote pipelines, inspect state, query knowledge, configure projects, and troubleshoot operational issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on activation can cause the agent to apply Ganglion-specific operational guidance in any task involving the project. <br>
Mitigation: Install only when the workspace is intended for Ganglion administration and confirm the current mode before running commands. <br>
Risk: The documented remote API can register tools, change agent behavior, patch pipelines, connect MCP servers, and roll back project state. <br>
Mitigation: Keep the HTTP bridge bound to localhost or otherwise strongly protected, review new tool, agent, and MCP code before registration, and avoid mutations during active runs. <br>
Risk: Pipeline execution requires OPENAI_API_KEY and may expose project context or incur model usage costs. <br>
Mitigation: Protect the API key, use trusted project directories, and verify configuration before pipeline execution. <br>
Risk: Rollback and mutation commands can alter project state. <br>
Mitigation: Commit or back up the project before mutations or rollback operations and inspect audit history before undoing changes. <br>
Risk: Shared knowledge stores can mix trusted and untrusted experiment history across bots. <br>
Mitigation: Isolate knowledge stores between trusted and untrusted experiments and use bot identifiers deliberately. <br>


## Reference(s): <br>
- [Codebase Guide on ClawHub](https://clawhub.ai/tensorlink-dev/codebase-guide) <br>
- [Ganglion Project Homepage](https://github.com/TensorLink-AI/ganglion) <br>
- [Commands & API Reference](references/commands.md) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Operations Guide](references/operations.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Common Workflows](examples/common-workflows.md) <br>
- [Sample API Requests](examples/sample-requests.md) <br>
- [Health Check Script](scripts/healthcheck.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash, curl, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are operational instructions for Ganglion CLI, HTTP bridge, configuration, health checks, and troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
