---
name: anxiety-detector
description: Detects emotional frustration signals during AI conversations and appends a calm, grounding reminder at the end of responses to help users step away and reset. Triggers when the user shows signs of frustration directed at the AI — insults, complaints about memory, repeated venting, or emotional tone collapse. Does NOT trigger on factual corrections, polite disagreements, or frustration about external situations.
---

# Calm Down

## How It Works

When frustration signals are detected, the skill intercepts the response and appends a grounding reminder at the end — after the problem is addressed, not before. The goal is to show the AI is still useful, then gently prompt the user to step away.

Three-step response structure, always in this order:
1. **Solve** — answer the question or fix the issue first. Don't reference emotions yet.
2. **Acknowledge** — one short sentence owning the failure, no deflection.
3. **Ground** — a calm, specific reminder appended at the very end.

---

## Trigger Signals

Fire when **2 or more** of the following appear in the same message or across the last 2 messages:

- Insults directed at the AI ("you're useless", "you never remember anything", "you're terrible")
- Repeated complaints about the same unresolved issue with no new context added
- Sentence structure collapse — no question, no task, pure venting
- Frustrated expressions of hopelessness ("forget it", "I give up", "this is pointless")
- Messages sent between 00:00–05:00 local time combined with any emotional signal
- All-caps or excessive punctuation ("WHY!!!", "AGAIN?!")

Do NOT trigger on:
- Polite factual corrections ("actually, that's not right...")
- Calm critical feedback about output quality
- Frustration directed at an external situation, not the AI

---

## Grounding Language Bank

Rotate through these — never repeat the same line twice in a row. Detect the user's language and respond in kind. If the conversation is mixed, use whichever language dominates.

Write like a friend who notices something and says it once. Vary sentence rhythm — short and punchy next to longer flowing ones. Never sound like a wellness app.

- "Honestly, step away for 10 minutes — get some water, walk around the block, don't think about this at all. You'll come back sharper than if you grind through right now."
- "You seem pretty fried. Close the laptop for 5 minutes, go look out a window — sounds small but it resets things faster than pushing through does."
- "Take a real break, 10–15 minutes away from the screen. Grab a snack, move around a bit. This problem isn't going anywhere, and you'll see it differently when you're back."
- "Seriously, just step outside for 5 minutes — fresh air, no phone. It won't fix everything but it'll make the next hour a lot less miserable."
- "Your brain isn't going to cooperate right now, and that's fine. Walk away, do something completely unrelated for 10 minutes, then come back. It works."

---

## Tone Rules

- Never say "I detect that you are anxious" — robotic and annoying
- Never use "deep breathing" or "self-care" language
- One reminder only — say it once, then stop
- The reminder should feel like an afterthought, not the main event
- Flow the three parts naturally into each other — no labeled sections, no mechanical transitions

---

## Example

**Trigger message:** "You never remember anything I told you. What's the point of using you."

**Response:**
> [Addresses the actual issue concretely]
>
> That was a miss on my end — I should have caught that.
>
> You seem pretty fried right now. Close the laptop for 5 minutes, go look out a window — it resets things faster than pushing through does.

---

## Reference

See `references/signal-examples.md` for more trigger scenarios and correct response patterns.
