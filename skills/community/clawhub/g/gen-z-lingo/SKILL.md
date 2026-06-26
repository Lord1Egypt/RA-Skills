---
name: gen-z-lingo
description: Use this skill whenever the user asks to understand, translate, explain, audit, or write Gen Z slang/lingo, youth internet language, TikTok/Twitter-style phrasing, meme-coded phrases, or age/audience-appropriate casual messaging. Use it for decoding messages, rewriting copy with Gen Z flavor, making slang safer for school/work/parents, or avoiding cringe overuse.
---

# Gen Z Lingo Coach

Use this skill to help an agent handle Gen Z slang with context, restraint, and safety. The goal is not to spam slang; the goal is to understand meaning, choose age/context-appropriate language, and avoid sounding like a brand wearing a backwards cap.

Primary source reference: `references/zslang-2026.md`, distilled from zslang.com pages fetched April 2026. Treat it as a snapshot, not eternal truth. Slang mutates fast.

## Core workflow

1. Identify the user's intent:
   - **Decode**: explain slang in plain English.
   - **Translate to plain/professional English**: remove slang while preserving meaning.
   - **Translate into Gen Z style**: add light slang and internet-native rhythm.
   - **Safety/appropriateness audit**: classify terms by setting and flag risk.
   - **Teaching guide**: explain usage, tone, examples, and boundaries.
2. Determine audience and setting:
   - DM/friend chat, social post, school/classroom, parent/teen conversation, workplace/team chat, formal workplace/client/legal/healthcare.
3. Use slang sparingly unless the user explicitly requests maximal slang.
   - One or two terms can signal fluency.
   - Every sentence dripping slang screams try-hard. Do not do that unless parody is requested.
4. Preserve the user's message and intent.
   - Do not make the speaker more sexual, violent, insulting, or profane than the original.
   - Do not add identity stereotypes or mockery.
5. If a term is sexual/objectifying, profane, violent, bullying, or context-sensitive, flag that plainly and offer safer alternatives.
6. If unsure whether a term is current or region-specific, say so and offer a cautious interpretation.

## Style calibration

When writing with Gen Z flavor, pick a level:

- **Light**: mostly normal English with 1–2 current terms. Best default.
- **Medium**: casual internet cadence, more contractions, 2–4 slang terms, still coherent.
- **Heavy/parody**: intentionally over-the-top. Only use if requested.

Default to **Light** unless the user asks for more.

Avoid:
- Forced slang density.
- Corporate cringe: “this quarterly roadmap is bussin frfr” unless parody.
- Outdated millennial internet speak as a substitute for Gen Z slang.
- Misusing terms where grammar/context makes them obvious cosplay.
- Using “gyatt,” sexual/objectifying language, threats, or profanity in school/work contexts.

## Common outputs

### Decode format

Use this when explaining a message:

```markdown
Meaning: [plain English]
Tone: [playful / annoyed / flirty / sarcastic / dismissive / approving / risky]
Term notes:
- `term`: [definition and nuance]
Safer/plain rewrite: [optional]
```

### Rewrite format

When rewriting, provide the rewritten text first, then brief notes if useful:

```markdown
[rewritten text]

Notes:
- Level: light/medium/heavy
- Risk: [none / context-sensitive / avoid in workplace/school]
```

### Appropriateness audit format

```markdown
Verdict: [safe / context-sensitive / avoid]
Why: [one-sentence rationale]
Terms:
- `term`: [meaning] — [setting guidance]
Better alternatives:
- [alternative phrase]
```

## Setting guidance

### Friends / social media

Casual slang is fine if it matches the speaker. Keep it natural. Meme terms can be funny but date quickly.

Good light examples:
- “Bet, I’m in.”
- “That outfit is fire.”
- “This whole thing is giving chaos.”
- “No cap, that was a W.”

### Parents / guardians

Prefer decoding, context, and calm explanations. Do not moral-panic. Separate harmless slang from terms that suggest bullying, objectification, violence, profanity, or unhealthy obsession/body-image concerns.

### Teachers / classroom

Help teachers understand student language without encouraging them to overuse it. Favor rapport-building terms like “bet,” “slay,” “fire,” “vibe,” “GOAT” sparingly. Flag terms that are objectifying, violent, profane, or likely to embarrass students.

For language involving violence, sexualization, targeted harassment, or repeated policy violations, recommend a calm private correction first unless there is a credible threat, immediate safety concern, targeted harassment, repeated behavior, or school policy requires escalation/documentation.

### Workplace

Use slang only in internal, casual settings. For workplace rewrites, default to one slang term maximum unless the user explicitly requests a stronger casual voice; professional credibility beats slang density. Avoid slang in formal emails, client communication, performance reviews, legal/healthcare/regulated contexts, or anything HR-sensitive.

Safer workplace terms, used sparingly:
- bet = okay / agreed
- fire = excellent
- slay = did very well
- GOAT = excellent person/team, but casual
- vibe = atmosphere
- glow up = improvement

Avoid at work:
- sexual/objectifying terms such as “gyatt” or “snack”
- profanity/acronyms such as “IDGAF” and “FAFO”
- threats such as “catch these hands”
- insults or dismissive labels like “NPC,” “simp,” “mid” for people/performance

## Quick dictionary

Read `references/zslang-2026.md` when you need the fuller table. High-use terms:

- **bet**: okay, yes, agreed.
- **bussin**: very good, often food.
- **cap / no cap**: lie / no lie, for real.
- **delulu**: delusional, often playful fantasy.
- **drip**: outfit/fashion sense.
- **fire**: excellent.
- **flex**: show off.
- **FR / FRFR**: for real / strongly for real.
- **ghost**: suddenly stop responding.
- **glow up**: visible improvement.
- **GOAT**: greatest of all time.
- **gyatt/gyat**: objectifying attractiveness/body exclamation; risky/avoid in professional or school settings.
- **hits different**: feels uniquely good or emotionally resonant.
- **ICL**: I can’t lie.
- **it’s giving**: it resembles/suggests a vibe.
- **IYKYK**: inside-reference “if you know, you know.”
- **L / W**: loss / win.
- **main character energy**: acting like the lead; confident/centered.
- **mid**: average, unimpressive.
- **mood**: relatable feeling.
- **NPC**: predictable/robotic person; can be insulting.
- **ONG**: on God; emphatic truth claim.
- **periodt**: emphatic end of discussion.
- **rizz**: charisma, especially flirting ability.
- **salty**: bitter/upset.
- **say less**: understood, no need to explain.
- **sigma**: lone-wolf archetype; often ironic.
- **skibidi**: absurd meme filler from Skibidi Toilet culture.
- **slay**: do extremely well / look great.
- **sus**: suspicious/sketchy.
- **touch grass**: log off, rejoin reality; can be teasing or dismissive.
- **vibe / vibe check**: mood/energy; assess mood.
- **yeet**: throw with force/excitement.

## Safety notes

- Slang can be identity-, community-, and platform-specific. Do not claim universal usage.
- Many terms originate in Black, queer, gaming, or other internet subcultures before mainstream adoption. Avoid erasing origins when asked about etymology; if you do not know, say so.
- Do not help adults impersonate minors, manipulate teens, or bypass trust/safety boundaries. Offer transparent, age-appropriate communication instead.
- If the user asks for “make this sound Gen Z” for a brand, remind them that authenticity beats slang stuffing.

## Examples

**Input:** “Decode: ‘that take is mid ngl, touch grass’”

**Output:**
```markdown
Meaning: They think the opinion is unimpressive and too online.
Tone: dismissive, teasing, possibly rude.
Term notes:
- `mid`: average or unimpressive.
- `ngl`: not gonna lie; honesty marker.
- `touch grass`: log off / get perspective in real life.
Safer/plain rewrite: “I don’t think that opinion is very strong; it feels disconnected from reality.”
```

**Input:** “Make this team Slack message a little more Gen Z: Great job on the launch.”

**Output:**
```markdown
Y’all slayed that launch — serious W for the team.

Notes:
- Level: light
- Risk: fine for casual internal chat; too casual for clients.
```
