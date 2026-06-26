# Verification Reference

Use this reference to verify a Team against its blueprint.

## Verification layers

### 1. Participants

Confirm the expected participants:
- every role the contract actually names — `main` / `worker` / `reviewer`, something custom, or a flat set of peers — rather than assuming a fixed topology
- which host each participant runs on, so same-host and cross-host readiness are not confused
- whether the required OpenClaw agents exist
- whether the ClawMem plugin is available to each participant in its own OpenClaw host
- whether each selected agent is `configured`, `bootstrap-on-first-use`, or `blocked`
- for same-host participants, whether the current control session can still reach them or whether session refresh / pairing repair is still pending
- for participants on other hosts, whether they can reach the shared ClawMem repo (there is no local dispatch path to verify; readiness runs through the repo)

### 2. Structure

Confirm the expected:
- org
- repos
- teams
- members
- collaborators

### 3. Access

Confirm each actor has the intended access:
- read
- write
- admin

If access is missing, inspect whether the gap is caused by:
- missing membership
- missing team-repo grant
- pending invitation
- wrong repo target

### 4. Contract

Confirm the canonical Team artifact exists and matches the blueprint:
- same roles
- same repo purposes
- same workflow contract
- same verification target

### 5. Happy path

Run one minimal workflow proof:
- create or inspect one task issue of a kind named in this Team's contract
- verify its body references the canonical Team artifact by id or path
- verify the assigned participant actually fetched the canonical Team artifact via an explicit tool call (`memory_get` or `issue_get`) before acting — auto-recall alone does not count. On a shared host, verify directly; when the participant is on a different host, the fetch must be observable through the participant's own tool trace, a citation comment on the task issue, or equivalent evidence
- verify every label used on the task belongs to the Workflow Label Schema in the contract; reject off-schema labels
- verify one actor can act and one result can be observed
- when the contract names multiple roles, verify each required role has a viable actor
- verify that a real handoff happened end to end. Two forms are valid, and the contract should name which one the Team uses:
  - direct dispatch on a shared host, when the runtime exposes agent-to-agent dispatch
  - repo-mediated pickup, when a participant on any host polls the shared repo (`issue_list state:open` plus the task-kind label) and picks up an unclaimed task
  Either counts as long as a different participant than the one who wrote the task actually moves it through the contract's status labels.
- do not count orchestrator-authored proxy writes, config inference, or shared backend authorship alone as proof that another participant executed the task
- if agent config or gateway state changed during bootstrap on a shared host, re-establish the session or pairing before claiming success; for cross-host teams there is no local pairing to repair — use repo-mediated evidence instead

### 6. Closure

Run the terminal-state proof:
- when the task reaches the terminal status label, the issue has also been closed (`state: closed`) via `issue_update`, ideally in the same mutation
- the canonical polling filter (`issue_list state:open` plus the task-kind label) no longer returns the completed task
- no worker re-picks the completed task on a subsequent turn

Setting the terminal status label without closing the issue, or closing the issue without the terminal status label, both fail this layer.

## Result format

Return:
- `ready` when all required checks pass, the worker fetched the contract explicitly before acting, labels on real issues stay inside the schema, and completed tasks no longer appear in the polling filter
- `blocked` when the Team cannot be used
- `partial` when the Team exists but one or more required steps remain, including session refresh, pairing repair, missing worker dispatch proof, missing contract fetch by the worker, off-schema labels on real issues, or finished tasks still visible in the canonical polling filter

Then list the smallest repair actions needed, starting with participant gaps when present.
