## Description: <br>
Build Azure AI Foundry agents using the Microsoft Agent Framework Python SDK (agent-framework-azure-ai). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegovind](https://clawhub.ai/user/thegovind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build persistent Azure AI Foundry agents in Python with hosted tools, MCP integrations, conversation threads, streaming responses, and structured outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples use powerful Azure-hosted tools, including code execution, file search, web search, and MCP integrations. <br>
Mitigation: Review generated code before use, restrict allowed tools, and require approval for sensitive MCP actions. <br>
Risk: Agent examples may handle Azure identities, tokens, prompts, or uploaded files. <br>
Mitigation: Confirm the Azure project and identity, keep tokens out of source code, and avoid uploading private files or prompts unless approved. <br>
Risk: Unpinned SDK versions can change behavior for generated implementations. <br>
Mitigation: Pin SDK versions before running copied examples in controlled or production environments. <br>


## Reference(s): <br>
- [Agent Framework repository](https://github.com/microsoft/agent-framework) <br>
- [Hosted Tools Reference](references/tools.md) <br>
- [MCP Integration Reference](references/mcp.md) <br>
- [Thread and Conversation Management](references/threads.md) <br>
- [Advanced Patterns Reference](references/advanced.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and bash code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for Azure AI Foundry agent implementation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
