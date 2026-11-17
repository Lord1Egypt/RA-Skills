# Refine

1. Establish the failing scenario from requirements, specifications, and relevant code.
   Inspect affected concepts, rules, callers, and tests.
2. Compare moves against the cause, including no change.
3. Record alternatives, benefit, cost, contract effects, and behavioral differences.
   Specify confirmed new behavior before implementing it.
4. For authorized code repairs, follow [build](build.md). Verify invariants, purpose, affected scenarios, and failure paths.
   Report preserved and intentionally changed behavior, regressions, and unknowns.

| Move | Choice and tradeoff |
| --- | --- |
| Split / merge | Split one concept or merge distinct concepts; weigh simplicity against capability and control. |
| Unify / specialize | Combine variants or retain specialized concepts; weigh generality against actual fit. |
| Tighten / loosen | Add or relax synchronization; weigh automation against manual control. |

Size, names, shared fields, or flow length alone MUST NOT determine a move.
Specialization is a defect only when it excludes required behavior.
Distinguish behavior-preserving refactoring from redesign.
