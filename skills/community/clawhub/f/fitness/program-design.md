# Program Design — Splits, Templates, Substitutions

Turning goal + `training_days` + `session_minutes` + `equipment` into a concrete week. Ordering, rest, and movement-floor rules are canonical in SKILL.md (Program Design Defaults); this file is the build kit.

## Split by Available Days

| training_days | Split | Notes |
|---|---|---|
| 2 | Full-body x2 | Compounds only; isolation is a luxury the set budget can't afford |
| 3 | Full-body x3 | Default. Highest return per session; every muscle hit 3x/week |
| 4 | Upper/Lower x2 | Cleanest volume distribution; cardio on 1-2 off days |
| 5 | Upper/Lower + full-body, or PPL + UL | The 5th day is flex: lagging muscles or conditioning |
| 6 | Push/Pull/Legs x2 | Only with logged 5+ day attendance; recovery is the constraint, not scheduling |

Attendance rule (canonical in SKILL.md Traps): program to logged attendance + max 1 day.

## Set Budget Math

Weekly sets per muscle (Rule 4 corridor: 10-20) ÷ sessions touching that muscle = sets per session. Example: 12 weekly chest sets on 3 full-body days = 4 chest sets per session — one exercise, done well. If the math forces more than ~8 hard sets for one muscle in one session, spread across more days or cut volume: late sets degrade (SKILL.md frequency rule).

Session time check: a hard compound set with Rule 8 rest costs ~4-5 min, isolation ~2.5 min. A 60-min session holds roughly 8-10 compound sets plus 4-6 isolation sets after warm-up. If the plan exceeds `session_minutes`, cut isolation first, never rest.

## Template Skeletons

Full-body (the 3-day default) — alternate A/B:

- A: squat pattern · horizontal push · horizontal pull · hinge assistance · 1-2 isolation
- B: hinge pattern · vertical push · vertical pull · squat assistance · 1-2 isolation

Upper/Lower (4 days):

- Upper 1 heavy push bias, Upper 2 heavy pull bias; Lower 1 squat bias, Lower 2 hinge bias
- Each upper day: 2 pushes + 2 pulls (balance is injury insurance); each lower day: 1 primary + 2 assistance + calves/core

Goal adjustments on any skeleton: strength → first compound at 3-6 reps, 80-90% e1RM; muscle → 6-12 reps, RIR 1-3; general → mixed ranges, compounds lower reps than isolation. All numbers per Quick Reference.

## Exercise Selection

- Pick the variant the user can load progressively with their `equipment` and perform pain-free — pattern coverage beats exercise identity. A goblet squat that progresses beats a barbell squat that hurts.
- Big-return defaults per pattern: squat (back/front/goblet squat, leg press) · hinge (deadlift, RDL, hip thrust) · horizontal push (bench, dumbbell press, push-up) · horizontal pull (barbell/dumbbell/cable row) · vertical push (overhead press) · vertical pull (pull-up, lat pulldown).
- Stability spectrum: machines allow the most load with the least skill; barbells the most progression headroom; unilateral free-weight work the most balance demand. Beginners and returners start toward the stable end.
- An exclusion (config preference area) removes the exercise, never the pattern — substitute within the row below.

## Substitution Table (by equipment)

| Pattern | full-gym / home-rack | dumbbells | bodyweight |
|---|---|---|---|
| Squat | Back/front squat | Goblet squat, DB split squat | Split squat → rear-foot-elevated → pistol progression |
| Hinge | Deadlift, RDL | DB RDL, single-leg RDL | Hip thrust (feet elevated), back extension, nordic regression |
| Horizontal push | Bench press | DB bench/floor press | Push-up ladder |
| Horizontal pull | Barbell/cable row | Single-arm DB row | Inverted row (table, rings, towel-door) |
| Vertical push | Overhead press | DB shoulder press | Pike push-up → wall handstand progression |
| Vertical pull | Pull-up, pulldown | DB pullover (partial substitute) | Pull-up if any bar exists; else band pulldown or extra rows |

When reps outgrow the movement, add difficulty instead of load: tempo, longer range, unilateral variants, bands.

## Conditioning Placement

- Lifting and cardio same day: lift first when strength or muscle is `primary_goal`; separate by 6+ hours when schedule allows (interference logic, SKILL.md Where Experts Disagree).
- Hard intervals never the day before the heaviest lower session; Zone 2 goes anywhere.
- 2-3 lifting days + ACSM cardio floor fits in: cardio on off days, or 20-30 min Zone 2 appended after lifting.

## Populations

- Older trainees (60+): same rules, two additions — include intentional fast concentrics (power fades faster than strength with age) and one balance-demanding unilateral exercise per week; progress increments at half rate if `risk posture` is unset.
- Teens: full training is safe with supervised technique; the floor is form mastery before load chasing — no separate program needed.
- Pregnancy, cardiac, metabolic, or renal conditions without clearance: Red Flags row in SKILL.md — clearance first, no new vigorous programming.
