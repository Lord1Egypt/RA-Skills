# SKILL: refactor-engine

## Purpose
Improve existing code structure (readability, modularity, maintainability) while preserving behavior.

## When to Use
- Complexity is growing and changes are becoming risky.
- Duplicate logic appears across modules.
- Tests exist (or can be added) to protect behavior.

## Inputs
- `target_area` (required, string): file(s)/module(s) to refactor.
- `refactor_goal` (required, string): what improves (e.g., reduce duplication, isolate side effects).
- `constraints` (optional, string[]): behavior must not change; performance bounds; compatibility.
- `validation_commands` (optional, string[]): tests/build/lint to run before/after.

## Steps
1. Establish a baseline:
   - run existing tests (or add a minimal characterization test)
2. Identify refactor seam(s):
   - extract pure functions
   - isolate I/O
   - reduce global state
3. Apply refactor in small commits/patches:
   - one transformation per step
   - keep diffs readable
4. Re-run validations after each meaningful transformation.
5. If behavior changes, revert that change and adjust approach.

## Validation
- Behavior is preserved (tests pass; outputs unchanged for known cases).
- Public interfaces remain stable (or are versioned/migrated explicitly).
- Complexity decreases measurably (smaller functions, fewer branches, less duplication).

## Output
- `refactor_summary`
- `files_changed`
- `behavior_guards` (tests added/used)
- `validation_results`

## Safety Rules
- Do not refactor without a behavior guard (tests or a deterministic reproduction).
- Avoid “big bang” rewrites.
- Do not change public APIs unless explicitly required.

## Example
Goal: “Extract request validation from controller into `validators/` and add unit tests.”
Validation: `pnpm test` after each extraction step.

