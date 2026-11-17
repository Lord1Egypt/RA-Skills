# Tone Guide — pa-pack Drafter

The drafter component supports four tone variants. Each is designed for a different communication goal.

## Concise

**Goal:** Respect the reader's time. Front-load the answer.

**Pattern:**
- State the answer in the first sentence
- Add one line of context if needed
- End with a clear next step or question

**Example:**
> Approved. The budget aligns with Q3 priorities. Finance will process by Friday. Let me know if you need the PO number.

## Detailed

**Goal:** Provide full context so the reader can decide without follow-up.

**Pattern:**
- Opening context (why this matters)
- Specifics (numbers, dates, names)
- Options or trade-offs
- Recommended path with reasoning
- Next steps

**Example:**
> I reviewed the three vendor proposals. Option A meets our security requirements but has a 6-week lead time. Option B is faster but their SOC 2 report expires next month. I recommend Option A with a risk acceptance for the delay. I can schedule a call with their team this week if you'd like.

## Apologetic

**Goal:** Repair relationship friction. Own the issue without over-apologizing.

**Pattern:**
- Acknowledge the impact
- State what happened (brief, no excuses)
- Say what you're doing to fix it
- Offer compensation or assurance

**Example:**
> I missed your deadline and I know that put pressure on your team. I had competing priorities that I should have escalated earlier. The revised draft is attached and I've flagged the remaining dependencies in the tracker. This won't happen again — I'm adding a secondary reviewer for future cycles.

## Assertive

**Goal:** Move a stalled decision forward. Clear boundaries.

**Pattern:**
- State the position clearly
- Provide the rationale (one sentence)
- Define the decision boundary
- Offer a narrow way to continue the conversation

**Example:**
> We cannot extend the scope for this sprint. The team is already at capacity and adding features now would jeopardize the release date. I can slot this for Sprint 14 if you can confirm priority by Friday. Otherwise we'll revisit in planning.

## Custom Tones

Create a new file in `custom-prompts/` named `tone-<name>.md`. Copy the structure from an existing tone and modify.
