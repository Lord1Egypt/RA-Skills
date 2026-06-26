---
name: fitness-for-desk-workers
description: >-
  Rebuild a body that's been sitting in a chair for years. Fix posture, build functional strength, and recover mobility. No gym required. For people who are deconditioned, overweight, or in pain from desk work.
metadata:
  category: skills
  tagline: >-
    Undo 10 years of sitting. Fix your back, build real strength, and move without pain. No gym membership needed.
  display_name: "Fitness for Desk Workers"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-18"
  openclaw:
    requires:
      tools: [calendar, filesystem]
    install: "npx clawhub install howtousehumans/fitness-for-desk-workers"
---

# Fitness for Desk Workers

If you've spent 10-20 years at a desk, your body has adapted to sitting: tight hip flexors, rounded shoulders, weak core, compressed spine, poor cardiovascular health. Standard fitness advice ("just go to the gym") ignores that you're starting from a deficit. This is a progressive protocol specifically for deconditioned desk workers — from can't-touch-your-toes to functional, pain-free movement.

## Sources & Verification

- **Physical Activity Guidelines for Americans** (U.S. Department of Health and Human Services) — the federal evidence-based recommendations for exercise volume, intensity, and progression. health.gov/our-work/nutrition-physical-activity/physical-activity-guidelines
- **ACSM's Guidelines for Exercise Testing and Prescription** (American College of Sports Medicine) — the clinical standard for exercise programming, including protocols for sedentary and deconditioned populations
- **NIH National Institute on Aging: Exercise & Physical Activity** — free guides on starting exercise at any age and fitness level, including illustrated routines. nia.nih.gov/health/exercise-and-physical-activity
- **"Becoming a Supple Leopard" by Dr. Kelly Starrett** — the most comprehensive reference on mobility work and correcting movement dysfunction from desk posture
- **Cochrane Reviews on Exercise for Low Back Pain** — systematic evidence reviews confirming that exercise and mobility work are first-line interventions for chronic desk-related pain. cochranelibrary.com

## When to Use

- User has spent years at a desk and is deconditioned
- Has back pain, neck pain, or shoulder pain from desk posture
- Wants to start exercising but doesn't know where to begin
- Tried gym routines before and got injured or quit
- Needs functional fitness, not bodybuilding

## Instructions

### Step 1: Assess where you are (be honest)

**Agent action**: Walk the user through this assessment, record their starting point in agent state. This becomes the baseline for tracking progress.

```
STARTING POINT ASSESSMENT:

MOBILITY:
[] Can you touch your toes? (Y/N)
[] Can you squat down with heels on the floor? (Y/N)
[] Can you raise both arms straight overhead without arching your back? (Y/N)
[] Do you have daily back, neck, or shoulder pain? (Y/N)

STRENGTH:
[] Can you hold a plank for 30 seconds? (Y/N)
[] Can you do 5 pushups (knees OK)? (Y/N)
[] Can you stand up from the floor without using your hands? (Y/N)

CARDIO:
[] Can you walk briskly for 20 minutes without stopping? (Y/N)
[] Can you climb 3 flights of stairs without being winded? (Y/N)

SCORING:
7-9 yes: You're in decent shape. Skip to Phase 2.
4-6 yes: Typical desk worker. Start at Phase 1.
0-3 yes: Significantly deconditioned. Start at Phase 0.
```

### Step 2: Phase 0 — Undo the damage (Weeks 1-2)

If you're in pain or extremely stiff, start here. This is not exercise — it's restoration.

```
DAILY ROUTINE (15 min, do at home, no equipment):

1. CAT-COW (2 min)
   On hands and knees. Arch your back up (cat), then drop belly down (cow).
   Slow, controlled. This wakes up your spine.

2. HIP FLEXOR STRETCH (2 min each side)
   Kneel on one knee, other foot forward. Push hips forward gently.
   Your hip flexors are the #1 problem from sitting. They pull on
   your lower back and cause most desk-worker back pain.

3. CHEST OPENER (2 min)
   Stand in a doorway, forearms on the frame, lean through gently.
   Reverses the rounded-shoulder posture from typing.

4. DEAD HANG (or modified) (1 min total)
   Hang from a pullup bar, tree branch, or door frame (carefully).
   If you can't hang: just reach overhead and stretch.
   This decompresses your spine.

5. WALKING (10 min minimum)
   Not fast. Not a workout. Just move your body.
   Walk outside if possible — sunlight matters for mental health too.

DO THIS EVERY DAY FOR 2 WEEKS BEFORE ADDING ANYTHING ELSE.
If you have pain that gets worse, see a doctor. Mild discomfort
that improves with movement is normal.
```

### Step 3: Phase 1 — Build the foundation (Weeks 3-8)

Three sessions per week. 20-25 minutes. No equipment needed.

```
THE ROUTINE (3x per week):

WARMUP (3 min):
- Cat-cow x 10
- Hip circles x 10 each direction
- Arm circles x 10 each direction

STRENGTH (15 min):
1. BODYWEIGHT SQUAT — 3 sets of 8-12
   Stand, feet shoulder width, sit back like into a chair, stand up.
   Can't go deep? Squat to a chair and stand back up.

2. PUSHUP — 3 sets of 5-10
   Can't do full pushups? Do them against a wall, then a counter,
   then knees, then full. Progress over weeks.

3. PLANK — 3 sets, hold as long as you can (target: 30 sec)
   On forearms, body straight, core tight. Don't hold your breath.

4. ROW — 3 sets of 10
   Fill two bags with books. Bend at hips, pull bags to your chest.
   Or use a table: lie underneath, grab edge, pull chest up.

5. HIP BRIDGE — 3 sets of 12
   Lie on back, knees bent, push hips up. Squeeze glutes at top.
   This reverses the hip flexor damage from sitting.

STRETCH (5 min):
- Hip flexor stretch (1 min each side)
- Hamstring stretch (1 min each side)
- Chest opener (1 min)

CARDIO (separate days or after strength):
- Walk 20-30 min, 3-4x per week
- Aim to be slightly out of breath but able to hold a conversation
```

### Step 4: Phase 2 — Build real capacity (Months 3-6)

```
PROGRESSION RULES:
- When you can do 3x12 of any exercise, make it harder
- Squat: hold a bag of books, then a backpack with weight
- Pushup: elevate feet, add a pause at the bottom
- Plank: extend to 60 sec, then add shoulder taps
- Row: heavier bags, slower movement
- Bridge: single leg

ADD:
- Lunges (3x10 each leg)
- Pike pushup (for shoulders)
- Step-ups onto a sturdy chair (3x10 each leg)

CARDIO:
- Progress walking to jogging intervals
  (walk 2 min, jog 1 min, repeat for 20 min)
- Or: cycling, swimming, hiking — whatever you'll actually do

CONSISTENCY > INTENSITY. 3 mediocre sessions per week beats
1 perfect session followed by nothing.
```

### Step 5: Posture fixes for ongoing desk work

If you still sit at a desk, these prevent re-damage:

```
AT YOUR DESK:
- Screen at eye level (stack books under your monitor if needed)
- Elbows at 90 degrees when typing
- Feet flat on floor
- Stand up every 30 minutes (set a timer, seriously)

THE 30-SECOND RESET (every 30-60 min):
1. Stand up
2. Reach arms overhead and stretch
3. Squeeze your shoulder blades together
4. Squeeze your glutes
5. Sit back down

This takes 30 seconds and prevents most desk-related pain
when done consistently.
```

## If This Fails

- **See a doctor or physical therapist** — if pain persists or worsens after 2 weeks of Phase 0, get a professional assessment. Many insurance plans cover PT with a referral. Community health centers offer sliding-scale fees.
- **Try just walking** — if the full routine feels like too much, walk for 10-20 minutes daily and do nothing else for a month. Walking alone produces measurable health improvements in sedentary people. Build from there.
- **Free community resources** — YMCAs offer financial assistance memberships, many parks departments run free outdoor fitness classes, and some physical therapy schools offer free clinics for supervised exercise.
- **Cross-reference: Burnout Recovery skill** — if the barrier isn't physical but motivational, burnout may be the underlying issue. Address the energy problem before the fitness problem.
- **Cross-reference: Anxiety Emergency skill** — if exercise triggers panic or anxiety (elevated heart rate can mimic panic symptoms), start with the anxiety stabilization protocol first

## Rules

- Always start with Phase 0 if the user has pain — exercise on top of dysfunction causes injury
- Never recommend heavy lifting, running, or high-impact exercise for deconditioned people
- Progress slowly — the goal is sustainable movement for life, not a 6-week transformation
- If pain increases with exercise (not mild discomfort, actual pain), recommend seeing a doctor

## Tips

- Walking is underrated. It's the single most important exercise for desk workers. It decompresses the spine, improves cardiovascular health, and requires zero recovery.
- Your hip flexors are the root of most desk-worker back pain. Stretch them daily — it's more important than any strength exercise.
- You don't need a gym. Bodyweight exercises + walking + stretching is enough for most people to go from deconditioned to healthy.
- Morning mobility routine (5 min of stretching) has a disproportionate impact on how your body feels all day.
- Sleep and nutrition matter more than the perfect exercise routine. You can't out-train a bad diet or 5 hours of sleep.

## Agent State

```yaml
fitness:
  phase: 0
  assessment_scores: {}
  start_date: null
  sessions_completed: 0
  current_exercises: []
  progression_history: []
```

## Automation Triggers

```yaml
triggers:
  - name: workout_reminder
    schedule: "3x per week at user's preferred time"
    action: "Workout day. Today's routine based on current phase. List exercises with sets/reps. Ask how the last session felt."

  - name: phase_progression
    condition: "sessions_completed >= 12 per phase"
    action: "You've completed enough sessions to consider progressing. Re-assess: can you do 3x12 of all current exercises? If yes, advance to next phase."

  - name: posture_reset
    condition: "user is at desk"
    schedule: "every 45 minutes during work hours"
    action: "30-second reset: stand, reach overhead, squeeze shoulder blades, squeeze glutes, sit. Done."
```
