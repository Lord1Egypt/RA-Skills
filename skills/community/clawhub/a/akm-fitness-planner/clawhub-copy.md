# AKM Fitness ClawHub Skill Page

## Skill Title

**AKM Fitness: Constraint-Aware Training Planner**

## One-line Description

Build the training profile first, then make workout decisions that respect body limits, equipment reality, recovery, and time budget.

## Install

```bash
npx skills add https://github.com/sirsws/akm --skill akm-fitness-planner --full-depth
```

## Public Sample

- GitHub sample record: `https://github.com/sirsws/akm/blob/main/branches/fitness/skill/SAMPLE_RECORD.md`

## What It Is

Most fitness agents answer too early.

They assume the user has one clear goal, enough time, normal recovery, and a stable gym environment.
That is usually false.

AKM Fitness fixes this by forcing the system to model the operator first:

- goal priority
- body constraints
- equipment context
- time budget
- recovery state
- adherence risks

Only then does it make a training decision.

## What Makes It Different

This is not just a workout prompt.
It is a three-stage method:

1. elicitation
2. structured record
3. execution decision

The output is not generic programming language.
It is a constraint-aware training judgment.

## Best Fit

Use this skill when:

- injuries or physical limits materially affect training
- equipment availability changes the decision
- the user needs realistic planning under hard time limits
- generic plans keep failing in practice

## Boundary

- not a medical diagnosis tool
- not a rehab replacement
- not a bodybuilding template generator
- does not pretend missing critical inputs are known

## Closing Line

**No profile, no serious plan.**
