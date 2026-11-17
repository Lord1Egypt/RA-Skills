# Project absorption methodology

## Target

This document is used to extend the core process in `SKILL.md`, suitable for larger "reference system to target project" capability absorption tasks. A reference system can be a code base, product, service, framework, library, CLI, plug-in, documentation system, or AI/Agent toolchain.

## Phase 1: Establish Target Project Baseline

Before diving into the reference project, establish a brief baseline for the target project:

- What is the purpose of the target project statement?
- What are the current top-level capabilities?
- What entry points, extension points and user workflows already exist?
- Which areas are still under active maintenance?
- Which areas are fragile, complex or over-engineered?
- What testing and verification commands are in place?

Don’t prematurely formulate renovation recommendations before understanding the target project baseline.

## Phase 2: Scan Reference Projects

Scan high-signal materials in reference systems:

- README and documentation: project location, usage model, installation, configuration.
- Package or build metadata: technology selection, dependency scope, script commands.
- Source code layout: architecture, module boundaries, naming conventions.
- Capability domain: product capabilities, architectural patterns, domain models, interface protocols, data flow, runtime behavior, development experience, quality system, delivery process, document knowledge, and ecological expansion.
- Project shape probe: select relevant directories and behavior entries according to the reference system type, without assuming that all projects have the same structure.
- Testing: expected behavior and edge scenarios.
- Example: User-facing workflow and quality of onboarding experience.

When recording observations, they should be recorded as “competencies,” not “documents.” For example, write "Has guided configuration wizard with environment checks" instead of "Copy setup.ts".

### Project shape probe

Select the scan angle according to the actual shape of the target and reference system:

- Front-end projects: pages, components, routing, state, data requests, forms, design systems, accessibility, performance, build.
- Backend projects: API, service boundary, database, queue, cache, authentication and authorization, task scheduling, observability, deployment.
- Tool or CLI project: command model, configuration, plugin mechanism, error output, installation distribution, templates.
- AI/Agent projects: skills, commands, hooks, rules, agents, MCP, prompts, workflow.
- Library project: public API, types, compatibility, build artifacts, examples, version policy.
- Documentation or knowledge base project: information architecture, navigation, examples, search, versioning, contribution process, release cadence.

If the project spans multiple modalities, prioritize 1 to 3 perspectives that are directly related to user goals to avoid expanding the absorption task into a full warehouse audit.

## Phase 3: Candidate Ability Scoring

Rate each candidate on a scale of 1 to 5.

| Dimensions | Questions |
|---|---|
| User value | Can it substantially improve the workflow of target users? |
| Fit | Is it consistent with the target project's architecture and roadmap? |
| Feasibility of originalization | Is it possible to recreate a protected expression without copying it? |
| Complexity | Can it be delivered safely and maintained over the long term? |
| Verifiability | Can correctness be verified through testing or review? |

Prioritize high-value, high-fit, low-risk candidates.

## Phase 4: Absorption Strategy

Choose a strategy for each candidate:

- **Enhancement**: Improve the existing abilities of the target item.
- **New**: Introducing new target project native capabilities.
- **Split**: Split an overloaded target concept or reference concept.
- **Merge**: Merge overlapping concepts in the target project.
- **Replace**: Remove weaker goal implementations once a more secure design is ready.
- **Documentation**: Only add knowledge, do not change the code.
- **Rejection**: Defer or give up clearly and explain the reasons.

## Phase 5: Implementation Sequence

It is recommended to proceed in the following order:

1. Documentation and boundary clarification.
2. Test or validate scaffolding.
3. Minimized target project native implementation.
4. Integrate with existing workflows.
5. Clean up duplicate logic and abandoned paths.
6. User-oriented documentation and examples.

## Stage 6: Review Questions

Before finalizing, answer the following questions:

- Will the target items remain consistent after assimilation?
- Are module boundaries preserved or improved?
- Is each new ability discoverable?
- Are there overlapping capabilities, portals, abstractions, configurations, runtime processes, tool functions, document commitments, or user workflows?
- Is there a good reason for adding new dependencies?
- Verify that the command was logged?
- Is the source of inspiration transparently stated without implying duplication of code?
