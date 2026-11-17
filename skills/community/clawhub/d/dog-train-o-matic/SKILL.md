---
name: dog-train-o-matic
description: "Generate a personalized, breed-and-age-aware dog training program: 5-minute daily exercise plans targeting the owner's specific behavior problems, week-by-week progression, breed drive profiles (herding/hunting/guarding energy outlets), and progress tracking with automatic plan adjustment. Use when the user asks for a dog training plan, help with a behavior problem (pulling, barking, jumping, recall failure, separation anxiety), puppy raising schedules, or wants to know why their breed behaves a certain way."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [dogs, training, behavior, puppies, obedience, pets]
---

# Dog Train-O-Matic

Most dog behavior problems are **under-exercised instinct in the wrong outlet** — a Border Collie herding children, a Beagle digging up the garden, a Husky demolishing the couch. This skill generates a personalized training program that pairs obedience work with **breed-appropriate instinct outlets**, sized to the dog's age and the owner's available minutes per day, then tracks progress and adjusts the plan weekly.

## Overview

`scripts/dog_trainer.py` combines three knowledge bases:

1. **Breed drive profiles** — what each breed group was bred to do (herding, hunting/scent, retrieving, guarding, sledding, companionship), what "enough exercise" means for that group, and which games satisfy the instinct (a Flirt Pole for sight-hound chase, nose-work puzzles for hounds, treibball-style pushing for herders)
2. **Behavior problem protocols** — evidence-based, positive-reinforcement progressions for the 12 most common problems: leash pulling, jumping on guests, recall failure, barking, digging, chewing, counter-surfing, nipping/mouthing, separation anxiety, crate training, pulling toward dogs (leash reactivity), and house soiling
3. **Age-aware structure** — puppy socialization windows (<14 weeks), adolescent regression (6-18 months — the age most dogs are surrendered), adult consistency, senior adjustments

It outputs a **week-by-week plan** with specific 5-minute exercises, success criteria for advancing, and a progress tracker that regenerates the plan when exercises plateau.

**Methods:** positive reinforcement / force-free only. No shock, prong, or alpha-roll — the modern veterinary-behavior consensus (AVSAB position) is that aversive methods increase fear and aggression long-term.

## When to Use

- "My dog pulls on the leash / barks at everything / jumps on guests / won't come when called"
- "Help me train my puppy" — especially the socialization-window scheduling
- "How much exercise does my breed need?" and "why does my dog DO that?"
- Building a multi-week plan with tracking, not one-off tips
- Rescue dog first-30-days structure (decompression period)

**Don't use for:** human-directed aggression with a bite history, severe separation anxiety (self-injury, escape injuries), or any fear presentation beyond mild — those need a certified behaviorist (CAAB/ACVB/CSAT) or vet behaviorist, possibly with medication. The tool flags these red flags explicitly and refers out.

## How It Works

1. **Profile the dog**: breed or mix, age, sex, problem list (pick from the 12 protocols), owner minutes/day, kids/other pets in home.
2. **Map breed → drive profile** → daily exercise needs (minutes × intensity), instinct outlets, and expected problem predispositions (a Jack Russell will dig; that's a feature).
3. **Select protocols** for each reported problem; each protocol is a 3-6 step progression with success criteria and per-session script cues.
4. **Compose the week**: the plan alternates protocol steps with instinct-outlet games and rest, sized to available minutes. Puppies get socialization checklist items; adolescents get "regression is normal" guardrails.
5. **Track**: log sessions (`log` command); when a step fails 3+ sessions or plateaus 5+ sessions, `plan --adjust` regenerates with remediation (easier criterion, more reps, added management).
6. **Red-flag screen**: every plan generation screens the problem list for professional-referral triggers.

## Quick Start

```bash
# A plan for an adolescent husky mix that pulls and howls
python3 scripts/dog_trainer.py plan --breed "siberian husky" --age-months 10 \
  --problems leash-pulling,barking --minutes 30

# Puppy socialization schedule (the 8-14 week window)
python3 scripts/dog_trainer.py plan --breed "golden retriever" --age-months 3 \
  --problems puppy --minutes 20

# Breed insight: what is this dog, really?
python3 scripts/dog_trainer.py breed "border collie"

# Log today's session and get tomorrow's
python3 scripts/dog_trainer.py log --step 2 --result success --note "loose leash 80% of block"
python3 scripts/dog_trainer.py today

# End-to-end sample
python3 scripts/dog_trainer.py demo
```

## Steps (Agent Workflow)

1. Collect the profile: breed/mix, age, problems, minutes/day available, household (kids? cats? second dog?).
2. Run `breed` first for the drive profile — it frames everything (a barking husky needs exercise, not a bark collar).
3. Run `plan`; read the red-flag screen with the user — refer out if triggered.
4. Walk the user through week 1 sessions explicitly: exact cue words, treat timing (mark within 0.5s), and the management changes (non-training environment edits).
5. On follow-ups, run `log` + `today`; use `plan --adjust` on plateaus.
6. Reinforce: 5 minutes daily beats an hour on Saturday. Consistency of cues across household members is the #1 variable owners control.

## Output Shape

```
TRAINING PLAN — Luna (siberian husky, 10 months, problems: leash-pulling, barking)
Red-flag screen: CLEAR (no aggression/fear triggers)

BREED PROFILE: SLED/WORKING
  Exercise floor: 90+ min/day mixed cardio; under-exercised huskies howl & destroy
  Instinct outlets: flirt pole, bikejoring, snuffle mats, structured fetch with cues

WEEK 1 (sessions are 5 min; do 2/day; total daily load ≈ 30 min incl. outlets)
  Mon  Protocol leash-pulling step 1 — 'Silence check' before door opens...
        Success: 4/5 door approaches with all-four-paws calm
  Mon  Outlet: 10 min flirt pole with obedience breaks (drop, wait)
  Tue  Protocol barking step 1 — identify triggers, log 3 barking episodes...
  ...
  Management (today, not training): front-clip harness; window film for
  passers-by; frozen KONG during work calls

ADJUST RULES: advance after 2 consecutive green sessions; if a step fails 3
sessions, drop back one criterion and double reps.
```

## Common Pitfalls

1. **Training instinct out of a dog.** You don't train a Beagle to stop sniffing; you give sniffing a job. Plans that only suppress behavior (bark collars, yelling) fail and worsen welfare. Always pair protocols with outlets.
2. **Missing the socialization window.** Puppies older than ~14 weeks have closed the easiest socialization period. For young puppies, socialization exposures outrank obedience drills in priority.
3. **Treating adolescent regression as failure.** The 6-18 month regression (previously solid recall evaporates) is developmental and temporary; plans mark it and hold criteria instead of punishing.
4. **Inconsistent cues across humans.** "Off", "down", "no jump" from different family members for the same behavior = dog learns none. Plans assign ONE cue per behavior; the whole household must use it.
5. **Sessions too long.** 5 minutes of focused reps beats 30 minutes of diminishing returns, especially for puppies. If the dog disengages, end on an easy win.
6. **Poisoning cues with frustration.** If "come!" predictably ends the fun (leash goes on, party's over), recall degrades. Protocols enforce: 8 of 10 recalls end with release-back-to-play.

## Verification Checklist

- [ ] Red-flag screen run and shown (aggression/fear/severe anxiety → refer out)
- [ ] Breed profile consulted before protocol selection
- [ ] Plan sized to actual available minutes (not aspirational ones)
- [ ] One cue word per behavior, agreed household-wide
- [ ] Management changes listed separately from training steps
- [ ] Progress logged; adjust rules explained to the owner

## One-Shot Recipes

**"My 8-month corgi nips my kids' heels when they run"**
```bash
python3 scripts/dog_trainer.py plan --breed corgi --age-months 8 --problems nipping --minutes 25
# → herding-drive outlet + kids-as-feeding-robots protocol + manage: no
#   unsupervised chase games for 3 weeks
```

**"Golden puppy arriving next week — what do I do first?"**
```bash
python3 scripts/dog_trainer.py plan --breed "golden retriever" --age-months 2.5 --problems puppy --minutes 20
# → socialization checklist scheduling (window closes ~14 wks), crate
#   foundations, name game, potty log structure
```

## References

- [`references/breed-drives.md`](references/breed-drives.md) — breed group profiles, exercise floors, instinct outlets
- [`references/protocols.md`](references/protocols.md) — the 12 behavior protocols with step criteria
