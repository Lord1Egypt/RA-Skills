# Portfolio Rules

## Cycle output

Default cycle output is exactly:

- 1 `WRITE_NOW` primary topic.
- 2 `BACKUP` topics.
- All remaining topics receive one of `MERGE`, `WATCH`, `SHORT_NOTE`, `COVERED_TRACK`, or `ABANDON`.

## Selection constraints

1. Primary and backups cannot all share the same company, event, or argument frame.
2. Same-event topics should be merged before ranking.
3. Recently published topics need an increment test: continuation, update, or repetition.
4. Time-sensitive backups must carry a recheck date before the window closes.
5. Watch topics must contain a trigger signal, expected evidence and review date.
6. When scores are close, prefer stronger evidence, clearer reader value and better portfolio coverage.
7. Published, adopted and closed lifecycle states do not automatically revert because of a new score.
8. Topics with a factual, privacy or boundary block cannot enter the primary or backup set.

## Lifecycle versus recommendation

Keep these fields separate:

- Lifecycle: `new`, `reviewed`, `adopted`, `published`, `watch`, `closed`.
- Recommendation priority: `P0`, `P1`, `P2`, `P3`.

Lifecycle records what happened to the topic. Priority records where current writing resources should go.

## Topic identity

Use a stable topic ID or Notion page ID as the write key. Title is for display and human verification only. Do not update pages using fuzzy title matching.

## Idempotent review block

Every evaluation block should include:

```text
[topic-evaluation]
run_id: YYYYMMDD-HHMM
review_date: YYYY-MM-DD
priority: P0/P1/P2/P3
net_score: 0-100
action: WRITE_NOW/BACKUP/MERGE/WATCH/SHORT_NOTE/COVERED_TRACK/ABANDON
[/topic-evaluation]
```

Repeated runs replace the existing block with the same `review_date` and `run_id` policy rather than appending duplicates.
