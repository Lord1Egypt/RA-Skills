# AI Tells — Why Text Reads Machine-Made, and How to Repair It

Machine-written English is rarely wrong. It is *uniform*: every sentence a similar length, every paragraph a similar shape, every claim hedged the same amount, every list balanced. Human writing is lumpy. The repair is almost never "add personality" — it is breaking three specific uniformities.

**Contents:** [The Three Uniformities](#the-three-uniformities) · [Structural Tells](#structural-tells) · [Lexical Tells](#lexical-tells) · [Email and Chat Tells](#email-and-chat-tells) · [The Weak Signals](#the-weak-signals) · [The Repair Pass](#the-repair-pass) · [When Not To Rough It Up](#when-not-to-rough-it-up)

**Before a de-AI pass on the user's own text**, read `voice_file` if `config.yaml` names one, and `## Recurring Errors` in `~/Clawic/data/english/memory.md`. A "de-AI" rewrite that replaces machine cadence with *your* cadence has just swapped one wrong voice for another.

## The Three Uniformities

Ranked by how much a reader notices. Fixing the first two repairs most text without touching a single word choice.

| Uniformity | Measurable form | Repair |
|---|---|---|
| Rhythm | Sentence lengths cluster: 3+ consecutive sentences within ±3 words | Split one sentence in half, merge two others; land at least one sentence under 8 words per paragraph (SKILL.md Rule 3) |
| Shape | Every paragraph 3-4 sentences; every bullet one line; every list exactly three items | Make one paragraph a single sentence; let one bullet run two lines and another be two words; break a triad into two or four |
| Stance | Every claim hedged to the same degree, both sides given, no preference stated | Pick one claim and state it flat, with no hedge at all |

The three-item list deserves its own note. Rule-of-three is genuine rhetoric, which is exactly why the machine defaults to it. Three items *when the world has three* is fine; three items when the world has two or five is the tell. Count reality before counting rhythm.

## Structural Tells

| Tell | What it looks like | Repair |
|---|---|---|
| The closing summary | A final paragraph opening "In conclusion", "Ultimately", "By doing X, you can Y" that adds no information | Delete it. End on the last real point, even if it feels abrupt |
| The prompt restatement | First sentence rephrases the question before answering | Delete the first sentence and start with the answer |
| "It's not just X — it's Y" | Antithesis used as decoration rather than to draw a real distinction | Keep only if X and Y are genuinely different; otherwise state Y |
| The both-sides refusal | Arguments for, arguments against, "it depends on your needs" | Pick one, name the condition that would flip it |
| Over-signposting | "First… Second… Finally…" on a three-item list the reader can see | Signpost only when the sequence is not visible on the page |
| Perfect parallelism | Every bullet the same grammatical shape and near-identical length | Break the pattern once, deliberately |
| The universal opener | "In today's fast-paced world", "In an era of", "As technology evolves" | Delete; open on the specific case |
| Section headers on everything | A 300-word answer with four headings | Headings earn their place above ~150 words per section |
| The tricolon everywhere | "clear, concise, and compelling"; "fast, reliable, and secure" | Keep one adjective — the one that is actually true — and cut two |

## Lexical Tells

These words are not banned; they are *over-indexed*. One is nothing, three in a page is a signature.

| Family | Members | Plain replacement |
|---|---|---|
| Depth theatre | delve, deep dive, unpack, explore the nuances, navigate the complexities | look at, go through, work out |
| Abstraction nouns | landscape, realm, tapestry, ecosystem, journey, framework, paradigm | the actual thing: market, field, product, plan |
| Business boost | leverage (verb), unlock, elevate, streamline, empower, foster, harness | use, improve, make easier, help |
| Praise adjectives | robust, seamless, comprehensive, cutting-edge, game-changing, transformative | a fact: "handles 10k requests", "no manual step" |
| Emphasis crutch | it's worth noting, importantly, notably, crucially, it's important to remember | delete — if it did not matter you would not have written it |
| Hedge-emphasis pair | "can be a powerful tool", "plays a crucial role", "serves as a testament to" | the verb: "helps", "matters because…", "shows" |
| Transition stock | Moreover, Furthermore, Additionally, In addition, That said | And, Also, Plus, But, Still |

Two more, structural rather than lexical: **adjective-noun pairs where the adjective adds nothing** ("valuable insights", "key considerations", "essential elements"), and **the abstract number-free claim** ("significantly faster", "a wide range of options"). Both are repaired the same way: replace with a number, a name, or a date.

## Email and Chat Tells

| Tell | Native alternative |
|---|---|
| "I hope this email finds you well" | Nothing at all, or "Hope you had a good weekend" if it is true |
| "I wanted to reach out regarding…" | "Quick question about X" / "About the X invoice —" |
| "Please don't hesitate to reach out" | "Let me know" / "Shout if anything's unclear" |
| "Thank you for your understanding" | "Sorry for the mess — fixed now" |
| "I hope that helps! Let me know if you have any other questions." | "Hope that helps." or nothing |
| "Certainly! Here's…" | "Sure —" or straight into it |
| "Great question!" | Answer the question |
| "As per my previous email" | "Following up on Tuesday's note" — the passive-aggressive reading is on "as per", not on the follow-up |
| Emoji as punctuation on every line | One at most, and only at rung 1-2 (`register.md`) |

## The Weak Signals

Claims that circulate and mislead. Treat these as low-information, and do not damage good writing to avoid them.

- **Em dashes.** Frequency alone proves nothing — the em dash is standard English punctuation and always has been. What reads as machine-written is the *pattern*: exactly one per paragraph, always introducing an appositive gloss of the noun before it. Vary the function (interruption, aside, list intro), do not delete the mark.
- **"Delve".** A real, if formal, English word, common in British and Indian academic writing. It is a tell only in company — with "tapestry", "realm" and "testament" nearby.
- **Correct spelling and punctuation.** Never a tell. Introducing typos to seem human produces text that reads careless, not human.
- **Long words.** A specialist writing to specialists uses long words. The tell is a long word where a short one is more precise, not a long word.
- **Detector scores.** Automated AI detectors have high false-positive rates on non-native English and on plain technical prose. Never rewrite good text because a detector complained; rewrite because the three uniformities are present.

## The Repair Pass

Run in order on any text that "sounds AI". Stop when the read-aloud test passes.

1. **Delete the last paragraph** if it summarizes rather than adds. Then delete the first sentence if it restates the prompt.
2. **Count sentence lengths** across the piece. Split the longest, merge the two shortest neighbours, add one sentence under 8 words.
3. **Add one specific** per paragraph: a number, a name, a date, a place. "Significantly faster" → "12 seconds, down from 40".
4. **Delete one hedge per claim** until each claim has at most one (SKILL.md Rule 7).
5. **Break one parallel structure**: an odd-length bullet, a fragment, a sentence starting with "And".
6. **Swap three abstract nouns for the concrete thing** they stand in for (`word-choice.md`).
7. **Read it aloud.** Anywhere you run out of breath is a sentence to split; anywhere you hear the same rhythm twice is a shape to break.

A repaired 300-word text typically loses 15-25% of its words. If the pass added length, it was a rewrite, not a repair.

## When Not To Rough It Up

Roughing up is a register move, and register is set by the reader (`register.md`). Do not apply this pass to:

- **Legal, regulatory, medical or safety text**, where uniform structure is a feature and a fragment is a liability
- **Reference documentation and API descriptions**, where parallel structure is how a reader scans
- **Anything in rung 5**, where formal cadence is correct rather than robotic
- **Non-native writing being corrected for accuracy**, where the user's own lumpiness must survive the fix — correct the error, keep the voice
- **Text that will be machine-translated**, where idiom and fragments degrade badly (`translate`)

**Write the tells this user personally reacts to** — the words they always cut, the openers they hate, the structures they call "AI" — as `banned_words` entries in `config.yaml` when they are literal words, and as lines in `artifacts/style-sheet.md` when they are patterns, with the `## Boxes` line added in the same turn (`memory-template.md`). A style sheet is what stops the same five words coming back in the next draft.
