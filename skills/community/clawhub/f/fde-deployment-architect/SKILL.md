---
name: fde-deployment-architect
description: "Stage 4 of FDE Delivery Loop. Turn an approved POC PRD into a runnable, risk-controlled deployment architecture and delivery plan covering system boundaries, data, permissions, integrations, environments, observability, and risk. Use for POC implementation planning, architecture review, data and permission mapping, integration design, and pre-deployment risk decisions. Do not use to rewrite business requirements, design agent behavior, or replace a production architecture review."
---

# FDE Deployment Architecture

Turn the POC PRD’s “what to build” into the minimum design that explains how to run it safely and how to prove that it runs.

## Required input

Read the POC PRD Specification Handoff Package from `fde-prd-writer`, especially functions and acceptance criteria, data and integrations, role permissions, dependencies, test scenarios, and risks.

If system boundaries, data sources, access methods, or acceptance scenarios are missing, mark the gaps and return to PRD Handoff. Do not present an unknown integration as a committed capability.

Use [references/architecture-input-guide.md](references/architecture-input-guide.md) to inventory systems, data, identity, environments, and operational constraints.

## Method

1. **Make boundaries explicit**: List users, customer systems, data sources, agent or application components, human actions, and external services. Show where data originates and where it goes.
2. **Choose the minimum runnable path**: For each POC objective, choose real integration, controlled mock, or human fallback. Record tradeoffs across delivery time, data sensitivity, customer IT constraints, cost, and observability. Prioritize validation of the critical risk over architectural breadth.
3. **Control access and risk**: Define identity, roles, least privilege, sensitive-data handling, audit, failure fallback, and human escalation.
4. **Define operational evidence**: Specify logs, metrics, demo data, acceptance records, and incident handling so `fde-poc-runner` can evaluate the POC.
5. **Make deployment decisions**: Separate acceptable POC risk, unacceptable risk, and matters requiring a customer decision.

See [references/architecture-rules.md](references/architecture-rules.md) for design selection, real integration versus mock tradeoffs, ADRs, and POC-to-production boundaries. When agents, external content, or executable tools are involved, read [references/security-checklist.md](references/security-checklist.md).

When choosing among rules, workflows, models, retrieval, single-agent, multi-agent, prototype UI, or data paths, read [references/technology-selection-guide.md](references/technology-selection-guide.md). Begin with the smallest testable design and add complexity only when failure evidence justifies it.

## Execution sequence

1. Work backward from PRD acceptance scenarios to the systems, data, tools, and human nodes that must exist.
2. Draw trust boundaries and data flows, not only a component diagram.
3. Choose real integration, mock, or human fallback for each critical risk.
4. Start with the simplest design and decide whether prompting, RAG, workflow, single-agent, or multi-agent behavior is necessary.
5. Define identity, least privilege, tool capability, human confirmation, and audit.
6. Design versioning for environments, configuration, models, Skills, datasets, and interfaces.
7. Define logging, metrics, traces, cost, feedback, and incident triage.
8. Record material tradeoffs as ADRs and produce the POC technical-debt and production-gap list.

## Architecture output modes

- **Architecture sketch**: When information is incomplete, show boundaries, unknowns, and a validation plan.
- **POC deployment design**: Produce the minimum design that can run in a controlled environment and collect evidence.
- **Architecture risk review**: Audit permissions, data, reliability, and extrapolation risk in an existing design.
- **POC-to-production gap**: List controls that must be added or rewritten for production. Do not claim the POC can be deployed directly.

When the user requests preproduction, launch readiness, canary rollout, rollback, operations, or knowledge transfer, read [references/production-transition.md](references/production-transition.md) and produce a separate production-transition work package. This skill produces architecture and planning only; it does not authorize production changes.

## Conflict handling

When business prioritizes speed, engineering prioritizes completeness, and security prioritizes restriction, do not recommend a vague “balance.” Compare candidate designs by their effect on success criteria, schedule, cost, and residual risk, then ask the appropriate decision owner to accept a choice. If no risk owner is available, reduce privilege or stop the high-risk path.

## Output

Use [references/deployment-architecture-pack.md](references/deployment-architecture-pack.md) to produce the **Deployment Architecture and Risk Package**.

The output must give downstream teams:

- A runnable environment, integration path, and data path.
- Tools, permissions, and boundaries available to the Agent Skill.
- Observability, test data, and fallback required for POC execution.
- Blocking matters requiring customer or technical-owner confirmation.

## Boundary

Design the minimum viable architecture for POC delivery. Do not replace enterprise production governance, security audit, or formal change approval. Escalate risks outside the controlled POC boundary rather than bypassing them.

## Quality gates

- The system-boundary diagram includes users, agent or application, data sources, tools, human nodes, and external systems.
- Every data flow has a source, destination, sensitivity, retention or deletion rule, and authorized actor.
- Every tool uses minimum capability, minimum privilege, and minimum autonomy, with human confirmation points stated.
- Real integration, mock, and human fallback choices include rationale and extrapolation limits.
- Environments, configuration, models or prompts, datasets, and interfaces are versionable.
- Logs, metrics, traces, cost, alerts, and fallback support reproducible POC runs.
- POC technical debt is explicit, and POC code is not represented as production-ready.

Score the output with [references/architecture-quality-rubric.md](references/architecture-quality-rubric.md). See [references/architecture-worked-example.md](references/architecture-worked-example.md) for a complete example and [references/architecture-field-handbook.md](references/architecture-field-handbook.md) for detailed review questions and patterns.

See [references/public-sources.md](references/public-sources.md) for public methodological sources.
