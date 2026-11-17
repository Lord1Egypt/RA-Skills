# Overengineering Guardrails

Use this file whenever recommending architecture changes, patterns, abstractions, rewrites, or broad refactors.

## Prefer The Smallest Responsible Change

Recommend the least complex change that addresses the observed risk. Avoid introducing layers, interfaces, factories, eventing, queues, generic frameworks, or new packages unless the code already shows pressure that justifies them.

## Pattern Recommendation Test

Before recommending a design pattern, answer:

- What concrete duplication, branching, coupling, lifecycle, or testing problem exists now?
- Why is a simpler local extraction insufficient?
- What complexity does the pattern add?
- How will callers become simpler or safer?
- What tests make the refactor behavior-preserving?
- Can this be introduced incrementally?

If the answers are weak, do not recommend the pattern. Mark it as an observation or leave it out.

## Rewrite Warning

Do not recommend rewrites unless there is strong evidence that incremental repair is riskier or more expensive. If a rewrite is plausible, provide staged alternatives and rollback considerations.

## False Positive Discipline

For each lower-confidence finding, state what would make it a false positive. Examples:

- runtime validation exists upstream
- framework middleware enforces authorization
- database constraints protect the invariant
- generated code is not meant to be edited
- low-volume internal job makes performance concern irrelevant
