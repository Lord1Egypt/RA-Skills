# Clarify Before Acting — Playbook

Extended guidance for the core rule in [`../SKILL.en.md`](../SKILL.en.md). Read this when a task is hard enough to warrant it. The core rule is enough for everyday use; this playbook is for the genuinely hard, ambiguous, or high-stakes ones.

The techniques here are distilled from practice and from how mature requirements-interview workflows behave, but deliberately re-expressed as *judgment heuristics* rather than machinery. There is no scoring model, no state file, no pipeline — just things a capable agent can do with its own reasoning on any platform.

---

Section index: 1 Mindset · 2 Homework before asking · 3 Clarity checklist · 4 Question queue · 5 Map the scope first · 6 Questioning lenses · 7 Knowing when to stop · 8 Proceeding on assumptions · 9 Task contract · 10 Full walkthrough · Validation and deliberate omissions

## 1. The mindset: expose assumptions, don't collect features

The failure mode of a vague request is not "missing features" — it is *hidden assumptions* that you and the requester hold differently. A feature list answers "what do you want?"; it does not catch the moment where you pictured a batch job and they pictured a real-time API.

So bias your questions toward surfacing assumptions:

- "I'm reading this as X — is that right?" beats "tell me more."
- "What happens when X fails / is empty / arrives twice?" surfaces edge assumptions the happy-path description hides.
- "What's deliberately *not* part of this?" surfaces scope assumptions.

## 2. Do your homework before you ask

A question you could have answered yourself is friction, and it erodes trust. Before asking a human:

1. Read the request again for what it already implies.
2. Inspect the codebase, docs, tickets, or data you have access to.
3. Only then ask — and only about what a human alone can decide (intent, scope, priorities, trade-offs, business rules).

When you ask, **cite the evidence** that prompted it:

> "I found JWT auth in `src/auth/` using the passport pattern. Should this feature extend that, or intentionally diverge?"

is far better than "How does auth work here?" — it shows you looked, and it lets the person confirm instead of re-explain.

Homework includes **memory**. On platforms that offer memory or past-session recall, search it for questions this user has already answered — preferences, prior decisions, settled trade-offs. A recorded answer retires a queued question without a round-trip; say which memory you reused so the person can correct it if it is stale. Memory shrinks the queue; it does not authorize guessing past an unanswered direction-changing unknown.

## 3. The clarity checklist — find the weakest spot

Treat these as the dimensions of "do I understand this?" Aim each question at whichever is currently weakest, not at whatever is easiest to ask.

| Dimension | The question behind it | A good probe |
|-----------|------------------------|--------------|
| **Goal** | Can I state the objective in one sentence, no "and/or"? | "When you say 'manage X', what's the very first action a user takes?" |
| **Constraints** | Do I know the boundaries and non-goals? | "Does this need to work offline, or is connectivity assumed?" |
| **Success** | Could I write a test that proves it works? | "If I showed you the finished thing, what would make you say 'yes, that's it'?" |
| **Context** | (Existing systems) Do I understand what I'm changing well enough to change it safely? | "This touches the existing order flow — should it reuse that path or stand alone?" |

State the targeting out loud in one line when it helps: *"The goal is clear, but success criteria are the weakest part, so:"* — it keeps the conversation legible and stops you from circling the part you already understand.

## 4. The question queue — one at a time, in order

The core rule says work a queue; this is how to keep it from degrading.

**Why a queue at all.** Dumping every question in one message turns a conversation into a questionnaire — people skim, half-answer, and you learn less per round. Asking whatever comes to mind next loses ordering: you burn patience on a detail before settling the goal it depends on. The queue holds both failure modes apart: everything is visible, but only one question is live at a time.

**The loop, per item:**

1. Ask the top question — just that one.
2. Listen. If the answer is itself ambiguous on a direction-changing point, probe it *before* moving on ("when you say X, always, or only on cold start?").
3. Reflect the answer back in one line so a misread surfaces now, not in review.
4. Mark it resolved, apply it to the queue (new unknowns in, dead questions out), and only then ask the next.

**Queue hygiene.**

- Every item must be direction-changing; reversible detail belongs to the assumptions list, not the queue. If the queue keeps growing past ~5 items, the real problem is usually an unconfirmed scope shape — go map the scope (§5) before continuing.
- Three or more open items: show the numbered list when you ask, so the person sees the remaining shape and can reorder it ("answer 3 first, I have opinions there").
- An answer that resolves several items at once is common and good — collapse the queue explicitly rather than asking now-redundant questions.

## 5. Map the scope before you drill

Before going deep on the most-described piece, list the top-level pieces of the work — the parts that can each succeed or fail independently. Depth-first questioning tends to overfit to whichever component the requester described most vividly, while a quieter sibling stays dangerously vague.

> "I'm reading this as three pieces: (1) ingest, (2) normalize, (3) a reviewer UI. The UI is clear; the other two aren't. Right framing? Anything missing?"

Confirm the shape first, then clarify each piece until none is direction-vague.

## 6. Questioning lenses — for when you're stuck

If a few rounds haven't converged, rotate the lens you question through. Use each once, then return to normal questioning:

- **Contrarian** — challenge a core assumption. "You said 10k concurrent users. What if it were 100 — does the design change, or is 10k an assumption rather than a measured need?" Often collapses imagined complexity.
- **Simplifier** — hunt for the minimal valuable version. "What's the smallest thing that would still be worth shipping?" Separates needed from assumed.
- **Essence** — when the core noun keeps shifting (it's been called a workflow, an inbox, and a planner), stop on features and ask *what the thing fundamentally is* before going further. A moving core noun is a signal you're clarifying symptoms, not the thing.

### Unknown-unknowns sweep

When the task is high-stakes, unusually novel, or still feels direction-vague after the normal lenses, look for decisions the requester may not know to name. Choose the cheapest useful action; do not run all four by default:

- **Blind-spot scan** — list decisions that could change the implementation but were not mentioned, then ask about only the direction-changing ones.
- **Diverge briefly** — sketch two or three materially different approaches to expose a hidden trade-off before choosing one.
- **Cheap falsification** — use a small prototype, measurement, or lookup when a low-cost test can disprove a key assumption.
- **Reverse-check after acting** — compare the implementation notes with the original goal and ask what default standard or expectation may have been missed.

These actions are ways to reveal unknowns, not reasons to postpone action indefinitely. Stop the sweep once no remaining unknown would change the goal, scope, owner, data model, or approach.

## 7. Knowing when to stop — the directional test

Do not chase a number. The test is qualitative:

> **Would any remaining unknown change the *direction* of the work** — a different goal, owner, shape, data model, or approach?

Use the loop boundary as a practical anchor: questions that could change the goal, scope, owner, or overall approach belong in the human/product decision loop; implementation details can stay in the execution loop with an explicit assumption. Feedback after acting may reopen the decision loop when it reveals that the clarified direction was wrong.

- If **yes**: name that unknown and resolve it with one more targeted question.
- If **no**: stop and act. Detail the person can correct on review is not a reason to keep asking.

Signals you are *not* ready (any one is enough):

- The core action or its target is still "TBD".
- Two genuinely different approaches are still live and you can't pick.
- A success criterion would be impossible to test as currently stated.
- The requester said "I'll check" or "not sure" on something direction-changing.

Signals you *are* ready: you could write the goal, the constraints, and at least one testable success criterion right now without inventing anything material.

### Respecting "just do it" — and telling it apart from "you ask too much"

Two different messages often arrive in similar words:

- **An explicit stop** — "don't ask, just do it", "stop asking and start". End the queue. Convert each remaining item into a stated assumption with its risk (§8), and say so plainly:
  > "Proceeding now. Still unclear: the retry behavior on partial failure. I'll assume fail-fast and surface it; flag me if that's wrong."
- **A pace complaint** — "you ask too much", "can we go faster". Not a stop. The membership of the queue is unchanged: every direction-changing unknown still gets asked, one at a time, each fully resolved before the next. What changes is form — shorter questions, tighter evidence, no re-asking what an answer already covered.

Reading a pace complaint as a stop silently drops unknowns the person still expects you to resolve; the queue shrinks by answers, not by impatience. When genuinely unsure which one you heard, ask once, cheaply: "To be clear — skip the remaining questions and assume, or keep going one at a time?"

## 8. When you proceed on assumptions, record them

The queue is where direction-changing unknowns go; the assumptions list is where *non-directional* ones go. Never move an item from the first to the second because asking felt slow — that is the silent guess this skill exists to prevent. The only legitimate transfers: the person explicitly stopped the questioning (an unambiguous "stop asking" — a pace complaint is not one, see §7), or a fresh answer (or memory) revealed the unknown was detail all along.

Whenever you act past an unresolved point, make the assumption visible so it can be caught cheaply:

```
- Assumed: {what you took to be true}
  Basis:   {why — the evidence or default you relied on}
  Risk if wrong: {what breaks / what rework it causes}
```

This turns a silent guess into a reviewable decision. It is the single highest-leverage habit in this playbook: it lets you keep moving without pretending you were certain.

## 9. Task contracts — make clarified work executable

Use a task contract at the end of clarification when another agent will execute the work, or when an unresolved assumption materially affects execution. It is the bridge from intent to action, not a second requirements document and not a prescription for the implementation.

```text
Result:      {the outcome that must be true}
Scope:       {what is included; what is explicitly out of scope}
Checkpoints: {the ordered evidence used to verify the result}
Stop if:     {a change in goal, scope, owner, data, or approach requires review}
Assumptions: {what is being assumed, why, and the risk if it is wrong}
```

For example, "improve the login endpoint's performance" is not yet a task contract. A clarified contract might be:

```text
Result:      Reduce average login response time under the agreed load.
Scope:       Change the login path and direct dependencies; keep the token
             semantics and response shape unchanged.
Checkpoints: Record a baseline; make the change; compare latency and error rate
             under the same load; run the affected tests.
Stop if:     The change requires a token, schema, or external API contract change.
Assumptions: The repeated lookup is the main bottleneck, based on the profile;
             if wrong, the optimization target must be revisited.
```

Do not invent values that were not clarified. Leave a field open, state the assumption, or stop and ask when filling it would change the direction of work.

## 10. Full walkthrough — from a vague request to a task contract

An end-to-end example showing the whole journey from a one-line user request to a task contract: three direction-changing unknowns, three questions, one memory reuse.

**User request:** "Help me optimize the orders service."

**Decision:** Unknown blast radius, vague goal, high redo cost → ❓ ask first (SKILL.md decision table).

**Homework (before asking):**

- Read the code: `list_orders` in `orders/service.py` issues two database round-trips per order; monitoring shows checkout-path p95 = 1.8s.
- Check memory: this user stated last month "no schema changes this quarter" — reuse that scope constraint, say so, and don't ask.

**Queue (ordered by impact):**

1. Is the goal lower latency or lower cost? Or both?
2. What is the success criterion — how fast, under what load?
3. Is the scope the orders service only, or does it include the gateway and frontend?

**Ask one at a time:**

- Q1 → "Latency first; checkout is the pain point." Reflect back: "Goal: reduce tail latency on the checkout path." Cost-related follow-ups are voided by the answer and dropped from the queue.
- Q2 → "p95 under 300ms at twice peak load." Reflect back and confirm.
- Q3 → "Orders service only; gateway is frozen this quarter." (Matches memory; state the reuse.)

**Contract:**

```text
Result:      Reduce checkout-path p95 latency from 1.8s to under 300ms.
Scope:       Change the orders service only; no schema or API contract changes.
Checkpoints: Baseline under 2x peak load; apply the fix; re-measure p95; run affected tests.
Stop if:     The fix requires a schema or API contract change.
Assumptions: The N+1 lookup is the dominant bottleneck, based on the profile.
```

**Handoff:** The contract goes to the executor. If a stop condition triggers during execution (say, the fix needs a schema change), return to asking — don't route around it.

Nothing already answerable from the code was asked; memory retired one potential question (the schema constraint); three direction-changing unknowns converged within three questions.

## Validating changes to this skill

The packaging smoke test proves the rule installs and projects correctly; it proves nothing about how an agent behaves. Changes here tend to be additive, and the drift they invite is toward asking too much — back into the blunt "always ask first" rule this skill exists to improve on.

So after changing this skill, run the mechanical case in a fresh session: give a clear, low-risk task that already names its file, symbol, or command — rename a symbol, run an existing test. The agent should just do it, with no clarifying question and no task contract. A question or a full contract on a one-line rename means the rule has become the friction it was meant to avoid.

A vague request that draws good questions is not evidence on its own; a rule that asked about everything would pass that too. The mechanical case is the one that can tell the two apart. Record what you observed, and do not treat the packaging test as behavioral evidence.

---

## What this playbook deliberately leaves out

For honesty about scope, and to keep it portable across agents, this skill does **not** include:

- **Numeric ambiguity scoring / thresholds.** Pseudo-precision. The directional test in §7 replaces it.
- **State files, resume, or persistence.** Platform-specific; out of scope for a portable rule. (This is about the skill not keeping *its own* state — checking memory your platform already provides, as §2 says, is the opposite of that.)
- **Pipeline handoffs / orchestration.** This skill shapes *how you think before acting*; it does not decide *who executes*.

If your platform offers a heavyweight, instrumented interview system (with scoring, persisted state, and orchestration), prefer that when you need it. This skill is the portable, judgment-only distillation that runs anywhere.
