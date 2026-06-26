# Development Modes

## yolo-super
Use when:
- the project is greenfield,
- or the user explicitly wants an aggressive rewrite,
- and there are no live-product constraints.

Behavior:
- take large coherent steps,
- allow architecture replacement,
- optimize for best outcome from the same prompt,
- default quality target is usually `polished-prototype`, not `first-playable`.

## guided-build
Use when:
- the project is greenfield or prelaunch,
- but the codebase still needs to remain easy for developers to understand and continue.

Behavior:
- still move quickly,
- but keep boundaries and docs cleaner,
- prefer maintainable architecture from the start.

## refactor-open
Use when:
- the project already exists,
- broad refactors are allowed,
- and the current structure is fighting the requested result.

Behavior:
- preserve what helps,
- replace what blocks quality,
- document migrations and compatibility concerns.

## surgical-live
Use when:
- the project is shipped, live, risky, or highly integrated,
- unless the user explicitly authorizes a broad rewrite.

Behavior:
- minimize blast radius,
- favor compatibility,
- preserve behavior outside the requested change,
- document rollback clearly.
