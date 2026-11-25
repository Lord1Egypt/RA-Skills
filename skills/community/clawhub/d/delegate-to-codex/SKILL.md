---
name: delegate-to-codex
description: >-
  Use when the user explicitly asks for repository work to be handed to
  Codex: "delegate this to codex", "have codex do it", or the slash command.
  Covers choosing the model, writing the handoff, running `codex exec`,
  reviewing the diff that comes back, and committing it. Never reach for it
  unasked: work you could do directly, do directly. Not for use from inside
  Codex unless the user asks for nested delegation.
---

# Delegate to Codex

The orchestrator owns task selection, decomposition, final review, Git history, and user communication. Codex owns inspecting the repository, choosing implementation details, editing its bounded scope, and running validation.

**What leaves the machine.** Codex sends the handoff prompt and whatever repository content it reads to the model provider its config points at, usually OpenAI. Do not delegate a repository, or put secrets in a prompt, that the user would not share with that provider. Every run uses the user's Codex account and counts against its quota or bill, which is why the model and effort choice below is explicit.

**Only delegate when the user asked you to.** Large, tedious, cross-cutting, or precisely specified is not a trigger. Once they have asked, the delegation covers the whole piece of work under discussion, including follow-up runs and the commits that finish it. Do not re-ask per run.

## Decide whether to delegate

Delegate work needing sustained repository context: debugging, multi-file changes, migrations, refactors, test-backed implementation, substantial investigation. Do it yourself when it is a trivial edit, a one-command lookup, or smaller than the overhead of composing, running, and reviewing a second agent call. Codex also works as a read-only reviewer of factual prose you wrote (`-s read-only`, no `--approve-for-me`): ask for findings only, each with the exact phrase, a source, and a confidence level, and freeze style explicitly so it reports errors instead of rewrites. Independent read-only reviews can run concurrently. Codex can also hunt for bugs: give each run one user's slice of the product (an owner of one business type, a customer), let it drive the running app with scratch Playwright specs, and ask for findings with repro steps and severity, no fixes. You triage them into fix runs.

Split into independently reviewable outcomes, never file-sized fragments. Keep a vertical change together when its schema, implementation, tests, and docs must agree. A single coherent run beats several context-starved calls, so split only for two reasons: a run killed for running too long, or a task wide enough to be worth a cold repository re-read per run.

When you do split:

- Run the pieces sequentially in one worktree, committing between each. Concurrent runs need a separate worktree per process; never two Codex processes in one tree. Separate worktrees still share one machine and one account: five fix runs in parallel hit the usage limit together and timed out each other's full test suites, while the same five run one after another in a loop script took 3–7 minutes each. Run them in sequence unless the runs are short and light. Sibling branches that touch one component break each other's test mocks on merge, so run the full suite on the merged result, not only on each branch.
- Give every prompt a boundary sentence naming the files the *other* runs own.
- Name the intermediate state the split invents, mark it temporary in the code, and forbid tests that assert it. The next run has to delete such a test, and a deleted assertion is indistinguishable from a weakened one under review.

## Select the model and effort

Respect an explicit user choice. Otherwise:

- `gpt-6.2-sol`: the default. Anything needing judgment, and most other work too: architecture, ambiguous behavior, unfamiliar or cross-cutting code, hard debugging, security and data-safety work, migrations, performance, a change whose correct shape must be discovered. We are still learning how it behaves, so record surprises (see the last section).
- `gpt-6-astra`: a TOKEN EATER. Only for creative tasks and really hard problems that Sol has already failed or clearly cannot carry. Never pick it for routine work.
- `gpt-5.6-terra`: mechanical, well-scoped implementation. Routine test additions, narrow refactors, config changes, dependency bumps, ordinary features with clear acceptance criteria.
- `gpt-5.6-luna`: cost-sensitive, high-volume work with an unusually clear path and success check. Avoid where a subtle mistake would be expensive.
- `gpt-6.1-sol`, `gpt-5.6-sol`, `gpt-5.5`: previous generations. On request, for compatibility, or for a workflow already evaluated on them.

Use explicit model names so routing is obvious. If the selected model is not enabled for the local account, report that and fall back only where permitted.

A detailed plan does not make a task mechanical. Judge by the cost of a subtle mistake, not by how precisely you wrote the prompt. Judge breadth separately from difficulty: a wide task invites the cheaper model to scope itself down without saying so, so move up a model or narrow the run.

**Default to `gpt-6.2-sol` at `medium` effort.** Drop to `low` for easier tasks: a clear path, a narrow scope, an obvious success check.

**`high` is not yours to spend.** Ask the user first, name the part that needs it, and run at `medium` if they decline or there is no one to ask. A user who asked for `high` has already authorized it. Otherwise do not ask about effort per call. Pass model and effort explicitly, and never swap a requested model without saying so.

## Establish the workspace

1. Resolve the exact repository or worktree path, and read the repo's instructions and release policy.
2. Snapshot `git status --short --branch`; record pre-existing edits and untracked files.
3. Define one bounded outcome, its acceptance criteria, and who owns commit and push.
4. Identify the destructive, external, privileged, or deploy-triggering actions that stay outside Codex's authority. Separate those from steps the repo's documented workflow requires, such as a translation or codegen script that calls a paid API: authorize those in the prompt or plan to run them yourself, or Codex stops and asks.
5. If the change adds to an enumerable set (MCP tools, routes, nav entries, status values, error codes), find every assertion that counts or lists it before writing the prompt and name those files as authorized to update. `grep -rn "toHaveLength([0-9]" <test dirs>`, plus a grep for the count as a numeral and spelled out in prose, finds most.
6. Accessible names are an enumerable set too. Reusing a component puts its labels on screen twice, and `getAllByRole` then fails by ambiguity rather than by behavior. Grep the locale catalog first, and say the new instance needs its own strings while the original's stay byte-identical.

A boundary drawn in paths does not hold inside a file several audiences share — a locale catalog, a constants module, a config. Name the frozen regions within it, or a rename sent after the manage-side copy also rewrites the marketing sentence sitting three keys away. State the acceptance criterion as an exact diff shape ("`git diff` shows exactly 78 changed lines, all `explanation` values"), so the boundary is checkable at a glance.

A clean worktree makes "every change in the diff is Codex's" true, which is what lets you review by diff alone. It survives only while nothing else writes to the tree. If the scope overlaps dirty files, say so in the prompt or isolate the work. A fresh worktree lacks gitignored files, so name any file Codex should edit outside it by absolute path into the checkout that owns it; a relative path gets a stray new copy.

Let Codex load the repo's own `AGENTS.md`, user config, and skills. Do not paste them in, and do not use `--ignore-user-config` or `--ignore-rules` outside reproducibility testing.

## Write the handoff prompt

Give Codex the intent and everything that affects correctness, then get out of the way on implementation detail.

Separate three kinds of input explicitly, because Codex weighs them differently:

- **Verified external facts.** A spec revision, a changed API, a fetched doc. Label them authoritative and say *"do not correct these from memory"*, or a model restores the field name it remembers. Declare here too any in-repo idiom that pattern-matches to a famous bug, such as money kept in whole units and rounded like cents.
- **Settled user decisions.** Say "do not revisit these."
- **Your design sketch.** Label it *shape suggestions*, subordinate to what the repo actually does.

**Pass conclusions and coordinates, not transcripts.** Codex re-reads the repo anyway, so a pasted survey is paid for twice and is stale by the time it is read. Carry only the exact `path/file.ts:line`, the helper that already solves the adjacent problem, and the invariant written down nowhere.

Template, omitting empty sections:

```markdown
You are the implementing agent for one bounded repository task.

Goal: <The finished behavior or artifact, not activities. Include the acceptance bar.>

Context: <Requirements, issue details, observed errors, evidence.>

Verified external facts, AUTHORITATIVE. Do not correct these from memory: <Spec/API facts checked this session, with the exact names and values.>

Decisions already made, do not revisit: <Settled choices, so they are not relitigated.>

Design, shape suggestions only. Follow the repository where it differs: <Layering, key signatures, sketches.>

Scope and constraints:
- Work only in the current repository/worktree.
- Read and follow all applicable AGENTS.md and repository instructions.
- Inspect the existing implementation and follow established local patterns.
- Preserve pre-existing user changes: <paths, or "the worktree is clean">.
- Do not modify <out-of-scope areas>; report the need instead.
- Inside <shared file>, leave <frozen regions> alone.
- Do not commit, push, deploy, publish, or perform external writes (anything leaving this machine; the dev server and backend on 127.0.0.1 are in scope).
- Do not change dependency manifests or lockfiles. If the work needs a package, stop and say which one and why.
- Resolve ordinary implementation details autonomously from repository evidence.
- If a material ambiguity would change public behavior, data safety, or scope, stop and explain rather than guessing.

Tripwires, existing invariants that must not break:
- Do NOT edit existing tests to make them pass. A failing existing assertion means the implementation is wrong.
- <Named fragile contracts: exact strings, counts, serialized shapes, orderings.>

Acceptance criteria:
- <Observable criterion 1>

Validation:
- Run <specific commands>. Report each command, its result, and anything not run.

Return a concise summary of the implementation, files changed, validation results, and remaining risks or questions. If you run out of room, stop and say plainly what you did not build. A truthful partial report is more useful than a tidy one.
```

Keep that last sentence. It converts a silent shortfall into a review item. Do not shrink the summary further; delegation's tokens go into reading the diff, and a tighter boundary saves more than terser prose.

**Naming the tripwires pays off more than anything else in the prompt, and it needs a carve-out or it backfires.** "Do not edit existing tests to make them pass", plus the exact fragile contracts (a serialized shape, a count stated in prose, a deliberate ordering), stops a suite going green because the assertions moved. When your change legitimately alters an expectation, say so and say where: extending a list or updating a count to describe deliberate new behavior is correct, deleting a case or relaxing `toEqual` into `toContain` is not.

For a signature or type migration rather than a behavior change, ask for existing tests to be adapted with a local shim named after what it replaces, so the assertions stay byte-identical. A rewritten assertion and a weakened one are the same diff shape.

**Read your own constraints for self-contradiction before sending.** A prompt that forbids the only way to do what it demands costs a full round trip. Check each "do not" against each "must". A change that deliberately reverses a behavior collides with "do not edit existing tests": grep the tests for the old behavior and name the assertions that may change. Read each absolute too ("nothing", "never", "always"): Codex applies it to every path it can reach, so name the paths it covers. "Nothing reloads while busy" once disabled a consenting Reload button along with the silent reloads it was meant for. A written style guide in the repo outranks "fix errors only, do not polish": say whether the run applies the guide or only fixes outright errors, or a copy review comes back as a sweep (218 sentence-case edits and 158 test literals from one such prompt).

Ask for diagnosis only when diagnosis was requested; ask for implementation and validation when a change was requested. State each constraint once. Do not add "think step by step" or generic coding advice.

## Invoke Codex

Verified against codex-cli 0.172.0:

```bash
codex exec \
  -C /absolute/path/to/repository \
  -m gpt-6.2-sol \
  -c 'model_reasoning_effort="medium"' \
  --approve-for-me \
  -o /unique/path/last-message.md \
  - < /unique/path/prompt.md
```

Send the prompt via stdin from a uniquely named file. Never interpolate user-controlled text into the shell.

- **`--approve-for-me` cannot be combined with `--sandbox`.** It already implies the workspace-write sandbox, and passing both fails argument parsing before any work happens. Use `-s read-only` without `--approve-for-me` for pure inspection.
- **Options belong to `codex exec`, so they must come before any subcommand.** `codex exec -C repo --approve-for-me -o out.md resume --last -` works. The same flags after `resume` die with `error: unexpected argument '--approve-for-me' found`, silently and looking like success.
- The `--approve-for-me` sandbox has no network, localhost included. A run that drives a dev server, a local backend, or Playwright needs `-c sandbox_workspace_write.network_access=true`. With it, a UI run can screenshot its own change, so put that in the acceptance criteria rather than keeping the visual check for yourself.
- `--add-dir /exact/path` only when another writable directory is needed. `--json` when a program needs event data or a thread ID, paired with `-o`. Omit `--ephemeral` when a follow-up may resume the session. `--skip-git-repo-check` only for a verified non-repository workspace.
- Never `--dangerously-bypass-approvals-and-sandbox` unless the user explicitly authorizes it inside an already-isolated environment. `--full-auto` is deprecated.

If a flag is rejected, read `codex exec --help`. Do not guess replacement safety flags.

## Run it and confirm it actually ran

Long runs exceed foreground tool timeouts. Prefer background execution, writing the exit status where nothing can overwrite it, and detach it from your session: a run started as your own background job dies with it, and a restart or context compaction killed five runs mid-edit. `setsid nohup` is not enough where the host kills its whole cgroup on restart, as one did mid-run; on Linux with systemd, run it as a transient user unit instead, and fall back to `setsid nohup` elsewhere:

```bash
systemd-run --user --unit=codex-<task> --collect bash -c 'codex exec ... > out.log 2> err.log; echo $? > exit.code'
# without systemd:
setsid nohup bash -c 'codex exec ... > out.log 2> err.log; echo $? > exit.code' < /dev/null > /dev/null 2>&1 &
```

**Never append `; echo "EXIT=$?"` or any trailing command to the invocation**, and never read a pipeline's exit code. The trailing command's own success becomes the status, so a failed run reports 0, and `pnpm test 2>&1 | tail -40` reports `tail`'s status. Trust the runner's summary line.

A CLI argument error is silent and looks exactly like success: exit 2, empty stdout, no `-o` file, an unchanged worktree. Before reviewing anything, confirm `exit.code` is `0`, the `-o` file exists and is non-empty, and `git status` differs from your snapshot unless the task was read-only.

Codex echoes the entire prompt to stderr before it starts, then everything it reads and thinks, so the file runs to tens of kilobytes. Never `cat` it. Use `tail -c 2000`, and read the `-o` file for the result. Its header does repay a look within seconds of launch: `grep -m3 -E '^(model|sandbox|reasoning effort):'` shows what is actually in force, and a wrong model is cheapest to stop before it edits anything. With `--json` that header is not written and stderr stays empty; read the model and sandbox from the session file instead: `grep -o -m3 -E '"model":"[^"]+"|"sandbox_policy":\{[^}]+' ~/.codex/sessions/*/*/*/rollout-*-<thread-id>.jsonl`.

For concurrent runs: a distinct handle, log, result path, and thread ID per task; a separate worktree per editing process; wait on every process and check every exit status; never `resume --last`.

Treat nonzero exit as failed delegation, distinguishing a tool or argument failure from an incomplete code change. **A killed run is a different case**, and writes no exit-code file at all. Kill by a PID read from `ps`, never `pkill -f <session id>` or a loop over `pgrep -f <pattern>`: the pattern also matches the shell running the command, which then dies with exit 144 and takes the rest of that command with it. Inspect before re-running: `git status` against your snapshot, `wc -l` the new files for truncation, the tail of stderr. A clean worktree means nothing is lost, so re-run narrower. A worktree of complete files means the kill landed during the summary and the work may be finished, so validate what is on disk and close small gaps yourself. A usage-limit stop looks like a failed run: exit 1, no `-o` file, partial edits on disk, and a stderr tail reading "usage limit … try again at HH:MM". Wait until then and `resume` the same session with "you were interrupted; inspect the worktree, finish, and validate" plus the original request. A fresh run would redo or fight the partial work. When the stop comes late, the diff on disk is often nearly complete: review it as you would a finished run and close the gaps yourself instead of waiting for the reset. One run died at its quota with only a duplicated message, two stale test selectors and a missing plural left to fix.

## Review

Codex's summary is a claim, not evidence. Verify independently:

1. Diff `git status` against the pre-run snapshot; note files it touched that you did not scope. A manifest or lockfile change is a decision, not a detail, even when it only promotes a package already installed transitively: that one moved remark into the Convex bundle.
2. Read the full diff of the source changes.
3. Check that existing tests were not weakened: `git diff -U0 <test paths> | grep -E '^-[^-]'`. Deletions should be pure refactors, never removed assertions. Read the paired `+` line before judging; a replaced expectation and a deleted one are one character apart.
4. Re-run the type check, linter, and test suite yourself. Compare the test count to before.
5. Check acceptance criteria, edge cases, error handling, security and data implications, and consistency with local patterns.
6. Confirm nothing was committed, pushed, deployed, or published.

When auditing coverage, grep for the behavior (a distinctive identifier, an error code, a header name), not for `it(`. Table-driven tests written with `it.each` hide their cases from a title-only search.

**A green suite is Codex grading its own work.** It wrote those cases against the implementation it had just written, so they pass by construction. Read them for two things: the input the implementation does not handle, and any test that primes by hand the state the real wiring should produce. When a test sets up the integration point instead of exercising it, write the one that goes through the real path. Layout is the common case: jsdom computes none, so an overflow or wrapping fix comes back with assertions on class strings. Those passed while one of the fixes still overflowed by 200px. Replace them with a browser test at phone width that measures where the text actually renders: the glyph rects, since a card that clips its overflow hides the text without widening the page. Specs Codex wrote but could not run, such as e2e against a shared backend, are unverified: run them before reviewing the diff, and when one fails, ask whether the product or the expectation is wrong before accepting a test edit. Flakiness under `--repeat-each` can be the harness rather than the code: parallel copies of one spec clash on a shared account or fixture. Re-run with `--workers=1 --repeat-each=N` before accepting a fix for a race. One came back with a file lock that hid the clash, and the real fault turned out to be a throttle that needed a retry.

**Look at user-visible copy in every locale the change touches**, rendered, not only English. Tests usually run in English, so translations reach review untested. A Russian notice ended in a double period: the abbreviated month (`окт.`) already carries one, and the sentence added another.

**When it stops and offers you options, check the repository before picking one.** The halt is the behavior you want, but the options are the ones it can see, and each may be a change where the answer is an existing convention. Grep for how the nearest sibling feature solves the same problem, and reply with that.

To correct, resume the same session with concrete evidence. A cleanup request riding along with a fix ("simplify it if you can") widens the scope: name the behavior it must keep, or leave it out. One once dropped a deliberate case while tidying an effect. Options precede the subcommand:

```bash
codex exec -C /absolute/path/to/repository -m <same model> -c 'model_reasoning_effort="<same>"' \
  --approve-for-me -o /unique/path/fix.md \
  resume <SESSION_ID> - < /unique/path/findings.md
```

Send findings via stdin from a file for anything longer than a sentence. Use `resume --last` only with exactly one recent session in that directory and no concurrency, and pass `-m` and the effort override again on every resume: `resume` does not inherit the session's model but falls back to the config default, silently (seen on codex-cli 0.162.1). A sandbox change on resume does take effect, so a read-only interview or diagnosis turn can continue in the same session with `--approve-for-me` to implement, keeping everything it has read. If the same material problem survives two focused attempts, reconsider the prompt, the model, the boundary, or whether to do it yourself.

## Commit, push, and report

Git history stays under orchestrator control, so tell Codex not to commit or push. Validate before staging, then stage by name, never with `git add -A`. Re-list the changed files right before committing and compare them against the set you reviewed; another process in the same tree can add to them between the two steps. Where a pre-commit hook stashes unstaged changes, as lint-staged does, skip it with `--no-verify` while another process is live in the tree, and only once its checks have passed on the full tree.

Commit only when requested or clearly authorized; "implement X" is not authorization to commit X. Push only on explicit request or when the workflow requires it, checking first whether it triggers CI, deployment, or publication. Prefer atomic commits per stable outcome.

Report by leading with the verified outcome, not with the fact that another agent was used: what changed, what validation you ran yourself and its result, commit and push state, and material caveats or skipped checks. Mark which claims you verified and which are Codex's. Never report success solely because `codex exec` exited zero.

## Propose improvements to this skill

Once the work is reported, say what the session taught about delegating and offer it as a concrete edit. Do that unprompted, including when the session went well, and never edit this file unasked.

**The bar is whether it would have changed what you did**: a surprise that cost a round trip, a defect that survived a green suite, a boundary or prompt technique that visibly worked or failed, a model or effort choice wrong in a way you can diagnose. Not a data point confirming advice already here, and not a lesson you did not actually learn. Anything true only of the repository you worked in belongs in *that* repo's `AGENTS.md`.

**Fold in; do not append.** Every delegation reads this file start to finish, so its length is a cost paid on every run. Put a lesson inside an existing paragraph. When a session contradicts what is here, propose deleting that advice rather than qualifying it into vagueness. Commit the skill separately from the work it came out of.

## Avoid recursive delegation

When this skill is loaded inside Codex itself, do not invoke another Codex process unless the user explicitly asks for another layer. Work with the tools already available.
