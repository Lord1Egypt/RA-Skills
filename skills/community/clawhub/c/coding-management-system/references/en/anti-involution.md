# Anti-Involution 2.2

Governance involution is the failure mode where a project keeps producing correct-looking governance output while the product stops moving. This file defines detection, budgets, and exit rules. Load it when a project has many documents and little shipped behavior, when a rebaseline is requested, or when the same risk keeps reappearing.

## Detection Signals

Treat two or more of these as an active involution signal and report it as the finding, not as a side note:

| Signal | Typical observation |
| --- | --- |
| Document volume exceeds source volume | Governance docs outnumber or outweigh the code they describe |
| Documents grow, behavior does not | A reporting period produces docs with no code change and no new verified behavior |
| Layered override notes | A live authority file carries `Superseded`, `CURRENT OVERRIDE`, or `this section is void` annotations |
| Repeated risk carry-forward | The same material risk appears in consecutive `Accepted With Risk` decisions |
| Accepted but never released | Work reaches `Accepted` while nothing ships to the user |
| Gate needs a human away from keyboard | A milestone sits nearly accepted for weeks on one manual check |
| Status self-coverage | STATUS or TARGET files are rewritten in place instead of being rebaselined and archived |

## Document Budget

- Keep the active governance set readable in one pass. Practically: Active Packet, loop log, one consolidated Work Order, one current QA decision, plus the current baseline.
- Everything else is history. Move it to `Docs/archive/YYYY-MM.md`. Do not delete it; move it.
- When adding a document, name the one it replaces. A new file with no predecessor is usually a duplicate state home.

## Archive Discipline

Right:

```text
Docs/TARGET.md  -> git mv Docs/archive/2026-09.md/TARGET.md
newDocs/REBASELINE-2026-09-06.md  (the new current authority)
```

Wrong:

```text
Docs/TARGET.md
  > Superseded by the 2026-09-01 revision.
  > CURRENT OVERRIDE: ignore the section above.
```

The wrong form forces every future reader and agent to reconstruct which layer is authoritative, and it makes conflict detection impossible to automate.

## Rebaseline Discipline

A rebaseline is additive, never in-place:

1. write the new baseline as `REBASELINE-<YYYY-MM-DD>.md`, or as a new dated baseline file if the project already uses that convention;
2. archive the previous baseline in the same pass;
3. update the Active Packet authority fingerprint;
4. run Alignment on the new baseline before dispatching new Work Orders.

Direction Alignment does not rewrite the target. Rebaseline then requires a separate Planning/Dispatch pass.

## Accepted With Risk Exit

`Accepted With Risk` is valid only with all four:

1. the core outcome demonstrably works;
2. the specific remaining gap, written as an unlock condition;
3. an owner;
4. a date.

Missing any of these, it is an unresolved blocker wearing a green badge. Three consecutive formal `Accepted With Risk` decisions on one Program trigger Direction Alignment before further expansion.

## Stop-Loss

Governance needs a pre-committed exit so a weak line is not kept alive by sunk cost:

- Set the stop-loss before the work starts: a budget ceiling, a time ceiling, or an evidence threshold.
- When the ceiling is breached, the default action is archive, not extend.
- A project that has consumed its budget and produced documents rather than behavior is reported for archival with its reusable parts extracted.
- Restarting the same goal from scratch to escape a stall is a failure mode. Cut the scope to the smallest publishable increment instead.

## Subtraction Gate

When a new direction, feature, or project is proposed:

1. name what will be dropped, paused, or archived to make room;
2. if nothing can be named, the new item waits;
3. prefer deepening one coherent data-to-user-value chain over starting a parallel one.

## Related

- Startup go/no-go questions and the scoring gate live in `project-lifecycle-navigator`.
- Stall and deterministic-path rules for the execution loop live in `agent-loop-engineering` (`references/en/anti-patterns.md`).
