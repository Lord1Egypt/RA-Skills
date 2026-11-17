<!-- Adapted from caldoai/skills untangle-codebase (MIT, Copyright (c) 2026 Maze). -->

# Untangle: the structural fix

Read this for `/audit --untangle [area or ticket]`, or when step 6 of `SKILL.md` routes a structural ticket here. Untangle refactors until pieces that change together sit together, so agents working in the code read less per change, break less without noticing, and find root causes faster.

Treat it as a goal: start the refactor and complete it to the end.

When started from an audit-map ticket or `.audit/HANDOFF.md`, read it first: its fix and findings are the starting list, and its done line is part of yours.

## 1. Ask

Besides untangling, there are two other things you may do:

| Addition | What it does |
|---|---|
| Comments | Remove comments that only restate the code. |
| Tests | Remove tests that wouldn't catch a real bug, and fix the ones that fail without one. |

List these (with their exact descriptions) and ask which to do, both preselected. If the user has already said, or the session runs without interruptions, take both. Then do only those.

## 2. Baseline

Change nothing yet.

- Reuse the audit's `SCAN.md` and `RECON.md`, or run step 2 of `SKILL.md` to produce them: they hold the stack, the commands, the house rules and the hot spots.
- Run the build, the linter and the full suite, and record the results. Tests failing now are listed, and are yours to fix only if the redesign fixes them.
- Record `python3 scripts/scan.py <path> --special` and `scripts/cochange.sh` in the decision log. Rerun both at the end; the difference is your progress.
- Script an import graph (for example `madge` for JS/TS, `pydeps` or `import-linter` for Python, `go list -deps`, `cargo modules`, a grep over `import` lines for Swift, Kotlin or Dart). Keep the script and rerun it as you go.
- For every path the redesign will touch that no test exercises, write a characterization test through its public interface first. This is the net that lets step 5 claim behavior is unchanged.

## 3. List every problem

Change nothing yet.

Start from `REPORT.md`'s `structural` fixes and the `design` findings, if an audit ran. Then go through the code with `lenses/design.md`: its one question, **should these pieces change together?**, and every probe under it. Write down every place the code gets the answer wrong, as in the decision log example. Each special case is a requirement the design never accounted for, so use them to work out what the system needs to be.

## 4. Redesign from first principles

Work out the fixes as if the system had known today's requirements from the start. Look for the one fix behind several problems, which often looks nothing like them; special cases are fixed by the design that makes them unnecessary, never one by one.

Ask the same thing of every fix, even one that looks better in the code: pieces that change together end up together, pieces that don't aren't tied, and everything depends on what changes less. Write each fix above the problems it solves, in the deep-module vocabulary.

When a fix has competing interface designs, design it twice (`codebase-design`'s design-it-twice pattern) and pick by depth, locality and seam placement. When a fix needs a decision that is the user's (it contradicts an ADR, renames a domain concept, or accepts a risk), resolve it with `grill-with-docs` before you build it. Where those skills are unavailable, do the same steps inline.

## 5. Fix everything on the list

One fix at a time, highest leverage first. After each fix the build and the full suite are green, and the fix is its own commit, so any regression bisects to one decision. New behavior goes test-first at the module's interface (`tdd`). A wide refactor whose blast radius breaks every caller at once goes expand–contract: add the new form beside the old, migrate callers in green batches, then delete the old form.

Remove the special cases the redesign makes unnecessary, and keep the ones the system still needs; before removing one, find why it was added (`git log -L`, blame, the PR). Bugs fixed along the way are welcome: record each in the log as a behavior change.

- **Comments** chosen: apply the `comments` probe in `lenses/design.md`.
- **Tests** chosen: do this last, since tests are the safety net. Give every test a class and act on it, per the `classify` probe in `lenses/tests.md`. Keep the characterization tests unless a behavior test now covers the same path.

## 6. Check, and repeat until done

Run `lenses/design.md` again over the changed code (in subagents, or yourself when the scan plans a sequential run), with the decision log so settled items stay settled. Repeat until nothing worth fixing is left.

Done when:

- As few special cases remain as possible: count them in the log's special-case list, and compare `scan.py --special` (a regex floor) against the baseline.
- A typical change lands in one place: `cochange.sh` pairs across folders are gone or explained.
- Every import is reasonable, and nothing imports anything more volatile than itself.
- The design re-check finds nothing worth fixing.
- Intended behavior is unchanged apart from bugs the refactor fixed: the baseline suite and characterization tests pass, and every behavior change is in the log.
- From an audit ticket: the ticket is resolved with its answer, the map's Decisions so far has its line, and `HANDOFF.md` names the next frontier ticket, as `DELIVER.md` describes.

## Tips

- **Start from a skeleton**: script away function bodies, so the whole codebase fits in context.
- **Summarize with subagents**: have them summarize parts of the codebase, so you can reason across all of it.
- **Enter where leverage is highest**: the hot spots and the largest `cochange.sh` clusters.
- **Keep the decision log** at `.audit/untangle-log.md`, so compaction loses less. When the redesign outgrows one session, chart the remaining decisions with `wayfinder`.
- **Use Git as evidence**: for how often pieces change, and what changes together.

## Decision log example

The list of problems:

```
- `ui/LogoutDialog.tsx:30` waits 100ms after closing and hopes the message input can take focus by then.
- `ui/Toolbar.tsx:40` and `ui/Menu.tsx:22` call the same actions, each with its own check for when they're disabled.
- `checkout/submit.ts:9` depends directly on `payments/stripe.ts`.
- `shortcuts/keymap.ts:18` has a switch with one case per action, separate from the menu's list.
- `ui/CommandPalette.tsx:55` keeps its own list of actions, and it's missing the newer ones.
- `ui/SettingsDialog.tsx:61` sets a global `skipRefocus` flag to stop the logout dialog it opens from sending focus to the message input.
- `history/undo.ts:30` has a special case for every action that can be undone.
- `refunds/refund.ts:22` wraps every Stripe call in `if (order.provider === "paypal")`.
- Every action handler has to call `track()` by hand, and some don't.
- `ui/Toolbar.test.tsx` and `ui/Menu.test.tsx` test the same actions separately.
```

Then with the fixes:

```
- Make the general `Dialog` give focus back to whatever had it before it opened, so the wait and the flag can both go.
  - `ui/LogoutDialog.tsx:30` waits 100ms after closing and hopes the message input can take focus by then.
  - `ui/SettingsDialog.tsx:61` sets a global `skipRefocus` flag to stop the logout dialog it opens from sending focus to the message input.
- Define a `PaymentProvider` interface that Stripe and PayPal both implement, so checkout and refunds no longer know which one they're using.
  - `checkout/submit.ts:9` depends directly on `payments/stripe.ts`.
  - `refunds/refund.ts:22` wraps every Stripe call in `if (order.provider === "paypal")`.
- Make every user action a command with a name, a handler and an undo, so the toolbar, menu, shortcuts, palette and undo history all run from one list.
  - `ui/Toolbar.tsx:40` and `ui/Menu.tsx:22` call the same actions, each with its own check for when they're disabled.
  - `shortcuts/keymap.ts:18` has a switch with one case per action, separate from the menu's list.
  - `ui/CommandPalette.tsx:55` keeps its own list of actions, and it's missing the newer ones.
  - `history/undo.ts:30` has a special case for every action that can be undone.
  - Every action handler has to call `track()` by hand, and some don't.
  - `ui/Toolbar.test.tsx` and `ui/Menu.test.tsx` test the same actions separately.
```
