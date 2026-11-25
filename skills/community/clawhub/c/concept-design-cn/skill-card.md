## Description:

仅在显式调用时使用。用 Daniel Jackson 的概念与同步方法设计、实现、审查和重构软件，编写规格并解释软件行为。检查 CONCEPT.md/SYNCS.md 结构，生成 Mermaid 关系图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenticweb4](https://clawhub.ai/user/agenticweb4)

### License/Terms of Use:

MIT-0

## Use Case:

供软件开发者从用户需要出发，定义概念与同步规则，并编写或审查软件规格。也可用于按授权实现或重构、解释软件行为，以及生成 Mermaid 关系图。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security guidance reports file-reading, network, and shell capabilities without a declared tool scope; inspection was partial because two local references could not be resolved.

Mitigation: Review tool access and any proposed file changes or commands, limit access to the intended project resources, and treat the benign scan verdict as informative rather than a safety guarantee.

## Reference(s):

- [Concept composition and sync](https://essenceofsoftware.com/tutorials/concept-basics/sync/#composing-concepts-with-syncs)
- [Concept criteria](https://essenceofsoftware.com/tutorials/concept-basics/criteria/)
- [Architecture guidance](artifact/references/architecture.md)
- [Specification reading guide](artifact/references/spec-reading.md)
- [Specification notation](artifact/references/spec-notation.md)
- [Execution, recovery, and migration](artifact/references/architecture-execution.md)
- [Diagram format](artifact/references/tool-diagram.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [中文 Markdown 规格、审查说明、Mermaid 图及代码修改]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [按请求选择设计、实现、审查、审计或解释模式；审查、审计和规划保持只读。]

## Skill Version(s):

2.5.4 (source: frontmatter; server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
