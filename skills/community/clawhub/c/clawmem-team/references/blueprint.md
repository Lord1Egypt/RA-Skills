# Team Blueprint Reference

Use this reference to produce a consistent Team blueprint.

## Goals

The blueprint should:
- be specific enough for bootstrap
- keep conventions explicit
- avoid hiding any Team protocol inside the plugin
- make participant readiness explicit when the Team depends on multiple agents
- be minimal enough that the user can understand and approve it

## Required sections

Return the blueprint with these sections:

### 1. Team Summary

- team name
- target outcome
- why this Team shape fits

### 2. Participants

Roles are user-defined. Do not default to `main` / `worker` / `reviewer` unless the user or the chosen template declares those roles; otherwise use whatever role names the user named, even if they are a flat set of peers.

For each participant include:
- name or agent id
- role (as named in this Team's contract)
- responsibilities
- whether it is human, agent, or mixed
- host: the OpenClaw host the participant runs on, and whether it is the same host as the orchestrating agent
- OpenClaw status: `existing`, `to-create`, or `user-confirmed only`
- ClawMem status: `configured`, `bootstrap-on-first-use`, or `blocked`

Record the overall host topology in the Team Summary:
- `single-host`: every participant shares one OpenClaw host
- `multi-host`: participants run on different OpenClaw hosts (possibly on different machines)
- `mixed`: some participants share a host and others are remote

Host topology changes how binding is delivered and how handoff is verified. Carry it through bootstrap and verification.

If a template has a minimum participant shape, say whether the current environment already satisfies it.

### 3. Repo Plan

For each repo include:
- repo name
- owner
- purpose
- whether it stores durable memory, workflow coordination, or both
- whether it already exists or must be created

### 4. Access Model

Include:
- organization boundary
- teams to create or reuse
- direct collaborators if any
- repo permissions by actor

### 5. Workflow Contract

Make the operating protocol explicit, and include a full Workflow Label Schema (see SKILL.md § Workflow label schema):
- handoff model
- issue and comment usage
- task-kind labels in use
- status labels, including exactly one terminal status
- assignment label format
- terminal closure rule: when a task reaches the terminal status, the issue is also closed via `issue_update state:closed` in the same mutation
- canonical polling filter workers use to pick up work; it must restrict to `state: open` so closed tasks do not reappear
- when to create, update, close, or summarize work
- where final outputs land

ClawMem stays label-agnostic. The Team owns the schema, and the blueprint is where it becomes explicit.

### 6. Canonical Artifact

The default and simplest shape is a ClawMem memory node with a stable label pair such as `kind:convention topic:team-contract`. It composes with the bundled `clawmem` skill's turn loop: when a task body cites the contract's `#<id>`, the participating agent fetches it via `memory_get` as authoritative tool output — no per-host install needed.

Where the memory node lives is a design call the agent makes after analyzing the user's setup:
- a dedicated team / coordination repo, when the Team will run many workflows or spans multiple domains
- the task repo itself, when the Team is lightweight or workflow and memory naturally belong together
- another user-approved repo

Requirements:
- the artifact contains the full Workflow Label Schema from section 5
- the artifact is addressable by a fixed repo + issue number and a stable label pair, so task bodies can cite it and `memory_get` resolves reliably
- do not create duplicate sources of truth

Markdown files or bootstrap issues can serve when the user prefers them, but a memory node is the default because it composes with the existing clawmem retrieval path.

### 7. Bootstrap Plan

List the exact order of work:
1. inspect current participants and existing state
2. prepare missing participants if required and supported by the runtime
3. create missing org / repo / team objects
4. set access
5. materialize the canonical artifact, embedding the Workflow Label Schema
6. define the task-body template every team task will use: it opens with an explicit `memory_get #<contract-id>` citation and inlines the most critical rules (allowed labels and the `done ⇒ state:closed` terminal rule) so a participant that skips the fetch still has the minimum. No per-host install is needed; the bundled `clawmem` skill's turn loop triggers the fetch when the id is cited.
7. seed the first workflow object if needed, using that task-body template

### 8. Verification Plan

Include:
- participant readiness checks
- structural checks
- access checks
- label-schema compliance check: labels on real issues belong to the Workflow Label Schema, and the terminal status is only ever set together with `state: closed`
- polling-filter check: the canonical `issue_list` filter no longer returns finished tasks
- turn-opener check: the assigned participant fetched the canonical artifact via an explicit tool call before acting, not only through auto-recall. On a shared host, verify directly; when the participant is on a different host, verify via observable signals — the participant's own tool trace, a citation comment on the task issue, or equivalent evidence
- workflow happy-path check
- failure conditions

## Output style

- Prefer short sections over dense prose.
- Use stable names that can be reused during bootstrap.
- If a template inspired the blueprint, say so explicitly.
- When presenting the blueprint to the user, lead with the plain-language summary described in [communication.md](communication.md); show the sections above as the technical layer.
