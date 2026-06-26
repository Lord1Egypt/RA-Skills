## Description: <br>
Build AI agents using the Azure AI Agents Python SDK (azure-ai-agents). Use when creating agents hosted on Azure AI Foundry with tools (File Search, Code Interpreter, Bing Grounding, Azure AI Search, Function Calling, OpenAPI, MCP), managing threads and messages, implementing streaming responses, or working with vector stores. This is the low-level SDK - for higher-level abstractions, use the agent-framework skill instead. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegovind](https://clawhub.ai/user/thegovind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build Azure AI Foundry agents with the Azure AI Agents Python SDK, including tool integration, threads, messages, runs, streaming responses, async clients, files, and vector stores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copyable function-tool examples include unsafe Python eval() behavior that could execute arbitrary local code if used directly. <br>
Mitigation: Replace eval()-based examples with a restricted math parser or explicit validated operations before using them in real agent code. <br>
Risk: Azure agent examples may access cloud resources, uploaded files, vector stores, or connected tools with the privileges of the configured credentials. <br>
Mitigation: Use least-privilege Azure credentials, avoid uploading secrets or regulated data, and clean up agents, files, and vector stores after experiments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thegovind/azure-ai-agents-py) <br>
- [Azure SDK for Python repository](https://github.com/Azure/azure-sdk-for-python) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [Tools reference](references/tools.md) <br>
- [Streaming reference](references/streaming.md) <br>
- [Async patterns reference](references/async-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Azure SDK examples for authentication, agent lifecycle, tool use, streaming, async workflows, file operations, and vector stores.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
