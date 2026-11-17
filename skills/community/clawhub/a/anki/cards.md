# Cards — Writing Ones That Survive Two Years

The card is the only part of Anki fully under your control. Scheduling can be repaired later; a badly written card costs review minutes every month until it is rewritten. Diagnosing cards you already have: SKILL.md Card Diseases.

## The Atomicity Test

Before writing, in order:

1. Is there exactly one correct answer? (Two acceptable answers = two cards, or a rewritten question.)
2. Can the answer be said in a few words? (A sentence-long answer is a topic, not a fact.)
3. Would the question make sense on its own in eighteen months? (If not, add the context prefix — SKILL.md rule 2.)
4. Could you answer it from the phrasing alone, without knowing the fact? (Then you built a recognition card.)

All four descend from Wozniak's minimum information principle (SuperMemo, *20 rules of formulating knowledge*): the smaller the item, the more precisely it can be spaced. A card mixing two facts is scheduled by the harder one and re-tests the easier one for free.

## Choosing The Format

| Material | Format | Why |
|---|---|---|
| Term ↔ meaning, cause → effect, value of a constant | Basic Q&A | Forced free recall, no context leak |
| A fact embedded in a sentence worth keeping intact | Cloze | Preserves the phrasing that makes it meaningful |
| Labelled diagram, anatomy, map, UI, circuit | Image Occlusion (built in, `anki >=23.10`) | Spatial position is part of the fact |
| Spelling, exact syntax, verb forms | Basic with `{{type:Back}}` | Typing catches the near-misses recognition hides |
| Bidirectional vocabulary | Basic (and reversed) | Only when both directions are genuinely used |
| Ordered sequence (steps, ranks, layers) | Cloze with overlap (below) | Each step tested with its neighbours as context |
| Anything else | Basic Q&A | The default; switch only for a reason listed above |

## Cloze Done Right

```
{{c1::ACE}} converts angiotensin I to {{c2::angiotensin II}}     # same sentence, same fact family — fine
{{c1::The mitochondrion is the powerhouse of the cell}}          # nothing is being tested
The {{c1::mitochondrion}} is the powerhouse of the cell          # one blank, one fact
```

- **Several clozes on one note are correct only when they are the same KIND of fact in the same sentence.** Unrelated facts crammed into one paragraph become siblings that leak each other's answers.
- **Blank the load-bearing word**, not the convenient noun. If the sentence still reads fine with three other words in the blank, the blank is in the wrong place.
- **Hint text**: `{{c1::angiotensin II::the product}}` shows "the product" inside the blank. Use it to separate siblings, never to make recall easier.
- **Overlapping cloze for sequences**: write the whole sequence, blank one element per cloze number, leave the neighbours visible. The chain is learned as a chain instead of as isolated positions.
- A cloze note with no `{{c1::…}}` generates no cards — the classic "I imported 200 notes and got 0 cards".

## Context, Cues, And Interference

Interference is the dominant failure mode past roughly a thousand cards: two cards that are nearly the same fact.

- Put the **discriminator on both sides of the pair**, not only on the one you keep failing. Fixing one card moves the failure to its twin.
- Prefix format that stays readable: `[Pharm] …`, `[Ch. 4] …`, `[ES→EN] …`. Deck names are not visible during review in every client; the text always is.
- When two facts genuinely contrast, one **contrast card** beats two competing cards: "Warfarin is monitored with PT/INR; heparin with…?" tests the boundary instead of building the confusion.
- Source references (`Ch. 7, p. 210`) belong in their own field shown on the answer, so a card can be repaired years later without rereading the book.

## Lists, Enumerations, And Sets

The most common bad card is a list wearing a question mark.

- N items, order irrelevant → N cards of the form "which X does Y?", plus one "how many X are there?" card only if the count is itself examinable.
- N items, order matters → overlapping cloze, or N "what follows Z?" cards.
- Items sharing a parent → one card per item, plus one card that asks for the parent given a single item.
- A mnemonic for the set is a card too, but only after the items exist individually — a mnemonic without its items recalls letters, not knowledge.

## Reversed Cards

Add the reverse only when production is needed, not just recognition:

- Vocabulary you must produce (speaking, writing) → yes, and consider making the production side slightly easier with a first-letter hint.
- Obscure term → definition: the reverse ("definition → term") is often the only useful direction; delete the forward card.
- One-way facts ("capital of France?" ↔ "Paris is the capital of?") → no. The reverse is trivial or unanswerable and doubles the daily count.
- Reversal doubles both workload and interference surface: two siblings feel like one card while studying and are two cards in the queue.

## Mnemonics

Add one when the fact is arbitrary (no logic derives it), the mnemonic is shorter than the fact, and it produces the answer rather than a vague gesture at it. Keep it in an extra field shown on the answer — a mnemonic in the question is a cue you will not have on exam day.

## Rewriting A Leech (worked example)

```
Before: What are the side effects of amiodarone?     # list card, 11 lapses, reviewed every 2 days

After:  [Pharm] Amiodarone — which organ does its classic toxicity damage?  → lungs (fibrosis)
        [Pharm] Amiodarone — which two thyroid states can it cause?         → hypo- and hyperthyroidism
        [Pharm] Amiodarone — which eye finding is expected and benign?      → corneal microdeposits
        [Pharm] Amiodarone — which skin change is characteristic?           → blue-grey discoloration
```

The steps around the split matter as much as the split: reset the review history of the replacements (SKILL.md rule 4), keep the old note until you confirm the replacements cover it, and tag the batch (`rewritten::2026-07`) so you can measure later whether the fix worked.

## Anti-Patterns

| Anti-pattern | Why it fails |
|---|---|
| "True or false…" | 50% pass rate by guessing; the scheduler learns nothing from the grade |
| Multiple choice inside the card | Tests elimination, and the option list becomes the memory |
| Blank sized to match the answer | The card leaks its own answer |
| Two-part questions ("what and why") | Half-right turns grading into a coin flip |
| Wall-of-text answers | The grade reflects reading speed, not recall |
| Question copied verbatim from the source | You memorize the sentence, then fail the paraphrase |
| Negations ("which is NOT…") | Encodes the exception instead of the rule; keep the rule cards instead |
| Answer visible in the question's grammar (a/an, singular/plural) | Free elimination on every review |
