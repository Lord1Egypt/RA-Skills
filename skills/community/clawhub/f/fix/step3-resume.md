# Step 3: Resume Original Work (fix-2)

**This is the most important step.** The user's original request must be completed — not just the fix itself.

**3-0. Infer user intent (MANDATORY — execute before any mechanical task listing)**:
From the user's /fix message (skill args) and session context, infer **"what outcome does the user want"**:
1. **Re-read /fix args**: identify which words the user emphasized and what they said "must be done"
2. **Cross-reference session context**: what is the current state of that work? Code modified but not verified? Not deployed? Not committed?
3. **Pin down the concrete meaning of "resolve / complete / proceed"**: the same word means different things in different contexts. "Resolve" = code fix? Through verification? Through deployment? — infer from session state
4. **State the inferred result as one sentence**: "What the user wants: {concrete action}". This sentence is the basis for all subsequent task listing
5. **Specify verification medium (HARD STOP — prevent scope reduction)**: copy the medium the user saw (URL, API endpoint, screen path, command output) verbatim. In fix Step 3 verification, **reproduce via that medium directly**. No detoured verification.

| User message | Verification medium (use verbatim in Resume) |
|--------------|----------------------------------------------|
| "/api/system-log?limit=30: HttpError" | `curl <APP_URL>/api/system-log?limit=30` (with cookie) — verify response status/body |
| "500 on the login screen" | Playwright on sign-in screen → submit → verify response |
| "Error when clicking X button on page Y" | Playwright on page Y → click X button → verify result |
| "File upload failure" | Reproduce with the same file + same form data via multipart POST |

Example: `/fix start with Critical` + session shows code modified but not verified → "What the user wants: Playwright verification that the modified code actually works" + verification medium: the screen path the user reported (e.g., `/dashboard/sso-callback`)

**5.5. Identify "missing question to user" (HARD STOP)**:

If the user's fix args contain expressions like "you didn't ask / the ask comes first / you skipped it / you should have asked", the fix's purpose is **to identify the missing question and ask the user directly in Step 3**. Do not autonomously decide the answer.

| User expression | Required action in fix Step 3 |
|-----------------|-------------------------------|
| "you didn't ask X" | Add an ask for X to the user in Step 3 |
| "Y is the ask that comes first" | Make the first action of Step 3 the Y ask |
| "you should have read the prompt, found what was missing, and put it in resume" | Re-read fix.md / the related skill and specify the missing step (usually an ask) in the fix-2 Resume |
| "distinguish in-progress vs waiting" / "you didn't ask about what's waiting" | Two separate asks for "in progress" + "waiting on" (do not merge into one option) |

**Self-check (every time the fix args contain "didn't ask / missing ask" keywords)**:
1. What specific question did the user want asked? — Identify from fix args
2. Is the asked subject "in progress" or "waiting on" or both? — Split into separate asks if both
3. Use free-text (Other) instead of guess options — assumption options force misalignment with user's real state
4. Make the ask the **first action** of Step 3, not the last

6. **Recognize user dismissal signals (HARD STOP — do not re-raise secondary facts)**: items the user has explicitly dismissed must **not be re-raised** in fix Step 1 verification / Step 3 reporting. Focus on the core work only.

**Dismissal trigger keywords**:

| User expression | Interpretation |
|-----------------|----------------|
| "Just force push over there" | That remote/branch state is out of verification scope |
| "Forget about that" / "That's done" | Item handled or irrelevant — do not raise |
| "Don't worry about it" / "Skip" | That fact is irrelevant to the core work |
| "Already did it" / "Handled" | User handled it directly — no re-verification/re-reporting |
| "Why do you keep bringing up X" / "Again with X" | Annoyance at secondary mention of X in the prior response — return to core immediately |

| # | Don't | Do |
|---|-------|-----|
| 1 | Re-report dismissed items under the pretext of "fact verification" | Verification is limited to the core work medium. Even if dismissed items appear in git fetch/grep, exclude them from report text |
| 2 | Statements that "prove the user's guess wrong" | Do not fabricate something the user never said and refute it. Quote only what the user said |
| 3 | After dismissal, re-mention the same fact "for accuracy" once more | One dismissal = permanent silence. Same in all follow-up responses |
| 4 | Continue mentioning X despite annoyance signals ("damn", "why X again", "wtf") | Annoyance signal = ↑ ask priority + immediate return to core. Zero mention of dismissed items from the next response |

**Self-check (every time before writing a response)**:
1. Did the user dismiss any item in the prior N messages?
2. If so, does that item appear in this response's text?
3. If it appears, is it directly tied to the core work? — remove if not essential to the core work

**3-0.5. Re-call rejected AskUserQuestion (HARD STOP)**:

If the turn immediately before fix had **AskUserQuestion rejected + /fix triggered** as the flow, then after fix Resume removes the reject cause, **re-calling ask with improved options** is part of Step 3's deliverable. Do not autonomously decide "end without re-call".

## Reject cause classification

| Reject reason | Can fix resolve it? | Resume handling |
|---------------|---------------------|-----------------|
| ask **secondary issue** (visual noise, stale context, inaccurate option description) | ✅ Yes | Remove cause in fix Step 2/3 → **re-call ask with improved options** |
| ask **intent rejection** (user denies the very intent to proceed) | ❌ No | No re-call. End with fix completion report |
| ask **option mismatch** (the options themselves are wrong) | ✅ Yes | Restructure options → re-call ask |
| ask **timing mismatch** (preconditions unmet) | ✅ Yes | Satisfy preconditions → re-call ask |

## Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | AskUserQuestion rejected → fix done → autonomously decide "end without re-call" | If fix resolved the reject cause, **re-call with improved options**. Reject ≠ permanent end |
| 2 | Default-interpret the reject reason as "user rejects the very intent" | Determine the reject reason from the user's immediate message (/fix args, annoyance signals). Distinguish intent rejection vs secondary issue |
| 3 | "We already asked once; let the user decide on their own" | A secondary issue that fix resolved leaves the user able to decide via ask. ask = decision trigger |
| 4 | Re-call by copy-pasting the rejected options verbatim | Reflect the reject cause in description (e.g., note "Summary cleaned up" → attestation the user can verify) |
| 5 | Avoid ask out of "re-call = nagging" thinking | Reporting reject-cause resolution + re-calling ask is not nagging. It restores user decision authority |

## Self-check (every time before entering fix Step 3)

1. Was there an **AskUserQuestion call in the turn right before this fix trigger**? → If no, skip this procedure
2. Was that AskUserQuestion **rejected**? (`The user doesn't want to proceed with this tool use`) → If no, skip
3. Determine reject reason from immediate user /fix args + annoyance signals → classify as intent rejection vs secondary issue
4. If it was a secondary issue and fix resolved it → include an **ask re-call** in fix Step 3 (part of the deliverable)
5. In the re-call's option descriptions, **state the fact fix resolved** as attestation (e.g., "Summary cleanup complete (only 1 active)")

## Reject reason default = secondary issue (HARD STOP)

When the reject reason is ambiguous, **default to "secondary issue" (re-call required)**. "Intent rejection" must be evidenced by user message — without evidence, treat as secondary.

| Evidence | Classification |
|----------|----------------|
| User followed reject with `/fix args` pointing at option/info problem (e.g., "the options are insufficient", "primary source not gathered", "you assumed", "why didn't you use it") | **Secondary issue** — fix-resolve cause → re-call ask |
| User explicitly said "cancel", "stop", "I won't" before or after reject | Intent rejection — no re-call |
| User provided primary-source data themselves (e.g., ran `/doctor` and shared output) after reject | **Secondary issue** — they wanted primary source first; ask now valid → re-call mandatory |
| No further user message after reject (silence) | Ambiguous → **default secondary** (re-call with safe options) |

| # | Don't | Do |
|---|-------|-----|
| 1 | Default reject reason to "intent rejection" → text-only options report → no re-call | Default to secondary issue → re-call with improved options after fix |
| 2 | User shared primary source after reject → assume "the user wants to decide for themselves" → text report only | Primary source share = "ask now ready" signal → re-call ask mandatory |
| 3 | Hesitate to re-call out of "will the user reject again?" worry → text options only | Re-call cost ≈ 0. Avoidance is the bigger cost (user anger) |

## Case history

When an immediately-preceding ask was rejected and `/fix` cleaned up the reject cause, the completion report must **not** autonomously decide "end without re-call" — re-call the improved ask. (See failed-attempts.md "reject re-call".)

**3-1. Resume existing in_progress tasks (HARD STOP)**:
If TaskList had in_progress/pending entries before entering fix, fix Step 3 must **continue executing those tasks** before fix can end. "Already in TaskList, so no need to separate" is not resume — **actual execution** is resume.

| # | Don't | Do |
|---|-------|-----|
| 1 | End fix saying "existing tasks are in TaskList, so no separation needed" | Continue executing existing in_progress tasks in fix Step 3 |
| 2 | Resume only fix-2's subject scope and ignore existing tasks | fix-2 + existing in_progress tasks are **all** resume targets |
| 3 | Shorten resume with "login success = verification complete" | Login is a prerequisite. Run each verification item (countdown, permissions, etc.) individually |
| 4 | After completing 1 Resume item → switch to AskUserQuestion "what's next?" | **Complete all Resume items sequentially**. Completing 1 is not a switch point — start the next item immediately |
| 5 | Sub-task completed → "this task is done, let's take a breath" | After sub-task completes, immediately move to the next item of the Resume task. AskUserQuestion only **after all Resume items complete** |

1. Re-read `fix-2` subject — it contains the full list from the initial request to the immediately preceding action
2. **Classify done/not-done**: confirm the current state of each task (done, in progress, not yet started)
3. **Identify missing tasks**: list the correct procedure step by step, compare with what actually ran, and find **skipped intermediate steps**. Example: in "create issue → branch → implement → PR", if issue creation was skipped, that is the missing task
3.5. **Retroactive correction of the trigger object (HARD STOP)**: If the `/fix` was triggered because an action on a specific object in the past missed a required step (e.g., "you missed RAG import when archiving file X earlier"), **you must retroactively perform the missing step on that exact past object (file X) in Step 3**. Applying the new rule only to tests or future objects is a violation. The object that triggered the fix must be fully corrected.
4. Register the not-done + missing tasks and execute sequentially
5. Produce each task's **original deliverable** (e.g., classification table, plan document, deployment result, checklist update)
6. Verify after completing all tasks

**Step 3 constraints**:
- **Destructive commands require AskUserQuestion even during fix** — `git checkout -- .`, `git reset --hard`, `rm -rf`, etc. must not be executed without approval even under the pretext of "restoring original work"
- **Do not reinterpret user instructions** — if fix feedback is ambiguous, confirm via AskUserQuestion. Do not flip interpretations like reading "don't lose the changes" as "delete the changes"

**Non-destructive verification is autonomous; only the destructive action is ask-gated (HARD STOP)**:

The destructive-command-requires-ask rule above is **not** a license to defer the *non-destructive verification* that precedes the destructive action. Resume's deliverable includes **autonomously running every read-only verification that informs the gated decision, so the ask is presented WITH the results already in hand** — not "should I even verify?".

Draw the boundary explicitly:

| Stage | Examples | In resume |
|-------|----------|-----------|
| **Non-destructive verification** (no state/infra mutation) | `terraform plan` / Semaphore `dry_run` (after env-parity check), `ansible --check --diff`, `kubectl diff`, `--dry-run=client`, read-only API GET, `git fetch`, build/test in a scratch dir | **Run autonomously.** Part of the Resume deliverable. Surface the diff/plan result |
| **Destructive / irreversible action** (mutates state, infra, remote) | `terraform apply` / Semaphore real apply, `ansible-playbook` (no --check), `kubectl apply`, `git push`, merge, deploy, `rm`/`reset --hard` | **Ask-gated.** Present the ask carrying the verification result from the stage above |

| # | Don't | Do |
|---|-------|-----|
| 1 | Defer the dry-run/plan together with the deploy because "deploy = user decision" | Run the dry-run/plan autonomously first → then ask only about the actual apply/deploy, with the plan result attached |
| 2 | Over-apply "destructive needs ask" to its preceding read-only step | Ask gates only the mutation. The read-only verification that feeds the decision is autonomous |
| 3 | Present a deploy ask with no plan result ("shall I deploy?") | Present "plan shows N add / M change / K destroy — proceed with apply?" — the user decides from evidence, not blind |
| 4 | Skip a known-risky dry-run entirely instead of running it the safe way | If the dry-run itself has a project-specific risk (e.g. Semaphore `dry_run:true` can apply — see project rules), satisfy the safe path first (verify env var parity / use local `terraform plan`), then run it. "Risky → skip" ≠ "make it safe → run" |

**Anti-patterns**:
- "Script creation complete. Run it later" — fix's goal is **completing the original work**, not improving tooling. Tooling is the means.
- **Only reporting "X is now possible" and stopping** — register the not-done task via TaskCreate and **execute it immediately**. A status report is a precondition for execution, not the result.
- **Do not stop at file generation (e.g., pr_body.md creation) without executing the actual application update command (e.g., gh pr edit --body-file).** Status report or file generation is not the final deliverable. The final state must be physically applied and verified via the target medium.
- **Do not assume "original work already ended, so Resume is unnecessary"** — original work = the **deliverable** the user wanted, not "the act of invoking a skill/command". Even if an upper workflow (N steps) was invoked, if one intermediate step was missed, that step's deliverable does not yet exist = original work incomplete. After fix, the missed step must **be run now**.
- **Do not assume "session ended, so re-running is impossible"** — most skills are stateless. Only the missed step needs to be run standalone. There's no need to redo the entire upper workflow.

**Forbid verification scope reduction (HARD STOP — 2nd recurrence prevention)**:

Do not use a different medium than what the user reported as a detour. Reproduce via the "verification medium" specified in fix Step 3-0.

| # | Don't | Do |
|---|-------|-----|
| 1 | User reports "/api/X error" → substitute verification with login success / other APIs working | Directly call the user-seen `/api/X` via curl/Playwright → verify response status/body |
| 2 | User reports "permission error on screen Y" → after DB ALTER, only confirm admin login | Enter the user-seen screen via admin session → reproduce the same interaction → confirm whether the permission error recurs |
| 3 | One step (login) passes → assume subsequent steps (permission check / page entry / API call) are OK | Run each subsequent step **individually** for every step in the user-reported medium |
| 4 | Assume "logs are clean → normal" | Logs clean + **the user-medium reproduction response** both required |

**Self-check (every time before reporting verification complete)**:
1. Did you copy the user's fix-args medium (URL/API/screen) accurately?
2. Did you call/reproduce directly via that medium?
3. Did you compare the response with the user-reported error to confirm "normal" vs same/similar?
4. Did you avoid detoured verification (different URL, different screen, logs only)?

(Case history: a verification reported "complete" after checking only login + dashboard load, while the user-reported API itself still reproduced the error — see failed-attempts.md "verification scope reduction".)

**Step 3 mandatory self-questions (MANDATORY before marking fix-2 complete)**:
1. Did Why analysis identify a "skipped intermediate step"? → If yes, that step is fix-2's **immediate execution target**
2. Can that step **run standalone now (stateless)?** → If yes, run it unconditionally. "Original work is done, skip" is a violation
3. If the missed step is a skill/tool invocation → execute in this fix Step 3 → complete through result handling
4. **PR work sync check (HARD STOP)**: If this fix's original work is an active PR (`gh pr list --state open` includes the work's branch), did new feature/fix implementations get reflected in the PR body's Test Plan? — `gh pr view <N> --json body` → confirm a `- [ ]` line matching the implemented behavior exists. Missing line = skipped step → add via `gh pr edit --body` before completing fix-2. Applies even when no test was written: a manually verified behavior still needs a Test Plan line so reviewers know what was checked
5. **Architectural finding record check (HARD STOP)**: During fix work, was a non-obvious architectural fact discovered (e.g., "X record has no Y field", "API Z silently fails on type W", "framework auto-strips Q under condition R")? If yes, decide its recording medium **before completing fix-2**:
   - Project-specific structural fact → `CLAUDE.md` (project root) or `<repo>/.claude/rules/<topic>.md`
   - Reusable across projects → `~/.claude/skills/<related-skill>/data/` or `~/.agents/rules/<topic>.md`
   - Session-local context only → no record needed
   - "Code change alone = fix complete" thinking is a violation. The discovery is **load-bearing knowledge** for the next person (or future session) touching this surface — silent loss = the same wall hit again
6. **Non-destructive verification precedence check (HARD STOP)**: Does completing the original work involve a destructive/ask-gated action (apply, deploy, merge, push)? → If yes, did you **autonomously run the preceding non-destructive verification (dry-run / plan / `--check` / `--dry-run` / read-only diff)** and attach its result to the ask? Presenting the ask without the verification result — or deferring the dry-run together with the destructive action — is a violation (see "Non-destructive verification is autonomous" boundary above)
