## Description: <br>
Implements agents using Deep Agents. Use when building agents with create_deep_agent, configuring backends, defining subagents, adding middleware, or setting up human-in-the-loop workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for implementation guidance when creating Deep Agents with custom models, tools, backends, subagents, persistence, MCP integrations, and human approval flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deep Agents can be configured to read and write real files or run shell commands. <br>
Mitigation: Keep filesystem roots narrow, test in disposable directories before production use, and require approval for shell commands and file writes. <br>
Risk: Persistence, MCP servers, and external tools can expose credentials or retain user data if configured loosely. <br>
Mitigation: Store secrets in environment variables or secret managers, verify MCP command and environment configuration, and define how persistent memories are scoped and cleared. <br>
Risk: Human-in-the-loop workflows may proceed without intended review if interrupts, checkpointers, or thread IDs are misconfigured. <br>
Mitigation: Configure a checkpointer and thread ID for interrupting flows, then test pause and resume behavior before relying on the workflow. <br>


## Reference(s): <br>
- [Common Patterns](references/patterns.md) <br>
- [Built-in Tools Reference](references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration, shell commands] <br>
**Output Format:** [Markdown with Python code examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes implementation gates for disk access, interrupts, persistence, and MCP subprocess setup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
