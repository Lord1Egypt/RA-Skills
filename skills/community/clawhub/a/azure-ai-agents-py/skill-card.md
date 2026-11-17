## Description:

Build AI agents using the Azure AI Agents Python SDK (azure-ai-agents). Use when creating agents hosted on Azure AI Foundry with tools (File Search, Code Interpreter, Bing Grounding, Azure AI Search, Function Calling, OpenAPI, MCP), managing threads and messages, implementing streaming responses, or working with vector stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegovind](https://clawhub.ai/user/thegovind)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill for guidance when building Azure AI Foundry agents with the Azure AI Agents Python SDK, including hosted agent workflows, SDK installation, authentication, tool use, streaming, file operations, vector stores, async patterns, and response formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes calculator examples that use unrestricted Python eval in agent tool implementations.

Mitigation: Replace eval-based examples with a restricted parser or safe math library before using the pattern in production code.

Risk: Generated agent code may automatically execute tools that modify data, call external APIs, spend money, or access sensitive resources.

Mitigation: Validate tool arguments and require explicit approval before invoking high-impact tools.

Risk: DefaultAzureCredential may select an unintended Azure identity in the runtime environment.

Mitigation: Verify the identity chain and selected credentials before deploying generated code.

Risk: File upload and vector store examples may send sensitive files to Azure services.

Mitigation: Upload only files intended for Azure processing and review data sensitivity before ingestion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thegovind/skills/azure-ai-agents-py)
- [Azure AI Agents SDK Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [Tools Reference](artifact/references/tools.md)
- [Streaming Reference](artifact/references/streaming.md)
- [Async Patterns Reference](artifact/references/async-patterns.md)
- [Azure SDK for Python Repository](https://github.com/Azure/azure-sdk-for-python)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for generating or reviewing Azure AI Agents Python SDK usage.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
