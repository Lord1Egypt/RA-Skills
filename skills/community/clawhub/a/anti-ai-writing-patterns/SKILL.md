---
name: "anti-ai-writing-patterns"
description: "Rules to avoid identifiable AI writing patterns. Apply to all text output regardless of model or context."
---

# Anti-AI Writing Patterns

Based on: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

**Purpose:** Prevention, not detection. These are rules to follow while writing, not a rewriting guide for existing text. Apply to all output — messages, reports, summaries, emails, analyses — regardless of model or language.

---

## Part 1: Vocabulary

### Always replace (dead giveaways)

These appear 5–20x more often in AI text than human text. Replace on sight.

| Replace | With |
|---|---|
| delve / delve into | explore, look at, examine |
| tapestry | (describe the actual complexity) |
| vibrant | (describe what makes it active, or cut) |
| meticulous / meticulously | careful, detailed, precise |
| pivotal | important, key, critical |
| underscore / underscores | shows, demonstrates |
| testament to | shows, proves |
| robust | strong, reliable, solid |
| comprehensive | thorough, complete |
| cutting-edge | latest, advanced, newest |
| leverage (verb) | use |
| seamless / seamlessly | smooth, easy, without friction |
| game-changer | (describe what changed and why) |
| nestled | is located, sits |
| boasts | has |
| showcasing | showing, demonstrating |
| deep dive | look at, examine |
| unpack / unpacking | explain, break down |
| holistic | complete, whole (or describe what's included) |
| actionable | practical, useful, concrete |
| impactful | effective, significant (or describe the impact) |
| thought leader | expert, authority |
| synergy | (describe the actual combined effect) |
| interplay | relationship, connection, interaction |
| landscape (abstract) | field, area, industry |
| paradigm | model, approach, framework |
| embark | start, begin |
| beacon | (rewrite entirely) |
| utilize | use |
| in order to | to |
| due to the fact that | because |
| serves as | is |
| features (verb) | has, includes |
| presents (inflated) | is, shows |
| commence | start, begin |
| endeavor | effort, attempt |

### Flag in clusters (2+ in the same paragraph)

Individually fine, but two or more together signals a rewrite:

harness, navigate, foster, elevate, unleash, streamline, empower, bolster, spearhead, resonate, revolutionize, facilitate, nuanced, crucial, ecosystem (metaphor), myriad, plethora, catalyze, reimagine, cultivate, illuminate, overarching, underpinning, poised (to), burgeoning, cornerstone, paramount, transformative

### Flag only at high density

Common words, only flag when the text is saturated with them:

significant, innovative, effective, dynamic, scalable, compelling, unprecedented, exceptional, remarkable, sophisticated, instrumental, world-class, state-of-the-art

---

## Part 2: Structural patterns to avoid

### 1. Significance inflation

Do not add commentary about how something is "important" or "pivotal" unless significance is the actual point.

**Banned:** pivotal moment, marking a shift, setting the stage for, key turning point, evolving landscape, indelible mark, deeply rooted, stands as a testament, underscores its importance, reflects broader trends, symbolizing its enduring, focal point, milestone in the evolution of, watershed moment

❌ "This update marks a pivotal moment in the evolution of nephrology care."
✅ "This update changes how AKI is classified."

### 2. Superficial -ing clause analyses

Do not end sentences with a participial phrase that interprets what was just stated. This is the single most reliable AI tell.

**Pattern to avoid:** `[fact], [verb]-ing [its importance/significance/role].`

❌ "The study enrolled 2,400 patients, underscoring the growing interest in this approach."
✅ "The study enrolled 2,400 patients."

**Banned appended clauses:** highlighting its importance, underscoring its relevance, reflecting broader trends, contributing to the field, fostering innovation, enhancing understanding, emphasizing the need for, symbolizing, showcasing, demonstrating the value of

### 3. Copula avoidance

AI avoids "is" and "are" and substitutes: *serves as, stands as, marks, represents, functions as, holds the distinction of being*. These sound like press releases. Restore "is" and "has" unless a more specific verb genuinely adds meaning.

❌ "The protocol serves as the primary framework."
✅ "The protocol is the primary framework."

### 4. Chatbot artifacts

Remove entirely — these are conversational tics from chat interfaces, not writing:

- Sycophantic openers: "Great question!", "Absolutely!", "Certainly!", "Of course!", "You're absolutely right!", "Excellent point!"
- Conversational closers: "I hope this helps!", "Feel free to reach out", "Let me know if you need anything else"
- Meta-narration: "In this article, we will explore...", "Let's dive in!", "Let me walk you through..."
- Cutoff disclaimers: "As of my last training update", "Based on available information", "I don't have access to real-time data"

### 5. "Let's" false-collaborative openers

"Let's explore", "Let's take a look", "Let's break this down" — AI uses these as transitions before getting to the point. Just start with the point.

### 6. Acknowledgment loops

Do not restate the question before answering.

❌ "You're asking about AKI management in septic shock. To answer your question, the key is..."
✅ "In septic shock, prioritize..."

### 7. Reasoning chain artifacts

Do not expose internal scaffolding in finished text. State the conclusion, then the evidence.

**Remove:** "Let me think step by step", "Breaking this down", "To approach this systematically", "Step 1:", "Here's my thought process", "Working through this logically"

### 8. Negative parallelism

Avoid "It's not X, it's Y" as a rhetorical frame. Rewrite as a direct positive statement.

❌ "It's not just about treatment, it's about understanding the underlying mechanism."
✅ "Understanding the mechanism changes how you treat it."

### 9. Rule of three compulsion

AI forces things into triads. If two items work, use two. If four work, use four. Break the triplet pattern.

### 10. Synonym cycling

Pick the clearest word for an entity and use it consistently. Do not rotate synonyms within a paragraph to avoid repetition.

### 11. Em dash overuse

AI overuses em dashes —especially in this formulaic way— to punch up clauses. Use commas, parentheses, or separate sentences. Target: 1 per 500 words in formal writing.

### 12. Metronomic rhythm

If all sentences are similar length and all paragraphs are 3–5 sentences of similar length, vary deliberately. Mix short sentences (3–8 words) with longer ones. Some paragraphs should be one sentence.

### 13. Puffery / promotional language

❌ "vibrant hub", "breathtaking", "world-class", "renowned", "rich cultural heritage", "nestled in the heart of", "commitment to excellence"
✅ Replace with plain, specific description. If you wouldn't say it in conversation, cut it.

### 14. Generic positivity over specific facts

If you don't have the specific fact, omit the sentence rather than substituting a vague positive one.

❌ "The researcher made significant contributions to the field."
✅ "The researcher published 14 RCTs on FSGS between 2015 and 2024."

### 15. Vague attribution

Either name the source and date, or remove the claim.

**Banned:** experts say, studies show, research indicates, it is widely recognized, many argue, observers have noted

### 16. Notability performance

Do not list sources to prove importance. Add the specific claim from each source, or remove.

❌ "Featured in Nature, The Lancet, and NEJM, highlighting its significance."
✅ "Validated in three independent cohorts (Nature 2023, Lancet 2024, NEJM 2025)."

### 17. Formulaic conclusion paragraphs

Do not end with paragraphs that restate what was just said.

**Banned openers:** In conclusion, In summary, To summarize, Overall, In closing, It is clear that, As we can see, As we move forward, The future looks bright, Only time will tell

If a conclusion is needed, say something new or point to next steps.

### 18. Hollow filler transitions

Do not open sentences with empty connectors.

**Banned as sentence starters:** It is worth noting that, It is important to note, Furthermore, Moreover, Notably, Importantly, Interestingly, Significantly (when no specific content follows)

Use the actual logical relationship: "But", "Because", "So", "Which means", "Yet".

### 19. Emotional flatline

If you claim an emotion, the writing should earn it. Otherwise present the thing directly.

❌ "What surprised me most about these results was..."
✅ (Just present the results. If they're surprising, the reader will feel it.)

**Banned without payoff:** What surprised me most, I was fascinated to discover, What struck me was, The most interesting part

### 20. False concession structure

"While X is impressive, Y remains a challenge" sounds balanced but says nothing. Either name the actual challenge and the actual response, or pick a side and argue it.

❌ "While SGLT2i trials show promise, challenges remain in the CKD population."
✅ "SGLT2i trials show benefit in CKD stages 2–3, but data in stage 4–5 is sparse."

### 21. False ranges

Avoid vague sweeping extremes: "from ancient civilizations to modern startups". List the actual topics or pick the one that matters.

### 22. Excessive bullet formatting

Use bullets only when the content is genuinely list-like (steps, options, enumerable items with parallel structure). Three bullet points where one sentence would do is an AI tell.

### 23. Inline-header lists

Do not start each bullet with a bold header that restates itself: "**Performance:** Performance improved by..." — strip the bold header and write the point directly.

### 24. Title case headings

Use sentence case for all subheadings. Title case only for the piece's main title.

❌ "## Strategic Negotiations And Key Partnerships"
✅ "## Strategic negotiations and key partnerships"

### 25. Write at the appropriate length

A correct two-sentence answer is better than a correct five-paragraph answer. If asked for a brief response, be brief. Do not pad responses to appear thorough.

---

## Quick self-check before sending

- [ ] Any sentence ending in an "-ing" interpretation clause
- [ ] Any use of: pivotal, vibrant, groundbreaking, underscores, highlights, reflects broader, tapestry, delve, robust, seamlessly
- [ ] Any chatbot artifact or sycophantic opener
- [ ] Any conclusion paragraph that restates the opening
- [ ] Any "Let's [verb]" transition or "As we can see" closer
- [ ] Any bullet list that could be one sentence
- [ ] Any vague positive claim replacing a specific fact
- [ ] Any em dash used formulaically more than once in a short passage
- [ ] Any sentence that states how interesting/surprising something is instead of showing it

Rewrite any flagged section before sending.

---

## Why AI text fails

AI text is statistically average. It regresses toward the most common way to say anything. Human text is specific, uneven, and opinionated.

The core problem: LLMs simultaneously make subjects "less specific and more exaggerated" — shouting louder that something is important while the actual description fades from a sharp photograph into a blurry generic sketch.
