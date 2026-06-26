# Main Worker Summary Queue Template

Use this reference when a user wants the current ClawMem Team demo shape moved out of the plugin and into an external template.

## Best fit

Use this template when:
- one agent should coordinate
- a worker pool should execute
- work should be visible in a shared queue repo
- task status should advance through an explicit label protocol

## Participant readiness

Before using this template, confirm each participating OpenClaw host has:
- the ClawMem plugin installed and enabled
- the bundled `clawmem` runtime skill available to the participating agent

Participants may all share one OpenClaw host or run on different hosts (possibly on different machines). Record this as the Team's host topology (`single-host`, `multi-host`, or `mixed`) and carry it through bootstrap and verification — the handoff between `main` and `worker` works differently in each case:
- single-host: direct dispatch between agents on the same host is possible
- multi-host: handoff is repo-mediated — workers poll the shared queue repo for unclaimed `queue:task` issues and pick up work from there; there is no direct dispatch to verify
- mixed: same-host workers use direct dispatch, remote workers use repo-mediated pickup; both paths have to be proven separately

Use this template with a default starting topology of:
- 1 main agent
- 2 worker agents

Treat fewer than 3 participating agents as not ready for this template. If the user wants a smaller setup, switch to a custom Team design instead of silently shrinking this template. The role names `main` and `worker` come from this template; a custom Team may use different names with the same shape.

For each selected participant, track these readiness layers:
- OpenClaw status: `existing`, `to-create`, or `user-confirmed only`
- ClawMem status: `configured`, `bootstrap-on-first-use`, or `blocked`
- handoff status: `verified`, `not-yet-tested`, `session-refresh-required` (same-host only), or `blocked`

Only treat a participant as ready when that agent can use ClawMem in its own OpenClaw host.
Only treat the template as fully ready when a real handoff has been observed — direct dispatch on a shared host, or a worker on another host actually picking up a queue task through `issue_list state:open` and updating it.

## Agent selection flow

- If only the current agent is known:
  1. Explain that this template expects `1 main + 2 workers`.
  2. Confirm the new worker agents will also run in the same OpenClaw environment with ClawMem available.
  3. If the runtime can create agents, prepare two worker agents after explicit user approval.
  4. Otherwise stop at a readiness plan and ask the user to create or expose the missing workers.
- If multiple agents already exist:
  1. Inspect or confirm the available agents.
  2. Filter out any agents that cannot use ClawMem in the current host.
  3. Ask whether to use the default 3-agent topology or to choose specific existing agents.
  4. If the user has no strong preference, keep the current agent as `main` and choose two existing agents as workers.

## Post-bootstrap session readiness

Same-host setups. If bootstrap changes the OpenClaw agent list, worker workspaces, gateway config, or pairing state on this host:
- assume the current session may no longer be a valid worker-dispatch path
- require a fresh session or repaired pairing before claiming the template is fully ready
- report `partial` instead of `ready` until one real worker handoff succeeds

Multi-host setups. There is no on-host pairing between the orchestrating agent and remote workers; readiness runs through the shared repo instead:
- each remote host must already have the ClawMem plugin enabled and the bundled `clawmem` skill active — that is the only prerequisite the user has to take care of per machine. Contract binding itself rides inside each task body, so the orchestrating agent does not install anything on remote hosts.
- each remote worker must actually poll the shared queue repo and pick up unclaimed tasks
- one real repo-mediated pickup has to be observed before this template is `ready`; until then it is `partial`

If multiple OpenClaw agents share one ClawMem backend identity (same host or different hosts):
- disclose that repo authorship and comments may still appear under one shared backend account
- do not use shared authorship alone as proof that different workers actually acted

## Recommended protocol

This template ships a concrete Workflow Label Schema. ClawMem stays label-agnostic, so this schema is owned by the template, not the plugin.

Task-kind labels:
- `queue:task`

Status labels (finite set — do not invent new values without updating the Team contract first):
- `task-status:todo`
- `task-status:handling`
- `task-status:blocked`
- `task-status:done` (terminal)

Assignment label:
- `assignee:<agent-id>`

Terminal closure rule:
- when a task moves to `task-status:done`, the worker must also close the issue with `issue_update state:closed`, ideally in the same call
- setting `task-status:done` without closing, or closing without `task-status:done`, both violate this schema

Canonical polling filters workers use to pick up work:
- assigned work: `issue_list state:open labels:queue:task assignee:<self>`
- unclaimed work: `issue_list state:open labels:queue:task,task-status:todo`

Because `issue_list` defaults to `state: open`, closed tasks never reappear in the polling filter.

## Recommended blueprint shape

Define:
- one main agent
- two worker agents by default
- one shared summary queue repo
- optional extra workers or private/project repos for deeper execution work when the user already operates a larger pool

## Bootstrap path

1. Inspect or confirm the available agents.
2. Confirm the current OpenClaw environment has ClawMem enabled for the participating agents.
3. Reconcile the current inventory with the required `1 main + 2 workers` shape.
4. Prepare missing worker agents if the runtime supports it and the user approves it.
5. Confirm which agents will act as `main` and `workers`.
6. If agent config or gateway state changed, record whether the current session needs refresh before worker verification.
7. Confirm the org boundary and who owns the queue repo.
8. Create or reuse the summary queue repo.
9. Create or reuse the team and grants.
10. Write the template contract, including the full Workflow Label Schema above, as a stable ClawMem memory node labeled with a pair such as `kind:convention topic:team-contract`. The agent decides whether the contract memory lives in a dedicated team / coordination repo or inside the task repo itself, based on the user's setup; record the choice in the blueprint.
11. Define the queue task-body template. Every queue task issue this Team creates opens its body with an explicit citation such as:
    > Team contract: `memory_get #<contract-id>` (kind:convention topic:team-contract) before acting.
    and inlines the schema's most critical rules (the `task-status:*` set, assignee format, and the rule that `task-status:done` must be set together with `state:closed` via the same `issue_update`). No per-host install is required — the bundled `clawmem` skill's turn loop triggers the fetch when the id is cited in the body.
12. Seed one queue issue to prove the flow works, using that task-body template.

## Demo flow

One minimal demo should show:
1. main agent creates a queue task; the task body references the canonical Team artifact by id or path
2. one worker agent receives a real handoff through a working dispatch path
3. that worker agent fetches the canonical Team artifact via an explicit tool call before starting work
4. that worker agent starts work, applies the Workflow Label Schema, and adds a progress comment
5. that worker agent posts the result
6. that worker agent sets `task-status:done` and closes the issue in the same `issue_update` call
7. the canonical polling filter (`issue_list state:open labels:queue:task`) no longer returns the completed task
8. the second worker agent can at least see the queue repo and task labels

The main agent writing queue comments on behalf of a worker does not prove the Team works.
Moving a task to `task-status:done` without closing the issue does not prove completion; the canonical polling filter must stop returning it.
If dispatch fails because the current session needs refresh, pairing repair, or another runtime fix, the result is `partial`, not `ready`.
