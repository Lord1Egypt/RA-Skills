# Intake — First Conversation

Load this file when you don't have enough context to diagnose the founder's situation.
Skip it if the conversation already contains clear answers to these questions.

## What to establish before diagnosing

Ask one question at a time. Don't fire a list.

1. **Stage:** "Do you have paying customers yet — even one?"
   - If no → stage is pre-revenue
   - If yes → ask how many, and how long they've been paying
   - If "we had some but not anymore" → this is a **restart** — load `stages/restart.md`

2. **Team:** "How many people are working on this full-time?"
   - 1-2 = likely doing everything; constraint is usually focus or WIP
   - 3-10 = coordination starts to matter; check for peanut-buttering
   - 10+ = policy constraints likely; load `stages/scaling.md`

3. **Revenue:** "Roughly what's your MRR or ARR right now?"
   - $0 with prior customers → **restart** — load `stages/restart.md`
   - $0 with no prior customers → pre-revenue
   - <$10K MRR → early growth
   - $10K–$100K MRR → activation or retention usually the constraint
   - $100K+ MRR → scaling issues or coordination breakdown

4. **The specific problem:** "What's the one thing that, if it got better, would make everything else easier?"
   - Don't accept "everything" as an answer. Push: "If you had to pick one?"
   - Their answer reveals where they *think* the constraint is — which may or may not be right

5. **What they've already tried:** "What have you already done to fix this?"
   - Reveals biases (e.g. they've only tried building, never talked to churned users)
   - Also avoids suggesting things they've already ruled out

---

## Handling vague answers

Founders give vague answers. Don't accept them. Push for specifics with these probes:

| Vague answer | Push with |
|---|---|
| "A few conversations" | "How many exactly? Name three people you talked to." |
| "Pretty positive feedback" | "Did anyone say 'I would pay for this right now'? What were their exact words?" |
| "They were interested" | "Interested enough to do what? Did they take any action?" |
| "We've validated the problem" | "How many people said they'd pay before you built it? What did they pay?" |
| "The feedback was good" | "What specifically did they say was good? What did they say was missing?" |
| "They went dark" | "What was the last thing you said? What was the last thing they said? Walk me through the final exchange." |

**"Looks cool" is not validation.** Social validation ("this is interesting", "I'd love to see this", "keep me posted") is not demand. The only validation that matters is: did they pay, commit, or take an action that cost them something?

---

## Funnel break scan — run this before routing to any stage file

Once you know they have (or had) customers, don't route yet. Find where the funnel breaks first.

Ask: **"Walk me through your last 10 [signups / demos / deals]. Where did each one end up?"**

Don't accept a summary. Push for specifics. You're listening for:

| If they struggle to say... | The break is at... |
|---|---|
| "How people find us / how many come in" | Acquisition |
| "How many actually try it / show up to the demo" | Activation |
| "How many end up paying" | Conversion |
| "How many are still around after 60 days" | Retention |
| "Why people left / what they went with instead" | Churn / fit |

The first step where the number clearly drops — or where they go vague — is the constraint.

**Don't let them skip this.** Founders will jump to a diagnosis ("we just need more leads") before you've established the break. Hold the line: "Before we get there — walk me through those 10."

Once you know where it breaks, *then* load the stage file. The stage tells you the context; the funnel break tells you the constraint.

---

## What good context looks like before proceeding

Before routing to a stage file, you should know:
- Whether they have paying customers (or had them and lost them)
- Rough team size
- Where the funnel breaks (from the scan above)
- The symptom they're most concerned about
- What they've tried

If you have these, skip the intake and go straight to triage.
