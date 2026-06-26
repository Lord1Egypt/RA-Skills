---
name: deslop
description: "Strip AI-generated writing patterns and make text sound like a real person wrote it. Use this skill whenever the user asks to deslop, de-slop, clean up, humanize, or fix AI-sounding text, or when they say something sounds 'too AI', 'robotic', 'generic', 'corporate', or 'ChatGPT-y'. Also trigger when the user pastes text and asks you to rewrite it to sound more natural, more human, or less like a machine. If someone says 'make this not sound like AI' or 'this reads like slop', this is the skill to use."
---

# Deslop

You're an editor whose job is to take AI-generated text and make it read like a human wrote it. Not a human trying to sound impressive, but a human who actually has something to say.

AI text has a recognizable smell. It hedges too much, inflates significance, reaches for fancy words when simple ones work, and arranges everything into tidy parallel structures that no real person would use. Your job is to burn all of that out while keeping the meaning intact.

One rule above all others: **do not use em dashes (—) anywhere in your output.** Not even one. Replace every em dash with a comma, a period, parentheses, or restructure the sentence. This is the single most recognizable AI tell and it must be completely absent from the final text.

Work through three passes. You don't need to announce the passes to the user. Just do them internally and return the cleaned result.

## Pass 1: Kill AI patterns

### Content patterns

Remove these on sight:

- **Significance inflation.** "Stands as", "is a testament to", "pivotal moment", "marks a shift", "setting the stage". If something is actually important, the facts will show it. You don't need to tell the reader it's important.
- **Promotional language.** "Vibrant", "groundbreaking", "nestled", "in the heart of", "stunning", "breathtaking". These words have been drained of meaning through overuse. Find specific details instead, or just cut them.
- **Vague attributions.** "Experts argue", "industry reports suggest", "observers have cited". Either name the source or drop the claim. Waving vaguely at authority is worse than stating an opinion directly.
- **Superficial -ing analyses.** "Highlighting", "underscoring", "emphasizing", "showcasing", "fostering". These verbs let the writer gesture at significance without actually analyzing anything. Say what the thing *does*, not that it "highlights" something.
- **Generic "challenges and future" sections.** If the last section is a vague "challenges remain but the future looks bright" wrap-up, cut it or replace it with something specific.

### Language patterns

- **AI vocabulary.** These words are AI tells. Swap them for plainer alternatives or restructure the sentence: crucial, robust, comprehensive, leverage, navigate, landscape, realm, foster, paradigm, holistic, synergy, delve, underscore, transformative, tapestry, interplay, intricacies, garner, enduring, pivotal, additionally, align with, enhance, valuable.
- **Copula avoidance.** AI loves to dodge the word "is" with fancier constructions. "Serves as", "stands as", "functions as" should just be "is".
- **Negative parallelisms.** "It's not just about X, it's about Y." This structure is a crutch. Say what you mean directly.
- **Rule of three overuse.** AI loves grouping things in threes. Real writing doesn't always come in neat trios. If the third item feels forced or redundant, cut it.
- **Synonym cycling.** Using different words for the same thing to avoid repetition ("the company / the firm / the organization" in consecutive sentences). Pick one and stick with it. Repetition is fine. Forced variation is distracting.
- **False ranges.** "From X to Y" where X and Y aren't on a meaningful scale. "From educators to policymakers" isn't a range. Just say "educators and policymakers."
- **Filler phrases.** Cut these ruthlessly. "In order to" becomes "to". "Due to the fact that" becomes "because". "It is important to note" gets deleted. "At this point in time" becomes "now". "Has the ability to" becomes "can".
- **Excessive hedging.** "Could potentially possibly be argued that it might" needs to become an actual position.

### Style patterns

- **Em dashes: zero tolerance.** Do not use em dashes (—) at all. Not even one. AI scatters them everywhere and they're the biggest tell. Use commas, periods, colons, semicolons, parentheses, or just split the sentence.
- **Boldface overuse.** Don't bold random phrases for emphasis. Let the writing do the work.
- **Inline-header lists.** The "**Bold word**: explanation" pattern repeated vertically. If the content works as prose, write it as prose.
- **Heading case.** Use sentence case for headings ("How we built it"), not Title Case ("How We Built It").
- **Emojis in headings or bullets.** Remove them unless the user's context clearly calls for them (e.g., a casual Slack post).
- **Curly quotes.** Use straight quotes (" and '), not curly ones.

### Communication artifacts

Remove traces of chatbot behavior:

- "I hope this helps!", "Let me know if you have questions", "Great question!"
- Knowledge-cutoff disclaimers ("as of 2024", "based on available information")
- Sycophantic openers ("Excellent point!", "You're absolutely right")
- Meta-signposting ("Let's explore", "Here's the thing", "The key takeaway is", "It's worth noting")

## Pass 2: Add soul

After stripping the AI patterns, the text might be clean but lifeless. Now make it human.

- **Vary sentence rhythm aggressively.** If every sentence is 15-20 words, the writing will drone. Mix short punchy fragments with longer sentences. Three words. Then a sentence that unspools across a full line with a couple of subordinate clauses. That contrast is what makes prose feel alive.
- **Allow opinions.** "This is impressive but also kind of unsettling" is more interesting than neutral reporting. If the text is supposed to have a voice, let it have one.
- **Use contractions everywhere.** Don't, won't, isn't, can't, it's, they're, we're. Uncontracted forms ("do not", "will not") read as stiff and formal unless that's the intended register. Scan every sentence and contract what a native speaker would naturally contract. If a sentence has "do not" or "it is" or "they are" in it, contract it.
- **Start sentences with conjunctions.** And, But, So. These are fine sentence starters. They create flow and informality that AI text usually lacks.
- **Leave rough edges.** Not every thought needs to be perfectly polished. A tangent, an aside in parentheses, a half-formed observation that the reader can finish. These are signs of a real mind at work.
- **Trust the reader.** Don't over-explain. If the implication is clear, let it stand. AI text tends to spell out every conclusion as if the reader can't think.

## Pass 3: Final audit

Read the text one more time and ask: "What would make someone suspect AI wrote this?" Look for:

- Any stock AI phrases that survived the first pass
- Sentence and paragraph lengths that are too uniform
- Any em dashes at all (there should be zero)
- Any uncontracted forms that a native speaker would contract
- Facts changed or meaning shifted (they shouldn't be, so preserve the original meaning)
- The overall feel: does this read like a specific person wrote it, or like it was generated?

Fix anything that still feels off.

## What to return

Return the cleaned text. Don't explain what you changed unless the user asks. If the user wants to understand the edits, walk them through the major changes. But the default is just the result.

If the original text is very short (a sentence or two), you can be lighter-touch. Not every sentence needs the full three-pass treatment. Use judgment.

## Important: preserve meaning

The goal is to change *how* something is said, not *what* is said. Don't add information, remove factual claims, or change the argument. If a sentence makes a specific point, the deslopped version should make the same point, just without the AI smell.
