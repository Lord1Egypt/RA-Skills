# SKILL: code-generation

## Purpose
Generate production-ready code (TypeScript/JavaScript/Python) that matches the repo’s conventions, is testable, and is safe to run.

## When to Use
- You have an explicit spec and acceptance criteria.
- A new module/component/function is needed.
- Small-to-medium scoped implementation work is requested.

## Inputs
- `spec` (required, string|object): functional requirements + acceptance criteria.
- `language` (required, enum: `ts|js|py`).
- `targets` (optional, string[]): files/modules to create or modify.
- `constraints` (optional, string[]): security/perf/compat requirements.
- `test_expectations` (optional, string): tests to add/run.

## Steps
1. Validate the spec:
   - confirm inputs/outputs
   - confirm error handling
   - identify missing requirements (ask if material)
2. Inspect existing code style and patterns in the target area.
3. Generate minimal, modular code:
   - small functions
   - explicit types (TS) where useful
   - clear error paths
4. Add or update tests aligned to acceptance criteria.
5. Update docs/config only if required by the change.
6. Provide a deterministic validation command sequence (lint/test/build).

## Validation
- Code is syntactically valid and follows project conventions.
- Tests cover the critical behavior and fail before the fix (when applicable).
- No secrets or credentials are introduced.
- Any external API usage is explicit and configurable (env/config), with timeouts and retries.

## Output
- `files_changed`: list of paths
- `summary`: what changed
- `validation_commands`: ordered commands to run
- `notes`: any assumptions or follow-ups

## Safety Rules
- Never embed secrets, private keys, or tokens.
- Never introduce dynamic code execution (`eval`, runtime compilation) unless explicitly required and sandboxed.
- Avoid network calls in tests unless explicitly controlled/mocked.
- Prefer additive changes over risky rewrites.

## Example
Input:
- `language`: `ts`
- `spec`: “Add `parseUserId(input)` that rejects non-UUID values.”

Output (excerpt):
- `files_changed`: `["src/utils/ids.ts", "src/utils/ids.test.ts"]`
- `validation_commands`: `["pnpm test", "pnpm lint"]`

