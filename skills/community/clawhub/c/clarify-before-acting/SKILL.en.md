---
name: clarify-before-acting
slug: yumingtao-clarify-before-acting
displayName: Clarify Before Acting
version: 1.3.0
summary: Resolve direction-changing ambiguity before acting on complex or high-cost requests.
license: MIT
description: >
  Before acting on a complex, ambiguous, or high-cost request, resolve direction-changing ambiguity first: do your own homework, check memory for questions already answered, work a question queue one item at a time, and never guess where direction is at stake. Skips trivial, mechanical, low-risk tasks. Triggers on "clarify before acting", "ask before doing", "确认需求", "先澄清再做", "方向不确定".
---

# Clarify Before Acting

Before acting on a non-trivial request, make sure you understand the *direction* of what's wanted — then act. The goal is a clear direction, not exhaustive detail.

## Contents

1. Quick Decision: Ask or Proceed?
2. When this applies (with trigger examples)
3. Do your homework first
4. Find the weakest spot
5. Work a question queue
6. Ask well
7. Know when to stop
8. When you proceed on assumptions
9. Close with a task contract when execution needs it
10. Out of Scope / Exception Quick Reference / FAQ / Language Support

## Quick Decision: Ask or Proceed?

| Decision | Action |
|----------|--------|
| ✅ Proceed directly | Trivial edits, low-risk file ops, reversible actions, user gave clear direction |
| ❓ Ask first | Affects >1 module, irreversible (deletes, force pushes), ambiguous requirements, redo cost clearly exceeding investigation cost (default reference: about 5 minutes of work, scaled to task size) |
| 🛑 Must ask | Direction-changing unknowns (see "Find the weakest spot") |

## When this applies

Engage when the request is complex, ambiguous, or costly to get wrong: architecture, requirements, schema or data changes, irreversible actions, or anything where "that's not what I meant" would waste real work.

Skip it for clear, mechanical, low-risk tasks — formatting, renaming, a single translation, or any request that already names the file, symbol, or acceptance test. When unsure, do one quick check, not an interrogation. This rule is a scalpel, not a tollgate.

Trigger examples:

- "Help me optimize the orders service." — Goal, success criteria, and scope are all unspecified.
- "Refactor the user module, and handle the performance too." — Two directional goals merged into one request; scope unknown.
- "Should we remove the caching layer?" — A directional architecture decision; clarify motivation and constraints before acting.

## Do your homework first

Answer everything you can from what is already available — the codebase, the docs, the request itself — before asking the human. Never ask what the code or context already tells you. When you do ask, cite the evidence that prompted the question (a file, a symbol, an observed pattern) so the person does not have to rediscover it.

**Check memory before re-asking.** If your platform offers memory or past-session recall, look there before posing a question. A question this user already answered — here or in an earlier session — must not be asked again: reuse the recorded answer, say you are doing so, and move on. Memory reduces the queue; it never silences a genuinely new direction-changing unknown.

## Find the weakest spot

Hold these four as a checklist and aim each question at whichever is least clear:

- **Goal** — what should actually happen, stated in one sentence with no "and/or".
- **Constraints** — boundaries, non-goals, explicitly excluded scope.
- **Success** — how you'll both know it worked; what a test would assert.
- **Context** — the change to an existing system; how this fits what's already there.

## Work a question queue

After homework and memory, whatever direction-changing unknowns remain go into an explicit queue — not into a guess:

1. **List** every open direction-changing unknown as one short question (typically 1–4). Three or more: show the numbered list so the person sees the shape of the conversation ahead.
2. **Order** by impact on direction — the question whose wrong answer would waste the most work goes first.
3. **Ask one at a time.** Ask the top question, listen, and reflect the answer back in one line. Only when that unknown is resolved does the next question go out. Never batch the queue into one message.
4. **Update the queue as answers land.** An answer may open a new unknown (add it) or void a queued question (drop it). Re-order and continue.
5. **The queue, not patience, decides when you act.** Work through it until no item remains; then act or write the task contract.

## Ask well

- One question at a time, drawn from the top of the queue. Let each answer shape the next.
- Probe assumptions, not feature lists. Ask "what are you assuming?" more often than "what do you want?".
- Sketch the scope's pieces before drilling into one, so depth on the loudest part does not hide a forgotten sibling.

## Know when to stop

Stop and act when the queue is empty — no remaining unknown would change the *direction* of the work (a different goal, owner, shape, or approach). Detail the person can correct later is not a reason to keep asking. Do not invent a numeric "confidence" score; the test is directional, not arithmetic.

Respect an explicit stop: only an unambiguous "stop asking — just do it" ends the questioning. Stop immediately, but state plainly what is still unclear and the risk of proceeding.

A pace complaint is not a stop. "You ask too much" or "hurry up" is feedback on *form*, not permission to skip: keep asking every direction-changing unknown, one at a time, each fully resolved before the next — just make each question shorter and better aimed. The queue shrinks by answers, never by impatience.

## When you proceed on assumptions

A direction-changing unknown is a reason to ask, not a license to guess. Fill it with an assumption only when the person explicitly stopped the questioning (an unambiguous "stop asking, just do it" — a pace complaint is not this), or the unknown is reversible detail that cannot change direction. For each assumption you then carry: what you assumed, why, and what breaks if you are wrong.

## Close with a task contract when execution needs it

When the clarified request will be handed to an executor, or when execution depends on an unresolved assumption, close with a concise task contract. This is not a rewrite of the user's prompt or an implementation plan; it is the shared definition of the result and its boundaries:

- **Result** — what must be true when the task is done.
- **Scope** — what's included and what's explicitly excluded.
- **Checkpoints** — ordered evidence that proves the result was achieved.
- **Stop conditions** — what should trigger a pause and re-asking.
- **Assumptions** — assumptions carried and the risk if they're wrong.

A ready-to-copy template (extended guidance and a filled example: [`references/playbook.en.md`](references/playbook.en.md) Section 9):

```text
Result:      {the outcome that must be true when the task is done}
Scope:       {what is included; what is explicitly out of scope}
Checkpoints: {the ordered evidence that proves the result was achieved}
Stop if:     {a change in goal, scope, owner, data, or approach requires review}
Assumptions: {what is assumed, on what basis, and the risk if it is wrong}
```

Skip the contract for clear, mechanical work that already names its file, symbol, or acceptance test. Keep it proportional; it is an execution handoff, not a mandatory questionnaire.

---

*Extended guidance — questioning lenses, patterns, scope mapping, and examples — lives in [`references/playbook.en.md`](references/playbook.en.md). Read it when a task is hard enough to need it; the rule above is enough for everyday use.*

## Out of Scope

This skill does **not** apply when:

- The request is trivial, mechanical, or low-risk (formatting, renaming, translation, single-file edits with clear intent).
- The direction is already unambiguous and testable.
- The user explicitly says "just do it" and the remaining unknowns are detail-level, not direction-changing — in that case proceed with stated assumptions.
- The task requires domain expertise the agent cannot verify internally; surface that as a known unknown rather than guessing.

## Exception Quick Reference

| Code | Scenario | Action |
|------|----------|--------|
| CBA-E01 | User stays silent on a directional question | Never silently fill: re-ask more concisely, or clearly state the risk and request a one-word confirmation |
| CBA-E02 | User explicitly stops the questions (an unambiguous "stop asking, just do it") | Stop asking immediately; convert each remaining unknown into a stated assumption with risk, say what remains unclear, and proceed |
| CBA-E03 | Pace complaints ("you ask too much", "hurry up") | Not a stop signal: keep the queue members unchanged and keep asking each directional unknown, but make the questions shorter and sharper |
| CBA-E04 | Direction still unknown after homework and memory checks | Do not act on a vague direction: list the remaining directional unknowns and ask one by one; if still blocked, ask the other party to decide between explicit options |

## FAQ

**Q: How many questions is too many?**
A: No hard cap, but each question must change a direction. If you can proceed with a stated assumption instead, do that. Stop asking the moment you can write the goal, constraints, and one testable success criterion.

**Q: The user said "you ask too much" — do I stop?**
A: Not necessarily. That is usually a pace complaint, not a stop. Keep the queue, just make questions shorter. Only stop when the user explicitly says "don't ask, just do it."

**Q: What if the user won't answer a direction-changing question?**
A: Distinguish two cases: (1) if the user explicitly says "stop asking / just do it", proceed with stated assumptions and risks; (2) if the user simply doesn't answer (silence), do not silently assume — rephrase the question once more concisely, or state the risk clearly and ask for a one-word confirmation. A direction-changing unknown must never be silently filled.

**Q: Do I ask before every edit?**
A: No. Only before direction-changing or high-cost actions. Mechanical edits go straight through.

## Language Support

This skill supports Chinese interaction. You may ask questions and receive answers in Chinese; the task contract and assumptions may be written in the user's preferred language.
