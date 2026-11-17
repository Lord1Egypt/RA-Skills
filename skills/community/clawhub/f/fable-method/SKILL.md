---
name: fable-method
description: "A 7-step problem-solving discipline loop that gives any model structured thinking: classify the ask, define done, gather evidence, decide, act surgically, verify by observation, report outcome-first. Use when the user says 'fable-method', or proactively when starting any multi-step task that no task-specific skill covers. Subcommands: plan, audit, report."
version: 1.0.0
author: Hermes Agent Community
license: MIT
platforms: [linux, macos, windows]
metadata:
 hermes:
 tags: [reasoning, problem-solving, verification, discipline, quality]
 related_skills: [fable-loop, fable-judge, fable-domain]
---

# fable-method

A discipline loop for any model. The goal isn't to look thorough - it's to be correct. Every step exists because I've watched agents skip it and produce confident garbage. Run the loop. Don't narrate the loop.

## When to use

You face a non-trivial ask: a bug, a failing test, a "why is X slow" question, a refactor, a production mystery. If the answer requires touching code, reading sources, or changing behavior under uncertainty, this is your loop. If the ask is genuinely trivial, see the **Triviality Gate** below and skip the loop entirely.

## The two gates

### Triviality Gate

Before running the loop, ask: is this trivial? A task is trivial when **all** are true:

- One file touched
- Under 10 lines changed
- No new behavior introduced (you're fixing an obvious typo, renaming a local, correcting a literal)
- No searching required (you already see the exact lines)

If all four hold: just do it. Two-sentence report. No loop, no ceremony. The loop exists to prevent errors, not to add overhead to work that can't go wrong.

If **any** of the four is false, run the loop.

### Fit Gate

Route the ask by where the answer lives:

| The answer lives in… | Route |
|---|---|
| Reachable sources (code, logs, docs, live systems) | Run the loop |
| A technique you don't know | Research first (web_search, web_extract), then run the loop |
| Your inference only - no source can confirm | Say so honestly. Don't fabricate evidence. |
| A specialized, recurring workflow | Make a skill. Don't hand-roll it every time. |

Never pretend a source confirmed something it didn't. Never invent a path you didn't read, a log line you didn't fetch, a test result you didn't run. If you can't observe it, you don't know it - say that.

## The 7-step loop

```
Step 0: Classify → What kind of ask is this?
Step 1: Define done → What does "finished" look like, concretely?
Step 2: Gather → What does the evidence say? (primary sources, not memory)
Step 3: Decide → One recommendation. Commit to it.
Step 4: Act → Smallest correct change. No collateral damage.
Step 5: Verify → Did the done criterion actually get observed?
Step 6: Report → Outcome first. Caveats next. No spin.
```

---

### Step 0 - Classify the ask

Before anything else, name the shape of what you're handling. Three shapes:

1. **Question / Assessment** - the user wants an answer or an evaluation, not a change. "Why is the dashboard slow?" "Is this API safe to ship?" Your job is to investigate and report, not to edit.
2. **Task** - the user wants something done. "Fix the failing date test." "Add rate limiting to the upload endpoint." Your job is to act and verify.
3. **Plan-first** - the task is large, risky, or ambiguous enough that acting blind is irresponsible. Produce a plan through Step 3, then stop and hand it back for authorization.

**Tie-break rule:** If you can't tell whether it's a question or a task, default to **question**. Investigating first never causes harm; acting prematurely often does. If you can't tell whether it's a task or plan-first, default to **plan-first**. Cheap insurance.

State the classification in one line. Don't bury it.

---

### Step 1 - Define done

Name the verification **before** you start working. If you can't state what "done" looks like in observable terms, you don't understand the ask well enough to begin.

By shape:

- **Question:** Done = a defensible answer backed by cited evidence, with the limits of that answer stated. "Dashboard is slow because the /summary endpoint does an N+1 query (confirmed in query log line 412). Caveat: I did not profile the frontend."
- **Task:** Done = a concrete, observable change. Name the specific test, command, or state that proves it. "The date test `test_parses_iso_week` passes and the full suite is green." Not "the test works" - name the exact command and the exact pass signal.
- **Plan-first:** Done = a written plan the user can authorize or reject, covering scope, steps, risks, and the done criterion for the eventual task.

Write the done criterion down. You'll check it against reality in Step 5. If you skip this, Step 5 becomes a vibe check, and vibe checks are how bugs ship.

---

### Step 2 - Gather evidence

**Orient first.** Before you search, read, or fetch anything, spend one breath understanding the terrain: what files exist, what the system looks like, where the answer is likely to live. A minute of orientation saves twenty minutes of flailing.

**Primary sources beat memory.** Always. Your training data is stale, your memory of a past session is unreliable, and "I think the config is in…" is not evidence. Read the file. Fetch the log. Run the command. Cite what you actually saw.

**Parallelize independent lookups.** If you need to read three files that don't depend on each other, read them in the same turn. If you need to search the codebase and fetch a doc page, do both at once. Sequential lookups where the later one doesn't depend on the earlier one waste your turns and the user's time.

**Read narrow.** Don't dump a 2000-line file into context when you need 40 lines around a specific function. Use `search_files` to find the location, then `read_file` with offset/limit to pull just what you need. Context budget is finite; spending it on noise degrades every downstream decision.

**Time-box mechanically.** Set a wall-clock bound on evidence gathering. If you're still searching after the bound, stop, report what you have, and ask the user. Don't let "one more search" become thirty minutes of silent thrashing. Use a hard count: "I will make at most N searches. If I haven't found it by then, I report and ask."

**Establish intent before changing behavior.** Before you modify anything, confirm you understand what the code is *trying* to do, not just what it currently does. A bug fix that breaks the intended behavior is a regression, not a fix. Read the surrounding context, check the tests, look at the callers.

**Surprises re-route the loop.** If the evidence contradicts your mental model - the bug isn't where you thought, the test isn't testing what you assumed, the config is different from what you expected - **go back to Step 0 or Step 1.** Do not press forward with a plan built on a wrong model. The most expensive failures come from agents who noticed a surprise and ignored it because they were already committed to a path.

---

### Step 3 - Decide and commit

**One recommendation.** Not three options with a passive "what do you think?" at the end. You did the investigation. Commit to a recommendation. If you genuinely can't decide between two equally-good options, pick one, state the tradeoff, and proceed - the user can redirect.

**Authorization gate.** Before Step 4, check: is this action irreversible or outward-facing? Irreversible = deleting data, dropping a table, removing a file the user didn't tell you to remove, changing a public API. Outward-facing = anything a user, customer, or external system will see or receive. If either is true, emit an `AUTH:` line and stop:

```
AUTH: This change modifies the public API surface. Proceed? (yes/no)
```

Wait for explicit confirmation. "Silence is not consent" - if the user hasn't said yes, you don't act.

**Name the scope.** State exactly what you will and won't touch. "I will modify `src/dates.ts` lines 45-60 and add one test case in `dates.test.ts`. I will not touch the formatting module or the timezone logic." Scope discipline prevents drift. If you find yourself wanting to touch something outside the named scope mid-Step-4, go back to Step 3.

---

### Step 4 - Act surgically

**Intent gate.** Before each edit, emit a one-line `INTENT:` statement stating what this specific change is for:

```
INTENT: Fix off-by-one in week parsing so ISO week 53 is accepted.
```

If you can't write a clear intent line, you don't understand the change well enough to make it. Stop and go back to Step 2.

**Recall gate.** Before editing, re-read the exact lines you're about to change. Context drifts. The file may have changed since you last read it. The line numbers may have shifted. A 2-second re-read prevents a 20-minute debugging session on a patch applied to the wrong location.

**Smallest correct change.** The goal is not "a change that works." The goal is the smallest change that is correct. Every extra line is a line that can break, a line that needs review, a line that drifts from intent. If you're rewriting a function when moving one line fixes the bug, you're wrong.

**Precise edits.** Use `patch` with enough surrounding context to uniquely identify the target. Don't rewrite whole files with `write_file` when a 3-line patch suffices. Precise edits are reviewable; whole-file rewrites are not.

**Track multi-part work with `todo`.** If Step 4 involves more than two distinct edits, or has a dependency chain (edit A, then test, then edit B), use the `todo` tool to track the parts. Mark each done as you complete it. This isn't ceremony - it prevents the "I forgot to run the tests" failure.

**Never destroy without looking.** Before deleting code, a file, or a test, confirm: (a) it's within your named scope from Step 3, (b) nothing else depends on it, (c) the user authorized it. `search_files` for references first. Deletion is the most common irreversible mistake.

**Failed-edit recovery ladder.** When a `patch` or `write_file` fails:

1. **Re-read the target.** The content may have changed. Read the current state of the file at the target location.
2. **Check for ambiguity.** Was your `old_string` not unique? Did the file have slightly different whitespace or indentation? Widen the context window in your `old_string`.
3. **Fall back to `read_file` + `write_file`** only if the targeted patch genuinely can't match after two attempts. This is a last resort - whole-file writes lose precision.
4. **If the file doesn't exist or the path is wrong**, stop and verify the path. Don't create a file at a guessed location.

Don't retry the same failing edit three times. If it didn't work twice, the model is wrong, not unlucky. Re-read and adjust.

**Standing prohibitions.** These apply unconditionally, in every Step 4, with no exceptions:

- **Never commit or push.** You don't have authorization to put changes into the repo history. That's the user's call.
- **Never weaken checks.** Don't delete a test to make the suite pass. Don't broaden an assertion to hide a failure. Don't skip a linter rule because it's noisy.
- **Never touch secrets.** No `.env`, no credentials files, no API keys, no tokens. If you see one, note it and move on. Don't read it into your output.
- **Never add dependencies.** No `pip install`, no new `package.json` entries, no new imports of third-party libraries the project doesn't already use. If the fix requires a new dependency, go back to Step 3 and get authorization.
- **Never delete outside scope.** If it's not in the scope you named in Step 3, you don't touch it. Period.

---

### Step 5 - Verify by observation

**Done criterion observed.** Go back to the done criterion you wrote in Step 1. Did you actually observe it? Not "I'm confident it would pass" - did you run the test? Did you see the green output? Did you fetch the response and see the correct value? Observation, not inference. If you predicted "test X passes" and you didn't run test X, you have not verified.

**Surrounding system healthy.** The fix isn't done if it broke something else. Run the broader suite. Check the callers of what you changed. If you modified a function, confirm its other callers still work. A fix that breaks a neighbor is a regression, not a fix.

**Twin check.** Did your change have an intended twin - a parallel path that should get the same fix, a test that should also be added, a doc that should also be updated? Emit a `TWINS:` line:

```
TWINS: Fixed week parsing in parseISOWeek. The same off-by-one exists in parseISOWeekDate - needs the same fix.
```

If the twin is in scope, fix it. If it's out of scope, note it in the report.

**3-cycle hard bound.** If you're in a verify → fix → verify loop, you get at most 3 cycles. If after 3 cycles the done criterion still isn't observed, stop. Don't enter an infinite retry loop. Report what you tried, what the current state is, and hand the problem back to the user with a clear description of where you're stuck. "I attempted 3 fix cycles. The test still fails because [reason]. The relevant log is [attached]. I need human input on [specific question]."

---

### Step 6 - Report outcome-first

**First sentence answers what happened.** Not what you did, not what you tried - what happened. The reader's first question is always "did it work?" Answer that in sentence one.

- ✅ "The failing date test now passes; the full suite is green."
- ✅ "The dashboard is slow because the /summary endpoint runs an N+1 query, confirmed in the query log."
- ❌ "I investigated the issue and made changes to the date parsing module." (What happened? Did it work?)

**Match the reader, not the work.** The user asked a question; answer it. Don't recap your entire investigation process unless they asked for it. The amount of detail in the report should match what the reader needs, not how much effort you expended. A 2-hour investigation that produced "the config had a typo" gets a 2-sentence report.

**Caveats present.** State what you did *not* verify, what you're *not* sure of, and what could still be wrong. "I fixed the parsing but did not check the timezone-adjacent tests. The fix assumes the input is always ISO format; non-ISO input is untested." Caveats are not weakness - they're honesty. Omitting them is dishonesty.

**PENDING line.** If there are prescribed follow-ups you did not take - a twin you noticed but couldn't fix, a test you couldn't run, a doc that needs updating - emit a `PENDING:` line:

```
PENDING: parseISOWeekDate has the same off-by-one (not in scope). PENDING: no integration test for the new path (unit test only).
```

**Cleanup debris.** Remove temporary files, scratch scripts, debug prints, and any artifacts you created during investigation. Don't leave `debug.log`, `test_output.txt`, or `scratch.py` lying around. The workspace should look like you were never there, except for the intended change.

**Artifact gate sweep.** Before finishing, scan your output for any owed lines you promised but didn't deliver: an `AUTH:` you left unanswered, a `TWINS:` you noted but didn't resolve, a `PENDING:` you forgot to carry into the final report. Every marker you introduced must either be resolved or explicitly carried forward. Unresolved `AUTH:` = you acted without authorization, which is a failure. Unresolved `TWINS:` in scope = incomplete work. Sweep them all.

---

## Three modes

The loop runs in one of three modes, depending on what's needed:

### Plan mode

Run Steps 0-3 only. Produce a plan: classification, done criterion, evidence summary, recommendation, named scope, and any `AUTH:` flags. Then **stop.** Do not proceed to Step 4. Hand the plan back for the user to authorize, reject, or redirect.

Use plan mode when the task is large, irreversible, ambiguous, or when the user explicitly asked for a plan before action.

### Audit mode

Grade existing work against the loop. Someone (you, another agent, a human) already did the work. Now evaluate it:

- Did they classify correctly? (Step 0)
- Was the done criterion stated and observed? (Steps 1, 5)
- Did they gather primary-source evidence, or did they reason from memory? (Step 2)
- Did they commit to one recommendation or hedge? (Step 3)
- Were edits surgical and within scope? (Step 4)
- Did they verify by observation, not inference? (Step 5)
- Does the report lead with outcome? Are caveats present? (Step 6)

Output a grade per step: **PASS**, **FAIL**, or **MISSING**. For any FAIL or MISSING, state what should have happened. Don't soften the grade - "mostly fine" is not a grade.

### Report mode

Rewrite an existing answer per Step 6's standards. The investigation is done; the answer exists but doesn't meet the reporting bar. Restructure: outcome-first first sentence, caveats, PENDING lines. Trim process narration the reader didn't ask for. Match the reader, not the work.

Use report mode when the substance is right but the communication is wrong.

---

## Compressed examples

### Example A: Task - fix failing date test

```
[Step 0] TASK. User wants the failing test fixed, not a diagnosis.
[Step 1] DONE = `pytest tests/test_dates.py::test_parses_iso_week -x` exits 0.
[Step 2] search_files for "iso_week" in tests/ → test at line 34.
 read_file tests/test_dates.py offset=30 limit=20.
 Test passes "2024-W53" to parseISOWeek, expects week=53.
 search_files for "parseISOWeek" in src/ → src/dates.ts line 88.
 read_file src/dates.ts offset=84 limit=15.
 Bug: `if (week < 53) week` - rejects week 53. Off-by-one.
[Step 3] Recommendation: change `< 53` to `<= 53` in src/dates.ts line 90.
 Scope: src/dates.ts line 90 only. Reversible, not outward-facing. No AUTH needed.
[Step 4] INTENT: Accept ISO week 53 in parseISOWeek.
 Recall gate: re-read line 90. Confirmed `< 53` present.
 patch src/dates.ts: `< 53` → `<= 53`.
 Edit applied.
[Step 5] Run: pytest tests/test_dates.py::test_parses_iso_week -x → PASSED.
 Run full suite: pytest tests/ -x → 42 passed, 0 failed.
 TWINS: parseISOWeekDate in src/dates.ts line 112 has the same `< 53` check.
 Out of scope - noting for report.
[Step 6] Report:
 The failing date test passes; full suite is green (42/42).
 Fixed an off-by-one in parseISOWeek (src/dates.ts:90): `< 53` → `<= 53`.
 PENDING: parseISOWeekDate (src/dates.ts:112) has the same bug - not in scope, needs the same fix.
```

### Example B: Question - why is the dashboard slow?

```
[Step 0] QUESTION. User wants an answer, not a change.
[Step 1] DONE = a defensible root cause cited from primary evidence, with limits stated.
[Step 2] search_files for "dashboard" in src/ → src/api/dashboard.ts, src/components/Dashboard.tsx.
 read_file src/api/dashboard.ts. The /summary endpoint loops over users
 and calls fetchUserSummary(id) per user. N+1 query pattern.
 terminal: grep for fetchUserSummary in logs → 47 calls per dashboard load.
 Evidence: N+1 confirmed in code (line 62) and in log (47 calls/request).
[Step 3] Recommendation: the dashboard is slow because /summary does an N+1 fetch.
 No action to take (question mode). Report the finding.
[Step 6] Report:
 The dashboard is slow because the /summary endpoint runs an N+1 query:
 it loops over each user and calls fetchUserSummary individually (47 calls
 per page load, confirmed in the query log). The fix is to batch the fetch
 into a single query, but I did not make that change (question, not task).
 Caveat: I analyzed the backend only. I did not profile the frontend render
 or the network waterfall - if the backend fix doesn't resolve the slowness,
 those are the next places to look.
```

---

## Final reminder

The loop is not a format. It's a discipline. Going through the motions without the thinking is worse than not running the loop at all - it produces confidently-structured garbage instead of honestly-uncertain work. If you're going to skip a step, say so and say why. If the evidence surprised you, go back. If you can't verify, say you can't verify. The point is to be correct, not to look thorough.