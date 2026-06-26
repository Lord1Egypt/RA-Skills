# Phase 2 — Coder Checklist

Use this while applying a change. Tick boxes as you go.

---

## Before You Start Editing

- [ ] Phase 1 is complete (hypothesis + scope + success criteria all written)
- [ ] You can state the **one** change you are about to make in one sentence
- [ ] You know which files will be touched, and they match the Phase 1 scope

## While Editing

- [ ] **One fix at a time** — a single logical change that proves/disproves the hypothesis
- [ ] **Full files** — prepared to show complete file contents, not snippets
- [ ] **No speculative refactors** — resist "while I'm here"
- [ ] **Scope held** — not opening files outside the Phase 1 scope

## Mid-Edit Stop Conditions

STOP editing and return to Phase 1 if you notice:

- [ ] The hypothesis doesn't match what the code actually does
- [ ] You need to edit a file that wasn't in Phase 1 scope
- [ ] The fix requires a deeper architectural change
- [ ] You don't actually understand why the current code looks the way it does

Each of these means Phase 1 was wrong. Cheaper to rewrite the hypothesis than patch through uncertainty.

## Scope Creep Warning Signs

- [ ] Adding imports for libraries Phase 1 didn't plan
- [ ] Modifying tests to make the build pass (instead of making tests pass by fixing code)
- [ ] Running `grep` / `find` to "explore" — that was Phase 1's job
- [ ] Cleaning up unrelated code in the same file
- [ ] Renaming things "while I'm here"

If any of these happen: STOP, revert the creep, return to Phase 1.

## Exit to Phase 3

Before you move to Validator, confirm:

- [ ] Exactly one logical change is applied
- [ ] Diff contains only the intended work
- [ ] No unrelated edits in the diff
- [ ] Full files are available for review
- [ ] You can point at the diff and say which line tests the Phase 1 hypothesis

Otherwise: revert the speculative parts, narrow the diff, try again.
