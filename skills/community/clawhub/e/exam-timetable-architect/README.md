# exam-timetable-architect

Turns "6 exams, 5 weeks, 40 topics, panic" into a day-by-day spaced study plan.
Topics ranked by exam-weight × weakness × difficulty, scheduled backwards from
exam dates with expanding reviews (+1/+3/+7/+14d), load-capped to your real
hours, with honest feasibility math ("need 4.2h/day, you declared 2h — here's
what to cut") and re-planning that works from *today* when life happens.

## The real-world problem

Every student builds timetables that fail the same way: syllabus-order study
(chapter 1 mastered, chapter 14 untouched), no reviews (each topic seen once),
load-blind scheduling (9h of blocks on a 3h day), and no recovery path after
the first missed day. The learning science is settled — spaced retrieval
practice is one of only two "high utility" techniques in Dunlosky et al.'s
2013 review — but the scheduling is tedious, which is why nobody does it by
hand. This tool does the scheduling so the human can do the studying.

## Quick start

```bash
cd scripts
python3 exam_planner.py init --hours 3.5
python3 exam_planner.py exam --add "Calculus II=2026-11-20" --weight 40
python3 exam_planner.py topic --add "integration by parts" --exam "Calculus II" \
  --difficulty 4 --weakness 4 --hours 3
python3 exam_planner.py plan          # feasibility check + day map
python3 exam_planner.py today         # what to do right now
python3 exam_planner.py done t1-s0    # check off a block
python3 exam_planner.py progress      # coverage vs reinforcement vs pace
python3 exam_planner.py replan        # after missed days
```

Python 3.9+, stdlib only. Store: `exam_plan.json` next to the script.

## What the outputs mean

- **Feasibility** — required hours (first study + spaced reviews) vs available
  hours before the last exam. Over capacity → ranked cut suggestions, not a
  fantasy schedule.
- **plan** — per-day blocks: 📖 first study, 🔁 review (recall-first,
  closed-book). Reviews never land after their exam; tight plans compress
  them to exam eve.
- **today** — overdue + today's blocks, reviews first (cheapest, highest
  retention-per-minute).
- **progress** — Coverage % (topics first-studied) separate from
  Reinforcement % (reviews done). Coverage-without-reinforcement is the
  illusion of competence; the tool refuses to hide it in one number.
- **replan** — drops un-executed future blocks and re-spaces from today.

## Design choices (why)

- **Priority = weight × proximity × weakness × difficulty** — near exams and
  weak heavy topics first; textbook order is ignored on purpose.
- **+1/+3/+7/+14 ladder** — approximates the Cepeda 2006 meta-analytic
  finding that optimal gap ≈ 10–20% of retention interval.
- **Review cost = 25% of first study** — re-learning is far cheaper than
  acquisition.
- **Units of 50+10 min, long break after 3** — attention-cycle-sized blocks.
- **Warning above 6h/day** — sleep debt destroys retention; a plan that
  requires all-nighters is a plan to fail.

## License

MIT © Denis Voronin
