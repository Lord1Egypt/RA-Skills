# Dog Train-O-Matic 🐕

**Personalized, breed-and-age-aware dog training programs: 5-minute daily exercise progressions for the 12 most common behavior problems, paired with breed-instinct outlets, management checklists, progress logging, and red-flag referral screening.**

## The Problem

Most "problem dogs" are **under-exercised instincts looking for an outlet** — and most training advice fails because it treats the symptom instead of the drive:

- The internet's generic advice ("be consistent, use treats!") ignores that a **husky needs 90+ minutes of real cardio**, that a **beagle's sniffing is the point of the walk**, and that a **border collie needs a job, not just a jog**
- Owners get breed-inappropriate plans, fail, and conclude the dog is broken. Shelters are full of 9-month-old dogs surrendered exactly at adolescent regression (6-18 months) — a *developmental phase* that punish-first trainers turn into a crisis
- **Force-free methods have solid scientific consensus** (AVSAB: aversive tools increase fear and aggression) but owners still reach for bark collars and alpha rolls because nobody gave them a concrete alternative plan
- The puppy **socialization window closes at ~14 weeks** — irreversible — and new owners waste it waiting for "all the shots" (safe socialization protocols exist and should be used)
- Bite-history and severe-anxiety cases get DIY plans when they need certified behaviorists

## What It Does

```bash
# Plan: adolescent husky that pulls and howls, owner has 30 min/day
python3 scripts/dog_trainer.py plan --breed "siberian husky" --age-months 10 \
  --problems leash-pulling,barking --minutes 30

# What IS this dog? (drive profile before protocol selection)
python3 scripts/dog_trainer.py breed "border collie"

# Puppy's first weeks — socialization window scheduling
python3 scripts/dog_trainer.py plan --breed "golden retriever" --age-months 3 --problems puppy --minutes 20

# Track progress; get advance/retreat guidance
python3 scripts/dog_trainer.py log --step 2 --result success --note "loose leash 80% of block"
python3 scripts/dog_trainer.py today
```

Every plan includes:

1. **Red-flag screen** — bite history, aggression, severe separation anxiety, deep fear → explicit certified-behaviorist referral instead of a dangerous DIY plan
2. **Breed drive profile** — exercise floor, instinct outlets (flirt pole, nose work, treibball...), and the predispositions to expect rather than fight
3. **Criterion-laddered protocols** — 12 problems × 5-6 steps each, with exact cue wording, success criteria, and advance/retreat rules
4. **Management checklist** — environment changes that start today (the part most advice skips)
5. **Age guardrails** — puppy socialization window, adolescent regression warnings, senior adjustments

## Who Needs This

- **New dog owners** — the 8-16 week socialization sprint is scheduled and prioritized for them
- **Owners of adolescent dogs** (6-18 months) — the surrender-spike age, handled with regression-aware plans
- **Breed-first-time owners** — the "why does my husky HOWL" crowd, who need drive profiles more than discipline
- **AI agents helping with pet questions** — structured plans with referral criteria instead of dangerous confident guessing

## Method Commitment

Force-free / positive reinforcement only, aligned with AVSAB position statements. No shock, prong, choke, or dominance-theater — and explicit referral out for cases that need professionals.

## Testing

```bash
python3 scripts/test_dog_trainer.py   # 37 assertions
```

## License

MIT © 2026 Denis Voronin
