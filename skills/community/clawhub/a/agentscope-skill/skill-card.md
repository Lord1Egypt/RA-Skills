## Description: <br>
This skill guides agents through AgentScope concepts, repository navigation, API lookup, examples, multi-agent orchestration, and deployment patterns for Python agent applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxf8126275](https://clawhub.ai/user/wxf8126275) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to answer AgentScope questions, inspect APIs, select examples, and draft or adapt AgentScope code for agent applications. It is especially useful for multi-agent workflows, tool use, memory, RAG, evaluation, and deployment planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages local code execution, shell access, file access, browser automation, and repository updates. <br>
Mitigation: Require explicit approval for execution, use sandboxed workspaces, limit API keys, and avoid exposing these tools to untrusted users. <br>
Risk: Clone and pull examples can update local code from a remote repository before an agent follows examples or runs commands. <br>
Mitigation: Pin repository versions or commits and review changes before allowing an agent to execute or adapt updated code. <br>
Risk: Examples reference provider credentials such as DASHSCOPE_API_KEY. <br>
Mitigation: Use least-privilege credentials, avoid logging secrets, and keep sensitive environment variables out of shared or untrusted sessions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wxf8126275/agentscope-skill) <br>
- [AgentScope documentation](https://agentscope.ai/docs/) <br>
- [AgentScope GitHub repository](https://github.com/agentscope-ai/agentscope) <br>
- [AgentScope design discussions](https://github.com/agentscope-ai/agentscope/discussions/categories/agentscope-design-book) <br>
- [Multi-agent orchestration reference](references/multi_agent_orchestration.md) <br>
- [Deployment guide](references/deployment_guide.md) <br>
- [AgentScope Runtime documentation](https://runtime.agentscope.io/en/intro.html) <br>
- [AgentScope Runtime GitHub repository](https://github.com/agentscope-ai/agentscope-runtime) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to inspect local AgentScope source files, examples, and API signatures before producing implementation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
