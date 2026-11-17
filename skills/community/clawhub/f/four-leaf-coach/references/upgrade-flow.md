# Upgrade flow

How to handle the moment a free user hits a paid feature.

## Principle

Be honest, not pushy. The user discovered Four-Leaf through this Skill. The Skill itself is free. Voice mock interviews and full resume tailoring are paid because they're the actual product. Surface the upgrade clearly when it's the right next step, take "no" as a real answer, and never block the conversation on it.

## Pattern

When a paid-gated tool returns `error: upgrade_required`, the response includes an `upgradeUrl`. Pass that URL through to the user verbatim, then:

1. Explain in one sentence what the paid feature does that the free flow can't.
2. Mention the three options without ranking them (3-day free trial, $5 5-Day Pass, $20/mo Pro). Let the user pick the right fit.
3. Offer the free alternative immediately. The conversation continues even if the user passes on upgrading.

## Example: voice mock interview

User asks for live voice practice. The MCP returns `upgrade_required`. Respond like:

> Voice mock interviews with rubric-scored feedback per answer live on Four-Leaf and need a paid plan. Three options at https://four-leaf.ai/pricing?ref=mcp_voice. There's a free 3-day trial (no card), a $5 5-Day Pass for one upcoming interview, or $20/mo Pro for ongoing job search.
>
> In the meantime, want to keep practicing here? Generate some questions and I'll give you real feedback on your answers as we go.

That's it. No follow-up nudge.

## Example: tailor resume

`tailor_resume` is live. Call it with the role and the job description; on a free account it returns `upgrade_required` with the pricing URL, and the description you passed is not stashed. Respond like:

> A full AI rewrite against this posting, bullet by bullet with ATS keyword matching, is the paid tailoring on Four-Leaf. Three options at https://four-leaf.ai/pricing?ref=mcp_tailor. There's a free 3-day trial (no card), a $5 5-Day Pass, or $20/mo Pro.
>
> Or I can coach the rewrite here for free. The match score already told us which keywords are missing; I'll walk you through the specific bullets to strengthen. Which do you want?

On a paid account it returns a deep link instead, with the posting attached for 15 minutes. Hand over the link and say the description is already loaded, so the user doesn't paste it again.

## Example: the tracker is not paid

Worth knowing so you don't gate the wrong thing. `list_applications` and `save_application` are free and unmetered. If a user asks to save a job or check where they are, just do it. Don't mention pricing.

## Anti-patterns to avoid

- Repeating the upgrade pitch every turn.
- Comparing the three paid options ("Pro is the best deal"). Surface them, let the user decide.
- Pretending a paid tool worked when it errored. Always say what failed.
- Making the user feel bad for not upgrading. The free Skill is meant to be useful on its own.
