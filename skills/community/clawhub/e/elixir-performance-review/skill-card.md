## Description:

Reviews Elixir code for performance issues including GenServer bottlenecks, memory usage, and concurrency patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Elixir code for performance risks in GenServer usage, memory behavior, concurrency patterns, ETS usage, and database access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires loading a sibling review-verification-protocol/SKILL.md file that is not included in the reviewed package, so review behavior can depend on an external instruction source.

Mitigation: Install only in environments where that protocol file is trusted, bundled, pinned, or otherwise controlled before agents use the skill for reviews.

## Reference(s):

- [Elixir Performance Review](https://clawhub.ai/anderskev/skills/elixir-performance-review)
- [GenServer Bottlenecks](references/genserver-bottlenecks.md)
- [ETS Patterns](references/ets-patterns.md)
- [Memory Patterns](references/memory.md)
- [Concurrency Patterns](references/concurrency.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review findings and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are expected to include anchored evidence and measured or observed facts for substantive performance claims.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
