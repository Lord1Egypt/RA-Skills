---
name: fde-agent-skill-designer
description: "Stage 5 of FDE Delivery Loop. Package an approved POC scenario, PRD, and deployment constraints into a reusable, evaluable, deliverable Agent Skill. When the user explicitly needs a demo or prototype, build a minimum runnable POC with mocks, guardrails, and smoke evaluations. Use for skill responsibility, workflow, tool boundaries, guardrails, evaluation, package creation, and controlled prototype construction. Do not connect to production without requirements, architecture, and authorization, and do not replace Stage 6 real-run validation."
---

# FDE Agent Skill Designer

Package a well-defined field task as an Agent Skill that can be invoked, evaluated, and reused on the target platform.

## Required inputs

Read the POC PRD Specification Handoff Package from `fde-prd-writer`and the Deployment Architecture and Risk Package from` fde-deployment-architect`.

Confirm target users, trigger scenarios, expected outcomes, available tools and data, permission boundaries, human confirmation points, and unacceptable results. When these are missing, return to the appropriate upstream skill instead of guessing system capability through prompting.

Use [references/skill-input-guide.md](references/skill-input-guide.md) to convert business specifications into a `task, context, rules, tools, output, evaluation` input model.

## Method

1. **Define responsibility boundaries**: State in one sentence whose task the Skill performs and what outcome it produces. State what it does not do and cannot promise.
2. **Design the task loop**: Define trigger, inputs, steps, tool calls, outputs, exceptions, and escalation around the user’s actual job.
3. **Build guardrails**: Define permissions, sensitive-information handling, fact verification, human confirmation, failure fallback, refusal, and handoff conditions.
4. **Design evaluation evidence**: Provide normal, edge, and failure cases for critical scenarios and connect them to POC success criteria.
5. **Adapt to the target platform**: State installation, tool, permission, publishing, and evaluation limits. Keep domain logic platform-neutral and place platform behavior in an adapter. If the platform is unknown, produce a design package only and do not claim direct installability.
6. **Package the delivery**: Produce an installable structure, clear metadata, and minimum usage examples. Keep domain content separate from platform-specific configuration.
7. **Build a POC when requested**: When the user explicitly asks for a runnable demo, choose the lowest sufficient delivery depth and generate a mock-first scaffold with no hidden external actions and with smoke evaluations. A running scaffold is not POC success.

See [references/skill-design-rules.md](references/skill-design-rules.md) for structure, progressive disclosure, instruction design, and anti-patterns; [references/evaluation-design.md](references/evaluation-design.md) for evaluation sets, rubrics, and regression; and [references/platform-adapters.md](references/platform-adapters.md) for platform differences.

## Execution sequence

1. Decide whether the task truly needs an agent. Prefer a conventional deterministic workflow when the rules are stable.
2. Freeze the role, trigger, outcome, and non-goals in one sentence.
3. Convert PRD rules into explicit decisions, exceptions, confirmations, and escalations.
4. Classify tools as data, action, or coordination tools, then define least privilege for each.
5. Design context sources, retrieval, memory, and fact verification so the model cannot invent policy.
6. Write the core `SKILL.md` and move detailed rules, templates, and scripts into progressively loaded resources.
7. Define the output contract, error format, and human-agent interface.
8. Build normal, edge, failure, safety, and regression evaluation sets.
9. Adapt to the target platform and verify installation, triggering, tools, permissions, and versioning.
10. When the user requests a demo or prototype, use [references/poc-build-mode.md](references/poc-build-mode.md) to generate and adapt the minimum runnable scaffold.
11. Run scaffold smoke evaluations and record mocks, permissions, versions, and production gaps.
12. Handoff to POC Run. Do not substitute a scaffold or offline example for a representative task run.

## Select the degree of freedom

- For fixed steps and high error cost, use a low-freedom workflow and deterministic scripts.
- For several valid paths under stable rules, use a medium-freedom decision table and controlled tools.
- Use a high-freedom agent only for open-ended work that requires dynamic exploration, and add stop, budget, and human-takeover controls.

## Output levels

Produce a platform-neutral **Agent Skill Design Package** by default. Create an installable directory only after the user identifies the target platform and requests files. Platform files must not change domain rules. If platform capability is insufficient, report the gap instead of silently removing a guardrail.

For reuse across Claude, Codex, or other compatible platforms, follow the `portable core → runtime adapter → distribution adapter` structure in [references/platform-adapters.md](references/platform-adapters.md). Do not create diverging copies of domain rules for each platform.

## Minimum runnable mode

When the user explicitly requests a demo, POC, or runnable Skill, confirm the target directory and authorization scope, then run:

```text
node scripts/scaffold-poc.js --output <target-directory> --name <POC-name> --scenario <scenario> --project-id <ID>
```Use [assets/minimal-poc/](assets/minimal-poc/) as the dependency-free scaffold. Replace domain logic, samples, and evaluations according to the PRD. At minimum, run`evals/run-evals.js`in the generated directory and record startup instructions, evaluation results, mock boundaries, external actions, hard failures, and known limitations in` poc-manifest.json`.

Do not overwrite an existing target directory. When file writes are not authorized, provide a build plan only. Before adding a real integration, return to Stage 4 to verify identity, data, network, audit, and fallback controls.

## Output

Use [references/agent-skill-pack.md](references/agent-skill-pack.md) to produce the **Agent Skill Design Package**. When the user requests actual skill files, follow the target platform’s format and use this package as the acceptance basis. When a runnable POC is also requested, deliver `poc-manifest.json`, the runnable scaffold, and smoke-evaluation results.

After generating files, run `node scripts/validate-skill-package.js <skill-folder>` to check directory naming, frontmatter, interface metadata, and local links. The script does not validate business correctness, guardrail effectiveness, or real-run quality. Complete Stage 6 against the evaluation set.

## Boundary

Do not add unauthorized tools, external writes, or high-risk automation merely to demonstrate capability. Skill design completion is not POC success. Handoff to `fde-poc-runner` for representative validation.

## Quality gates

- `description` states both what the Skill does and when it should trigger, and the Skill name matches its directory.
- `SKILL.md`contains only the core workflow; detailed knowledge is placed one level deep under` references/`.
- Insufficient input, tool failure, uncertainty, and high-risk actions have explicit handling.
- Every tool has purpose, permission, parameters, return behavior, failure handling, and human confirmation rules.
- The output has a fixed structure, quality criteria, and unacceptable-result definition.
- The evaluation set includes normal, edge, failure, safety, and unauthorized-action cases.
- Evaluation data is traceable to Skill, model, and tool versions.
- When the platform is unknown, the package does not claim direct installation or automatic execution.
- Runnable mode includes normal and blocked interactions, mock or real boundaries, external-action declarations, and model-free smoke tests.
- A page that starts is not business acceptance. Representative results must enter Stage 6.
- Generated scaffolds never overwrite an existing directory or connect to production by default.

Score with [references/skill-quality-rubric.md](references/skill-quality-rubric.md). See [references/skill-worked-example.md](references/skill-worked-example.md) for the full conversion from a business task to a Skill structure, [references/skill-pattern-catalog.md](references/skill-pattern-catalog.md) for common workflow and human-agent patterns, and [references/poc-build-mode.md](references/poc-build-mode.md) for controlled demo and POC construction.

See [references/public-sources.md](references/public-sources.md) for public methodological sources.
