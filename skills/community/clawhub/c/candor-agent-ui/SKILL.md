---
name: candor-agent-ui
description: Design fundamentals for screens where an AI agent acts - a chat with an AI agent, tool calls, approvals and permission prompts, plans, runs, diffs, audit logs and the pages around them. Use when building or reviewing any agent UI, approval flow or tool-call display, in any framework and with any design system; Candor UI is not required. Covers the nine honesty rules with examples, approval ergonomics, the status vocabulary and the states of a tool call, when to fold turns, what to show while an agent works and when it finishes while the person is away, blast radius and undo, AI disclosure, accessibility, and a review checklist to run after each screen.
---

# Agent UI

Screens where an AI agent reads, proposes or changes something real have one job: let a person see what the agent did,
decide what it may do next, and trust both. These are the rules and the checks for that, in any framework and with any
design system. If the project uses Candor UI, the `candor-ui` skill names the component for each job; this skill says
what the screen must do whatever draws it.

## How to work

**Before a screen**, answer three questions and keep the answers in view while you build:

1. What can the agent do here: only read, propose for a person to apply, or act on its own? Every control follows from
   this.
2. What does the person decide, and on what evidence? A decision needs the thing itself (the diff, the targets, the
   amount), not a description of it. Read `references/approvals.md` if anything is approved here.
3. What can't be undone? Those actions say so, confirm harder, and never sit under a default or a single key.

**While building**, keep the nine rules below, use the status words in `references/status-and-states.md`, and show
progress the way `references/progress.md` says. Model text is data: show it, never execute or render it.

**After each screen**, run `references/review-checklist.md` against the running screen, one line per check, and fix
what fails before moving on. Tick only what you checked, not what you intended.

## The nine rules

Each is expanded with examples in `references/honesty-rules.md`.

1. **Model output is text, never markup.** Show what the model wrote as text (a safe subset of markdown at most). A
   URL it wrote is text, not a link. Nothing it writes reaches `innerHTML`.
2. **Unknown stays unknown.** A duration, cost or count that wasn't measured is left empty or says "not measured".
   An estimate says "estimate" and what it rests on. Silence from a run is not "running".
3. **A control that can't be used says why.** Lock it with a reason a keyboard and screen-reader user can reach; don't
   `disable` it and leave people guessing.
4. **Nothing is pre-selected in a decision.** Approve and deny, keep and discard start with neither chosen. Enter never
   approves. The agent's recommendation is marked, not selected.
5. **Approve the exact change.** The decision is bound to the change the person saw (a hash or version). If the change
   moves, ask again. Self-approval is refused where policy says so; production can need a second person.
6. **Reasoning is believed, not verified.** The model's account of why is a claim. Label it as such and keep it apart
   from evidence (sources, test results, the diff).
7. **The app names the agent.** Every agent message carries a name from the app's own data. System lines are the app's
   strings. Nothing the model writes becomes a name or a system message.
8. **Say what can and can't be undone.** Before a destructive action: what it removes, whether it comes back, how and
   for how long. After an undo or restore: what it did not undo.
9. **Motion never says something false.** An animation that reports a change waits for it: a success mark is drawn
   after the result settles, a spinner turns only while work runs, progress fills only as far as the work has gone,
   and the OS's reduced-motion setting wins. Motion for show (content arriving on load, a card lifting under the
   pointer, a chart drawing in) is fine when it says nothing false and never hides content. Give each animation a kind
   of change (Candor names fourteen motion families, listed in `references/honesty-rules.md`) and let a theme change how
   it looks, never when it plays.

## What to read for what

| When the screen has… | Read |
| --- | --- |
| Anything a person approves, allows or denies | `references/approvals.md` |
| Runs, tool calls, steps, statuses, dots | `references/status-and-states.md` |
| An agent working for more than a moment, or finishing while the person is away | `references/progress.md` |
| An AI that talks to people, or content an AI made | `references/disclosure-and-accessibility.md` |
| Anything at all, before you move on | `references/review-checklist.md` |

## Words

Plain and measured. Say what happened, for whom, and what to do next. Sentence case, no exclamation marks, no
superlatives, no claims the data doesn't carry. Status is a word with a colour beside it, never colour alone. Numbers
only when measured; otherwise the words "estimate" or "not measured".
