# Skill Classes
#tags: skills review

## memory skill
**Typical concerns:** retrieval quality, degraded mode, hygiene, schema stability, regression tests.

**Checklist:**
- retrieval is deterministic enough
- degraded mode is honest
- memory writes have one clear owner
- stale state can be refreshed
- schema output is machine-checkable

## continuity skill
**Typical concerns:** checkpoints, durable state, restart safety, stop rules, context recovery.

**Checklist:**
- next action is always visible
- checkpoints exist before long tasks
- recovery path is named
- stale or missing state is handled explicitly
- the skill does not rely only on raw chat history

## network diagnosis skill
**Typical concerns:** topology correctness, one-fix-one-verify discipline, route clarity, rollback awareness.

**Checklist:**
- the likely fault domain is narrowed early
- one change is verified before the next one
- local versus remote path is explicit
- destructive changes are gated
- fallback behavior is named

## orchestrator skill
**Typical concerns:** session handling, fallback behavior, tool/runtime coupling, prompt discipline.

**Checklist:**
- session reuse rules are explicit
- tool choice is deterministic
- failure of the orchestrator path is handled
- round output is structured
- the skill does not assume hidden state

## tooling or skill-creator skill
**Typical concerns:** lifecycle gates, validators, packaging, enforcement, folder hygiene.

**Checklist:**
- validator expectations are met
- packaging path is explicit
- reference split is sensible
- versioning is honest
- publish gate is named

## workflow or methodology skill
**Typical concerns:** autonomy boundaries, deterministic sequencing, failure handling, easy navigation.

**Checklist:**
- branch rules are explicit
- the shortest safe path is visible
- failure and stop rules are short and concrete
- examples match the real flow
- the flow is cheap for weak models

## infra or deployment skill
**Typical concerns:** operational safety, environment assumptions, restart behavior, rollback, observability.

**Checklist:**
- environment assumptions are stated
- changes can be reversed
- health checks exist
- deploy and rollback are separate
- action order is clear

## hybrid skill
**Typical concerns:** mixed responsibilities, hidden overlap, split between runtime and maintenance, too much scope.

**Checklist:**
- the primary class is named
- the secondary class is named
- overlap with other skills is bounded
- runtime and maintenance are split cleanly
- the user can tell when to use it
