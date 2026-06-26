# Behavior Discipline — destructive commands / multi-repo tracking / chained fix / anger→TDD switch

This topic bundles the behavior-discipline rules that fire during the fix flow.

## Destructive-command restraint (HARD STOP)

**Never run filesystem/index-destroying commands (`git reset --hard`, `git checkout -- .`, `rm -rf`, etc.) for the purpose of reverting or resetting work without prior coordination and user approval.** When a reset is unavoidable (e.g., undoing a temporary commit), step through a non-destructive alternative (`git reset --soft` / `git reset HEAD~1` followed by per-file `git restore`) and perform it safely.

| # | Don't | Do |
|---|-------|-----|
| 1 | Run `git reset --hard HEAD~1` to destructively drop a temporary local commit | Use `git reset --soft HEAD~1` or `git reset HEAD~1` to release the commit while preserving changes, then apply per-file `git restore` if needed |
| 2 | Unilaterally run `git checkout -- .` or `git restore .` to wipe all working-directory edits at once | Keep open the possibility that changes must be preserved; restore carefully per file, or roll back safely only after user confirmation |

## Multi-repository original-work tracking and context discrimination (HARD STOP)

**When you receive an error report or `/fix` feedback while switching back and forth across multiple projects (repositories), do not get trapped in the narrow view of the currently active directory — replay the whole session history.** Identify which target repository was the "Original Work" (the recent build error, push failure, or edit target) and **cross-verify via the full local repository state** (`git status`, `git log`) before switching to the correct target and handling the work.

| # | Don't | Do |
|---|-------|-----|
| 1 | Get a commit-convention error in repo A but, absorbed in repo B (recently edited), try to fix the wrong commit | Read the feedback, switch the working directory immediately to repo A where the bad commit actually exists, and amend the correct commit |
| 2 | When the subject of the user's feedback is omitted during multi-project work, impulsively assume the current folder is the target and edit it | Quickly tour each workspace running `git status` or `git log -n 5` to determine which project holds the error target |

## Chained-fix dependency declaration and completed-task pruning (HARD STOP)

**On `/fix`, the registered `fix-2 (Resume)` task must declare the preconditions under which the work can run safely — to prevent configuration damage from stale execution** — and during the session `cleanup` step, prune **only completed (`[x]`) tasks**; do not unilaterally delete in-progress or held (stale) incomplete tasks.

| # | Don't | Do |
|---|-------|-----|
| 1 | Register only the bare `Resume` command on the `fix-2` task without preconditions (Depends on) and base commit SHA (Reference commit) | Record preconditions and snapshot, e.g. `- [ ] fix-33: 🔄 Resume original work: ... (Depends on: <environment-normalization condition>, Reference commit: <SHA>)` |
| 2 | During session `cleanup`, freely delete stale incomplete `fix-*` tasks recorded in `task.md` without tracking history | Prune only completed (`[x]`) `fix-*` tasks; keep held or in-progress incomplete tasks intact |

## Immediate TDD auto-switch on user-anger / deception signals (HARD STOP)

**When two signals co-occur — a strong user-anger signal (profanity / hostile language) plus a direct verification-failure claim (e.g. "it's not installed", "it's not applied", "the fallback doesn't work either", "neither X nor Y works", "it still shows the old one") — stop the ad-hoc Edit/rebuild/install attempts immediately** → extract the logic under verification into a pure function → write Red unit tests (3+ scenarios) → confirm fail → Green implement → confirm pass → switch to verifying the new build via a code grep of the installed artifact. Three or more repeated ad-hoc fixes accumulate the same mistake, so TDD is mandatory.

| # | Don't | Do |
|---|-------|-----|
| 1 | Keep repeating ad-hoc Edit + rebuild + install even after an anger signal + verification-failure claim | Switch to TDD immediately: extract the logic to a pure function → Red tests (normal + user-reported scenario + edge case, at least 3) → confirm fail → Green implement → confirm pass → installed-artifact grep |
| 2 | Conclude "success" from the install command's output line alone | Confirm a substring grep match of the new logic inside the installed dir artifact (`~/.vscode/extensions/<id>-<ver>/dist/`, `~/.cursor/extensions/...`). Zero matches = install failed = retry. matches > 0 = verification passed |
| 3 | Think "the user is angry, so quickly try another new fix" | An anger signal = a procedure-defect signal. One more ad-hoc attempt = the same mistake repeated. TDD is faster in the end (unit tests catch regressions immediately) |
| 4 | Reuse the same path prefix in a command after `cd` (e.g. `cd packages/X && code --install-extension packages/X/file.vsix`) | After `cd`, use the filename only (`cd packages/X && code --install-extension file.vsix`) or an absolute path. Just before composing the command, check `pwd` + duplicated path prefix |

### Procedure

1. Detect co-occurrence of an anger/profanity signal + at least one verification-failure-claim keyword
2. Check whether the just-attempted fix was an ad-hoc Edit + the count (3+ = mandatory TDD)
3. Extract the logic under verification into a pure function (existing inline logic → a separate helper file)
4. Write unit tests: normal case + reproduce the user-reported scenario + edge case (e.g. null/undefined input, empty collection)
5. Run tests → confirm Red (report the failure result explicitly)
6. Fix the logic → confirm Green (report all scenarios passing explicitly)
7. Import the helper into the caller (extension.ts, etc.) and apply it
8. build + install → confirm a substring grep match of the artifact code at the installed-artifact path
9. Report verification to the user in the form "Red N failing → Green N passing → installed grep N matches"

### Exceptions

- The user explicitly instructs "no TDD, fix directly" or "do it fast, ad-hoc"
- Logic for which pure-function extraction is impossible (e.g. code with only a UI side effect, direct vscode-API dependency)
- The anger signal stems from a cause other than verification failure (e.g. timeout, policy refusal)
