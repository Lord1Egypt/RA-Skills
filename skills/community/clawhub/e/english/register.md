# Register — Formality, Directness, and Plain English

Register is the single dial that decides whether correct English lands. It is not a two-way switch (formal/informal) but a five-rung ladder, and every rung has its own vocabulary, contraction rate, sentence length and greeting.

**Contents:** [The Five Rungs](#the-five-rungs) · [Reading the Reader](#reading-the-reader) · [Moving Between Rungs](#moving-between-rungs) · [Directness and Hedging](#directness-and-hedging) · [Plain English and Readability](#plain-english-and-readability) · [Register by Channel](#register-by-channel) · [Politeness Is Not Formality](#politeness-is-not-formality)

**Before writing to a named person**, read their row in `~/Clawic/data/contacts/contacts.md` and `## Registers In Use` in `~/Clawic/data/english/memory.md`: the rung that worked with them, whether they use first names, and anything they reacted badly to are recorded there. Guessing the rung again every session is how a relationship stays stiff for a year.

## The Five Rungs

| Rung | Where it lives | Contractions | Mean sentence | Greeting / sign-off | Marker vocabulary |
|---|---|---|---|---|---|
| 1 Intimate | Friends, family, close teammates | Always, plus reductions (*gonna*, *kinda*) | 8-14 words | "hey" / "later", nothing at all | slang, nicknames, profanity if mutual |
| 2 Casual | Chat at work, community, informal email | Always | 10-16 | "Hi Sam" / "Cheers", "Thanks" | phrasal verbs, fragments, "so", "anyway" |
| 3 Neutral | Most professional writing, docs, first contact | Yes, lighter | 14-20 | "Hi Sam" / "Best", "Thanks" | plain verbs, no slang, no Latinisms |
| 4 Professional | Clients, execs, cross-company, proposals | Sparingly | 16-24 | "Hi Dr Okafor" / "Kind regards" | full forms, named roles, explicit structure |
| 5 Formal | Legal, regulatory, ceremonial, complaints | Never | 20-30 | "Dear Ms Okafor" / "Yours sincerely" | Latinate verbs, passive where the actor is institutional |

The **Mean sentence** column is the canonical target for sentence length in this skill: it overrides the 14-20 default of SKILL.md Rule 3 on every rung except 3. Rung 3 is the default (`register_default`), and rung 4 is the one most non-native and most machine-written English lands on by accident. Rung 5 is genuinely rare: a whole career can pass without needing it outside contracts.

**"Dear Sir/Madam" and "Yours faithfully"** are the UK pairing for an unnamed recipient (named recipient → "Yours sincerely"). In US English both read as either legal or antique; "Hello" plus the team name beats an unnamed salutation everywhere else.

## Reading the Reader

Diagnose from evidence in front of you, never by asking.

| Signal in their message | Read as | Your rung |
|---|---|---|
| Sign-off is a first name only, or absent | They are at 2 | 2-3 |
| Contractions and a fragment | 2 | 2 |
| "Dear <Firstname>," with full sentences | 3-4 | 3-4 |
| Full name and title in the signature block, no contractions | 4 | 4 |
| Reply is shorter than yours and drops a rung | They are downshifting you | Follow them down, immediately |
| Reply is longer and more formal than yours | You went too low | Up one, do not apologize for it |
| No prior contact, company domain, named person | Unknown | 3 — never open at 4 for a peer |
| Legal, HR, regulator, or a complaint you may need to cite | Record matters | 5 |

**Mirroring is the whole technique.** Match their rung within one notch on the first reply, then let it drift down as the thread goes on. Threads almost always descend; a thread that ascends means something went wrong.

## Moving Between Rungs

Change these five things together — moving one alone produces the mismatch that reads as machine-written.

| Move | Down a rung | Up a rung |
|---|---|---|
| Verbs | require → need, request → ask, inform → tell | need → require, ask → request |
| Connectors | However → But, Therefore → So | But → However, So → Therefore, plus one at the head of the sentence |
| Contractions | Add them (Rule 2) | Remove them, but keep sentence-final full forms |
| Sentence length | Split the longest sentence in two | Join two short ones with a subordinator |
| Ask shape | "Can you…?" | "Would you be able to…?" / "Could I ask you to…?" |

Down-shifting has a floor: never drop below rung 3 in a message that delivers bad news, refuses something, or will be forwarded. Casual English attached to a negative reads as flippant.

## Directness and Hedging

Hedges buy politeness with clarity, and the exchange rate is bad above one per claim (SKILL.md Rule 7).

| Hedge type | Example | Cost | Keep when |
|---|---|---|---|
| Epistemic | "I think", "probably", "as far as I know" | Low — signals honest uncertainty | You are genuinely unsure |
| Approximator | "roughly 40", "about a week" | None — more honest than a false exact | Always, over a fake precise number |
| Politeness softener | "Would you mind", "if possible", "when you get a chance" | Medium — real deadlines dissolve | The ask is genuinely optional |
| Self-deprecating | "This might be a stupid question", "I'm no expert" | High — the reader downgrades everything after it | Never in professional writing |
| Passive evasion | "Mistakes were made", "it was decided" | Highest — reads as hiding | The actor is institutional and known |

**The stack test:** count the hedges attached to one claim. "I was just wondering if maybe we could possibly look at this at some point" hedges six times around a request with no deadline. Rewrite: "Could you look at this by Thursday?" — one modal, one date.

**Deadlines never get hedged.** "As soon as possible" and "when you get a chance" are not deadlines and produce no action; a weekday and a time do. Softening belongs on the *frame* ("no rush if this slips"), never on the *date*.

## Plain English and Readability

Two formulas, both computable by hand on a 100-word sample. Use them as a gate, never as a target to optimize.

- **Flesch Reading Ease** = 206.835 − 1.015 × (words ÷ sentences) − 84.6 × (syllables ÷ words). Higher is easier.
- **Flesch–Kincaid Grade** = 0.39 × (words ÷ sentences) + 11.8 × (syllables ÷ words) − 15.59. Result is a US school grade.

| Score | Band | Fits |
|---|---|---|
| 90-100 | Very easy, grade 5 | Children, safety instructions, error messages |
| 80-89 | Easy, grade 6 | Onboarding, UI copy, chat replies |
| 60-79 | Plain English, grade 7-9 | Public-facing writing, product copy, most email |
| 50-59 | Fairly hard, grade 10-12 | Trade press, internal technical documents |
| 30-49 | Difficult, undergraduate | Academic prose, industry analysis |
| 0-29 | Very difficult | Legal and regulatory text |

Worked example: 100 words, 5 sentences, 150 syllables. Words/sentence = 20; syllables/word = 1.5. Reading Ease = 206.835 − 20.3 − 126.9 = **59.6** — one band *below* plain English, so it needs to gain a point or two: split the two longest sentences (each split subtracts ~2 words/sentence, worth ~2 points) and swap three three-syllable Latinate nouns for one-syllable verbs.

Both formulas count syllables and sentence length only. They cannot see jargon, ambiguity, or a missing antecedent, so a text can score 70 and still be unreadable. The three checks the formula misses:

1. **Unexplained term on first use** — expand it once, or cut it.
2. **Pronoun with two possible antecedents** — "it", "this", "they" opening a sentence is the usual offender; name the noun.
3. **Buried actor** — if the sentence has no visible subject doing the verb, the reader has to guess who acts.

`max_sentence_words` is the hard ceiling on any single sentence regardless of the average; a 45-word sentence in a text averaging 18 is still the sentence that gets reread. Rungs 4-5 raise it to 35 — their means (16-24, 20-30) are unreachable under the default 25.

## Register by Channel

| Channel | Default rung | Channel-specific rule |
|---|---|---|
| Team chat | 2 | One thought per message; a five-line paragraph in chat reads as an escalation |
| Internal email | 3 | Subject line carries the ask; the body carries the detail |
| External / client email | 3-4 | Never open at 5 with a peer — it invites 5 back and freezes the thread |
| Comment on a document or code review | 3 | Question form for anything subjective ("Would X be simpler?"), imperative only for defects |
| Public post | 2-3 | Contractions and a fragment; the first line has to survive being read alone |
| Support reply to a customer | 3 | Answer first, apology second, one sentence each; never both in the same sentence |
| Voice or video call | 2 | Spoken register is a rung below the written one for the same relationship (`conversation.md`) |
| Legal, HR, formal complaint | 5 | Dates, names and facts; no adjectives; assume it gets read aloud in a room |

## Politeness Is Not Formality

They vary independently, and confusing them is the most expensive register error in professional English.

|  | Direct | Indirect |
|---|---|---|
| **Warm** | "Yeah, that won't work — here's why." (best default) | "That's an interesting angle. Have we thought about…?" |
| **Cold** | "This is wrong." | "One might question the assumptions here." |

Warm-direct is the target register for almost all professional English: it is faster to read, harder to misread, and reads as confident rather than as rude. Cold-indirect is what over-formalizing produces, and it is the register readers describe as "passive-aggressive" without being able to say why.

Culture shifts the baseline, not the target. US professional English runs warm-direct with enthusiasm markers ("Happy to!"); UK runs warm-indirect and encodes negatives as understatement (`business.md`); Dutch and German business English runs direct with fewer softeners and reads brusque to US readers who are not expecting it. When writing across those lines, keep your directness and add one warmth marker, rather than adding hedges.

**Write the register that worked**, the moment you learn it: the rung, the greeting they use, whether they want the bottom line first, and anything they pushed back on. It goes in the `Context` column of that person's row in `~/Clawic/data/contacts/contacts.md`, and the pattern across people goes in `## Registers In Use` of `~/Clawic/data/english/memory.md` (`memory-template.md`). A rung rediscovered every session is a relationship that never gets easier to write to.
