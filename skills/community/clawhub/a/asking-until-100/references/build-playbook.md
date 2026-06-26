# Build Playbook

Use this file when the task is about project setup, build systems, deployment, CI, packaging, or
delivery.

## Check first

- runtime and version constraints
- package manager and lockfile expectations
- target environment
- build output type
- CI provider
- deploy target
- secrets or configuration requirements
- rollback expectations

## Repo-aware checks

- inspect CI files before asking which provider is canonical
- inspect lockfiles before asking which package manager is authoritative
- inspect deploy files before asking which target is primary
- keep rollback and success criteria as explicit questions when they remain unstated

## Missing evidence that should trigger more questions

- failing command output is absent
- runtime version is unknown
- package manager is implied but not stated
- deploy target is missing
- success criteria are vague
- the request mixes scaffolding and migration without naming the current state
