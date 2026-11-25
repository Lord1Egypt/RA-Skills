---
name: concept-design
description: "Use only when explicitly invoked. Design, specify, implement, review, refactor, or explain software with Daniel Jackson's concepts and synchronizations. Check CONCEPT.md/SYNCS.md structure and generate Mermaid relationship diagrams."
metadata:
  language: en
  translation_of: concept-design-cn
  version: "2.5.4"
---

# Concept design

Summary of Daniel Jackson's concept design: **Application = Concepts + Synchronizations**.

> “With the concepts in hand, we now associate their actions through synchronizations:”
> — Daniel Jackson, [Concept composition and sync](https://essenceofsoftware.com/tutorials/concept-basics/sync/#composing-concepts-with-syncs) (2022-09-14)

Start from user needs. Concepts define independent behavior; external synchronization rules compose that behavior by specifying which action completions, under which conditions, trigger subsequent actions.

## Core constraints

- Each concept owns state and actions for one purpose; concepts do not invoke one another or read one another's state. External identities carry no internal structure from another concept.
- The operational principle (OP) illustrates how the purpose is fulfilled through a representative history; it does not replace the full contract or guarantee progress.
- Composition may restrict behavior but must preserve each concept's contract. Check contracts, OPs, purposes, and application scenarios separately.
- Each definition has one authoritative source. Distinguish confirmed, proposed, inferred, and open statements; test decisions with evidence, assumptions, and counterexamples. Keep unresolved matters open and unexecuted checks unverified.
- Compare alternatives, including no change or removal; revisit assumptions after repeated failures. Refactoring preserves behavior; state intentional changes explicitly.

For engineering design, implementation, review, or project rules, apply the [engineering architecture](references/architecture.md) for directories, naming, responsibilities, and dependencies.

## Choose a mode

Select a mode from the request and read only that mode and references needed for the current step. Each mode file links every reference it needs directly; links between references are see-also only. Inspect read-only when intent is unclear; carry existing authorization across modes.

| Mode | Purpose |
| --- | --- |
| [design](references/modes/design.md) | Design concepts and synchronizations |
| [settle](references/modes/settle.md) | Consolidate discussions and decisions |
| [prd](references/modes/prd.md) | Write the PRD, specifications, and acceptance criteria |
| [build](references/modes/build.md) | Implement or refactor against confirmed specifications |
| [review](references/modes/review.md) | Review design and implementation |
| [guard](references/modes/guard.md) | Audit, reconstruct, check drift, specify pipelines, and generate diagrams |
| [refine](references/modes/refine.md) | Compare improvements and apply authorized corrections |
| [explain](references/modes/explain.md) | Explain behavior from specifications and source code |

Review, audit, drift, and plan-only requests remain read-only; other changes stay within authorized scope. Do not change specifications to conceal implementation defects.

## Expression and verification

Use the [reading version](references/spec-reading.md) by default; expand the [specification notation](references/spec-notation.md) when precision is needed.
Read the [tool encoding](references/tool-encoding.md) when running the checker or generating diagrams; report unsupported content as unchecked.
Use Mermaid in Markdown for diagrams; passing syntax checks does not establish purpose fulfillment, contract conformance, or runtime correctness.

## References

- Concepts and synchronizations: Daniel Jackson, Beyond Objects.
- Engineering execution: Meng and Jackson, WYSIWID.
