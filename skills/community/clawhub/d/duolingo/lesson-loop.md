# Lesson Runtime Loop

Every session runs one topic at a time with quick iterations.

## Standard Loop (60-90 seconds)

1. Present one micro-challenge.
2. Collect attempt.
3. Grade and explain one correction.
4. Run one reinforcement prompt.
5. Update queue and session log.

## Placement Loop (new topic)

- Run 2-5 questions from easy to hard.
- Stop early after clear level signal.
- Set initial lane in `curriculum.md`.
- Add first lessons to `queue.md`.

## Session Writeback

After each loop, update:
- `topics/<slug>/sessions.md` with outcome
- `topics/<slug>/queue.md` with next item
- `memory.md` with streak and rotation notes

## Difficulty Adjustments

- 2 misses in a row -> drop one difficulty step.
- 3 clean wins in a row -> raise one step.
- Repeated misses on same node -> inject guided review before new content.

## Exit Rule

Session ends only after a clear next action is queued:
- next lesson id
- next review due window
- checkpoint trigger if threshold met
