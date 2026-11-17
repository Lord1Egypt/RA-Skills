# Decision Log — Persistent Record Format

Storage: `~/Clawic/data/collaborate/decisions.md`, appended at convergence time when `log_decisions` is on (default). If the user has their own convention (team ADRs, repo docs), that convention is the home and this log is skipped — one home per decision, never both.

## Entry Template

```markdown
## [YYYY-MM-DD] <decision in one line>
- **Status**: active | superseded by [date] | revisited [date]
- **Owner**: <who decided>
- **Options considered**: <the candidates, one line>
- **Counterpart**: <who/what lens; recruited or simulated>
- **Surviving objection**: <steelman-quality, verbatim if from a real party>
- **Revisit trigger**: <observable, thresholded condition — quality bar in convergence.md>
- **Outcome of exchange**: position changed | position held | deadlock (crux: <one line>)
```

Unresolved deadlocks get entries too — both positions, the crux, why it stopped, what reopens it (`deadlock.md`, Recording the Unresolved).

## Rules

- **Append-only.** Never edit a past entry's substance; a reversed decision gets a NEW entry and the old one's status flips to `superseded by [date]`. The history of reversals is decision data — how often triggers fire, which lenses catch real problems.
- **Written at convergence, by the owner.** Records reconstructed later inherit the winner's memory; the surviving objection is the first casualty.
- **Check before opening any exchange.** Routing check 1 (SKILL.md): a question with an `active` entry is settled — answer with the citation. Re-litigation happens only through the entry's trigger.
- **Revisit pass when a trigger fires.** The firing trigger reopens exactly that question: fresh exchange, new entry, old status updated. A trigger observed but ignored converts the log from memory into decoration.
- One line per entry field; a decision needing paragraphs of context should link to the artifact (design doc, PR) rather than duplicate it.

## Folder Layout

```
~/Clawic/data/collaborate/
├── config.yaml     # declared variables: round_cap, budget_share, solo_undo_threshold, counterpart_mode, log_decisions
└── decisions.md    # this log, append-only
```

Long-form user material (a house critique-register guide, an escalation-path doc) lives as its own file in the same folder, referenced from `config.yaml` by path.

## What the Log Buys

- Settled-question detection: the exchange you do not re-run (the most common budget leak in long-lived projects).
- Dissent protection: recorded objections make disagree-and-commit safe for the dissenter (`deadlock.md`).
- Counterpart calibration: after several entries, which lenses produced position movement and which produced ceremony — feeds future Counterpart Selection.
