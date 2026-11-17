## Description:

Review, refactor, and explain Java code using distilled Effective Java principles for API design, immutability, generics, enums, streams, exceptions, concurrency, and serialization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbingqiang](https://clawhub.ai/user/linbingqiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review, refactor, and explain Java code through an Effective Java lens, prioritizing correctness, API safety, encapsulation, type safety, concurrency, and maintainability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refactoring guidance may lead an agent to change Java source in ways that affect public API compatibility or behavior.

Mitigation: Review proposed patches and compatibility assumptions before applying them, especially for public APIs, concurrency guarantees, and serialization compatibility.

Risk: Review recommendations may be incomplete when project context is missing.

Mitigation: Provide relevant source files, API contracts, tests, and thread-safety or serialization expectations so findings can be grounded in the codebase.

## Reference(s):

- [Effective Java Review Checklist](references/review-checklist.md)
- [Effective Java Item Map](references/item-map.md)
- [ClawHub Skill Page](https://clawhub.ai/linbingqiang/skills/effective-java)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with prioritized findings, explanations, and optional code patches or examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include line-referenced review findings, compatibility assumptions, and validation notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
