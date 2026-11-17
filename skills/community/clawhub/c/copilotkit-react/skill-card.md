## Description:

CopilotKit React best practices for agentic applications that guide agents when writing, reviewing, or refactoring React code using CopilotKit hooks, providers, chat UI components, shared state, tools, or generative UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[generaljerel](https://clawhub.ai/user/generaljerel)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to generate, review, and refactor CopilotKit React applications with consistent patterns for provider setup, agent hooks, tool rendering, context sharing, chat UI, and suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following the context-sharing examples could expose sensitive app context such as secrets, tokens, customer data, private identifiers, or unnecessary user-role details.

Mitigation: Share only the minimum fields needed by the agent, and require clear consent plus server-side controls before exposing sensitive application data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/generaljerel/skills/copilotkit-react)
- [CopilotKit documentation](https://docs.copilotkit.ai)
- [CopilotKit project repository](https://github.com/CopilotKit/CopilotKit)
- [useAgent hook](https://docs.copilotkit.ai/reference/v2/hooks/useAgent)
- [useFrontendTool hook](https://docs.copilotkit.ai/reference/v2/hooks/useFrontendTool)
- [useRenderTool hook](https://docs.copilotkit.ai/reference/v2/hooks/useRenderTool)
- [useCopilotReadable hook](https://docs.copilotkit.ai/reference/v1/hooks/useCopilotReadable)
- [CopilotKit provider](https://docs.copilotkit.ai/reference/v1/components/CopilotKit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with React and TypeScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for CopilotKit React v1 and v2 APIs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
