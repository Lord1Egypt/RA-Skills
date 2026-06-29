# Precision Profiles

Precision profiles define project-specific defaults.

## Profile Rules

- A profile MUST be explicit.
- A profile MUST scope heuristics to a language, stack, or project type.
- A profile MUST NOT claim cross-project truth for stack-specific checks.
- A profile MAY define default build, test, and review cadence.
- A profile defines defaults only. It does not define round truth.

## Suggested Profile Families

- `go-web`
- `go-cli`
- `ts-node`
- `frontend`
- `python-service`

## Examples Of Scoped Heuristics

- `go vet` belongs to Go profiles only.
- `tsc` belongs to TypeScript profiles only.
- bundle-size checks belong to frontend profiles only.
- import-cycle checks MAY differ by language and tooling.

## Unsafe Pattern

Do not write a heuristic once and present it as universally correct for all repositories.
