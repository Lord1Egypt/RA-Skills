## Description:

Create Agent App helps Codex clarify requirements, select architecture, generate or refactor production-grade TypeScript agent applications, and report real validation results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leogoat2004](https://clawhub.ai/user/leogoat2004)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or harden TypeScript agent application bases for CLIs, web apps, API services, internal tools, and multi-agent or workflow-first systems. It guides Codex through requirements gathering, architecture tradeoffs, approval gates, implementation, and validation reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README install command references a mutable source, so the installed skill can differ from the reviewed release.

Mitigation: Install from a pinned, reviewed commit or release when possible.

Risk: Generated plans may request file writes, package installation, network access, database changes, browser automation, or secret access.

Mitigation: Review the generated brief and keep the skill's confirmation and approval gates in place before granting privileged access.

Risk: Validation claims can be misleading if checks are skipped or credentials are unavailable.

Mitigation: Require exact commands and outcomes, and mark live LLM smoke as not run when credentials or network access are unavailable.

## Reference(s):

- [Create Agent App README](README.md)
- [Architecture Patterns](references/architecture-patterns.md)
- [Generation Contract](references/generation-contract.md)
- [Grill Questions](references/grill-questions.md)
- [Harness Contract](references/harness-contract.md)
- [Industry Architecture Signals](references/industry-architecture-signals.md)
- [Modern Selection Policy](references/modern-selection-policy.md)
- [Official Docs](references/official-docs.md)
- [Provider Patterns](references/provider-patterns.md)
- [Safety Policy](references/safety-policy.md)
- [Validation Policy](references/validation-policy.md)
- [ClawHub skill page](https://clawhub.ai/leogoat2004/skills/create-agent-app)
- [OpenAI practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- [OpenAI Agents SDK JS docs](https://openai.github.io/openai-agents-js/)
- [OpenAI Responses API reference](https://platform.openai.com/docs/api-reference/responses)
- [Anthropic Building Effective AI Agents](https://resources.anthropic.com/building-effective-ai-agents)
- [AWS agentic AI enterprise architecture guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/govern-architect-agentic-ai/enterprise-architecture.html)
- [Google Cloud production-ready AI agents guides](https://cloud.google.com/blog/topics/developers-practitioners/five-guides-to-building-and-scaling-production-ready-ai-agents)
- [Microsoft AI agent orchestration patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [TypeScript documentation](https://www.typescriptlang.org/docs/)
- [Zod documentation](https://zod.dev/)
- [Vitest documentation](https://vitest.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated TypeScript project files and command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes architecture rationale, file-change summaries, validation outcomes, live LLM smoke status, and remaining risks when generation completes.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
