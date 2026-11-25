# The Five-Agent Pipeline

Writer -> Breaker -> Fixer -> Spec Writer -> Live Tester. For user-facing features where browser-only bugs matter.

## Tier 3 — Five-agent pipeline (Writer → Breaker → Fixer → Spec Writer → Live Tester)

Use this for user-facing features with forms, redirects, auth flows, or
multi-step wizards. It is the three-agent pipeline plus a fix loop and
browser verification, which is what catches the class of bug that unit
tests structurally cannot.

```
Writer -> Breaker -> Fixer -> Spec Writer -> Live Tester
```

| Role | Job | Writes |
|---|---|---|
| **Writer** | Implements the change | the code |
| **Breaker** | Finds problems. Never writes fixes. | `breaker-<slug>.md` |
| **Fixer** | Applies fixes from the Breaker's findings | `fixer-<slug>.md` |
| **Spec Writer** | Writes tests from the user's perspective | `spec/...` + `spec-writer-<slug>.md` |
| **Live Tester** | Exercises the change in a real browser/app | - |

The Breaker and the Fixer are deliberately **separate agents**. Two reasons:

1. **Different postures.** A model in adversarial mode is good at finding
   problems and bad at writing fixes - it stays in "find what's wrong" mode.
2. **Self-rationalization.** When the same agent finds and fixes, it can
   explain away its own findings. A separate Fixer treats the findings as
   input, not as something to argue with.

### The Breaker prompt

Give the Breaker the artifact, not the author's reasoning, and tell it
explicitly not to fix anything:

```text
Review the change at <path-to-diff-or-branch>. Your ONLY job is to find
problems.

- Run the tests
- Check edge cases, empty states, and boundary values
- Look for security issues: authorization, injection, IDOR, secrets in logs
- Identify logic errors
- Question the assumptions
- YAGNI: flag speculative generality, unused abstractions, or features the
  task does not exercise
- DRY: flag duplicated logic, duplicated domain concepts, duplicated
  validation
- REINVENTION: flag a new helper/service/constant built when the codebase
  already has one - name the existing one to use
- UNNECESSARY INDIRECTION: flag a dependency, wrapper, or conversion layer
  replaceable by the standard library or a few lines
- DOCS: check that the project docs were updated to match the change -
  README.md, AGENTS.md, docs/*, .agents/*, the rulebook tracker, module lists,
  architecture notes. Grep for what changed and flag any doc that still
  describes the old behavior. A doc describing behavior the change did not
  touch is not a finding.

Do NOT suggest fixes. Just report what's broken.

Output: write findings to <path>/breaker-<slug>.md with severity labels
(block-merge / high / medium / low), a `## YAGNI & DRY Review` section, and
end with a `## Scope & Skipped` section.
```

### The Fixer prompt

The Fixer runs on two verdicts, and the verdict decides what happens next.

- `ACCEPT WITH FIXES` - apply the fixes the Reviewer listed.
- `BROKEN` - apply everything needed to address the Breaker's findings and
  the Reviewer's rationale. **The branch then goes back through the Breaker
  and the Reviewer.** That is the normal path for a `BROKEN` verdict, not an
  escalation.

```text
Apply the required fixes from the findings at <path>/breaker-<slug>.md.

- Fix all block-merge and high findings
- Fix medium findings when it is safe to do so
- Defer low findings that need a product decision - list them, do not guess
- For YAGNI findings: remove the speculative code unless a real user journey
  needs it
- For DRY findings: extract only if the extraction is simpler than the
  duplication. Never introduce a harder abstraction to satisfy DRY
- For REINVENTION findings: delete the new implementation and use the
  existing one named in the finding
- For UNNECESSARY INDIRECTION findings: remove the dependency or wrapper
- For DOCS findings: update the project docs the change made wrong -
  README.md, AGENTS.md, docs/*, .agents/*, the rulebook tracker, module
  lists, architecture notes. The same grep that found the stale doc confirms
  the fix.

Run the tests after each fix group. Do not commit until they pass.
Do not push. Do not merge.

Output: write a summary to <path>/fixer-<slug>.md
```

If a fix breaks a previously-passing test, the Fixer reconciles it - not the
Breaker.

### Opening the PR

**A PR is opened only after the review comes back `ACCEPT`** (or
`ACCEPT WITH FIXES` with every fix applied and the tests green). Never open a
PR for unfinished work.

A PR is a claim that the work is complete. A branch carrying unresolved
Breaker findings, unapplied Fixer work, or a `BROKEN` verdict does not support
that claim, and a PR opened on it produces CI results for code that is about
to change, review comments attached to a diff that no longer exists, and no
way to tell which version was approved.

Use the project's own PR template if it has one. Fill out every section
before opening it.

**Verify the docs before creating the PR.** A PR that ships code whose docs
still describe the old behavior makes the wrong thing look right to the next
person.

```bash
grep -rn "<the thing that changed>" README.md AGENTS.md docs/ .agents/ 2>/dev/null
```

If any hit still describes the **old** behavior, the docs are missing. Two
options, and only two:

1. **Route back to the Fixer** to update the docs, then re-run the Breaker
   check on the updated branch.
2. **Update the docs in the main session** when the fix is small and obvious
   enough that spawning a Fixer would cost more than doing it.

Either way the PR does not open until the stale hits are gone. Do not open a
PR with a known-stale doc and note it for later - "I'll fix the docs in a
follow-up" is how the next person reads the wrong thing.

**Only the agent that owns the final push opens the PR.** In this tier that is
the Live Tester - it is last, and the PR head is the version that was driven
in a real browser. If the Fixer's work breaks a previously-passing test, the
Live Tester has to go back and confirm the fix, so the PR opens against a
verified head.

Opening the PR is not the decision to ship. The PR waits for a human to
review and merge it; opening it only makes the reviewed work visible for
that review.

### Ordering

Run the roles **sequentially**. Do not spawn the next role until the previous
one reports back.

```
Writer -> Breaker -> Fixer -> Spec Writer -> Live Tester
```

Spawning them in parallel wastes work: the Fixer needs the Breaker's findings,
and the Spec Writer needs the fixes to write tests against.

**Check for a still-running duplicate before spawning.** If a spawn was retried
after a transient error, two copies of the same role can run concurrently and
write conflicting files.

### Choosing the tier

| Change | Tier |
|---|---|
| User-facing feature: forms, redirects, auth flows, multi-step wizards | Tier 3 if available, else Tier 2, else Tier 1 |
| Large feature, many files, many interacting callers | Tier 2 if available, else Tier 1 |
| A change that touches money, state transitions, or webhooks | Tier 2 or 3, plus the money checklist |
| Backend only: migrations, services, internal APIs | Tier 1 |
| Config, dependencies, docs | Tier 1, and often a read-through is enough |

---
