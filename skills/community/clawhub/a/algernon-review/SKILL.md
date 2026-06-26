---
name: algernon-review
version: "1.0.0"
description: >
  FSRS-4.5 flashcard review session for OpenAlgernon. Use when the user runs
  `/algernon review`, says "revisar flashcards", "quero revisar", "cards em atraso",
  "modo revisao", "review session", or asks to practice due cards. Handles all card
  types (flashcard, dissertative, argumentative), AI evaluation of open-ended
  answers, automatic FSRS scheduling, N1/N2/N3 promotion, and correction card
  generation.
---

# algernon-review

You run the interactive flashcard review session with FSRS-4.5 spaced repetition.
You handle flashcards (binary reveal), dissertative cards (AI-graded), and
argumentative cards (AI-graded). At the end, you check promotion eligibility and
save the session.

## Constants

```bash
ALGERNON_HOME="${ALGERNON_HOME:-$HOME/.openalgernon}"
DB="${ALGERNON_HOME}/data/study.db"
```

## FSRS-4.5 Parameters

- DECAY = -0.5, FACTOR = 0.2346
- Stability (S) = days to reach 90% retention
- Grades: 1 = Again, 3 = Good

## Step 1 — Fetch Due Cards

```bash
sqlite3 "$DB" \
  "SELECT c.id, c.type, c.front, c.back, c.tags, c.source_title, c.deck_id,
          cs.stability, cs.reps, cs.state
   FROM cards c
   JOIN card_state cs ON cs.card_id = c.id
   JOIN decks d ON d.id = c.deck_id
   JOIN materials m ON m.id = d.material_id
   WHERE cs.due_date <= date('now')
   [AND m.slug = 'SLUG']
   ORDER BY cs.due_date ASC
   LIMIT 50;"
```

(Include `AND m.slug = 'SLUG'` only if a specific slug was provided.)

If no cards due: "No cards due for review. Great job staying on top of it." and stop.

Display: "Starting review: N cards due."

## Step 2 — Review Loop

### Flashcards (type = 'flashcard')

1. Show front. AskUserQuestion options: ["Show answer"]
2. Show back. AskUserQuestion options: ["Again", "Good"]
3. Run FSRS update (see Step 3).

### Dissertative and Argumentative Cards

1. Show front. AskUserQuestion options: ["Ready to answer"]
2. AskUserQuestion: "Type your answer:" (free text)
3. Evaluate the response against the reference answer (card back):
   - Dissertative: check accuracy of key points, completeness
   - Argumentative: check that both sides are represented, trade-offs identified
   - Output: brief feedback + suggested grade (1 or 3) + optional MISCONCEPTION note
4. Show evaluator feedback + reference answer. AskUserQuestion options: ["Again", "Good"]
   (Use the user's button choice, not the AI suggestion.)
5. Run FSRS update using the user's chosen grade.
6. If a MISCONCEPTION was detected, create a correction card:
   ```bash
   sqlite3 "$DB" \
     "INSERT INTO cards (deck_id, type, front, back, tags)
      VALUES (DECK_ID, 'flashcard',
              'CORRECTION: MISCONCEPTION_QUESTION',
              'CORRECT_EXPLANATION',
              '[\"[correction]\",\"[N1]\"]');
      INSERT INTO card_state (card_id, due_date)
      VALUES (last_insert_rowid(), date('now'));"
   ```

## Step 3 — FSRS Scheduling

For each graded card, compute new values and update `card_state`.

### Read current state:
```bash
sqlite3 "$DB" \
  "SELECT stability, difficulty, reps, lapses, state, last_review
   FROM card_state WHERE card_id = CARD_ID;"
```

### Compute elapsed days (if last_review is not NULL):
```bash
sqlite3 "$DB" \
  "SELECT ROUND(julianday('now') - julianday('LAST_REVIEW'), 2) AS elapsed;"
```

### State transitions:

| State      | Grade | New stability             | New difficulty              | New state  | Interval         |
|------------|-------|---------------------------|-----------------------------|------------|------------------|
| new        | Good  | 0.4                       | 0.3                         | review     | 1 day            |
| new        | Again | 0.1                       | 0.4                         | learning   | 1 day            |
| learning   | Good  | stability * 1.5           | MAX(0.1, difficulty - 0.05) | review     | MAX(1, ROUND(S)) |
| learning   | Again | stability (unchanged)     | MIN(1.0, difficulty + 0.1)  | learning   | 1 day            |
| relearning | Good  | stability * 1.5           | MAX(0.1, difficulty - 0.05) | review     | MAX(1, ROUND(S)) |
| relearning | Again | stability (unchanged)     | MIN(1.0, difficulty + 0.1)  | relearning | 1 day            |
| review     | Good  | S * EXP(0.9*(1-R))        | MAX(0.1, difficulty - 0.05) | review     | MAX(1, ROUND(S)) |
| review     | Again | MAX(0.1, stability * 0.2) | MIN(1.0, difficulty + 0.1)  | relearning | 1 day, lapses+1  |

For review+Good, compute retrievability first:
```bash
sqlite3 "$DB" \
  "SELECT EXP(LN(0.9) * ELAPSED / STABILITY) AS R;"
```

### Update:
```bash
sqlite3 "$DB" \
  "UPDATE card_state SET
     stability   = NEW_S,
     difficulty  = NEW_D,
     due_date    = date('now', '+' || INTERVAL || ' days'),
     last_review = datetime('now'),
     reps        = reps + 1,
     lapses      = NEW_LAPSES,
     state       = 'NEW_STATE'
   WHERE card_id = CARD_ID;
   INSERT INTO reviews (card_id, grade, scheduled_days, elapsed_days)
   VALUES (CARD_ID, GRADE, INTERVAL, ELAPSED);"
```

## Step 4 — Promotion Check (after all cards)

For each card reviewed with grade = Good where reps >= 5:
```bash
sqlite3 "$DB" \
  "SELECT c.id, c.tags, c.deck_id, cs.reps
   FROM cards c JOIN card_state cs ON cs.card_id = c.id
   WHERE c.id = CARD_ID AND cs.reps >= 5;"
```

If reps >= 5 and tags contain `[N1]`, check deck retention over last 7 days:
```bash
sqlite3 "$DB" \
  "SELECT CAST(SUM(CASE WHEN grade=3 THEN 1 ELSE 0 END) AS REAL) / COUNT(id) AS retention
   FROM reviews r JOIN cards c ON c.id = r.card_id
   WHERE c.deck_id = DECK_ID AND r.reviewed_at >= datetime('now', '-7 days');"
```

If retention >= 0.9:
- Generate a deeper N2 version of the card (N2: differentiator + when to use + main trade-off).
- Insert as new card with tag `[N2]`, due today.
- Apply same logic for `[N2]` cards: promote to N3 (full technical depth, production
  nuances, edge cases).

## Step 5 — Session Summary

```
Session complete.
Cards reviewed: N
Again: X  |  Good: Y
Retention this session: Z%
Next review: [earliest due_date from card_state]
```

Append to today's conversation log:
```bash
echo "[HH:MM] review session | Cards: N | Retention: Z% | Promotions: P" \
  >> "${ALGERNON_HOME}/memory/conversations/YYYY-MM-DD.md"
```
