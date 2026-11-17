## Description:

Use when designing, reviewing, or refactoring a CLI that must serve AI agents alongside humans, or when converting an API or SDK into an agent-usable CLI interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate, design, and refactor command-line interfaces for reliable use by humans, AI agents, and orchestration systems. It supports reviews of output contracts, schema introspection, dry-run behavior, safety boundaries, delegated authentication, and CLI-to-agent integration patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Testing guidance includes eval-based shell harness examples that could execute command strings supplied by the CLI under review.

Mitigation: Treat the snippets as design guidance, replace eval loops with structured command manifests or argv arrays, and run CLI review tests in a sandbox with disposable credentials and non-production data.

Risk: The security verdict is suspicious because unsafe shell examples appear in a reference file.

Mitigation: Review generated or copied test harnesses before execution and scan the skill before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agents365-ai/skills/agent-native-design)
- [Design Patterns](references/design-patterns.md)
- [Rubric](references/rubric.md)
- [Review Checklists](references/checklists.md)
- [Examples and Non-Examples](references/examples.md)
- [Testing an Agent-Native CLI](references/testing.md)
- [When CLI vs MCP vs Both](references/hybrid-mcp-cli.md)
- [Citations](references/citations.md)
- [Anthropic: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Anthropic: Beyond permission prompts](https://www.anthropic.com/engineering/claude-code-sandboxing)
- [Writing CLI Tools That AI Agents Actually Want to Use](https://dev.to/uenyioha/writing-cli-tools-that-ai-agents-actually-want-to-use-39no)
- [Building a CLI That Works for Humans and Machines](https://www.openstatus.dev/blog/building-cli-for-human-and-agents)
- [MCP vs CLI: Benchmarking Tools for Coding Agents](https://mariozechner.at/posts/2025-08-15-mcp-vs-cli/)
- [CLI Tools vs MCP: Better AI Agents With Less Context](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with structured review sections, examples, and inline code or shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include rubric scores, risk summaries, prioritized refactor plans, JSON contract examples, and CLI design checklists.]

## Skill Version(s):

1.3.5 (source: server release evidence and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
