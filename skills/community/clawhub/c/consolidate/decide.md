# User Decision (Formal Review) + Fix

Present classification results to the user from Step 4 and decide on Axis B (Formal Review action) only. AI Review Summary posting and Findings deferred registration are **procedure** (Step 7 / 7.6), not user decisions. fix is only executed when the user explicitly instructs (typically via Step 8 next-action or follow-up turn).

Entry: `Skill("consolidate", "decide ...")` or `pr.md` Workflow Step 5 / Step 6.

## Step 5: Formal Review Decision (Axis B only)

**Axis A (Findings handling) ask is forbidden (HARD STOP — 3 recurrences 2026-05-24)**.

The AI review handling flow is procedure:
- Condition (a): CodeRabbit walkthrough + Copilot review both posted normally → Step 7 auto-post AI Review Summary
- Condition (b): CodeRabbit walkthrough only OR Copilot error → Step 3.5 Internal Review Fallback → Step 7 auto-post AI Review Summary
- Actionable findings → Step 7.6 auto-register to fix_plan.md `[REVIEW_FEEDBACK]` (defer by default)
- fix is a **separate step only on explicit user instruction** (Step 8 next-action or a follow-up turn like "apply the review")

**Step 5 is Axis B (Formal Review action) only**. Ask only when you are a requested reviewer. Otherwise skip Step 5 and proceed directly to Step 7.

### Axis B ask precedes Summary medium decision/posting (HARD STOP — added 2026-05-26)

**When you are a requested reviewer, the Step 5 Axis B ask MUST precede the Step 7 Summary posting (whether issue comment or Formal Review body).** "Summary = procedure (automatic)" applies only to **Axis A (findings handling / whether to post)**, **not to the medium decision**. The Summary's medium (issue comment vs Formal Review body) is **dependent on the Axis B answer**, so posting the Summary in any medium before the Axis B answer strips the user of their Formal Review decision authority.

#### Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | As a requested reviewer, post the Summary as an issue comment without the Axis B ask | Axis B ask **first** → decide the medium per the answer (APPROVE/COMMENT/REQUEST_CHANGES/Skip) → then post |
| 2 | Execute post.md's "Non-Mergeable → issue comment only, Formal Review skipped" auto-rule without asking when `mergeable: CONFLICTING` | Even when CONFLICTING, a requested reviewer asks Axis B first. The medium auto-skip applies **only after** the ask answer |
| 3 | "Summary is automatic procedure, so post it now and handle Axis B later" | "Summary auto-post" is limited to Axis A (whether to post). The medium depends on Axis B → ask first |
| 4 | Evaluate post.md's medium table before the Axis B ask to fix the medium | The medium table takes **both** the Axis B answer + mergeable. Do not finalize the medium while Axis B is unanswered |

#### Self-check (every time before posting the Summary — HARD STOP)

1. Are you a requested reviewer? (`gh pr view --json reviewRequests` + cross-check active account) → If No, this gate does not apply (auto-post issue comment OK)
2. If Yes, **has the Axis B ask already been answered?** → If No, **posting the Summary is forbidden**. Call the Axis B ask first
3. Only after the Axis B answer, decide the medium (feed the Axis B answer + mergeable into the post.md Step 7 medium table)
4. If the thought "it's CONFLICTING so it's an issue comment anyway" arises = violation signal. Even CONFLICTING requires the Axis B ask first

### Don't / Do — Axis A ask forbidden (HARD STOP)

| # | Don't | Do |
|---|-------|-----|
| 1 | Call an Axis A ask ("Post summary as-is / Fix actionable items / Skip") | Proceed automatically to Step 7. Posting the Summary is procedure, not a user decision |
| 2 | Ask the user about Findings handling | Findings are auto-registered to fix_plan.md `[REVIEW_FEEDBACK]` in Step 7.6 (defer by default) |
| 3 | "fix is more natural, so Recommended" / "it's Critical/Important, so recommend fix" thinking | fix only on explicit user instruction. No auto-recommendation |
| 4 | Apply the archive rule "no auto-application" to Summary posting too | "No auto-application" applies only to fix (code changes). Summary posting is procedure (separate domain) |
| 5 | Bundle Summary posting + Findings handling into one ask | Summary = procedure (automatic), Findings = auto deferred registration. fix is a separate step (Step 8 or explicit instruction) |

### Self-check (before entering Step 5)

1. Are you a requested reviewer? (`gh pr view --json reviewRequests`) → If Yes, ask Axis B only. If No, skip Step 5 → Step 7
2. Are you building an Axis A option? → Don't. Proceed automatically to Step 7
3. If a "Fix actionable items" or "Whether to post the Summary" option appears = violation

| # | Don't | Do |
|---|-------|-----|
| 1 | Place "Fix actionable items" as the first option + mark it Recommended | Place "Post summary as-is" as the first option. Fix goes second-or-later (Recommended marking forbidden) |
| 2 | "Fix is more efficient, so mark it Recommended" / "Critical/Important findings → recommend fix" thinking | Independent of efficiency or severity. Acting on the AI review is the user's autonomous decision. Recommended marking itself is forbidden |
| 3 | Auto-place "Fix actionable" as the first option when severity is Critical/Important | Severity belongs in the option description. Order prioritizes "decision preservation" |
| 4 | "User decides on fix anyway, so first-position is fine" thinking | First option = implicit Recommended. Order itself is a statement of intent |

### Axis B: Formal Review action (HARD STOP — required when you are a requested reviewer)

**Pre-check: am I a requested reviewer?**

```bash
GH_TOKEN="$(gh auth token --user <account>)" \
  gh pr view <N> -R <owner>/<repo> --json reviewRequests --jq '.reviewRequests[].login'
# Match against current `gh auth status` active account
```

If the current account appears in `reviewRequests`, present the Axis B ask (the only ask in Step 5 — Axis A has been removed per the HARD STOP above):

```javascript
AskUserQuestion({
  question: "Formal Review action (you are a requested reviewer)?",
  options: [
    { label: "APPROVE", description: "Findings clean / Critical 0 / merge OK" },
    { label: "REQUEST_CHANGES", description: "Critical findings exist — block merge" },
    { label: "COMMENT only", description: "No formal verdict — just post review body" },
    { label: "Skip formal review", description: "Issue comment Summary only (no PR-level review)" }
  ]
})
```

**Why Axis B matters even though Axis A is removed**: Posting the Summary as an issue comment (Step 7 procedure) is *not* the same medium as a GitHub Formal Review. Formal Review (B) is a separate medium — GitHub PR review state (APPROVE / CHANGES_REQUESTED / COMMENTED) that gates merge. Posting the Summary issue comment without an APPROVE (B) leaves the PR blocked by an unfulfilled review request even if all CI/tests pass.

#### Conditional gate: merge-recommendation verdict → no Skip option (HARD STOP)

**If the AI Review Summary verdict in Step 7-A indicates merge recommendation** (🟢 / "Merge OK" / "Ready to merge" / "Merge ready"), remove the `Skip formal review` option from Axis B. The user must choose APPROVE / REQUEST_CHANGES / COMMENT — not Skip. Reason: Skip leaves `reviewDecision: REVIEW_REQUIRED` unresolved, contradicting the merge-recommendation verdict.

```javascript
// When AI Review Summary verdict = merge-recommendation
AskUserQuestion({
  question: "Formal Review action (Summary verdict = merge recommendation — Skip not allowed)?",
  options: [
    { label: "APPROVE", description: "Findings clean / Critical 0 / merge OK — default for merge-recommendation verdict" },
    { label: "REQUEST_CHANGES", description: "Re-evaluation: Critical findings actually exist — block merge" },
    { label: "COMMENT only", description: "Verdict reconsidered: post review body without merge gating verdict" }
  ]
})
```

If the Summary verdict is non-merge (Critical findings exist, Test Plan incomplete, CI failing), keep all 4 options including Skip.

| # | Don't | Do |
|---|-------|-----|
| 1 | Post issue comment Summary and end, when you are a requested reviewer | Axis B is mandatory when you are a requested reviewer — answer Axis B before entering Step 6/7 |
| 2 | Assume "Summary comment counts as APPROVE" | Issue comment ≠ Formal Review. GitHub merge gates check the `reviews` array, not issue comments |
| 3 | Skip Axis B because findings are clean | Clean findings + requested reviewer = APPROVE (default), still requires the explicit POST |
| 4 | Present Skip option when Summary verdict is merge-recommendation | Remove Skip option for merge-recommendation verdicts. Skip + merge-OK verdict = contradiction (reviewDecision unresolved) |
| 5 | Post Summary verdict = "🟢 merge OK" but answer Axis B as Skip | Summary verdict and Formal Review action must align — merge-recommendation Summary mandates APPROVE/REQUEST_CHANGES/COMMENT |

### Step 5 AskUserQuestion option drift forbidden

Step 5 asks only Axis B (Formal Review action). **Detailed fix-scope options like "which Critical to apply" belong in Step 6 and only on explicit user instruction**. If the Step 5 question drifts into a "fix-scope multiSelect" or reintroduces an Axis A "whether to fix" option, it's a signal that both Step 3.5.3 and Step 7 (posting) are being forgotten.

## Step 6: Fix or Reject (only on explicit user instruction)

**Fix is executed only on explicit user instruction** — typically from the Step 8 next-action ask after Summary posting, or from a follow-up user turn such as "apply the review". There is no Step 5 fix-approval gate (Axis A has been removed). **Critical items, if the user instructs a fix, must be fully fixed and verified before re-posting the updated Summary** so the Summary verdict reflects the actual code state.

| # | Don't | Do |
|---|-------|-----|
| 1 | code-reviewer reports "Must Fix" → immediately execute Edit | Wait for explicit user fix instruction (Step 8 or follow-up turn) → Edit → Critical fully verified → re-post or update Summary → Step 8 merge ask |
| 2 | Skip ask with "Critical, so of course fix it" reasoning | Even Critical requires an explicit user fix instruction. Severity ≠ autonomous fix authority |
| 3 | Receive code-reviewer result → skip posting review comment → fix immediately | Post Step 3.5.3 comment → Step 4 classification → Step 5 Axis B (if requested reviewer) → Step 7 Summary post → Step 8 next-action ask (fix lands here only if user instructs) |

### Branch ownership check before fixing

| Branch creator | Allowed action |
|----------------|---------------|
| Self (gh issue develop) | Code fix + commit + push |
| Others (dependabot, user branch) | Comment-only — no code changes |

### Pushback procedure (for Rejected items)

When a suggestion is technically incorrect, YAGNI, or conflicts with architecture:

1. Write a concise technical reason (not defensive, not performative)
2. Reply in the PR review thread: `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies -f body="..."`
3. Record in checklist as `[REJECTED]` with reason

Example pushback:
```text
Suggestion: "Add retry logic for this API call"
Rejection: "Caller already handles retries (see middleware.ts:45). Adding here creates double-retry. YAGNI."
```

### Fixing accepted items

**Critical/Important items must be fixed AND verified before proceeding to the next stage (Summary posting, merge recommendation):**

1. Code fix + commit + push
2. Wait for CI pass (`gh run watch` or `gh pr checks`)
3. **Runtime verification of the fix's actual behavior (HARD STOP)** — see "Review-suggested API call runtime verification" below
4. Check `[x]` for the corresponding item in PR Test plan (`gh pr edit --body`) **only after step 3 passes**
5. Post Summary and recommend merge only after verification is complete

The "Shall we merge?" question is allowed only after all Critical items have been fully verified.

After fixing, commit with message referencing the review:
```text
fix: address CodeRabbit review on PR #NUMBER
```

### Review-suggested API call runtime verification (HARD STOP)

**When a review suggestion (AI bot OR Internal Code Review subagent) replaces one API call with another (e.g., "prefer X over Y", "use vscode.open instead of openExternal"), CI pass + type-check + build success do NOT verify the fix. Runtime verification is mandatory before claiming the Important/Critical is fixed.** CI checks compile-time correctness, not API semantics. A wrong API substitution (e.g., a command that resolves URIs as file paths when the original handled them as extension URIs) compiles cleanly, builds cleanly, and breaks at the first user click.

#### Why this rule

The fix author is often the same agent that wrote the review (Internal Code Review = code-reviewer subagent dispatched by this skill). Internal Review suggestions inherit the same blind spots that produced them — runtime verify is the only independent check. AI bot suggestions (CodeRabbit, Copilot) have analogous risk: pattern-match correctness without dispatch-semantics verification.

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | "CI pass + type-check + build OK → Important fixed" report | CI pass + build OK ≠ runtime correctness for API-substitution fixes. Add a runtime verification step before checking PR Test Plan items |
| 2 | "Review suggestion came from a trusted source (Internal Review / CodeRabbit), so apply + commit" | Internal Review's author may be the same agent that wrote the buggy code. **Look up authoritative docs for the new API** (context7, official API ref, working PoC in the same repo) — if the docs/PoC contradict the suggestion, push back instead of applying |
| 3 | "API replacement is a 1-line change so verify is overkill" | API replacement is HIGH risk. Wrong API often compiles cleanly. 1-line changes need MORE verify, not less — the wrong API hides in a single working-looking line |
| 4 | Push the fix and rely on PR Test Plan checkbox as the verify | The checkbox is just a checkbox. The verify is the actual runtime exercise (install vsix → click → observe behavior; or curl the affected endpoint; or load the changed UI route) |
| 5 | "Author of the suggestion already explained why" → trust without independent check | The explanation may be wrong. **Cross-check against**: (a) authoritative API docs, (b) an existing working sibling implementation in the same repo (e.g., `feat/resume-in-extension` PoC branch for this PR), (c) ride a runtime smoke test |

#### Self-check (every time before checking the PR Test Plan item as `[x]`)

1. Did this fix REPLACE one API call with another (e.g., `vscode.env.openExternal` → `vscode.commands.executeCommand('vscode.open', ...)`)? — Yes ⇒ rule applies
2. Did you look up authoritative documentation (context7 / official API ref) for the NEW API's actual semantics? — `vscode.open` handles file/URL paths, NOT extension URIs; that fact would have killed the suggestion at design time
3. Is there a working sibling implementation in the same repo using the OLD API? (`git branch -a` for PoC branches, `grep` for similar call sites) — if yes, the OLD API is the proven path; replacing it requires positive evidence the NEW API is superior, not just "more correct in theory"
4. Did you exercise the changed code path at runtime? (vsix install + manual click for extension code; curl for endpoints; browser navigation for routes)
5. Did the runtime exercise produce the expected outcome, OR did it produce a new error (e.g., `EntryNotFound`)?

If step 5 produced a new error, **REVERT the API substitution immediately** and downgrade the finding in the Summary (e.g., Important → Minor, deferred — "no reliable success signal exists for this dispatch; openExternal best-effort is the accepted path per PoC branch").

#### Cross-reference

- `~/.agents/rules/external-publication-verification.md` — covers PR-body claims and external public statements
- `superpowers:receiving-code-review` "Verify before implementing" — covers external bot review reception
- This rule covers **the gap** between those two: applying an Internal Review's own suggestion + the runtime verify obligation specifically for API-substitution fixes

### 'Apply' interpretation rule for user instructions

When the user specifies an application scope such as "apply only X" or "don't apply X", it **by default means code implementation scope**. If AI Review Summary editing is required, the user explicitly states the target like "in the Summary" or "remove from the review". When the target is unclear, **use AskUserQuestion to confirm "is it code implementation scope or Summary editing?"** — arbitrary interpretation is forbidden.

## Next

→ `post.md` (Step 7 Post AI Review Summary + Formal Review)
