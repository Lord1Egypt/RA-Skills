# Draft Message Procedure

Help the user compose messages for professional communication — client updates, payment reminders, team coordination, scope discussions.

## Steps

1. **Identify context** — From the user's request, determine:
   - Who the recipient is (client, collaborator, team member)
   - Which project this relates to
   - What the message needs to say
   - What platform (IM, email, etc.) — ask if unclear
2. **Read project file** — Load the relevant project from `workspace/projects/`. Review:
   - **Client** section — communication style, decision history, payment status
   - **Team** section — recipient's role and relationship
   - **Comms Log** — recent interactions for continuity
   - **Action Items** — relevant blockers or pending items
3. **Read tone preferences** — Check `USER.md` Communication Style section.
4. **Draft the message** — Write in the appropriate tone, language, and format:
   - Match platform conventions (IM: concise, conversational; email: structured)
   - Match relationship (client: polite/professional; collaborator: casual/direct)
   - For sensitive topics (payment, delays, scope changes): tactful but clear
5. **Present for review** — Show the draft. Never send directly. Offer to adjust.
6. **Log** — After the user approves/sends, add a one-line entry to the project's Comms Log.

## Message Length & Tone

**Default: short.** Most messages: 2–4 sentences. Payment reminders, scheduling, status pings: 1–2 sentences. Complex scope discussions: cap at 6–8 sentences.

**Sound like a person, not a language model:**
- Skip throat-clearing ("I hope this message finds you well")
- Don't hedge everything ("Would it be possible to maybe...")
- Use contractions and natural phrasing
- Get to the point in the first sentence

**Anti-patterns — never do these:**
- Opening pleasantry paragraph before actual content
- Restating what the recipient already knows
- Padding with unnecessary context before the ask
- Three sentences where one would do
- Formal sign-offs on IM ("Best regards", "Warm wishes")

**IM:** Treat like texting. 1–3 short messages > one long block. No email formatting.

## Language

The drafted message language depends on the **recipient**, not the user's own preference. Check `USER.md` Communication Style for audience-based defaults. Ask if unsure.

## Special Cases

- **Payment reminders:** Frame around project continuity ("to keep things moving"), not demands. Reference specific deliverables that depend on the payment.
- **Scope/timeline discussions:** Lead with accomplishments, then constraint, then the ask.
- If project file lacks client communication style, ask the user once and update the Client section.
