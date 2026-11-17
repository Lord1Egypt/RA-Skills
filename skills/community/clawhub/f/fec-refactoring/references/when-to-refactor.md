# When to Refactor

## Refactor Now

Refactor when a structural problem directly increases the cost or risk of the work currently in front of you and the intended behavior can be kept stable. Strong situations include:

- a change is difficult because one responsibility is tangled with unrelated work;
- the same concept must be edited in several places;
- a public-looking API is difficult to use safely and a compatibility path exists;
- duplicated decisions are already drifting;
- state or data ownership is obscuring reliable reasoning;
- tests are hard to target because responsibilities are fused.

## Record and Defer

Defer when the smell is real but unrelated to the current goal, the safety net is insufficient for a risky transformation, or the required compatibility work is larger than the immediate value. Record evidence and a candidate sequence instead of starting an opportunistic redesign.

## Stop Refactoring

Stop when:

- the structural objective has been met;
- the next step changes observable behavior;
- the next step crosses a public contract without an explicit compatibility plan;
- the Diff Budget is expanding materially;
- verification can no longer distinguish a regression from the baseline;
- the remaining motivation is aesthetic preference rather than change cost or correctness risk.

## Practical Heuristic

A useful refactoring makes the next meaningful change easier to understand, localize, verify, or reverse. If it does not improve one of those properties, require stronger evidence before continuing.
