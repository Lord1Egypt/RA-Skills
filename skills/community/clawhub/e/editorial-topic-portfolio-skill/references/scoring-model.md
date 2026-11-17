# Scoring Model

## Base score

Only score topics that pass the hard gates or have recoverable HOLD status.

| Dimension | Weight | Question |
|---|---:|---|
| Originality and information increment | 20 | What new framework, evidence, connection or boundary does the article add? |
| Reader judgment value | 20 | What real decision or structural change can the core reader understand? |
| Evidence readiness | 15 | Are primary sources, dates, numbers, counterarguments and boundaries available? |
| Timeliness and window | 15 | Is the topic inside a useful window, or does it have durable long-tail value? |
| Position fit | 15 | Does it match the AI line, researcher stance, collection and audience? |
| Portfolio contribution | 10 | Does it fill a matrix gap and avoid recent-topic duplication? |
| Execution feasibility | 5 | Are materials and scope manageable in the current cycle? |
| Total | 100 |  |

Each dimension uses a 0-5 raw score, then converts to its weighted maximum.

## Risk deductions

Maximum 20 points:

- Uncertain fact or policy status: -1 to -6.
- Competitive coverage rapidly increasing: -1 to -5.
- Topic too broad or likely to become a survey: -1 to -4.
- High overlap with recent content: -1 to -4.
- Public-expression or compliance risk: -1 to -5.

Always output base score, each deduction, and net score.

## Priority bands

- P0: net >=82, gates pass, evidence readiness >=12/15, originality >=16/20.
- P1: net 70-81, gates pass, only small research gaps remain.
- P2: net 50-69 or recoverable HOLD; must include trigger and recheck date.
- P3: net <50 or unrecoverable BLOCK.

## Actions

- `WRITE_NOW`: current primary topic.
- `BACKUP`: current-cycle backup.
- `MERGE`: combine into another article.
- `WATCH`: wait for a defined signal.
- `SHORT_NOTE`: reduce to a short observation or case material.
- `COVERED_TRACK`: already published; track only new facts.
- `ABANDON`: close with a concrete reason.

## Manual override

A manual override must record:

- topic ID;
- overridden rule or score;
- decision and reason;
- operator;
- effective date and expiry date;
- evidence expected to revisit the override.

A manual override cannot bypass a factual, privacy or external-action block.
