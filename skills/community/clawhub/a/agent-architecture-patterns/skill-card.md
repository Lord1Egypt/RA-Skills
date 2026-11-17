## Description:

AI Agent architecture patterns library with 10 patterns for single and multi-agent systems

This skill is ready for commercial/non-commercial use.

## Publisher:

[banxian87](https://clawhub.ai/user/banxian87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose, explain, and adapt single-agent and multi-agent architecture patterns such as ReAct, Reflection, Self-Critique, Plan-and-Solve, Tree of Thoughts, Manager-Worker, Peer-to-Peer, Hierarchical, Market-Based, and Pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runnable ReAct example and documentation include an eval()-based calculator pattern that can execute arbitrary JavaScript.

Mitigation: Replace it with a strict arithmetic parser before real use, and validate all LLM-generated tool arguments before invoking tools.

Risk: Copied examples may expose sensitive task inputs or tool outputs through verbose logs.

Mitigation: Review logging behavior before deployment and redact or suppress sensitive inputs, intermediate reasoning, and tool results.

Risk: Agent examples may be extended with file or network tools that execute outside the intended task boundary.

Mitigation: Sandbox file and network tools, limit permissions, and review proposed tool calls before enabling production use.

## Reference(s):

- [Agent Architecture Patterns on ClawHub](https://clawhub.ai/banxian87/skills/agent-architecture-patterns)
- [Pattern overview](patterns/README.md)
- [ReAct paper](https://arxiv.org/abs/2210.03629)
- [Tree of Thoughts paper](https://arxiv.org/abs/2305.10601)
- [Reflection paper](https://arxiv.org/abs/2303.11366)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [AutoGen](https://github.com/microsoft/autogen)
- [LangChain](https://github.com/langchain-ai/langchain)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript code examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pattern-selection advice, implementation examples, and tests; runnable examples should be reviewed before execution.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
