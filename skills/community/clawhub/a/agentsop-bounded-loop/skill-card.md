## Description:

Agentsop Bounded Loop gives agents framework-agnostic guidance for designing LM-driven loops with explicit counters, progress witnesses, stagnation checks, budgets, and escalation paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsope](https://clawhub.ai/user/agentsope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when building, diagnosing, or porting cyclic LM workflows such as agent retries, plan-act-observe loops, multi-agent handoffs, optimizer passes, and test-fix cycles. It helps them replace vague stop conditions with deterministic counters, progress witnesses, safety budgets, and escalation paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence an agent to make loop-control changes that are too strict, too loose, or mismatched to the application.

Mitigation: Review proposed counters, progress witnesses, budgets, and escalation behavior against the target workflow before deployment.

Risk: Refusing to simply raise recursion or iteration limits can change existing operational behavior.

Mitigation: Validate the replacement bounds with regression tests that cover permanent failure, stagnation, and successful completion paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentsope/skills/agentsop-bounded-loop)
- [R1 source evidence](references/R1-source-evidence.md)
- [R2 cross-framework comparison](references/R2-cross-framework.md)
- [LangGraph GRAPH_RECURSION_LIMIT documentation](https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT)
- [LangGraph issue 6731](https://github.com/langchain-ai/langgraph/issues/6731)
- [CrewAI issue 330](https://github.com/crewAIInc/crewAI/issues/330)
- [LangGraph FAQs and gotchas](https://sumanmichael.github.io/langgraph-cheatsheet/cheatsheet/faqs-gotchas/)
- [CrewAI delegation ping-pong writeup](https://azguards.com/technical/the-delegation-ping-pong-breaking-infinite-handoff-loops-in-crewai-hierarchical-topologies/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline examples and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose framework-specific loop counters, exit predicates, tests, budgets, and escalation branches.]

## Skill Version(s):

0.1.1 (source: server release evidence; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
