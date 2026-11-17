## Description:

Vercel AI Elements guidance for building AI chat interfaces, tool execution displays, reasoning views, job queues, and workflow UI components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building React AI interfaces use this skill for guidance on installing Vercel AI Elements components and wiring chat, prompt input, tool execution, approval, reasoning, queue, and workflow visualization UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow uses mutable package and registry commands that can change generated source or lockfiles over time.

Mitigation: Prefer pinned reviewed versions where possible, run installation in a normal development environment without unnecessary secrets, and review generated source and lockfile changes before merging.

Risk: Prompt input and speech features may process user files, pasted content, or voice input.

Mitigation: Add clear user consent, file type and size limits, server-side validation, and privacy and retention disclosures before enabling these features.

Risk: Tool and confirmation state names depend on the installed AI SDK version.

Mitigation: Verify state strings against the local AI SDK documentation or exported types before relying on copied examples.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/ai-elements)
- [Conversation Components](references/conversation.md)
- [Prompt Input Components](references/prompt-input.md)
- [Workflow Components](references/workflow.md)
- [Visualization Components](references/visualization.md)
- [Vercel AI Elements shadcn Registry](https://ai-elements.vercel.app/r/[component-name])

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript/TSX examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes component import patterns, state names, and usage examples; does not execute commands itself.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
