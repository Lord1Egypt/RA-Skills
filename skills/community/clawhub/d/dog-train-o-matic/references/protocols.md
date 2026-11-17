# Behavior Protocols

The 12 criterion-laddered, force-free protocols behind the plan generator. Each has 4-6 steps, a management note, and an expected duration. Advance after 2 consecutive successful sessions; drop back a step after 3 failures.

## Principles Behind Every Protocol

1. **Positive reinforcement only.** No shock/prong/alpha rolls — AVSAB's position statement links aversives to increased fear and aggression. Reward what you want; remove the payoff for what you don't.
2. **Management before training.** Change the environment first (gates, harnesses, cleanup). Every rehearsal of the wrong behavior pays it; management stops the salary.
3. **Criteria ladders.** Each step is barely harder than the last. If a step fails 3 sessions, the dog is telling you the leap was too big.
4. **One cue per behavior, household-wide.** "Off" and "down" and "no!" for jumping = three noises for nothing. Pick one word, everyone uses it.
5. **Timing: mark within 0.5s.** A clicker or a consistent "yes!" at the exact moment; treats follow within 1-2s.
6. **Short sessions.** 5 minutes of sharp reps; end on an easy win. Disengagement means the session already ran too long.

## The Protocols (summary)

| Problem | Protocol | Steps | Weeks | Core idea |
|---|---|---|---|---|
| leash-pulling | Loose-leash walking | 6 | 4 | leash tension never pays; reward at the seam |
| jumping | Four-on-the-floor greetings | 5 | 3 | install sit, make jumping boring (attention removed) |
| recall | Rocket recall | 5 | 6 | name → jackpot; 8/10 recalls release back to fun |
| barking | Bark budget & trigger work | 5 | 4 | remove payoff, thank-you protocol, distance work |
| digging | Sanctioned digging | 5 | 3 | give digging a home; redirect, never punish |
| nipping | Gentle mouth | 5 | 3 | toy-as-answer; withdrawal of play on tooth contact |
| chewing | Right thing in the mouth | 5 | 3 | trade game + drop cue + chews on schedule |
| counter-surfing | Counters are boring | 5 | 2 | counters NEVER pay (management = 80% of this one) |
| crate | Crate as bedroom | 5 | 3 | crate predicts chews; never punishment |
| separation | Alone-time confidence | 5 | 6 | micro-departures below stress latency; film it |
| leash-reactivity | Distance before drama | 5 | 8 | LAT: trigger predicts chicken; distance shrinks slowly |
| house-soiling | Potty protocol | 5 | 4 | schedule + huge outdoor rewards + enzyme cleanup |
| puppy | Foundations + socialization | 5 | 8 | exposures OUTRANK drills before 14 weeks |

Full step text lives in `scripts/dog_trainer.py` (`PROTOCOLS` dict) and is printed by the `plan` command.

## Red-Flag Referral Criteria (do NOT plan through these)

- **Any bite that broke human skin** — certified behaviorist (CAAB/CSAT) or veterinary behaviorist (ACVB)
- **Human-directed aggression** (lunging to bite, not frustration) — refer out
- **Severe separation anxiety**: self-injury, breaking teeth/nails escaping, drooling-soaked crates, hours of distress — CSAT + vet (medication is often appropriate)
- **Deep fear presentations**: shutdown, freezing, trembling beyond brief startle — behaviorist
- Sudden behavior change in an adult dog → **vet first** (pain and illness drive a surprising share of "behavior problems")

## Common Failure Modes & Fixes

| Symptom | Diagnosis | Fix |
|---|---|---|
| Progress for 2 weeks, then regression at 8 months | adolescent regression, not failure | hold criteria, keep paying, wait it out |
| Perfect at home, nothing outdoors | cue not proofed; too big a distraction leap | 3 steps back in distraction level |
| Dog performs then immediately misbehaves | paying the wrong moment — reward leaked to the wrong behavior | sharpen timing, use a marker |
| Works for trainer, not owner | owner's mechanics (timing/treat delivery) | owner does 10 slow reps with coaching |
| Protocol stalls at step N for weeks | criteria jump too big | split the step in two |
