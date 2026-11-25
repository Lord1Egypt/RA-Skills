---
name: delegate-to-muse
description: >-
  Use when the user explicitly asks for repository work to be handed to Muse:
  "delegate this to muse", "have muse do it", or the slash command. Covers
  workspace trust, writing the handoff, running `muse exec`, reviewing the diff
  that comes back, and committing it. Never reach for it unasked: work you could
  do directly, do directly. Not for use from inside Muse unless the user asks
  for nested delegation.
---

# Delegate to Muse

Muse Code is Meta's terminal coding agent. The orchestrator owns task selection, decomposition, final review, Git history, and user communication. Muse owns inspecting the repository, choosing implementation details, editing its bounded scope, and running validation.

**What leaves the machine.** Muse sends the handoff prompt and whatever repository content it reads to Meta's model service. Do not delegate a repository, or put secrets in a prompt, that the user would not share with that provider.

**Only delegate when the user asked you to.** A task being large, tedious, cross-cutting, or precisely specified is not a trigger. Those you do yourself. Once the user has asked, the delegation covers the piece of work under discussion: follow-up runs, corrections, and the commits that finish it, until they say otherwise. You do not re-ask per run.

Invocation checked with **Muse Code 1.4.7** and `muse-wonder-1.0`. Historical examples below retain the versions on which they were observed. If a flag is rejected, read `muse exec --help` and adapt to the installed version rather than guessing at a replacement safety flag.

## Decide whether to delegate

Delegate work that benefits from sustained repository context: debugging, multi-file changes, migrations, refactors, test-backed implementation, substantial investigation.

Do it directly when it is a trivial edit, a one-command lookup, or smaller than the overhead of composing, running, and reviewing a second agent call.

Split a large request into independently reviewable outcomes, not file-sized fragments. Keep a vertical change together when its schema, implementation, tests, and docs must agree. Run dependent tasks sequentially. The constraint on running two at once is **editing**, not concurrency: two runs that edit need separate worktrees, but two read-only runs share one tree happily. A leads-investigation and a fresh subsystem audit ran side by side in the same checkout, both exited 0 and left the tree untouched. So parallelise investigation freely, and reserve the worktree ceremony for runs that write.

A single coherent run beats several context-starved calls. Do not split merely because the user said "split the task."

Do split when a run has been **killed for running too long**, or when a subscription quota interrupts it before a validated outcome. That is an operational constraint, not a preference. Split along outcomes that stand alone, tell each run which half is not its job, and name the files the other half owns so the boundary cannot blur.

The cleanest split of all is **peeling a refactor off the feature that needs it**. Send the reshaping as its own run with the acceptance bar "every existing test passes with no edits to any test file". That is a mechanical pass condition that needs no judgment from you at review time, and it hands the next run a validated seam instead of asking one run to refactor and build at once. Review a pure move by diffing the moved block against `git show HEAD:<file>` to confirm it is byte-identical.

Splitting for **breadth** rather than for a kill is the other good reason, and it has a price: every run cold-starts and re-reads the repository, so three runs over one feature pay for three explorations. Buy that only when the surface is genuinely wide (a backend layer, then the UI on top of it, then polish), and make it pay by running them **sequentially in one worktree, committing between each**. The commit does the work: it keeps each diff reviewable on its own, lets a bad run be discarded with `git reset` without taking the good ones with it, and hands the next run a tree whose earlier half is already validated.

Weigh that against what 1.3 does by itself: it fans a broad task out to subagents rather than walking the repository serially, so a genuinely wide read can come back complete in minutes. One whole-repo audit ran 45 subagents under a single `muse exec`. Send the wide run first and split only when it comes back thin. When it does, its own **gap list** is the queue for run two: ask every broad prompt to close by naming what it did not reach, then aim the next run at the most valuable name on that list. A repo-wide audit that returned one real defect and declined to pad closed by naming booking-concurrency as unread; the targeted run into that gap produced the fix worth shipping.

## Select the model and effort

Use **`muse-wonder-1.0`** at **`medium`** reasoning effort unless the user specifies otherwise. Do not switch models or effort to work around an account limit without their agreement.

Pass both settings explicitly. Muse Code 1.4.7 still defaults effort to `high`; an omitted flag does not mean medium. Its accepted tiers are `none|minimal|low|medium|high|xhigh|max|ultra`.

Use the exact model id. The old blanket advice to append `-contributor` applied to Spark and must not be carried over to a new model. This CLI exposes `--contributor-mode on|off` separately; preserve the user's configured mode rather than inferring a suffix or a price. `muse model-profile show muse-wonder-1.0 --effort medium` inspects the local profile, but does not prove account access. Smoke-test a newly selected id with the intended effort and `Reply with exactly: OK` before a long run. Read `muse exec --help` if an installed version differs.

A successful smoke test proves that the request can run, not that the subscription has enough quota for the feature. In one session on the user's reported $5 plan, two successive five-hour usage windows ended with quota errors: the first left backend files, the second added UI and translations, and neither reached tests or a final report. Treat that as an observed limit of that account and workload, not a universal plan allowance or a model-quality benchmark. Inspect the remaining diff and narrow the next run to a validated outcome instead of replaying the entire broad handoff after each reset. Ask before changing the user's chosen agent; if they authorize a direct finish, stop retrying Muse and complete the work yourself.

Judge **breadth** separately from difficulty. A wide task invites any model to scope itself down silently: you get correct work covering less ground, not wrong work. On broad surfaces, narrow the run rather than hoping.

## Establish the workspace

Before invoking:

1. Resolve the exact repository or worktree path.
2. Read the repo's instructions and release/deployment policy.
3. Snapshot `git status --short --branch`; record pre-existing edits and untracked files. Snapshot the **gates** too. "Make every check green" invites a run to green one that was already red before it arrived, and it will tell you so while doing it: a locale task ended with an unrelated Deptrac violation silenced by a fresh `skip_violations` line, correctly reported as pre-existing and fixed anyway, because green was the bar I had set. Run the checks yourself first, then name the failing ones in the prompt and say that a pre-existing failure is out of scope, to be reported rather than fixed.
4. Define one bounded outcome, its acceptance criteria, and who owns commit and push.
5. Identify destructive, external, privileged, or deploy-triggering actions that stay outside Muse's authority.
   When you point Muse at neighbouring callers only to learn validation or conventions, mark
   those files read-only unless changing them is part of the outcome. A group-admin handoff
   cited two controllers as validation references and unintentionally invited Muse to move
   their rules into a service; one explicit boundary would have avoided the correction run.
6. If the change adds to an **enumerable set** (routes, nav entries, status values, error codes, tool lists), find every assertion that counts or lists that set *before* writing the prompt, and name those files in it as authorized to update. `grep -rn "toHaveLength([0-9]" <test dirs>` plus a grep for the current count both as a numeral and spelled out in prose finds most of them. Miss one and the run ends with a handful of failures it correctly refuses to touch, costing a round trip.

   Registries that live in **config** are the same trap in different clothes, and they cost more, because they fail at the lint or architecture step rather than the test step, once the implementation is already written: an architecture linter's per-class exception list, a DI manifest, a codegen allow-list. The tell is that every existing sibling of the file you are about to add already appears in some config file.

   Grep for a registry's **values**, not just its symbol. One permissions registry was traced to every consumer by name and the run still came back with a red test, because that test asserted the nine literal strings in an API response and never mentioned the registry's class at all. A symbol search cannot find a hardcoded copy.
7. Separate external actions that must stay outside Muse's authority (deploys, pushes, publishing) from ones the **repo's own documented workflow requires**, such as a codegen or translation script that calls a paid API. Muse stops and asks before the second kind. That is correct of it and still a wasted round trip, so either state in the prompt that the step is the repo's documented workflow and is authorized, or run it yourself afterwards.

### Workspace trust is the failure mode unique to Muse

Muse loads a repository's `AGENTS.md`, project skills, and hooks **only if the workspace is trusted**. An untrusted run still succeeds, still edits files, and still reports confidently. It simply never saw your project rules.

Trust comes from `~/.config/muse/trust.json`, or per-run from `--trust-workspace`, or implicitly from `--yolo`. Neither flag writes to `trust.json`. Help calls both "this run", so a workspace you trusted with a flag yesterday is untrusted again today unless the config file says otherwise.

Muse does warn, on stderr:

```
muse: warning: rules file at <path>/AGENTS.md exists, but the workspace is untrusted,
so it is skipped for this session; restart with --trust-workspace to load project rules
```

Muse's stderr is small, a couple of hundred bytes on a routine run, so read it every time rather than tailing it. A run whose stderr lacks a `workspace trust: trusted` line did not have your project instructions. That line names its origin, `source=user-config` for a standing entry in `trust.json` and `source=run-flag` for `--trust-workspace`. But the flag wins the label, so it reports how trust was granted this time rather than whether the config would have granted it anyway. Expect a second warning in any repository carrying both `CLAUDE.md` and `AGENTS.md`: Muse loads `AGENTS.md` and ignores `CLAUDE.md` in that directory. Harmless where `CLAUDE.md` only points at `AGENTS.md`, a silent gap where the two have drifted apart.

### Foreign personal context

Muse also loads the **user's Claude configuration** (`~/.claude/CLAUDE.md` and the Claude skill catalog) as "foreign personal context". `--help` says only "foreign personal rules and skills", so the specific files are behaviour observed on 1.0.2 rather than a documented contract. This is usually what you want, and it means personal preferences carry across without pasting them. It also means Muse may cite Claude skills that it cannot actually run. Pass `--no-foreign-personal-context` when you need a run isolated from that, such as reproducibility testing.

Do not paste `AGENTS.md`, user config, or skills into the prompt. Fix trust instead.

A clean worktree is worth creating before you start, because it makes "every change in the diff is Muse's" true, which is what lets you review by diff alone. If the scope overlaps dirty files, say so in the prompt or isolate the work. Muse has worktrees built in: `-w create` with `--worktree-base <ref>`, or `-w existing --worktree-existing <path>`.

## Write the handoff prompt

Give Muse the intent and everything that affects correctness. Then get out of the way on implementation detail: it should inspect the repo and match local patterns.

**Separate three kinds of input explicitly**, because they carry different authority:

- **Verified external facts**: a spec revision, a changed API, a fetched doc. Muse cannot derive these from the repo and **its training data may contradict them**. Label them authoritative and say *"do not correct these from memory."* Without that line, a model will quietly "fix" a correct new field name back to the one it remembers. Keep the words *"from memory"*, and resist shortening it to a flat "do not correct these": the narrow phrasing is what lets a run override you when it has *evidence*, which you will need, because some of your authoritative facts will be wrong. One prompt asserted a table name taken from a migration filename; Muse read the model, found the name belonged to a different model entirely, used the right one, and said so in its report. That is the behavior you are buying.
- **Settled user decisions**: say "do not revisit these."
- **Your design sketch**: label it as *shape suggestions*, subordinate to what the repo does.

**Pass conclusions and coordinates, not transcripts.** If you explored the repository before delegating, do not paste the survey in. Muse re-reads the repo anyway and is good at it, so a pasted survey is paid for twice and is liable to be stale by the time it is read. Carry across only what Muse would have to be lucky to find: the exact `path/file.php:line` where the defect lives, the name of the helper that already solves the adjacent problem, the invariant that is true but written down nowhere. One line of coordinates beats a page of survey.

Gather those coordinates carefully, because a wrong one arrives labelled authoritative and costs a detour. `sed -n '20,50p;85,100p'` prints two disjoint ranges with no separator and reads as one continuous block. A test's name from the first range landing above a different test's body from the second was enough to put a false claim in a prompt. Print one range at a time, or label them.

Template, omitting empty sections:

```markdown
You are the implementing agent for one bounded repository task.

Goal: <The finished behavior or artifact, not activities. Include the acceptance bar.>

Context: <Requirements, issue details, observed errors, evidence.>

Verified external facts, AUTHORITATIVE, do not correct from memory: <Spec/API facts checked this session, with exact names and values.>

Decisions already made, do not revisit: <Settled choices, so they are not relitigated.>

Design (shape suggestions; follow the repository where it differs): <Layering, key signatures, sketches.>

Scope and constraints:
- Work only in the current repository/worktree.
- Read and follow all applicable AGENTS.md and repository instructions.
- Inspect the existing implementation and follow established local patterns.
- Preserve pre-existing user changes: <paths, or "the worktree is clean">.
- Do not modify <out-of-scope areas>; report the need instead.
- Do not commit, push, deploy, publish, or perform external writes.
- Resolve ordinary implementation details autonomously from repository evidence. You are
  pre-authorized to make the judgment calls this task needs. Do not stop to ask me to choose
  between reasonable options; pick one, implement it, and say in your report what you picked
  and why.
- If a material ambiguity would change public behavior, data safety, or scope, stop and explain
  rather than guessing. Stop only on a genuine contradiction between two things stated above.

Tripwires, existing invariants that must not break:
- Do NOT edit existing tests to make them pass. A failing existing assertion means the implementation is wrong.
- <Named fragile contracts: exact strings, counts, serialized shapes, orderings.>

Acceptance criteria:
- <Observable criterion 1>

Validation:
- Run <specific commands>. Report each command, its result, and anything not run.
- Add permanent tests for this work as real files under <test dir>. Separately: do not leave
  behind throwaway probes you wrote only to answer a question for yourself.

Return a concise summary of the implementation, files changed, validation results, and remaining risks or questions. If you run out of room, stop and say plainly what you did not build. A truthful partial report is more useful than a tidy one.
```

That last sentence earns its place: it converts a silent shortfall into a review item.

So does the pre-authorization pair in the constraints, and more so on 1.3, which is tuned to confirm consequential actions before taking them. Across five implementation runs carrying that wording verbatim none stalled on a question, and the escape hatch was used as intended: one run chose a read-scoped gate over a literal copy of a sibling's write gate, explained that copying would have put `idempotent` on a GET, and offered to switch. The judgment call gets made and surfaced, rather than halting the run or happening silently.

Naming the tripwires is the highest-leverage part of the prompt. "Do not edit existing tests to make them pass" plus a list of the exact fragile contracts prevents the failure mode where the suite goes green because the assertions moved.

That rule needs a carve-out, or it backfires. When your change legitimately alters an existing expectation, such as a new route added to an asserted list or a count going from 47 to 63, say so explicitly and say where: *extending an expected list, or updating a count, to describe deliberate new behavior is correct; deleting a case or relaxing `toEqual` into `toContain` is not.* Left implicit, you get either a red suite it refuses to touch or a quietly weakened assertion.

**Read your own constraints for self-contradiction before sending.** The expensive failure is not a vague prompt, it is a prompt that forbids the only way to do what it demands. Before sending, check each "do not" against each "must".

For anything the framework assembles rather than the file states, like routes and their middleware, resolved DI, or effective config, derive the fact from the framework's own introspection instead of reading the source. Re-deriving a route table with `php artisan route:list --json` demolished two claims of the *every sibling does X* kind that had come from reading the routes file. But check the shape of what introspection hands back before you trust it: the first pass reported all 90 public routes as unthrottled and ungated, because the JSON prints fully qualified middleware class names and the filter was matching route-file aliases. **Suspiciously uniform results mean your matcher is matching nothing**, and a plausible, wholly wrong answer is the expensive failure here, because it goes into the prompt as an authoritative fact.

Ask for diagnosis only when diagnosis was requested; ask for implementation and validation when a change was requested. State each constraint once. Do not add "think step by step" or generic coding advice.

## Invoke Muse

```bash
muse exec \
  --yolo \
  --model muse-wonder-1.0 \
  --reasoning-effort medium \
  --session-id "$SID" \
  --prompt-file /unique/path/prompt.md \
  > /unique/path/result.md 2> /unique/path/err.log
```

Run it from the repository directory. `muse exec` has no `-C` flag: set the working directory with your shell, or root policy-gated workspace tools elsewhere with `--workspace <path>`.

Put that `cd` in the **same command** as the invocation. Your shell's working directory persists between tool calls, so a `cd backend/` from an earlier command silently becomes the next run's workspace root. The workspace root is what policy-gated tools are scoped to. Stderr's first line, `muse: workspace root: <path>`, tells you which root it actually picked; read it rather than assuming.

**There is no `-o` flag. Stdout is the result.** Redirect it or lose it.

`--yolo` disables approval prompts and the shell sandbox and trusts the workspace for that run. It is the right flag for unattended implementation in a repository the user already works in. For pure inspection, drop it and pass `--trust-workspace --disable-approval --disable-write`: project rules still load, approval stops defaulting to `on-request` with nobody there to answer it, and the last one turns read-only from a request into a partial control: it blocks Muse's file-editing tools, though shell commands can still write. **Telling a run not to modify anything is not enforcement.** Three repo-wide audits were held read-only by prompt wording alone and all three behaved. But that was trust, not a control, and one confused run would have edited the tree. `--disable-write` blocks non-shell workspace writes; its harsher sibling `--disable-shell` blocks workspace shell execution too, which is usually too much for an investigation that needs `grep` and `git log`. Word the prompt's ban the same way. "Do not run the tests" reads as "do not execute anything", and a good run obeys: an audit of `Accept-Language` parsing returned its whole header-to-locale table marked as inference, because it read the parser instead of running it. Half a minute of `php -r` afterwards turned that table into fact and confirmed a bug the reading had only suspected. Name the slow suite you want skipped, and say the run may evaluate pure logic in a scratch REPL. (`--user-input-auto-resolve` is the related escape hatch, for a run that may try to ask you a question.)

Generate `SID` yourself with `uuidgen` before the run. Muse accepts any UUID for `--session-id` and reuses that session on a later `muse exec` with the same id, so you can plan a correction round trip without parsing a session id out of the output. `muse resume` is the interactive TUI path and is not for headless use.

Write the prompt to a uniquely named file and pass `--prompt-file`. For work that may span a quota reset or reboot, keep prompts, the session UUID, results and stderr in a private persistent cache directory rather than `/tmp`; a reboot cleared those temporary artifacts in the quota-interrupted session above while the source edits survived. Never interpolate user-controlled text into the shell.

Other flags worth knowing:

- `-w create --worktree-base HEAD` for an isolated worktree; `-w existing --worktree-existing <path>` to reuse one.
- `--json` emits a durable JSONL event stream. Events are discriminated by `payload_type`; the session UUID is `stream.id` where `stream.kind` is `session`, and assistant text arrives as `run.output.delta`. Only worth it when a program consumes the events, because it is far noisier than the plain-text result.
- `--approval-mode untrusted|on-request|never` and `--disable-approval` control approval independently of the sandbox, which is what lets you keep the sandbox on for an audit.
- The rest of the safety group is easy to miss because `--help` prints it in a trailing section, below the long alphabetical block: `--disable-sandbox` (shell filesystem/network), `--sandbox-network <MODE>` (default `proxy-only`), `--disable-write`, `--disable-shell`, `--enable-shell-tool`. Read `muse exec --help` to the **end**. Piping it through `head` cuts the safety flags off, and their absence is not obvious from what remains.
- `--no-session-log` suppresses the on-disk transcript. Leave it off, because that transcript is the audit trail you will want at review time.
- `--max-model-steps <N>` caps runaway loops.
- `--disable-web-tools` for an offline-only run.
- `--image <path>` attaches a screenshot, repeatable.

## Run it and confirm it actually ran

Long runs exceed foreground tool timeouts. Prefer background execution with the exit status written where nothing can overwrite it:

```bash
{ muse exec ... > result.md 2> err.log; echo $? > exit.code; }
```

**Never append `; echo "EXIT=$?"` or any trailing command to the invocation.** The trailing command's own success becomes the command's exit status, so a failed run is reported to your harness as exit 0.

That applies to the wrapper above as well, and it is the reason for the wrapper rather than a flaw in it: the braced group also exits with `echo`'s status, so **the status your harness reports for that command is meaningless. Only `exit.code` counts.** Expect the two to disagree and believe the file. One background run in a long session was reported to the harness as exit `-1` while `exit.code` held `0` and the result was complete and correct.

Before reviewing anything, confirm all three:

1. `exit.code` is `0`;
2. `result.md` exists and is non-empty;
3. `git status` differs from your snapshot (or the task was genuinely read-only).

Muse fails loudly, which is a real advantage over agents that exit silently: a bad model id, an auth problem, or a tool error produces exit 1, empty stdout, and one clear line on stderr. Read `err.log` in full; it is small. Check it for the untrusted-workspace warning even on a successful run.

**A killed run is a different case, and re-running it blindly wastes the work.** When your harness stops a long background run, no exit-code file is written at all: absent, not nonzero. Inspect before deciding. Check `git status` against your snapshot, `wc -l` the new files for truncation, and the tail of stderr. A clean worktree means it was still reading and nothing is lost; re-run, ideally narrower. A worktree full of complete files means it was killed while emitting its summary and the work may be finished, so validate what is on disk before throwing it away. The same audit applies to a subscription-quota error or `model stream idle timeout after 180000ms`: either can exit 1 with empty stdout after writing substantial but unvalidated code. Read the quota reset timestamp from stderr and convert it to the user's timezone; do not retry before it. A desktop reminder only notifies the user, it does not resume Muse or the orchestrator. This audit also applies to a reboot that clears the prompt, result, and exit files while Muse's server-side session survives: inspect the repository first, then continue with the same session id rather than starting over.

**A run that is merely slow may actually be deadlocked, and it will never notice.** Muse waits for long jobs by polling from a shell, and the loop it writes is often self-matching: `pgrep -f "playwright test ..."` matches whole command lines, and that string is sitting in the loop's own arguments, so it finds itself and the condition never goes false. To check whether your own delegated run is stuck this way, look for its polling loop rather than waiting longer:

```bash
ps -eo pid,ppid,etime,args | grep '[w]hile pgrep'
```

Anything there whose parent is the Muse process is a wait that cannot end. **Kill the loop, not the run**: the blocked tool call returns and Muse carries on with its context intact, where killing the run throws away everything it has done. Two habits follow. When a run passes roughly twice its expected time with no new files appearing, check the process tree before assuming it is thinking. And before retrying a slow validation command, check for a live copy of it under Muse, because overlapping suites compete for CPU and turn the retry into its own source of flakes. The same trap catches your own cleanup: `pkill -f killstuck.sh` matches the shell running it, so filter out `$$`.

For concurrent runs: a distinct session id, prompt file, result path, and log per task; a separate worktree per editing process; wait on every process and check every exit status.

A trailing `Shell cwd was reset to <path>` on stderr says nothing about success; ignore it. A long run's result file holding the same summary twice is not cosmetic, though. Read both copies. One report's first summary said a Deptrac violation was pre-existing and left alone, and its second said the violation was fixed with a config line. The second was true. The later summary reflects the later state, so when the two disagree, believe it and go read the diff.

## Review

Muse's summary is a claim, not evidence. Verify independently:

1. Diff `git status` against the pre-run snapshot; note files it touched that you did not scope. Untracked build artifacts (`__pycache__/`, coverage files, a stray log) are evidence it validated rather than scope creep, but never stage them. Muse also writes throwaway test files into the real test directory to prove a property to itself and deletes them before finishing; confirm they are gone, because a killed run leaves them for the next full suite to pick up as real tests. Forbid them up front, but **in the same breath as asking for permanent tests**, or you get the opposite of what you want. Told only "do not leave scratch test files in the repository", one run wrote six good HTTP tests, verified itself with them, deleted every one, and shipped a complete feature with zero coverage. It was obeying the instruction as written. Make "tests exist for this work" its own acceptance criterion, and check the suite total afterwards: a feature that lands without moving the count did not get tested.
2. Read the full diff of the source changes.
3. **Check that existing tests were not weakened**, cheaply: `git diff -U0 <test paths> | grep -E '^-[^-]'`. Deletions should be pure refactors (a signature gaining an optional parameter, an import line), never removed assertions. Expect legitimate hits and know them on sight: a type union widening, a fixture list growing, an expectation replaced with a new value. Read the paired `+` line before judging. A replaced expectation and a deleted one are one character apart in this output and mean opposite things.
4. Re-run the type check, linter, and test suite **yourself**, scoping each command the way you told the run to scope it; a formatter pointed at the whole tree instead of the changed paths returns pre-existing drift you then have to prove innocent. A broader command is not a stricter check, only a noisier one. Compare the test count to before. Treat every exit code the report quotes as provisional: they go **stale**, which is the commonest way a report is wrong. One run truthfully reported its lint check green, kept editing, and handed back a tree that failed the same command with 11 errors in its own new files. Nothing was fabricated and the summary was still false, so tell the run to validate as the **last thing it does, after its final edit**.
5. Check acceptance criteria, edge cases, error handling, security and data implications, and consistency with local patterns.

   When the change narrows a **shared** predicate, grep for every other caller before accepting. Tightening one policy's `update` from a read predicate to creator-only also silently tightened two other endpoints authorizing on the same ability. Those are behaviour changes nobody asked for, behind a one-line diff, invisible to a green suite because nothing covered the paths it closed.
6. Confirm nothing was committed, pushed, deployed, or published. When repository state cannot settle that, as with a branch that moved mid-run or a remote ref that advanced, read the transcript rather than reasoning from timestamps. Unless you passed `--no-session-log`, every run persists to `~/.local/share/muse/sessions/<YYYY>/<MM>/<DD>/<session-id>/`, and `grep -r 'git push' <that dir>` answers it in one command. The same tree shows how the run worked: `grep -oE '"tool_name":"[^"]+"' session.jsonl | sort | uniq -c` gives the tool mix, and a populated `subagent/` directory the fan-out.

Watch for any report that names a *narrower* command than the one you asked for. "focused suites remain green" is a run that never went near the whole-project check. Read a sudden collapse in a report's detail as a warning rather than as efficiency. The shortest reports are reliably the ones concealing a suppression, a skipped check, or a claim they could not support.

**A green suite is Muse grading its own work.** The cases it adds are written against the implementation it just wrote, so they pass by construction. Read them for the input the implementation does *not* handle, like an unsorted array where order reaches the user, an empty collection, the second item, or a row dated in the past. Also read their *comments* against what the assertion underneath actually executes, because a comment claiming coverage costs nothing to write and reads exactly like the real thing.

So delete the feature and watch which cases go red. That is the only check separating a live assertion from a decorative one. Copy the file first and restore from the copy: the reflex, `git checkout <file>`, restores from HEAD. That is the code *without* the fix, so it silently discards the run's work while looking like a clean revert, and the tell is a `git diff --stat` that comes back empty. Expect two shapes in the output: tests asserting the new behaviour go red, tests asserting nothing *else* broke stay green. Both are wanted. When auditing coverage by grep, search for the *behavior*, like an identifier, an error code, or a header name, not for `it(` or `public function test`, because table-driven cases hide from a title-only search.

For lint-driven refactors, name what each original diagnostic site accomplished before accepting its replacement, especially reset, rollback, confirmation, optimistic-update, and time-boundary behavior. A zero-warning run once removed a discard confirmation entirely and the suite stayed green, because that contract had no test.

**Trust the citations; audit the claims built on them.** Factual accuracy on repository reading is high. One audit's fifteen-odd anchors each landed on a line that said what it was claimed to say, so spot-check rather than re-derive, and spend the saved effort on judgment. The stretching happens one level up: in the **comparative** claim those anchors are wired into (*every* sibling does this, the *only* outlier), and in the **severity** attached to them. Both failed in one audit. "Unlike every other public listing route" was false, an adjacent block having lacked the same middleware all along; and a spoofable `X-Forwarded-For` was filed low by borrowing the *adjacent* route's comment calling that header "a brake, not a security control". That was true where it was written, and false of the caller ten lines down keying a brute-force budget on the same helper. Run the grep behind any claim shaped *every* or *only*, and check where a severity judgement's justification came from, not only where its line numbers point.

Cheaper still, put those instructions in the prompt rather than saving them for review. An audit told to enumerate framework-assembled sets with the framework's own introspection closed by reporting, unprompted, where it had and had not earned its comparative claims. A review habit you can describe is usually cheaper as a prompt constraint.

**Before acting on a report, settle what it could not.** Treat a broad audit's implementation queue as hypotheses even when its anchors are accurate: reopen each target immediately before writing its handoff and verify the claimed absence. One audit mapped its domain correctly and still queued two actions that already existed, and the fresh check prevented two duplicate builds. And when a report names its own unverified assumption, settle that before triaging anything underneath it. 1.3 will tell you which hop it could not check, and that sentence is worth more than the findings stacked on it. Three defects ranked as ordinary-use overbooking all rested on whether a database's OCC tracks index ranges or only documents, a question it correctly said the repository cannot answer; one fetch of the vendor's docs evaporated all three. Such assumptions are almost always external, like an isolation level, a proxy's header handling, or a framework's escaping, which is exactly why they are yours to resolve and not the run's.

**When it stops and offers you options, check the repository before picking one.** A halt on a genuine contradiction is the behavior you want, but the options it proposes are the ones it can see, and every one may be a change when the answer is an existing convention. Grep for how the nearest sibling solves the same problem, and reply with that rather than authorizing a change.

To correct, re-run with the **same `--session-id`** and send findings via `--prompt-file`:

```bash
muse exec --yolo --model muse-wonder-1.0 --reasoning-effort medium --session-id "$SID" \
  --prompt-file /unique/path/findings.md > /unique/path/fix.md 2> /unique/path/fix-err.log
```

Keep the intended model and effort explicit on a continuation; preserve the existing worktree rather than creating another one. Do give it its own prompt and result paths: reusing the first run's filenames overwrites the evidence you are correcting from, and you will want the original when the second report disagrees with it.

When the correction is "make the linter pass", **ban the escapes in the same message**: no `eslint-disable`, no `@ts-expect-error`, no `any`, and no semantic disguise that moves the same operation behind an API the rule does not recognize. For example, an identity reducer standing in for a state setter, or a `setTimeout(..., 0)` wrapper. A rule that genuinely should not apply must be argued for in the report rather than silenced. Say too that the tests must keep covering what they covered, or type errors inside a test get "fixed" by deleting the assertion that caused them.

Limit correction loops. If the same material problem survives two focused attempts, stop and reconsider the prompt, the task boundary, or whether to do it yourself.


## Commit and push

Git history stays under orchestrator control:

- Tell Muse not to commit or push.
- Review and validate before staging; stage only files belonging to the bounded task.
- Write a commit message describing the verified outcome.
- Commit only when requested or clearly authorized. "Implement X" is not authorization to commit X.
- Push only on explicit request or when the enclosing workflow requires it. Check first whether the push triggers CI, deployment, or publication.

Prefer atomic commits per stable outcome; one coherent commit for tightly coupled parts of a single feature.

## Report

Lead with the verified outcome, not with the fact that another agent was used. Include what changed, what validation you ran yourself and its result, commit/push state if any, and material caveats or skipped checks.

Mark clearly which claims you verified and which are Muse's. Never report success solely because `muse exec` exited zero.

## Propose improvements to this skill

Every delegation teaches something about delegating. Once the work is reported, say what the session taught and offer it to the user as a concrete edit; they decide whether it lands. Offer it unprompted, including when the session went well. Never edit this file without being asked.

**The bar is whether it would have changed what you did.** A lesson earns its place if it would have saved a round trip, caught a defect earlier, or prevented a wrong turn:

- a surprise that cost a round trip: an assertion you did not know existed, a halt you could have pre-authorized, a flag that behaved unlike its documentation;
- a defect that survived Muse's own green suite, with the review habit that would have caught it;
- a boundary, splitting, or prompt technique that visibly worked or visibly failed;
- an effort choice that was wrong in a way you can diagnose.

**What does not belong here**, because this is the commonest way a skill rots:

- anything true only of the repository you were working in. A schema quirk, a build trap, a naming convention belongs in that repo's own `AGENTS.md`, where the next agent working there will read it. Route by who needs it: "how to delegate" here, "how this codebase behaves" there.
- a single data point confirming advice already given.
- a lesson you did not actually learn. A session where nothing surprised you should produce no edit, and saying so plainly is a better report than a manufactured insight.

**Fold in; do not append.** This file is read start to finish before every delegation, so its length is a cost paid on every run. A new lesson usually belongs inside an existing paragraph, as the sentence that makes it concrete, rather than as a section of its own. Prefer the specific anecdote to the general principle. When a session contradicts advice already here, propose deleting that advice rather than qualifying it into vagueness.

## Avoid recursive delegation

When this skill is loaded inside Muse itself, do not invoke another Muse process unless the user explicitly asks for another layer. Work with the tools already available.
