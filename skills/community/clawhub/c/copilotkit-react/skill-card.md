## Description: <br>
CopilotKit React best practices for agentic applications, covering provider setup, agent hooks, tool rendering, state management, chat UI, and suggestions for v1 and v2 CopilotKit APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GeneralJerel](https://clawhub.ai/user/GeneralJerel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill when writing, reviewing, or refactoring React applications that integrate CopilotKit providers, hooks, tools, shared agent state, chat components, and suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CopilotKit context may expose more application state than necessary. <br>
Mitigation: Review useCopilotReadable and shared-state examples so only relevant, non-sensitive state is exposed to agents. <br>
Risk: Generated tool handlers may perform sensitive mutations without enough user control. <br>
Mitigation: Review CopilotKit tool handlers before deployment and require explicit user confirmation for sensitive actions. <br>


## Reference(s): <br>
- [CopilotKit documentation](https://docs.copilotkit.ai) <br>
- [CopilotKit GitHub repository](https://github.com/CopilotKit/CopilotKit) <br>
- [useCopilotReadable reference](https://docs.copilotkit.ai/reference/v1/hooks/useCopilotReadable) <br>
- [useCopilotAction reference](https://docs.copilotkit.ai/reference/v1/hooks/useCopilotAction) <br>
- [useFrontendTool reference](https://docs.copilotkit.ai/reference/v2/hooks/useFrontendTool) <br>
- [useRenderTool reference](https://docs.copilotkit.ai/reference/v2/hooks/useRenderTool) <br>
- [CopilotKit component reference](https://docs.copilotkit.ai/reference/v1/components/CopilotKit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and TSX code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable behavior.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact metadata version 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
