# Human In The Loop — Approval, Escalation, And Handoff

Two different mechanisms that get confused: **approval** pauses one action mid-task and resumes; **escalation** hands the whole task to a person and ends the agent's run. Design them separately.

**Before changing a trigger or an approval rule**, read the escalation policy in `~/Clawic/data/agents/artifacts/escalation-policy.md` (via `## Boxes`) and the agent's `specs/<agent>.md`. Escalation rules are the part of an agent most often changed by whoever was annoyed most recently.

## Approval: Pausing One Action

- Triggered by **tool tier** against `autonomy_level` (SKILL.md Rule 5), evaluated in the executor, never by the model deciding to ask (`implementation.md`).
- The request shows **the rendered arguments and the reversibility**, not the tool name. "Approve `send_email`?" approves nothing; the recipient, the subject and the body approve something.
- Approval is for **one action with those exact arguments**. Re-approve if anything changes after the grant — argument substitution after approval is a real attack (`security.md`).
- A denial returns a result the model can act on: *"not approved: the customer is not eligible. Propose an alternative or escalate."* A denial that returns nothing produces a retry loop.
- Approvals need a **timeout with a defined outcome** — deny, escalate, or queue — because an approval waiting for a human who went home must not leave the task hanging.
- Batch approvals only for identical low-tier actions. A single click covering forty heterogeneous actions is a rubber stamp with an audit trail.

## Escalation: Handing Over The Task

Triggers must be observable, not judgments the model makes about itself:

| Trigger class | Concrete condition |
|---|---|
| Risk | Any irreversible action; money above a threshold; anything with legal, safety or health content |
| Repeated failure | Two failed attempts at the same goal, or a loop detector hit |
| Out of scope | The request is outside the agent's stated purpose |
| Missing capability | The needed tool does not exist or returned `not authorized` |
| Sentiment | Explicit anger, a threat, or a request for a human |
| Policy | A named customer segment, a flagged account, a regulated topic |
| Budget | The cost or turn cap tripped with the task unfinished |

Write them as a list in the system prompt (`prompts.md`) **and** enforce the mechanical ones in code. A trigger only in the prompt fires most of the time, which is the worst reliability profile there is.

## The Handoff Packet

An escalation without context makes the human redo the work, and the user repeat themselves. Every handoff carries:

1. **Who** — the user or account, by `contacts.md` key where one exists, never a duplicated record (`memory-template.md`).
2. **What they want** — one sentence, in their words.
3. **What was tried** — tools called and what came back, three bullets maximum.
4. **Why it escalated** — the trigger that fired, named.
5. **Recommended next action** — the agent's best proposal, marked as a proposal.
6. **Where to look** — the trace or task id.

Keep it under a screen. A packet longer than the transcript gets skipped, and then escalation is worse than no agent.

## Calibrating The Rate

- Both directions are failures. Over-escalation destroys the value; under-escalation produces the incident that ends the pilot.
- The number that matters is not the escalation rate but the **reversal rate**: escalations a human immediately hands back are the trigger being wrong. Track both, always together (`evaluation.md`).
- Start deliberately over-cautious and loosen with evidence: one trigger at a time, measured on the eval set and on the reversal rate. Tightening after an incident is expensive; loosening after a boring month is cheap.
- Never loosen an irreversible-tier gate on the strength of a quiet month. That gate exists for the tail event, and quiet months are its normal state.
- Do not gate on a model-reported confidence score unless you have checked, on your eval set, that low-confidence runs actually fail more often. Uncalibrated confidence produces escalations that correlate with verbosity, not with risk.

## Resuming After A Human

- Feed the human's decision back as a tool result, not as a new user message: it keeps the trajectory coherent and the trace readable.
- Include *what* the human decided and any correction they made, so the agent does not repeat the proposal in the next turn.
- If the human did the work themselves, the agent's task ends as `escalated` — do not let it continue and duplicate the side effect (`architecture.md`).
- Long pauses invalidate assumptions and prompt caches: on resume, re-read the state that could have changed rather than trusting the pre-pause context (`context.md`).

## Asynchronous And Unattended Runs

- Scheduled and queue-driven agents have no human present. Either the autonomy level covers everything the task can hit, or the task must be able to **park**: save a checkpoint, notify a person, resume when answered.
- A parked task needs an owner and a deadline, or it becomes an invisible backlog. Route parked tasks to a real queue someone watches.
- Notification channel and target belong in `config.yaml` under the integrations preference area; the person belongs in `contacts.md` by key.

## Designing The Approval Surface

- One screen: what will happen, to whom, whether it can be undone, and the two buttons.
- Show the diff for anything that changes existing state — before and after, not a description of the change.
- Make "deny with a reason" as easy as approve; the reason is what improves the trigger.
- Log every decision with who, when, and the exact arguments. That log is the audit trail for the tiers that need one, and the input to calibration.

**When an escalation policy or an approval rule is agreed**, write it to `~/Clawic/data/agents/artifacts/escalation-policy.md` — triggers, packet contents, approval surface, timeout behavior — add its `## Boxes` line, and mirror the trigger list into the agent's `specs/<agent>.md`, in the same turn (`memory-template.md`). Escalation rules that live only in a prompt get quietly edited during an incident and never reviewed afterwards.
