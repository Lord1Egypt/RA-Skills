## Description:

A comprehensive guide and reference for building agents using LangGraph 1.0, including ReAct agents, state graphs, and tool integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luochang212](https://clawhub.ai/user/luochang212)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as a Chinese-language tutorial and reference for building LangGraph agents, workflows, middleware, memory, MCP integrations, supervisor patterns, RAG, and web search examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may send user content or file-derived content to external model and search providers.

Mitigation: Require user consent, redact sensitive data, and review provider configuration before running examples.

Risk: Examples rely on .env API keys for external services.

Mitigation: Keep secrets out of source control, use local secret management, and rotate any exposed keys.

Risk: Local-file context examples can be unsafe when pointed at untrusted paths.

Mitigation: Run demos in an isolated environment and restrict file paths to reviewed tutorial data.

Risk: Prompt-only or tutorial-level authorization checks may be insufficient for production use.

Mitigation: Add real application authorization checks before adapting the examples to production systems.

Risk: Tutorial dependency versions may drift or introduce behavior changes.

Mitigation: Pin dependencies and review examples before reuse.

## Reference(s):

- [Dive Into LangGraph ClawHub page](https://clawhub.ai/luochang212/skills/dive-into-langgraph)
- [Dive Into LangGraph online documentation](https://luochang212.github.io/dive-into-langgraph/)
- [Quickstart](references/1.quickstart.md)
- [StateGraph](references/2.stategraph.md)
- [Middleware](references/3.middleware.md)
- [Human in the Loop](references/4.human_in_the_loop.md)
- [Memory](references/5.memory.md)
- [Context Engineering](references/6.context.md)
- [MCP Server](references/7.mcp_server.md)
- [Supervisor](references/8.supervisor.md)
- [Parallelization](references/9.parallelization.md)
- [RAG](references/10.rag.md)
- [Web Search](references/11.web_search.md)
- [LangGraph official documentation](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangChain official documentation](https://docs.langchain.com/oss/python/langchain/overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language tutorial content with examples that may use local environment variables and external LLM or search providers.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
