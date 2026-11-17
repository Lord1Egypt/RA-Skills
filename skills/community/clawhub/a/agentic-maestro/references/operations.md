# Operations: running several executors on one machine

Defaults from one setup; adjust per machine.

## Concurrency
- Up to 4 executors at once (they are mostly idle while waiting on the model).
- At most 2 heavy check commands at any moment, through the lock script: put
  `"gatePrefix": "<skill>/scripts/gate.sh"` in the brief spec so every gate command is wrapped
  (`GATE_SLOTS`, `GATE_LOCK_DIR`, `GATE_MAX_WAIT`).
- Sandboxed executors may not be able to write the default lock directory under `$TMPDIR` (gate.sh then
  exits 69). Set `GATE_LOCK_DIR` in the brief's env exports to a directory every sandbox can write,
  owned by you with mode 0700, and test it INSIDE one executor's sandbox before relying on it.
- Container runtimes capped (for example 2 CPUs). Never run a full battery alongside executors. Use
  `nice -n 5`, not background QoS (background priority made checks 3–4 times slower).

## Lanes and ownership
- The plan gives each parallel lane a file set it owns. Shared hotspots — barrel/index files,
  lockfiles, migration and decision-record numbers, generated files, `docs/CODEMAP.md` — belong to one
  lane or are reserved for integration. Allocate migration numbers in the plan, not at merge time.
- Stack dependent features: start B from unmerged A's branch, and rebase when A lands.

## Git
- Before the first executor runs, make sure the project ignores `.agent-logs/`, `.agent-briefs/` and
  `.agent-runs/`.
- Before committing an executor's work, run `scripts/scope-check.sh` and `git status`; never a blind
  `git add -A`.
- Some sandboxes cannot commit inside git worktrees: the orchestrator commits. Such an executor cannot
  merge either (its "merge" is only working-tree content): the orchestrator merges the base branch and
  commits the merge BEFORE launching the executor, or records the result as one two-parent merge
  commit afterwards, never as a plain commit.
- Push every lane with an explicit refspec (`git push -u origin HEAD:refs/heads/<branch>`), check the
  exit code, and check that local HEAD equals the remote branch: a stacked worktree branch inherits its
  parent's upstream, so a bare `git push` fails or targets the wrong branch.
- Commit messages follow the project's attribution rules (some projects forbid AI trailers).

## Background jobs
- Track every background job (the harness's background task, or `spawn.mjs` under a watcher); never
  fire-and-forget with `&`. A "running" status with a dead process is orphaned: cancel and relaunch.
- Run CLI agents with stdin closed or fed (`spawn.mjs` feeds the brief and closes it); some wait for
  stdin forever otherwise.

## Reviewer prompts
- Delta-scoped: the commit range, the fix diff PLUS the invariants it touches and any open findings.
- "Keep it tight, budget for the final report."
- Findings as P1/P2/P3 with file:line, then a verdict: PASS / PASS-WITH-FOLLOWUP / NEEDS FIXES.
- Frame as correctness and input-validation verification, not attack wording (content filters).

## Keep context small
- The project instruction file stays at most ~15 KB (rules, commands, index). Long per-area
  conventions live verbatim in `docs/conventions/<area>.md`, where `conv.sh` can quote them.
- Progress/history files keep recent milestones; older ones are archived verbatim.
- Regenerate `docs/CODEMAP.md` after merges that add, move or rename files.
- Read only the report block and `result.json` of a run by default; read the FULL report and logs
  whenever the status is not done, any exit code is non-zero, or the verdict is not PASS.

## Cost ledger
`spawn.mjs --ledger docs/agent-ledger.tsv --feature F12 --round 1 --role build` appends one row per run
(time, harness, model, effort, seconds, exit, session, tokens, cost when the CLI reports it). After
arbitration, fill the `findings` column of the review row (for example `P1=0 P2=2 P3=1`). Use it to
route the next feature: a component class that needed 3+ fix rounds on a cheap executor goes to a
stronger one next time. For in-process agents, add the row by hand.
