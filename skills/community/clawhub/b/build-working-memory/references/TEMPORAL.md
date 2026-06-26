# Structured Events and Temporal Support

Use this reference when the memory system must support temporal recall, event ordering, duration questions, or date-sensitive retrieval.

## Goal

Preserve not just broad topics, but **answer-bearing events** with enough structure to support:
- which happened first
- how many days/weeks/months between X and Y
- how long before/after
- how many events before a threshold event

## Event record schema

Store structured events in `memory/events.json` as a flat append-only list.

Recommended event object:

```json
{
  "event_type": "purchase|issue|attendance|action|milestone|social|life|delivery|membership|generic-event",
  "action": "purchase|preorder|order|arrival|booking|issue|malfunction|clean|fix|trim|setup|service|repair|attendance|start|finish|met|joined|moved|accepted|generic",
  "object_hint": "white adidas sneakers",
  "text": "I cleaned my white Adidas sneakers last month.",
  "session_id": "abc123",
  "timestamp": "2023/05/30 (Tue) 09:00",
  "date_text": "5/30",
  "normalized_date": "2023-05-30",
  "relative_time": "last month",
  "has_explicit_date": true,
  "has_relative_time": true
}
```

## Write rules

### Keep in `memory/events.json`
- user-stated dated events
- relative-time events that can be normalized from session timestamp
- one-off factual actions that later temporal questions may depend on
- purchases, issues, meetings, attendance, starts/finishes, moves, joins, repairs, setup events

### Keep out
- assistant filler
- generic advice
- repetitive topical discussion without an event
- vague sentiment without an anchorable event

## Relative-date normalization

Resolve against the session timestamp when possible.

Recommended conversions:
- `today` -> same day as session
- `yesterday` -> minus 1 day
- `last Saturday` / `last Sunday` -> previous matching weekday
- `last weekend` -> previous Saturday as canonical anchor
- `N days/weeks/months ago` -> subtract `N`, `7*N`, or `30*N` days
- `mid-February` -> 15th of that month
- `M/D` -> same year as session timestamp unless clearly impossible
- `Month D` -> same year as session timestamp unless clearly impossible

Do not invent precision beyond the heuristic. If normalized dates are approximate, keep the original `relative_time` text too.

## Retrieval rules

### Default retrieval
Load:
- resumption.md
- MEMORY.md
- threads.md
- relevant daily logs
- top-ranked events from `memory/events.json`

### Rank events higher when they:
- mention question entities directly
- contain normalized dates
- contain relative time phrases
- have event types like `issue`, `purchase`, `attendance`, `action`, `milestone`
- look like singleton answer-bearing facts rather than repeated topical chatter

## Lightweight deterministic support

Use deterministic helpers for narrow temporal tasks before handing off to the model.

### Pairwise ordering
For questions like:
- "Which happened first, X or Y?"
- "Who did I meet first, A or B?"

Procedure:
1. Extract candidate entities from the question
2. Filter events mentioning those entities in `text` or `object_hint`
3. Keep only events with normalized dates when possible
4. Sort by normalized date ascending
5. Emit the earliest matched event as structured evidence

### Delta questions
For questions like:
- "How many days before X did Y happen?"
- "How long had I been doing X when Y happened?"

Procedure:
1. Gather top relevant dated events
2. Compute pairwise day deltas over a small candidate set
3. Feed those deltas to the model as evidence, not as the final answer unless the mapping is unambiguous

### Counting-before-threshold questions
For questions like:
- "How many charity events happened before Z?"

Procedure:
1. Identify threshold event `Z`
2. Filter dated events belonging to the event family in question
3. Count only events with normalized dates strictly earlier than threshold
4. Provide both the count and the counted examples

## Failure modes to watch

- preorder vs purchase vs arrival conflation
- repeated topic chatter outranking singleton event lines
- approximate date normalization overwhelming precise dates
- over-aggressive symbolic pruning causing regressions

Prefer **soft structured evidence + model judgment** over brittle hard-coded answer substitution.
