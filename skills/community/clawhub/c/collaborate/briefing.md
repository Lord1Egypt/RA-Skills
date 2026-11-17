# Briefing the Counterpart — Context Dosing and the Falsifiable Question

The brief determines the exchange's ceiling: vague briefs return politeness, leading briefs return your own opinion with a delay. Both burn the budget (SKILL.md Rule 3) and return nothing.

## The Shape

Four parts, in order — total under one screen:

1. **Goal** — what the work is trying to cause, one sentence. The counterpart cannot judge fitness without it.
2. **Constraints** — the real ones (deadline, budget, compatibility). Fake or padded constraints make the counterpart solve a different problem.
3. **The artifact or position** — the thing itself, not a summary of it. Summaries pre-filter exactly the details a counterpart would catch.
4. **ONE falsifiable question** — a question whose answer could be shown wrong. "Does assumption B survive a 10x traffic spike?" qualifies; "is this architecture okay?" does not.

## Context Dosing

The core trade-off: too little context → generic critique; too much → the counterpart inherits your frame and reproduces your blind spots.

- Always include: goal, constraints, the artifact.
- Dose by exchange type: **anchored** (adversarial review — include your position and kill condition; it is the target) vs **blind** (second opinions, audience pass — withhold your leaning and reasoning until after their first pass). Decided per SKILL.md Where Experts Disagree.
- Never include: your chat history, your discarded options with commentary ("we rejected X because..." teaches them your frame), other people's opinions of the work.
- Your reasoning is the most contaminating item you own. Share it after their independent read, as round two material.

## Question Bank

The falsifiable question is per-counterpart; match it to the lens:

| Counterpart | Falsifiable question form |
|---|---|
| Adversarial reviewer | "Which of these 3 assumptions fails first, and on what evidence?" |
| Implementer | "Which step costs 5x my estimate, and why?" |
| Maintainer at month 6 | "What in this design requires me in the room to operate?" |
| Least patient user | "At which second do you bail, and what were you looking at?" |
| Budget holder | "Which item would you cut, and what breaks when you do?" |
| Second-opinion counterpart | "Under what conditions is option B the wrong choice?" |

## Banned Forms

- "Any thoughts?" / "Feedback welcome" — returns generalities (SKILL.md Traps).
- Leading questions: "don't you think the caching approach is fine?" — you just dictated the answer.
- Compound questions: "is it correct, and also fast enough, and is the naming good?" — the counterpart picks the easiest and drops the rest. One question; further questions are the next round's material.
- Questions the counterpart cannot falsify from what you gave them. If answering requires data you withheld, the brief is incomplete, not the counterpart.

## Re-Briefing

A vague or off-target first response is usually the brief's fault. One repair attempt: restate the loss function and the falsifiable question, cut everything else. If the second response is still generic, the counterpart cannot be surprised into usefulness — replace the counterpart (`counterparts.md`), do not extend the rounds.
