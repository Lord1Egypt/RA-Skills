# Post-Summary Next-Action Ask

After AI Review Summary post + Status line output, ask for the PR handling direction (merge/verify/defer). Final stage of the consolidate workflow.

Entry: `Skill("consolidate", "next ...")` or `pr.md` Workflow Step 8.

## Step 8: Post-Summary Next-Action Ask (MANDATORY — immediately after Status line)

Immediately after the Status line output, **ask the user for the PR handling direction**. Terminating without presenting options = procedural violation, **except** when the routing table below explicitly permits skipping (i.e., the only possible follow-up is "defer", so there is genuinely no actionable next step).

### Finding-first ordering (HARD STOP — finding decision precedes merge)

**When the PR has actionable findings, the finding-handling decision is a SEPARATE axis that PRECEDES the merge decision.** Do not lead with the merge question, and do not present finding-handling + merge as a `questions` array in a single turn — they form a dependency chain (a preceding decision determines the meaning of the following one → sequential ask), not parallel tracks.

| Precedent axis (ask FIRST) | Dependent axis (ask AFTER the finding answer) |
|----------------------------|-----------------------------------------------|
| Finding handling (which findings to apply / defer) | Merge (merge content/timing depends on whether findings are applied first) |

**Why finding-first**: applying a finding changes what gets merged (fix → reflected in branch → then merge) vs defer (merge as-is). The merge option's meaning is undetermined until the finding decision is made — leading with merge inverts the dependency.

**Post-hoc review PR (HARD STOP)**: when the PR exists specifically to retrospectively review already-merged/deployed commits (see MEMORY "post-hoc review PR" workflow), **finding resolution IS the PR's purpose**. Merge (e.g., develop alignment) is strictly secondary — ask the finding-handling axis first; never lead with the merge question.

**Post-hoc review PR finding options exclude "defer" (HARD STOP)**: since finding resolution is the very reason the PR exists, the finding-handling ask must NOT offer a "defer all (track only)" option — deferring the findings contradicts the PR's purpose ("pulled it in to review, why defer the review?"). The finding axis is a **scope decision only** (which findings to fix — e.g., "essential mismatches only" vs "all C+I"), and the chosen scope is **applied immediately**, not deferred. A "defer all" option belongs to normal PRs where merge is the goal; on a post-hoc review PR it is forbidden.

| # | Don't | Do |
|---|-------|-----|
| 1 | Put the merge question as Q1 and finding-handling as Q2 | Finding-handling axis is asked FIRST; merge is a follow-up after the finding answer |
| 2 | Present merge + finding-handling as a `questions` array in one turn | Dependency axis → sequential: 1st finding-handling, then (after the answer) merge |
| 3 | On a post-hoc review PR, lead with "merge to develop?" | Post-hoc review PR purpose = finding resolution. Lead with finding handling; merge secondary |
| 4 | Treat finding-handling and merge as parallel tracks | They are a dependency chain — the finding result determines the merge content |
| 5 | Offer "defer all (track only)" as a finding option on a post-hoc review PR | Post-hoc review PR = finding resolution is the purpose. Finding options are scope-only (which to fix), applied immediately. No defer-all option |

**Self-check (Step 8 entry, before any AskUserQuestion)**:
1. Does the PR have 1+ actionable findings? → If yes, finding-handling is a precedent axis
2. Is this a post-hoc review PR (PR exists to review already-merged commits)? → If yes, finding-first is mandatory
3. Am I about to present merge + finding-handling in one `questions` array? → STOP. Split: finding-handling first, merge as a sequential follow-up
4. Is the merge question leading (Q1)? → If findings exist, invert: finding-handling leads
5. Is this a post-hoc review PR? → finding options must NOT include "defer all" (deferring contradicts the PR's purpose). Offer scope choices only (which findings), applied immediately

### Routing: next vs wip

| Situation | Skill to use | Reason |
|-----------|-------------|--------|
| Single PR consolidate completed | `Skill("next")` | "Follow-up action after task completion" pattern. single question with 2-4 options |
| Consolidating multiple PRs in sequence | `Skill("wip")` | 1 question per task for independent per-PR decisions (questions array up to 4) |
| Fewer than 1 follow-up action (no option other than defer) | Skip ask, terminate with report | Clearly no next step |

### Authorship gate — no merge option on others' PRs (HARD STOP)

**Before composing any merge option, confirm the PR author is the current account.** consolidate is a review tool — when you are a *requested reviewer* on someone else's PR, your role ends at APPROVE / review feedback. Merging is the **author's** domain (branch ownership — same principle as `decide.md` Step 6 "branch ownership check before fixing", extended to merge-option presentation). For a PR authored by someone else, **do not present a merge option at all** (not even as a non-Recommended option).

> **Formal Review event for peer reviewer** (author ≠ me, non-requested): the Formal Review event decision (APPROVE / COMMENT / REQUEST_CHANGES) is **NOT** part of Step 8 next-action options — it is handled at Step 7 Summary POST per `post.md` "Non-requested reviewer event policy". Critical > 0 → REQUEST_CHANGES auto; merge gate failures → COMMENT auto; APPROVE candidate → ask. Step 8 next-action ask runs AFTER the Formal Review POST and asks the post-review follow-up (relay deferred findings to author / hold / done) — never re-asks the Formal Review event.

```bash
# Pre-check before merge-option composition
AUTHOR=$(gh pr view <N> -R <owner>/<repo> --json author --jq '.author.login')

# The comparison target is the API identity of the gh account being used for THIS repo
# (per ~/.agents/rules/git.md account mapping: es6kr → DrumRobot, daegunsoftDev → daegunjhy).
# Do NOT use `gh auth status` "active" account — when multiple accounts are logged in,
# the active one can differ from the account whose token is actually being used for the repo.
# Do NOT use `git config user.email` — commit identity ≠ GitHub API identity.
ACCOUNT_FOR_REPO=$(  # the gh user matching the repo owner per git.md mapping
  case "<owner>" in
    es6kr) echo DrumRobot ;;
    daegunsoftDev|daegunjhy) echo daegunjhy ;;
    *) gh auth status 2>&1 | awk '/Logged in/{print $7; exit}' ;;
  esac
)
ME=$(GH_TOKEN="$(gh auth token --user "$ACCOUNT_FOR_REPO")" gh api /user --jq '.login')
# Mismatch ($AUTHOR != $ME) → no merge option
```

| # | Don't | Do |
|---|-------|-----|
| 1 | Present "Squash merge (Recommended)" on a PR authored by someone else | Author ≠ me → omit merge options entirely. Offer review-scoped options only (relay deferred findings to author / hold / done) |
| 2 | "4 merge conditions met → recommend merge" regardless of authorship | 4-condition check is necessary but not sufficient. Authorship is a prerequisite gate for any merge option |
| 3 | Treat APPROVE on another's PR as license to drive the merge | APPROVE satisfies the review request; the merge decision/timing belongs to the author |
| 4 | Offer "apply Minor then merge" on another's branch | Code changes on another's branch are forbidden (branch ownership). Deferred findings are already in the Internal Review comment for the author |

**Self-check (before composing options on a consolidate-completed PR)**:
1. `gh pr view <N> --json author` → capture `$AUTHOR`.
2. Resolve `$ACCOUNT_FOR_REPO` per the owner → account mapping (`~/.agents/rules/git.md`), then `$ME = gh api /user --jq '.login'` with that account's token. **Do not** compare against `gh auth status` "active" account or `git config user.email`.
3. If `$AUTHOR != $ME` → merge options forbidden. Options = "relay deferred findings to author / hold / done (review complete)". Report APPROVED state + that merge is the author's call.
4. If `$AUTHOR == $ME` → proceed to the merge-condition option guide below.

### Option composition guide (single PR — next skill, **own-authored PRs only**)

To pass the `block-merge-without-review.sh` guard, **the merge option description must explicitly include "AI Review Summary posted (URL)"**.

| Merge 4-condition satisfaction | Recommended options (Recommended at top) |
|-------------------------------|------------------------------------------|
| 4/4 satisfied | (1) Squash merge — AI Review Summary posted (URL) (2) Apply Minor then merge (3) Defer |
| 1+ Test Plan unchecked | (1) Verify unchecked items (web-browser/curl) (2) File separate issue then merge (3) Defer |
| 1+ CI failures | (1) Investigate CI cause (2) If failure unrelated to PR, file separate issue (3) Defer |
| Formal Review unapproved | (1) Self-approve (2) Request reviewer (3) Defer |
| AI Review Summary not posted | **Cannot reach this stage** — Step 7 requires posting |

### Deferred Actionable tracking option (MANDATORY — when merging + Critical/Minor not applied)

When pushing a merge while not immediately applying actionable items (Critical, Minor), the **tracking location must be explicitly stated in the option**. Vague descriptions like "subject to separate PR" are forbidden.

**Tracking medium (checklist) branching (per workflow environment)**:

| Environment detection | Tracking medium | Format |
|----------------------|----------------|--------|
| `{workspace}/.ralph/fix_plan.md` exists (Ralph autonomous) | fix_plan.md | `- [ ] [BLOCKED] [REVIEW_FEEDBACK] {reviewer}: {summary} — {action direction}` |
| `{workspace}/checklist.md` exists (Ralph not in use) | checklist.md | `- [ ] [BLOCKED] {summary}` |
| GitHub Issue collaboration workflow | Separate Issue | `gh issue create` — specify "deferred from PR #N" in title/body |
| Handled by additional commit in the same PR | Separate commit | Do not use "subject to separate PR" — push to this PR |

**Option description requirements**:

When a merge option entails deferred actionable items, the description must include all of:
1. AI Review Summary URL (passes block-merge-without-review.sh)
2. **Tracking location of deferred items** (checklist / Issue number)
3. **Form of deferred items** (`[BLOCKED]`, `[REVIEW_FEEDBACK]`, Issue title, etc.)

**Deferred scope branching (MANDATORY — branching options required if 2+ actionable items)**:

If actionable items (Critical + Minor + Refactor) total 2 or more, do not create a single "Critical only" option; instead present **3-way branching options**:

| Branch | Applicable case | description example |
|--------|----------------|---------------------|
| **Critical only deferred** | When Minor is applied immediately or decided to be ignored | "Critical 1 item checklist [BLOCKED] + Minor ignored in this PR (No action)" |
| **Minor only deferred** | When Critical is applied immediately | "Critical applied immediately + Minor in checklist [BLOCKED]" |
| **All deferred** | All actionable items handled in next session or separately | "Critical + Minor all in checklist [BLOCKED]" |

**Option example (GitHub Issue environment, 1 Critical + 2 Minor)**:

```typescript
[
  {
    label: "Merge PR + Critical only as separate Issue",
    description: "AI Review Summary posted (URL) | 1 Critical filed as new Issue + 2 Minor No action. squash merge"
  },
  {
    label: "Merge PR + all actionable as separate Issues",
    description: "AI Review Summary posted (URL) | Critical + Minor all filed as Issues × 3 (title: \"deferred from PR #N: {summary}\"). squash merge"
  }
]
```

**Reinforced self-check** (immediately before option drafting — additional items):

5. If actionable items total 2 or more, are all **3 branching options** included? (Critical only deferred / Minor only deferred / All deferred — matching the branching table above)
6. Is "All deferred" always included as one of the recommended options regardless of the number of actionable items?

**Don't / Do table**:

| # | Don't | Do |
|---|-------|-----|
| 1 | Abstract description like "subject to separate PR" | Specify tracking medium (fix_plan.md/Issue/checklist) + form (`[BLOCKED]`, etc.) |
| 2 | Push medium decision onto the user without autonomous determination | Auto-detect environment (whether `.ralph/fix_plan.md` exists) and present medium options |
| 3 | Omit form of deferred items (`[BLOCKED]`, Issue title) | Indicate form inline in the option description |
| 4 | Omit tracking location after "Critical to be handled later separately" | Bundle immediate registration in the tracking medium as a task right after merge |

**Self-check (immediately before option drafting)**:

1. Does the merge option entail 1+ unapplied actionable items?
2. Has the tracking medium been determined per environment (whether `.ralph/` exists)?
3. Does the option description include all of (a) AI Review Summary URL (b) tracking location (c) form?
4. Is the post-merge tracking-medium registration bundled as a separate executable task?

### Cross-PR Epic bundling auto-suggest (offer when deferred findings accumulate across PRs)

After registering this PR's deferred items in the tracking checklist, check whether the checklist now holds un-bundled deferred findings spanning **2+ distinct PRs**. If so, add one extra (non-merge) next-action option offering to bundle them into a single Epic tracking issue:

| Condition | Extra option |
|-----------|-------------|
| 2+ PRs with un-bundled `[REVIEW_FEEDBACK]` deferred items in the checklist | "Bundle deferred findings into an Epic tracking issue" |

- This is an **offer**, not an auto-run — Epic issue creation needs explicit user approval (`git.md` no-autonomous-issue-create). The caller selects whichever epic-bundling workflow is registered in the environment (vendor-agnostic — `gh issue create` with sub-issue links is the minimal path).
- Do not add this option when only the current PR has deferred items — single-PR deferral is already covered by the section above.
5. **Reject findings axis check (HARD STOP — 2026-05-24)**: are there 1+ findings auto-classified as Reject in Step 4? → If yes, **Reject findings must appear as a user-override option** in this Step 8 ask. See "Reject finding option mandate" below

### Reject finding option mandate (HARD STOP — added 2026-05-24)

**A Reject decision must also be user-overridable.** Even if Step 4 auto-classified a finding as Reject via the `superpowers:receiving-code-review` "Push back when wrong" procedure, the Step 8 next-action ask must **expose that Reject decision to the user**. If Reject disappears from the options, the user cannot choose "apply it anyway" / "keep it Rejected" → Resume scope shrinks.

#### Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | After auto-classifying Reject in Step 4, fully exclude the Reject finding from the Step 8 ask options | Expose the Reject finding to the user as a separate option or axis. The user can decide to override Reject |
| 2 | "The Reject rationale (repo convention, etc.) is clear, so omitting the option is OK" thinking | Even with a clear rationale, the user decision step is separate. Reject = AI judgment, override = user authority |
| 3 | Assume "Accept/Defer options alone are enough" | Present all three to the user: Accept option / Defer option / **Reject override option** |
| 4 | Assume "the Push back when wrong procedure has no user-confirmation step, so auto-Reject is OK" | superpowers is an evaluate→respond framework. The Step 8 ask is the final decision gate. Two separate domains |

#### Option design pattern (when a Reject finding exists)

```typescript
[
  {
    label: "Apply Accept findings + Reject as-is (Recommended)",
    description: "AI Review Summary posted (URL) | Accept N items applied + Reject M items kept (reason: <repo convention etc.>)"
  },
  {
    label: "Apply ALL findings (override Reject)",
    description: "AI Review Summary posted (URL) | Accept N + Reject M (override — user decided to apply despite the pushback reason)"
  },
  {
    label: "Defer all findings",
    description: "AI Review Summary posted (URL) | fix_plan [BLOCKED] [REVIEW_FEEDBACK] for Accept N + Reject M (override option preserved)"
  },
  {
    label: "Hold",
    description: "Decision pending"
  }
]
```

A **Reject-only application option** is also possible (e.g., Accept defer + Reject override):
```typescript
{
  label: "Override Reject only (defer Accept)",
  description: "AI Review Summary posted (URL) | Reject M applied (user override) + Accept N deferred to fix_plan"
}
```

#### Self-check (every time before option drafting)

1. Are there 1+ Reject findings in the Step 4 classification?
2. If yes, did you include a Reject override option in the Step 8 options?
3. Did you state the Reject rationale in the option description? (gives the user info to judge "is that rationale enough? override?")
4. If only "Accept only" / "Defer only" options are presented = violation (Reject override omitted)

### Invocation pattern

```text
Skill("next") with args:
  "After PR consolidate — ask for PR #N handling direction
   - 4-condition status: <CI/Review/TestPlan/Mergeable>
   - AI Review Summary URL: <comment-URL>
   - Option candidates: ..."
```

The next skill performs the AskUserQuestion call + result handling. The consolidate skill is only responsible for invoking next.

### Self-check (on Step 8 entry)

1. Was the Step 7.5 status line output?
2. **Is the PR authored by the current account?** (`gh pr view <N> --json author`) → If **no**, merge options are FORBIDDEN (see "Authorship gate" above). Offer review-scoped options only
3. Is there at least 1 PR handling direction candidate? (including defer)
4. If a merge option is among the candidates: (a) is the PR self-authored? (b) does the description include the attestation?
5. For a single PR, did you decide to route to next; for multiple PRs, to wip?

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Terminate after outputting only the Status line | Invoke next/wip per the routing table |
| 2 | Avoid the ask by reporting "awaiting explicit user instruction" | Defer is also an option — proceed with the ask |
| 3 | Omit attestation from the merge option description | Include "AI Review Summary posted (URL)" → passes block-merge-without-review.sh |
| 4 | Compress 4 PRs into next during a multi-PR consolidate | Route to wip (1 question per PR) |
| 5 | Present a merge option on a PR authored by someone else | Authorship gate first — author ≠ me → no merge option; relay deferred findings to author / hold / done |

## Workflow termination

Handle user decisions based on the next/wip invocation result. The consolidate skill terminates here.
