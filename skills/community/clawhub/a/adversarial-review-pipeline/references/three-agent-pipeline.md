# The Three-Agent Pipeline

Writer -> Breaker -> Reviewer. The classic adversarial shape.

## Tier 2 — Three-agent pipeline (Writer → Breaker → Reviewer)

The classic shape. Use it when your environment supports subagents and the
change is large enough to justify the coordination cost. It is **not** the
default, and a single-agent Tier 1 review is a legitimate choice for most
changes.

```
Writer  ->  Breaker  ->  Reviewer  ->  Human
 (code)     (findings)   (verdict)    (decide)
```

| Role | Job | Writes |
|---|---|---|
| **Writer** | Implements the change | the code |
| **Breaker** | Finds problems. Never writes fixes. | `breaker-<slug>.md` |
| **Reviewer** | Reconciles and produces a verdict | `review-<slug>.md` |

**Each role sees a different slice, and that is the point:**

- The **Writer** sees only the requirement.
- The **Breaker** sees only the Writer's output - never the Writer's
  reasoning. That isolation is what makes it adversarial.
- The **Reviewer** sees both the artifact and the findings, and reconciles
  them into a verdict.

### The Writer prompt

```text
Implement <the task>.

Scope the change first: list every place it must reach, and find every
caller of anything you change. That list is the scope - extra features are
not.

Then take the smallest complete change, in this order:
1. Does it need to exist at all? Skip anything nobody asked for and name it
   in one line.
2. Does the codebase already have a component for this? Use it the way the
   surrounding code does.
3. Standard library or platform feature? Use it, unless the project has
   its own.
4. Installed dependency? Use it. Do not add a dependency for a few lines.
5. One line a reader gets at a glance? One line.
6. Otherwise, the minimum code that works.

Deletion beats addition. Keep the codebase's own layers, interfaces, and
conventions. No wrapper, option, config, or "for later" code nobody asked
for.

Be lazy about the solution, never about the change: finish every part the
task needs, including the callers, tests, and fixtures the change breaks.

Validation at trust boundaries, error handling that prevents data loss,
security, accessibility, and anything explicitly requested are never cut.

Also update the project docs the change makes wrong - README.md, AGENTS.md,
docs/*, .agents/*, the rulebook tracker, module lists, architecture notes.
Update them whenever the change affects public interfaces, workflows, or
project state. The test is not "did you touch a doc" but "is any doc now
wrong": grep for the thing you changed and see what still claims the old
behavior. Name the docs you updated.
```

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

### The docs are part of the change

**The Writer owns the project docs the change makes wrong, and the Breaker
checks them.** A branch that changes how the project works and leaves the
docs describing the old behavior is an incomplete branch - and it is the kind
of incompleteness that survives review, because a reader of the diff sees
code, not the doc that contradicts it.

Update these whenever the change affects public interfaces, workflows, or
project state:

- `README.md`
- `AGENTS.md`
- `docs/*`
- `.agents/*`
- the rulebook tracker
- module lists
- architecture notes

The check is the same on both sides:

```bash
grep -rn "<the thing that changed>" README.md AGENTS.md docs/ .agents/ 2>/dev/null
```

Every hit that still describes the **old** behavior is a finding. The
severity depends on what the doc governs:

| The stale doc governs | Severity |
|---|---|
| setup, install, how to run it, a public interface | `high` - a reader will get it wrong |
| an internal workflow, module list, architecture note | `medium` - it misleads the next person to change it |
| a tracker row that no longer matches reality | `medium` |

A doc describing behavior the change did **not** touch is not a finding. The
point is accuracy, not coverage.

### The Reviewer prompt

The Reviewer reconciles. Critically, it does **not** rubber-stamp the
Breaker - if the Breaker found nothing, the Reviewer verifies independently.

```text
Review the change at <path-to-diff-or-branch> and the findings at
<path>/breaker-<slug>.md.

- If the Breaker found issues: assess severity and propose fixes
- If the Breaker found nothing: verify independently. Do not trust the
  Breaker either.
- Review the `## YAGNI & DRY Review` section: is the speculative code or the
  duplication worth the complexity? Recommend removal, extraction, or accept
  with a rationale.
- Check every finding against the code before accepting it. A finding that
  does not hold up should be dropped, with the reason.

Produce a final verdict: ACCEPT / ACCEPT WITH FIXES / BROKEN / REJECT.

  - ACCEPT: ready to ship
  - ACCEPT WITH FIXES: apply the listed fixes, then ready to ship
  - BROKEN: needs more work. A Fixer applies the fixes and the branch goes
    back through the Breaker and Reviewer
  - REJECT: we will not accept this change for the stated reasons. Stop and
    escalate to a human

Do NOT merge the branch. Your output is a verdict document only.

Output: write the verdict to <path>/review-<slug>.md
```

### BROKEN is a loop, REJECT is a stop

These two verdicts do very different things, and conflating them is how a
pipeline stalls.

| Verdict | What happens next | Interrupts the pipeline? |
|---|---|---|
| `ACCEPT` | the review is done and the report is ready for the human decision | no |
| `ACCEPT WITH FIXES` | apply the listed fixes, then the report is ready for the human decision | no |
| `BROKEN` | a Fixer applies all the fixes, then the branch goes back through the Breaker and Reviewer | no |
| `REJECT` | stop and report why | **yes** |

**No verdict ships anything on its own.** Every one of them ends in a report
that a human reads and acts on - the Reviewer recommends, a human decides.
The difference between the verdicts is only *how much more work happens
before* that report reaches the human.

**BROKEN means "this needs more work," not "this is finished and wrong."** A
branch that comes back `BROKEN` is normal pipeline traffic: the Fixer
addresses the findings and the branch re-enters the loop at the Breaker. The
person running the pipeline is not interrupted for it, because the loop is
doing the work the human would otherwise have to request.

**REJECT is the stop signal.** It means the change will not be accepted as
written, for the reasons the Reviewer gave. Escalate that one.

Every verdict ends at the same place: a report a human reads. The internal
fix-and-recheck rounds happen first, on their own, so the person reading the
report is looking at the best version of the change rather than the first
draft of it. The shipping decision is theirs alone, and the pipeline does not
make it.

### The verdict is not the decision

The Reviewer produces a recommendation. A human decides. Report back with:

- **What was written** - the change itself
- **What the Breaker found** - count by severity
- **What the Reviewer recommends** - the verdict and any unresolved concerns
- **Your confidence** - and anything you could not verify

Keep the report to what changes what the reader does. Do not narrate the
agents or the steps.

### Cost, and when it is not worth it

The three-agent pipeline costs roughly three times a single-agent review. If a
Tier 1 review finds nothing and the change is not on a risky path, you have
already spent the budget. Do not run the pipeline to feel thorough.

The combined tier table is at the end of Tier 3.

---
