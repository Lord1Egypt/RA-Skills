---
name: architect-4c
description: Use Simon Brown's C4 model only when explicitly invoked to generate Mermaid architecture diagrams and documentation from source code, design notes, or discussions. Cover system context, containers, components, and code, with dynamic and deployment views as needed.
metadata:
  language: en
  translation_of: architect-4c-cn
  version: "0.1.0"
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills/tree/main/skills/en/architect-4c
---

# C4 Architecture Diagrams and Documentation

## Core understanding

Use Simon Brown's C4 model to describe architecture through Context, Container, Component, and Code. Inputs may include discussions, design material, source code, and runtime configuration.

## Official principles

These points summarize the model described on the [C4 website](https://c4model.com/).

- Use software systems, containers, components, and code elements as hierarchical abstractions.
- Expand through context, container, component, and code diagrams.
- Add system landscape, dynamic, and deployment diagrams as supporting views.
- Keep the model independent of notation. Different notations can express the same model.
- Keep the model independent of tooling. Choose tools that suit the project.

Choose diagrams for the audience. Context and container diagrams suffice for most teams. Add other views as needed. See the [diagram guidance](https://c4model.com/diagrams).

## Four levels

### Context

Treat the target system as a whole. Show its purpose, direct users, and external collaborators. Leave internal services, databases, and code for later levels. External means outside the current system boundary, including other systems in the same company.

### Container

Expand one system to show applications and data stores, their responsibilities, technologies, and communication. A container is a runtime boundary for executing code or storing data, such as a web application, background process, or database. Docker, virtual machines, folders, and libraries alone do not establish container boundaries.

### Component

Expand one container into units of functionality with explicit interfaces and collaboration. Components execute within their container, are typically not independently deployed, and need not match folders.

### Code

Expand one significant component into relevant classes, interfaces, functions, or data structures. Keep only details needed for the question, preferably generated from source or tooling. Code is level four. Dynamic and deployment diagrams are supporting views.

## Views and references

Load only the needed view references. Before drawing, read the shared [diagram and visual guidelines](references/diagram-guidelines.md).

| Diagram | Main question | Template and checks |
|---|---|---|
| L1 System context | How does the system collaborate with its environment? | [Context](references/context.md) |
| L2 Container | How do applications and data stores communicate? | [Container](references/container.md) |
| L3 Component | How are responsibilities organized inside one container? | [Component](references/component.md) |
| L4 Code | How is one component implemented? | [Code](references/code.md) |
| Dynamic | How does one scenario execute? | [Dynamic interaction](references/dynamic.md) |
| Deployment | Where do instances run in one environment? | [Deployment](references/deployment.md) |

A system landscape uses Context's people and systems across a wider scope. For native Mermaid C4 notation, see the [syntax reference](references/c4-syntax.md).

## Workflow

1. Establish the audience, question, system boundary, and current or target state. Reuse confirmed scope and identify gaps that affect boundaries.
2. Inspect entry points, startup configuration, interfaces, data access, and deployment configuration. Record each object's type, responsibility, parent, and source location.
3. Select views and expand significant objects. Preserve identity, external collaborators, and relationship meaning. Add dynamic or deployment diagrams when behavior or environment needs explanation.
4. Deliver diagrams, brief explanations, evidence, and unresolved points. Follow existing documentation locations, otherwise use `docs/architecture/`.

## Completion checks

- Expansion is consistent across the L1 system, L2 containers, L3 components, and L4 code. Leave unexpanded objects at their existing level.
- Containers follow runtime boundaries and components follow internal responsibilities. A microservice's level depends on system boundaries, with team ownership as supporting evidence.
- Structural relationships support dynamic interactions. Significant state changes and failure responses have owners. Support timeout, retry, and idempotency policies with evidence or mark them unconfirmed.
- Deployment diagrams name the environment and map instances to logical containers. Support replica counts, availability zones, and failover with configuration or explicit design decisions.
- Distinguish design goals, source facts, and inference. A source dependency alone cannot prove a runtime call. Examples are not evidence of the actual architecture.
- Check Mermaid rendering and layout, then each view's semantics. Record validation scope and state when no renderer was run.

[Sources and example conventions](references/sources.md)
