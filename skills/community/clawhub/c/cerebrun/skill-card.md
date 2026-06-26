## Description: <br>
MCP client for Cerebrun - comprehensive personal context and memory management system. Retrieve user context layers (language, projects, identity, vault), perform semantic search, manage knowledge base, and interact with LLM Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niyoseris](https://clawhub.ai/user/niyoseris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to connect an agent to Cerebrun for persistent personal context, knowledge-base search, project and goal management, and LLM Gateway conversation access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may retrieve sensitive personal context, stored keys, vault fields, or prior LLM conversations. <br>
Mitigation: Restrict agent access to higher-sensitivity context layers and require explicit confirmation before retrieving Layer 2, Layer 3, vault, identity, stored-key, or conversation-history data. <br>
Risk: Sensitive prompts or stored context may be sent through the LLM Gateway. <br>
Mitigation: Confirm the destination provider and prompt contents before using chat_with_llm, and avoid sending secrets or vault data through the gateway. <br>
Risk: A broadly available API key can expose personal memory and knowledge-base data to any agent that can invoke the skill. <br>
Mitigation: Configure CEREBRUN_API_KEY deliberately, scope runtime access to trusted agents, and avoid sharing the key in prompts, logs, or reusable command snippets. <br>


## Reference(s): <br>
- [Cerebrun MCP API Reference](references/REFERENCES.md) <br>
- [Cerebrun MCP endpoint](https://cereb.run/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/niyoseris/cerebrun) <br>
- [Publisher profile](https://clawhub.ai/user/niyoseris) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON-RPC examples, shell commands, and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Cerebrun API key supplied through CEREBRUN_API_KEY or an explicit --api-key argument.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
