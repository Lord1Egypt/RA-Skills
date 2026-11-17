# Sources and example conventions

Checked on 2026-11-04. Simon Brown created the C4 model.

## Official sources

- The [home page](https://c4model.com/) lists hierarchical abstractions and diagrams, supporting diagrams, notation independence, and tooling independence.
- [Abstractions](https://c4model.com/abstractions) defines containment across systems, containers, components, and code elements.
- [Diagrams](https://c4model.com/diagrams) describes the four static levels, supporting views, and view selection.
- [Notation](https://c4model.com/diagrams/notation) describes elements, relationships, titles, and legends.
- [Mermaid C4 documentation](https://mermaid.js.org/syntax/c4.html) describes native syntax and layout support.

The entry's official principles summarize these descriptions. Each view reference also links to its official definition.

The official site and example diagrams use [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This skill uses independently authored prose and a payment-platform example.

## Skill reference

[softaworks c4-architecture](https://github.com/softaworks/agent-toolkit/blob/main/skills/c4-architecture/SKILL.md) informed the workflow and syntax guidance. Official C4 definitions govern the levels, with Code as level four.

## Example conventions

The six templates share one fictional payment platform. The merchant order system and payment provider are external. The platform contains a payment application and database. Jobs are components inside the application, and the code diagram expands only payment processing.

Idempotency, atomic notification tasks, result reconciliation, leases, and retry limits are example design decisions. Two application instances and one database illustrate deployment mapping. Verify these choices against project evidence before use.

This skill maintains its own [diagram and visual guidelines](diagram-guidelines.md).
