---
name: fde-playbook-productizer
description: "Stage 8 of FDE Delivery Loop. Turn validated customer-delivery learning into a reusable delivery playbook, product-capability candidate, or new Agent Skill with explicit applicability, evidence, standard steps, and maintenance ownership. Use for post-POC scale, productizing customer learning, implementation standardization, and reusable Skill assets. Do not treat a one-off customer request as a universal product feature."
---

# FDE Delivery Playbook Productizer

Extract the effective parts of one customer delivery into an asset that helps the next FDE deliver faster and more reliably.

## Required input

Read the Adoption and Value Review Package from `fde-adoption-and-value`. Revisit original evidence from discovery, charter, PRD, architecture, Skill Design, and POC Run as needed.

Standardize only what has been validated and whose applicability can be explained. By default, require two independent deliveries across two customers or teams, or one delivery plus a reproducible experiment. Anything below that threshold is a **candidate observation** only. Do not standardize one customer’s preference, an unresolved workaround, or a feature request without value evidence.

Use [references/productization-input-guide.md](references/productization-input-guide.md) to compare common and differing evidence across engagements. Do not abstract directly from one success summary.

## Method

1. **Extract repeated patterns**: Identify repeated problems, workflows, delivery steps, data or integration conditions, and value signals.
2. **Bound applicability**: State eligible customers, preconditions, counterexamples, risks, and non-reusable parts. Prevent “one successful case fits every customer.”
3. **Choose the asset form**: Select the minimum effective form among a delivery playbook, product-capability candidate, template, evaluation set, deployment blueprint, or new Agent Skill.
4. **Prioritize productization**: Rank only candidates that meet the minimum evidence threshold, then consider reuse, value, implementation cost, and strategic alignment.
5. **Create the maintenance loop**: Assign an owner, version, validation metrics, and review triggers. Route new insights back to `fde-problem-discovery`.

See [references/productization-rules.md](references/productization-rules.md) for commonality, abstraction, maturity, priority, and retirement rules. See [references/asset-patterns.md](references/asset-patterns.md) for asset forms and selection conditions.

## Execution sequence

1. Collect complete problem, condition, solution, outcome, and failure evidence from at least two independent deliveries.
2. Build a cross-project comparison that distinguishes surface similarity from shared task and value structure.
3. Label customer-specific configuration, configurable variables, stable core, and non-reusable content.
4. Choose the right abstraction level: configuration, template, component, playbook, Skill, or product capability.
5. Prioritize by evidence, coverage, value, savings, cost, risk, and strategic alignment.
6. Build the minimum asset package with trigger, inputs, steps, boundaries, evaluation, and owner.
7. Ask an FDE who did not participate in the original engagement to reuse it in a new scenario.
8. Promote, hold, demote, or retire the asset based on the reuse test.
9. Route new problem hypotheses to discovery and formal product candidates to roadmap governance.

## Abstraction test

Two customers using the same model is not a product commonality. Real commonality should appear across several dimensions: target role, task structure, inputs, business rules, value, and constraints. Prefer configuration and adapters for regulatory, internal-policy, and system-field differences.

## Consumer perspective

Productization is not documentation for the original author. A new FDE must be able to discover, assess, install or configure, execute, validate, and upgrade the asset. Anything that requires oral explanation from the original FDE is not mature.

## Output

Use [references/productization-playbook.md](references/productization-playbook.md) to produce the **Reusable Delivery Playbook**. When recommending a new Agent Skill, hand the validated task, boundaries, guardrails, and evaluation cases to `fde-agent-skill-designer`.

Load [references/product-strategy.md](references/product-strategy.md) when comparing productization directions. Strategy frameworks may support prioritization but never replace delivery evidence.

When the user wants a portfolio item, public case study, demo narrative, or market content, read [references/public-case-study-template.md](references/public-case-study-template.md). Publish only customer-authorized, de-identified, metric-reviewed content. Otherwise produce an internal version or an explicitly labeled synthetic case.

## Boundary

Recommend standardization and productization, but do not replace product-roadmap governance, formal engineering initiation, or commercial prioritization.

## Quality gates

- At least two independent deliveries or equivalent reproducible experiments support the candidate.
- Commonality comes from the problem, task, constraints, and value, not merely interface or customer wording.
- Fixed core, configurable variables, and non-reusable parts are explicit.
- The asset form matches repeated delivery cost; not every pattern becomes a product feature.
- Applicability, counterexamples, dependencies, risks, evaluation, and usage instructions are included.
- A new user can reuse the asset without oral explanation from the original FDE.
- Owner, version, maturity, feedback, review, and retirement conditions are defined.
- Customer-sensitive data, proprietary workflows, and authorization boundaries are removed.

Score with [references/productization-quality-rubric.md](references/productization-quality-rubric.md). See [references/productization-worked-example.md](references/productization-worked-example.md) for a complete example and [references/productization-field-handbook.md](references/productization-field-handbook.md) for asset operations, reuse testing, roadmap feedback, and open-source release rules.

See [references/public-sources.md](references/public-sources.md) for public methodological sources.
