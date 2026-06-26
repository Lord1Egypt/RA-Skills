# Bootstrap Reference

Use this reference to execute a Team blueprint safely.

## Order of operations

1. Inspect participants and existing state first.
2. Reconcile selected participants and existing state with the blueprint.
3. Prepare missing participants when the blueprint requires them and the runtime exposes that capability.
4. Create missing governance objects.
5. Create missing repos.
6. Apply access and membership.
7. Create the canonical Team artifact as a stable ClawMem memory node in the repo chosen for contract hosting (dedicated team repo or the task repo, per blueprint). Use a stable label pair such as `kind:convention topic:team-contract` and embed the full Workflow Label Schema.
8. Define the task-body template every team task will use. It opens with an explicit `memory_get #<contract-id>` citation and inlines the most critical rules (allowed labels and the `done ⇒ state:closed` terminal rule) so a participant that skips the fetch still sees the minimum. No per-host install is required; the bundled `clawmem` skill's turn loop triggers the fetch when the id is cited.
9. Seed the first workflow object only if the blueprint requires it, using that task-body template.
10. Hand off to verification.

## Inspection checklist

Inspect:
- whether the current OpenClaw environment has ClawMem installed and enabled
- whether the bundled `clawmem` runtime skill is available for the participating agents
- available OpenClaw agents or the user-confirmed participant list
- whether the required agents already exist
- whether each selected agent already has a ClawMem route, will bootstrap on first use, or is blocked
- host topology: whether every participant shares one OpenClaw host, runs on a different host, or a mix. Contract binding travels through ClawMem so no per-host install is needed, but handoff mode (direct dispatch vs. repo-mediated pickup) and how verification gathers evidence depend on the topology.
- role names the user (or the chosen template) has declared, so the contract does not silently default to `main` / `worker` / `reviewer`
- whether the current control session can still reach the participants it owns on this host, or whether a fresh session / repaired pairing will be needed after mutation; for participants on other hosts, confirm instead that they can reach the shared ClawMem repo
- organizations
- teams
- repo existence
- repo access
- collaborator state
- pending invitations if access is not visible yet

## Mutation rules

- Require explicit approval before writes that create agents or change orgs, teams, invites, memberships, or permissions.
- Only attempt agent creation when the current runtime exposes that capability. Otherwise stop with a readiness gap and ask the user to prepare the missing agents.
- If bootstrap changes agent config, worker workspaces, gateway state, or pairing state, record the need for post-bootstrap session refresh explicitly instead of hiding it.
- Do not report `ready` from structure-only mutations when real worker dispatch still depends on session refresh, pairing repair, or another runtime fix.
- Reuse existing names when they already satisfy the blueprint.
- Do not create extra repos or teams "just in case."
- Keep one authoritative Team artifact. Do not split the contract across multiple uncoordinated places.
- The terminal status label in the Workflow Label Schema must map to a closed issue. Never end a task by flipping a label alone; pair the label change with `issue_update state:closed` in the same mutation so the canonical `issue_list state:open` polling filter drops the task automatically.
- Every participant, regardless of role name or host, must fetch the canonical Team artifact by explicit tool call (`memory_get` or `issue_get`) at the start of each team task it picks up. The bundled `clawmem` skill's turn loop triggers this automatically when the task body cites the contract id, so the rule is met by task-body convention plus clawmem compliance — no separate per-host install is needed. Do not rely on auto-recall to deliver the contract, because the plugin frames auto-recall as background context, not instructions.

## Canonical artifact options

Prefer a durable ClawMem memory node with a stable label pair such as `kind:convention topic:team-contract`. It composes with the bundled `clawmem` skill's turn loop — when a task body cites the contract id, the participating agent's `memory_get` call returns the body as authoritative tool output rather than an auto-recall hint.

Where the memory node lives is a design decision the agent analyzes:
- a dedicated team / coordination repo when the Team will run many workflows or spans multiple domains
- the task repo itself when the Team is lightweight or workflow and memory naturally belong together
- either choice is valid; state it in the blueprint

Markdown files or bootstrap issues are acceptable fallbacks when the user prefers them.

Requirements:
- the artifact holds the Workflow Label Schema for this Team
- its address (repo + issue number + stable label pair) is deterministic, so task bodies can cite it and `memory_get` resolves reliably

When the blueprint does not specify one, stop and ask rather than guessing.

## Seed object

If the Team needs a first runnable example, create only one seed object:
- first queue task
- first review request
- first operating note

For multi-agent templates, that seed object proves the workflow only when a real worker path can act on it.
If the current session cannot reach the worker after bootstrap, stop at `partial` and surface the exact session or pairing repair needed.
