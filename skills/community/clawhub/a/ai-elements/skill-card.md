## Description: <br>
Vercel AI Elements guidance for building chat interfaces, displaying tool execution, showing reasoning, and creating job queues with React UI components. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill for guidance on integrating Vercel AI Elements components into AI-powered React interfaces, including chat, prompt input, workflow, tool execution, approval, and visualization patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated `npx shadcn add` commands download component code into the target project. <br>
Mitigation: Review the command, registry URL, and resulting component diff before running or committing changes. <br>
Risk: The skill can activate on broad UI terms such as Queue, Tool, Message, Conversation, or PromptInput. <br>
Mitigation: Confirm the task is specifically about Vercel AI Elements before applying its component guidance. <br>
Risk: Tool and confirmation state strings depend on the installed AI SDK version. <br>
Mitigation: Check the local `ai` package version and exported types before copying state names into application code. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/anderskev/ai-elements) <br>
- [Publisher profile](https://clawhub.ai/user/anderskev) <br>
- [Conversation Components](references/conversation.md) <br>
- [Prompt Input Components](references/prompt-input.md) <br>
- [Workflow Components](references/workflow.md) <br>
- [Visualization Components](references/visualization.md) <br>
- [AI Elements shadcn registry](https://ai-elements.vercel.app/r/[component-name]) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with TypeScript, TSX, and bash code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; generated commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
