# Collect AI Reviews

Collect AI reviews (CodeRabbit, Copilot, etc.) posted on the PR and load the verify→evaluate→respond framework.

Entry: `Skill("consolidate", "collect ...")` or `pr.md` Workflow Step 3.

## Step 3: Collect AI Reviews

```bash
# PR review comments (inline)
gh api repos/{owner}/{repo}/pulls/{number}/comments

# PR issue comments (summary)
gh pr view <NUMBER> --comments --json comments
```

Identify reviews from:
- `coderabbitai[bot]` — CodeRabbit
- `copilot[bot]` — GitHub Copilot
- Other bots with `[bot]` suffix
- **Human MEMBER/OWNER reviews and review-shaped comments (HARD STOP)** — enumerate every `reviews[]` entry whose `author.is_bot == false`, plus every `comments[]` entry whose `authorAssociation` is `MEMBER`/`OWNER`/`COLLABORATOR` AND whose body contains a review-style header (Code Review headers, `### Findings`, `### Issues`, `Critical`, `Important`, `Should fix`, `Must fix`, localized equivalents in any language). Each such reviewer (login) is a distinct **Source** that must be carried forward into the findings table — do not collapse them under "Internal Code Review". Query: `gh pr view <N> --json reviews,comments --jq '[.reviews[] | select(.author.is_bot==false) | {kind:"review", login:.author.login, body}] + [.comments[] | select(.authorAssociation == "MEMBER" or .authorAssociation == "OWNER" or .authorAssociation == "COLLABORATOR") | {kind:"comment", login:.author.login, body}]'`. Cross-check returned bodies for review-style headers before declaring a `comment` entry a review source.

### Source-Specific Handling

All AI reviewers are **external reviewers** — treat their suggestions as proposals to evaluate, not orders to follow.

| Reviewer | Strengths | Watch out |
|----------|-----------|-----------|
| **CodeRabbit** | Full codebase context, walkthrough, security checks | Can suggest over-engineering; may not understand project conventions |
| **Copilot** | Inline code suggestions, style consistency | May miss cross-file context; suggestions can break other callers |

Before accepting any suggestion:
1. Check: Technically correct for THIS codebase?
2. Check: Breaks existing functionality or callers?
3. Check: Reason for current implementation? (grep for usage)
4. Check: Works on all platforms/environments?
5. Check: Conflicts with user's prior architectural decisions?

## Step 3.6: Invoke superpowers:receiving-code-review

**MANDATORY**: Before analyzing, invoke the review-receiving skill to load the verification framework:

```text
Skill("superpowers:receiving-code-review")
```

This loads the verify→evaluate→respond protocol. Follow it for every feedback item in Step 4 (classify).

**Abort if unavailable (HARD STOP)**: If the `Skill("superpowers:receiving-code-review")` call fails or the skill does not exist, **immediately abort the consolidate procedure**. Report to the user "Cannot use the `superpowers:receiving-code-review` skill; aborting consolidate" and terminate. Analyzing reviews without the verify→evaluate→respond framework risks blind acceptance, so alternative continuation is prohibited.

## Next

→ If the external AI review is walkthrough only / in a failure state, go to `internal.md` (Step 3.5 Internal Review Fallback)
→ Otherwise, go to `classify.md` (Step 4 Analyze and Classify)
