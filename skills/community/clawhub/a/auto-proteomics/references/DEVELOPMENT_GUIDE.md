# Development Guide

## Objective

Maintain this repository as a public skill first, not a private lab notebook.
The design target for `v0.x` is:
- easy for a stranger to understand
- low token cost in chat use
- runnable for the shipped path
- explicit about what is real now versus planned later

## Public architecture

Use four lightweight layers:
- `L1`: `SKILL.md` for trigger cases, shipped scope, and public boundary
- `L2`: `references/WORKFLOW_INDEX.yaml` for routing and shipped-vs-scaffold classification
- `L3`: `scripts/` for runnable code
- `L4`: `references/` for stable guidance that should not be repeated in every chat

## Release rule

Every public document should answer two questions clearly:
- What can a normal user run today?
- What exists only as scaffold for future versions?

If a route is not shipped, say so directly.
Do not imply support just because a placeholder script exists.

## Documentation rule

Prefer this pattern:
- short promise in `SKILL.md`
- concrete routing in `WORKFLOW_INDEX.yaml`
- exact command in the relevant workflow script
- durable explanation in one reference file

Avoid:
- hidden assumptions tied to one private environment
- long conceptual prose in the entry file
- claiming validation that has not been completed on public data
- duplicating the same protocol across multiple docs

## Public `v0.x` product boundary

Shipped:
- processed DDA LFQ downstream analysis from MaxQuant-like protein-level tables

Scaffold only:
- raw DDA identification
- DIA quantification
- phosphoproteomics differential analysis
- enrichment workflows
- multi-omics planning and integration

## How to extend safely

When adding a new route:
1. decide whether it is scaffold or shipped
2. update `references/WORKFLOW_INDEX.yaml`
3. document the runtime and input contract
4. ensure the workflow has a stable entry command
5. only move it into the public promise after it is runnable and documented

## Quality bar for public release

Before calling a route shipped, confirm:
- the entry command runs
- required inputs are documented
- outputs are documented
- docs do not depend on private context
- the route is clearly separated from unfinished scaffold

## Validation posture

Mock examples are useful for structure checks.
They are not the same as public biological validation.
If a real dataset onboarding case is still in progress, document it as onboarding or future validation work, not as completed release evidence.
