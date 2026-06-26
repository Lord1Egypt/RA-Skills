# Internal Review Fallback + UI Capture Verification

Internal Code Review fallback when external AI review is insufficient (CodeRabbit Free walkthrough only, Copilot failure) + UI change PR capture attachment verification.

Entry: `Skill("consolidate", "internal ...")` or `pr.md` Workflow Step 3.5 / Step 4.5.

## Step 3.5: Internal Review Fallback

**Trigger conditions** (run fallback if any of these apply):
- **CodeRabbit is walkthrough only** (Free plan — provides only summary without line-by-line review)
- **Reviewer failure/error** — review is impossible such as Copilot "encountered an error"
- **Copilot subscription unavailable** — `pr.md` Step 2.4 availability pre-check returned not-available (free account / no org seat / 404 on `/user/copilot_billing` and `/orgs/<org>/copilot/billing`). **This is the auto-fallback path — no AskUserQuestion required.** Record the substitution in the Summary's reviewer matrix (e.g., "Copilot unavailable on the acting account/org — auto-fallback per Step 2.4")

**Worktree (from Step 2.7)**: the PR branch is already checked out into a worktree by `pr.md` Step 2.7. Dispatch the code-reviewer **against that worktree path** so it reads real files (not just `gh pr diff`) and can run tests/build locally. Pass the worktree path in the agent prompt (`Repository: <worktree-path>`). The reviewer should still use `gh pr diff <N>` for the canonical PR diff, but reads file bodies + runs verification in the worktree.

**Fallback procedure:**

1. **Call `Skill("superpowers:requesting-code-review")` (MANDATORY)** — this skill loads the review framework and includes code-reviewer agent dispatch. When the skill returns the review result, proceed to the "Check existing review comment" and "Post/update review comment" sub-steps below (still within Step 3.5).

| # | Don't | Do (correct alternative) |
|---|-------|-------------------------|
| 1 | Dispatch `Agent(subagent_type: "code-reviewer")` directly | Call `Skill("superpowers:requesting-code-review")` → skill includes agent dispatch |
| 2 | Classify review based on code-reviewer result alone | Apply both the requesting-code-review skill framework + receiving-code-review verify→evaluate→respond |
| 3 | **Analyze 18 files directly from chat text and jump to Step 7** (Step 3.5.3 comment posting omitted) | **`## Internal Code Review — [requesting-code-review](...)` comment must exist on GitHub** to enter Step 4. Chat analysis is auxiliary; comment posting is the primary medium |
| 4 | "Trigger satisfied but superpowers skill not installed, so substitute with self-analysis" | Internal Code Review comment posting is mandatory even without the skill — if the superpowers skill call fails, post the self-analyzed result as a comment using the same title template (skill bypass allowed, comment bypass forbidden) |
| 5 | "CodeRabbit findings are detailed enough — verify them myself and skip the Internal Review skill call" | Trigger condition is satisfied **independent of CodeRabbit's quality**. The Internal Review's purpose is to add a *second independent perspective*, not to compensate for missing detail. Detail quality of an existing reviewer does not dismiss the trigger. Always invoke `Skill("superpowers:requesting-code-review")` when the trigger condition matches |
| 6 | User says "fall back to internal-review on Copilot rate-limit" → interpret as "I verify CodeRabbit findings personally" | "Internal-review" = the **superpowers code-reviewer skill**, not self-verification. User's args reinforce the trigger; they do not authorize self-substitution |

### Self-check (always before entering Step 5 AND Step 7 — HARD STOP)

Two gates: Step 5 (User Decision ask) and Step 7 (Summary post). Both forbid entry without the Internal Review comment when the trigger matches.

Before posting **either** the Step 5 AskUserQuestion **or** the Step 7 `## AI Review Summary`, run the following self-check:

1. Was the state CodeRabbit walkthrough only (Free plan) or reviewer error? → If Yes, Step 3.5 trigger is satisfied
2. If trigger was satisfied, was a `## Internal Code Review` comment posted on the GitHub PR? → `gh api .../issues/{N}/comments | jq '.[] | select(.body | startswith("## Internal Code Review"))'`
3. If the comment is absent → **forbid entering Step 5 or Step 7**. Return to the Step 3.5 procedure and post the comment first
4. Does the comment body contain dual-label findings (Type | Severity) or their equivalent?

**Why Step 5 also gated**: the user's decision options must reflect both reviewer streams (CodeRabbit + Internal). Posting Step 5 ask with only CodeRabbit findings + self-verified Reject/Accept classifications leaves the user without the second independent perspective that justified the consolidate flow. Re-call Step 5 ask after the Internal Review comment exists.

### Medium decision (MANDATORY — inline targets decide the posting medium)

The Internal Review's posting medium branches on whether **inline targets** exist (auto-fire policy below: line-specific 🔴 Critical + 🟡 Important findings by default; ALL line-specific findings with the `--inline` flag):

| Inline targets | Medium | First post (no prior Internal Review) | Re-review (prior Internal Review exists) |
|----------------|--------|----------------------------------------|------------------------------------------|
| **1+ exist** | **Single reviews API POST** — `gh api POST .../pulls/{N}/reviews`: `body` = full Internal Review findings, `comments[]` = inline annotations | First `gh api POST .../reviews` — no PATCH target exists yet | **New review POST every time** (no PATCH/PUT of the prior review — each re-review is a fresh time-ordered review, like external bots) |
| **None** | Issue comment (`gh pr comment`) | First `gh pr comment <N>` — no PATCH target exists yet | **PATCH the existing comment** (`gh api repos/{owner}/{repo}/issues/comments/{id} --method PATCH --input <file>`) — forbid a parallel new comment |

**Merge state does not change the medium (HARD STOP).** A merged or closed PR still takes the reviews API POST with `comments[]` inline when inline targets exist — the auto-fire policy (line-specific 🔴 Critical + 🟡 Important → review POST) applies **regardless of merge state**. The reviews API accepts inline comments on a merged PR against its head SHA. A post-merge review is still a review POST, not an issue comment. Do NOT downgrade to `gh pr comment` because the PR is merged.

**Existing-artifact check before posting** (per medium):

```bash
# Issue-comment medium: find prior Internal Review comment (PATCH target)
gh api repos/{owner}/{repo}/issues/{N}/comments --jq '.[] | select(.body | test("Internal Code Review")) | "\(.id) \(.updated_at)"'
# Review medium: prior reviews are left as-is (time-ordered records) — no check needed beyond counting for the re-review note
```

| # | Don't | Do (correct alternative) |
|---|-------|-------------------------|
| 1 | Post the full findings as an issue comment AND a stub-body inline review (2 artifacts, body pointing at the comment) | One reviews API POST carrying both: full findings in `body` + line annotations in `comments[]` |
| 2 | PATCH/PUT a prior review's body on re-review | Re-review with inline targets = new review POST every time |
| 3 | Add a parallel issue comment when a prior Internal Review comment exists (no-inline medium) | PATCH the existing comment |
| 4 | Ask the user which medium to use at runtime | The inline-target count decides the medium deterministically |
| 5 | Downgrade to an issue comment because the PR is merged/closed (post-merge review) | Merge state is irrelevant — reviews API POST + `comments[]` works on merged PRs (against head SHA). Apply the auto-fire policy regardless of merge state |

### Post the Internal Review (MANDATORY — must complete before entering Step 4)

Post the code-reviewer result via the medium decided above. **The review (or comment) must exist on the PR before proceeding to Step 4** — substitution with a text report is forbidden.

#### Interactive gate (when `--interactive` is on — literal or auto-activated by args)

Before the POST step (the title-template + medium-decided POST in the rest of this Step 3.5 procedure), the caller MUST follow the **Interactive flow contract** defined in `SKILL.md`:

1. Write the Internal Review body to `.tmp/internal-review-draft.md` (do not POST yet)
2. Emit a chat summary (finding counts per Severity + verdict line + draft path)
3. Call `AskUserQuestion` with options: `Approve as-is` / `Edit (specify in Other)` / `Reject — do not POST`
4. Apply user edits → re-present → re-ask, until Approve or Reject
5. On Approve, proceed to the medium-decided POST in the rest of Step 3.5. On Reject, skip the POST and record the reason in chat.

If `--interactive` is off, proceed directly to the medium-decided POST (deterministic flow). Inline annotation bodies (per "Inline auto-fire policy" below) are part of the draft and reviewed in the same ask — do not POST inline comments separately under interactive mode.

**Title template (MANDATORY — first line of the review body / comment body)**:
```markdown
## Internal Code Review — [requesting-code-review](https://skills.sh/obra/superpowers/requesting-code-review)
```
Do not write `code-reviewer` as plain text; use the link format above.

#### 🌐 Verify repository default language before posting (MANDATORY)

Subagents (code-reviewer, etc.) tend to output in English. If different from the target repository's default language, **translate before posting**.

```bash
# 1. PUBLIC repo check (opensource.md "PUBLIC English enforced")
GH_TOKEN="$(gh auth token --user <account>)" gh repo view <owner>/<repo> --json isPrivate -q '.isPrivate'
# false → post in English only (HARD STOP if Korean detected, retry after English translation)
# true → proceed to next step
```

```bash
# 2. Check private repository default language (sample recent PR/issue/commit bodies)
GH_TOKEN="$(gh auth token --user <account>)" gh pr list -R <owner>/<repo> --state all --limit 5 --json title,body | grep -P '[\x{ac00}-\x{d7a3}]' | head -3
# Korean match → Korean default repository
# No match → English default or new repository
```

**Translation procedure** (subagent English output → Korean default repository):
- Translate body to Korean before posting (keep code blocks, identifiers, and file paths in their original form)
- Keep dual-label labels (`🔴 Critical`, `⚠️ Potential`, `🟡 Minor`, etc.) as-is since they are standard
- Technical terms (rename, slug, consumer_key, terraform apply, etc.) may remain in English within Korean context

**Self-check** (just before posting):
1. Which is dominant in the body, Korean or English?
2. Does it match the repository's default language?
3. If mismatched, translate immediately → re-run the self-check

**Forbidden pattern**: Copy-pasting subagent English output directly into a Korean default repository. Do not bypass with "technical reviews feel natural in English" reasoning.

### Inline auto-fire policy (no runtime ask)

When inline targets exist, the single reviews API POST carries them in `comments[]` so the author sees each finding on the exact line in the GitHub UI. **This fires automatically by the policy below — do NOT ask the user at runtime.**

**Auto-fire policy** (this decides the medium — see "Medium decision" above):

| Invocation | Inline targets |
|------------|----------------|
| Default (no flag) | Line-specific 🔴 Critical + 🟡 Important findings only |
| `--inline` flag on the consolidate call | ALL line-specific findings (Minor/Refactor included) |
| No line-specific finding matches the policy | No review POST — issue-comment medium |

**Fallback (diff-scope / line verification)**: a finding whose file is not in the PR diff, or whose line cannot be verified against PR head (`git show <head>:<path>`), is **demoted to review-body text only** — never force an inline comment for it (422 risk). No finding is dropped. If ALL inline candidates demote this way, the medium falls back to issue comment.

**Mechanics**: head SHA fetch, JSON payload format, `comments[]` fields, and verification follow `post.md` "Optional Inline Review" procedure (event = `COMMENT`). The `body` field of the same POST carries the full Internal Review findings (title template + strengths + findings + assessment).

| # | Don't | Do (correct alternative) |
|---|-------|-------------------------|
| 1 | Ask the user "post inline review?" at runtime | Apply the auto-fire policy table deterministically. The only user control is the `--inline` flag at invocation |
| 2 | Inline-annotate every finding by default | Default = Critical + Important line-specific only. ALL requires the explicit `--inline` flag |
| 3 | Force inline for a finding outside the PR diff | Demote to review-body text (fallback row above) |
| 4 | Put a stub/pointer body in the review POST and the full findings elsewhere | The review POST `body` IS the Internal Review — full findings live there |

### Mandatory self-check before entering Step 4 (HARD STOP — run on every invocation)

Step 4 may proceed only if both conditions below are satisfied:

1. **Verify posted-artifact URL**: per the medium — review medium: `gh api repos/{owner}/{repo}/pulls/{N}/reviews` contains this session's review (body starts with "## Internal Code Review"); comment medium: `gh api .../issues/{N}/comments` contains this session's comment.
2. **No self-reporting**: Reporting the classification result as text does not equal posting. **The review/comment must be visible on the PR page** to count as posted.

If unmet, **immediately return to Step 3.5.3** and post via the decided medium. After posting, print the URL → proceed to Step 4.

**Forbidden pattern**:
- Outputting only a classification table of code-reviewer results as text → jumping to the user with "scope of changes?" (Step 5 position)
- "Classification is clear, so skip posting the comment" reasoning
- "User will respond anyway, so post later" reasoning

### Review comment ≠ AI Review Summary (HARD STOP — 5 recurrences 2026-05-22)

The Internal Review is a Copilot substitute (detailed findings); the Summary is the overall reviewer consolidation (table). **Always post as 2 separate posts** — the Internal Review medium follows the "Medium decision" table above (review POST when inline targets exist / issue comment otherwise), while the Summary's medium (issue comment vs Formal Review body) is decided by `post.md` Step 7. The "single combined post" pattern (Internal Review inlined into the Summary body) is deprecated.

**Why always 2 posts**: At the Step 5 AskUserQuestion moment, the user must see the review content to decide. The "inline integration when posting Summary" pattern leaves no review medium present at ask time, preventing user decisions. The Internal Review is always posted first, independent of the Summary decision.

| Condition | Post count | Posting order |
|-----------|--------------|---------------|
| External AI review exists (Copilot/CodeRabbit Pro) + Internal fallback | 2 | Internal Review → Summary |
| **Internal fallback only (sole source)** | **2** (do not merge into 1) | Internal Review → Summary |
| External AI only without Internal Review | 1 | Summary only |

| # | Don't | Do (correct alternative) |
|---|-------|-------------------------|
| 1 | "Internal fallback is the sole source, so inline-merge into the Summary" reasoning | Post the Internal Review first → then post the Summary separately. Keep media separated |
| 2 | At Step 5 ask time, show review content only via chat text | Post the Internal Review on the GitHub PR right before Step 5 ask — its URL may be included in the ask option description |
| 3 | Step 4 → Step 5 direct jump (Step 3.5.3 posting omitted) | Strictly follow the order: Step 3.5.3 posting → Step 4 classification → Step 5 ask |

### Reviewer failure detection

In the reviews array, if a COMMENTED-state review's body contains text such as "encountered an error" or "unable to review", classify that reviewer as failed (e.g., bodyLen ~117 chars, "Copilot encountered an error and was unable to review this pull request").

**Variety of normal review formats (false positive caution)**:

Copilot review bodies are naturally posted in different formats depending on PR complexity. All of the following are recognized as normal reviews:

- **Detailed format**: "Pull request overview" + "Reviewed changes" section + file table + inline comments
- **Concise format**: "Pull request overview" + change summary + advertising link (simple PR with no actionables)
- **Inline-comment style**: Large bodyLen + `<details>Comments suppressed due to low confidence` section + 1+ inline comments

**Absence of `Reviewed changes` section ≠ partial failure**. Example of actual normal case (PR #110 merged): bodyLen 2040, hasReviewedChanges:false, "Comments suppressed" + 1 inline. Trust only explicit error keywords ("encountered an error", "unable to review") for partial failure detection.

This ensures PRs always get substantive review even when external AI tools provide limited feedback or are completely unavailable.

### Procedure violation prevention

Strictly enforce the order Step 3.5 → Step 4 → Step 5 → Step 7. Do not skip the review comment (Step 3.5.3) and jump to Step 5 (Summary approval). **Proceeding to post the Summary while the review comment is not yet posted on the PR = procedure violation.**

Include the posted review as the primary review source for Step 4 (`classify.md`). Reference with `code-reviewer` attribution in the AI Review Summary (Step 7, `post.md`).

## Step 4.5: UI Change PR Capture Verification (HARD STOP — reviewer's duty)

**The reviewer must classify a PR as an actionable item if it is a UI change PR with no capture attached.** When the author omits the capture-attachment duty, calling it out is part of the review.

### UI change detection

```bash
gh pr diff <N> -R <repo> --name-only | grep -E '\.(tsx|jsx|svelte|vue|css|scss)$|^(app|pages|routes)/'
```

If matched, it is a UI change PR — subject to capture-attachment verification.

### Capture absence check

```bash
# Search PR body + all comments for image/capture patterns
gh pr view <N> --json body,comments --jq '.body, (.comments[].body)' | grep -cE '!\[.*\]|<img |\.webp|\.png|\.gif|\.mp4'
```

If 0, capture is absent.

### Don't / Do table

| # | Don't | Do (correct alternative) |
|---|-------|-------------------------|
| 1 | Ignore UI change PR with capture absent → omit from Summary | Add `[REVIEW_FEEDBACK] Missing capture attachment — UI change PR must include at least one main screen image` to Step 4 actionable classification |
| 2 | "Reviewer can verify directly" reasoning | Preserve PR tracking value — visual change history must remain on the PR itself, not only at code-review time but also after PR archive |
| 3 | Reviewer generates and posts the capture themselves as a PR comment | Capture generation is the author's domain. The reviewer marks it as actionable to prompt follow-up by the author |
| 4 | Silent pass when code-workflow `--no-capture` opt-out was used | For UI change PRs, capture duty applies regardless of opt-out. Opt-out applies only to non-UI PRs |

### Application timing

Right after Step 4 Classify, before Step 5 Summary posting. If the classification result contains a "UI capture missing" actionable, include it in the Summary body so the author can follow up with attachment.

Detailed rule: see `skills/github-flow/pr.md` Step 8 "UI Change PR — MANDATORY" section (in this repo; installed locally as `~/.claude/skills/github-flow/pr.md`).

## Next

→ Internal Code Review comment posted + UI capture actionable verified → `classify.md` (Step 4 Analyze and Classify)
