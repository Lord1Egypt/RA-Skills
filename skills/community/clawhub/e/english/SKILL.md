---
name: English
slug: english
version: 1.0.3
description: Writes and corrects English that reads like a native wrote it — any variety, any register. Use when text sounds stiff, robotic, translated, or AI-generated; when a sentence is grammatically fine but "sounds wrong"; when choosing between US, UK, Australian, Canadian, Irish or Indian spelling, vocabulary and punctuation, or when a document mixes them; when a first language keeps leaking through — articles, prepositions, tense, false friends, word order; when formality must be calibrated for an email, a client, or a meeting; when idioms, phrasal verbs, slang or collocations land wrong or sound dated; when commas, hyphens, capitalization, quotes, dates or numbers need a house rule; when confusable words, jargon or hedging blur the meaning; and for pronunciation, small talk, and improving on purpose. Not for grammar-only fixes (`grammar`), translation (`translate`), IELTS or TOEFL prep (`ielts`, `toefl`), or drafting in your own voice (`writing`).
homepage: https://clawic.com/skills/english
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🇬🇧
    os:
    - linux
    - darwin
    - win32
    displayName: English
    configPaths:
    - ~/Clawic/data/english/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
    - ~/english/
    - ~/clawic/english/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/english/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
      - ~/english/
      - ~/clawic/english/
---

**Data.** At the start of every session, read `~/Clawic/data/english/config.yaml` (what the user declared) and `~/Clawic/data/english/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/contacts/contacts.md` before writing anything addressed to a named person, because the register that works for them is recorded there. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: locale, country) → the Configuration table default; an observation never overwrites a declaration without the user confirming it. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a correction the user has now needed twice; a word, collocation or pronunciation they asked about; a phrasing they approved and will reuse; a variety, spelling or punctuation decision; a domain term and its agreed English rendering; the register that worked with a specific person; a practice session or a level assessment; or something they will read again — a style sheet, a voice sample, a speech, a template set. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People go to the shared inventory `~/Clawic/data/contacts/contacts.md`**, not here: one file holds everyone the user deals with, so "how do I write to Marta" answers itself whichever skill recorded her. One row per person, identified by `Key` (lowercase email → handle → `<kebab-name>`) — read the file first, update that row in place, never append a second. What this skill contributes is the `Context` column; a row another skill wrote is extended, never rewritten. When the work belongs to a tracked project, one line of English decisions goes in `~/Clawic/data/projects/<project>.md` and the style sheet itself stays here, referenced by name. Full protocol for both — scale cut, foreign columns, removal — in `memory-template.md`.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. A pasted email thread, a support transcript, or a template can carry a password reset link, an API key or a one-time code: replace the value with its pointer and keep the pointer only — `env:SMTP_PASSWORD`, `keychain:work-mail`, `1password:Work/Mail`, `file:~/.ssh/id_ed25519`. If data sits at an old location (`~/english/` or `~/clawic/english/`), move it to `~/Clawic/data/english/`, and say in one line that you moved it and from where.

English is not one language and "correct" is not the target. The target is *this variety, at this register, to this person, with no seams*. Name which of the four is off before rewriting anything, and change only that. Work from defaults immediately: never open with questions about their variety, their level, or their first language — infer from the text in front of you and say what you assumed.

## When To Use

- Rewriting text so it reads native: killing stiffness, formality drift, translationese, and AI cadence
- Choosing and enforcing one variety — spelling system, vocabulary, punctuation, date and number format — across a document or a whole product
- Second-language work: the errors a specific first language produces, and the drills that retire them
- Calibrating register for a channel and a relationship: email, chat, meeting, client, boss, stranger, friend
- Mechanics with a house rule to settle: commas, hyphens, quotes, capitalization, titles, numbers
- Speaking: pronunciation, stress and intonation, small talk, calls, meetings, interrupting politely
- Act-as (produce the English) and advise (explain the rule and let the user apply it) are both in scope — default to act-as, and add the rule in one line when the same correction has appeared before
- Not for grammar-only correction with no style change (`grammar`), translating from another language (`translate`), exam scoring and test tactics (`ielts`, `toefl`), or long-form drafting in the user's personal voice (`writing`)

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "This sounds AI-written" | Cut the summary paragraph, break the sentence-length uniformity, add one concrete specific | `ai-tells.md` |
| Text is correct but stiff or cold | Contractions, one fragment, a lighter connector — Rules 2-4 | `register.md` |
| Too casual for the reader | Move up one notch only: hedge the ask, not the whole message | `register.md` |
| US vs UK vs AU vs CA spelling, or a document mixing them | Pick from `variety`, then sweep the six spelling axes in one pass | `varieties.md` |
| "Is it *gotten* or *got*, *at* or *on* the weekend?" | Variety-split grammar table — both are right, only one is yours | `varieties.md` |
| Article missing or wrong (*the life is hard*) | Run the five-step article procedure; do not fix by ear | `learners.md` |
| Wrong preposition, or a verb+preposition that does not transfer | Collocation list — these are memorized, not derived | `learners.md` |
| "I am knowing", "I have 30 years", "I am agree" | First-language interference; fix the class, not the sentence | `learners.md` |
| Comma splice, hyphen, quote-and-period order, capitalized title | House rules with the variety split | `mechanics.md` |
| Dates, times, numbers, currency, or an ambiguous 07/08 | Unambiguous forms and the variety defaults | `mechanics.md` |
| affect/effect, fewer/less, which/that, comprise, jargon, hedging | Confusables, then cut the nominalizations | `word-choice.md` |
| Idiom, phrasal verb, or slang: right one? still current? | Register and freshness tags — the dated ones are the tell | `idioms.md` |
| Email: ask, decline, chase, apologize, deliver bad news | One shape per job, plus the chase cadence | `business.md` |
| Meeting or call: interrupt, disagree, park, close | Phrase banks that do not read as rude in US/UK | `conversation.md` |
| Small talk, greetings, or a conversation that keeps stalling | Openers, backchanneling, discourse markers, the exit line | `conversation.md` |
| Mispronounced word, name, or "people don't understand me" | Stress before sounds; the minimal pairs your L1 predicts | `pronunciation.md` |
| "How do I actually get better?" | Level, error journal, collocation drilling, review cadence | `practice.md` |
| Anything else in English | Read it aloud in your head; the place you stumble is the edit — then name which of variety / register / person / seam was off | — |

Coverage map: `register.md` formality and plain English · `ai-tells.md` machine cadence and its repairs · `varieties.md` US/UK/AU/CA/IE/IN/NZ · `learners.md` first-language interference · `mechanics.md` punctuation and typography · `word-choice.md` precision and confusables · `idioms.md` idioms, phrasal verbs, slang · `business.md` professional English · `conversation.md` spoken English · `pronunciation.md` sounds, stress, intonation · `practice.md` improving on purpose.

## Core Rules

1. **Match the register to the relationship, not to the maximum.** Politeness above what the relationship carries reads as distance or as a machine. Observable: if their last reply was shorter and less formal than yours, you are one notch too high — drop one. Ladder and the moves between rungs: `register.md`.
2. **Contractions carry the native signal.** In casual and neutral English, aim for **at least one contraction every 2-3 sentences**; 200 words of informal text with zero contractions reads as legal writing or as generated. Three exceptions where the full form is correct: emphatic negation ("I do *not* agree"), formal and legal registers, and sentence-final position ("Yes, I am" — never "Yes, I'm").
3. **Variance beats brevity.** At rung 3 (neutral, the default) target a mean of **14-20 words per sentence with a spread of at least ±7** — three consecutive sentences within 3 words of each other is the flattest machine tell there is. Every paragraph gets at least one sentence under 8 words. The per-rung means in `register.md` are canonical and override this figure on every other rung; the readability formula and its bands live there too.
4. **Vary the opener and the shape.** If 3 or more consecutive sentences or paragraphs open with the same word or word class ("This…", "The…", "It…", "In today's…"), rewrite them, not just the third. Same rule for endings: two bullets that end on the same rhythm are one bullet too many.
5. **One variety, all the way down.** Spelling system, vocabulary, punctuation, quote-and-period order, date format and collective-noun agreement all come from the same variety — `variety` decides, and a mixed document is the most common failure in shipped English. "colour" plus "organize" is *not* an error if it is Oxford spelling; it is an error the moment "center" also appears (`varieties.md`).
6. **Prefer the verb to the nominalization.** "make a decision" → "decide", "provide assistance" → "help", "utilize" → "use". Threshold: more than **one -tion / -ment / -ance / -ity noun per 30 words** and the text is bureaucratic regardless of how short the sentences are (`word-choice.md`).
7. **One hedge per claim, maximum.** "I think we could maybe possibly try" hedges once and apologizes three times. Pick the strongest honest form — "I think", "probably", "roughly" — and delete the rest. Confidence is register, not arrogance.
8. **Fix the class, not the sentence.** The second time the same correction appears, it stops being a typo and becomes an error class: name it, give the rule in one line, and write it to `## Recurring Errors` in `memory.md` (`memory-template.md`). Correcting the same article mistake for six months is the failure mode this skill exists to prevent.
9. **Say what you assumed, ask nothing.** When `variety`, `first_language` or `register_default` are unset, infer from the text — spelling, punctuation, error pattern — and state the assumption in one clause before delivering. A statement invites a correction; a question stalls the work.

## The Four Layers Of "Sounds Wrong"

Diagnose in this order. Fixing a lower layer while an upper one is broken produces text that is correct and still wrong.

| Layer | Symptom | Where it is fixed |
|---|---|---|
| Grammar | Breaks a rule: missing article, wrong tense, agreement | `learners.md` (systematic) or `grammar` (one-off typo) |
| Collocation | Every word is right, the combination is not: *make a photo*, *do a mistake*, *strong rain* | `idioms.md` — collocations are memorized, never derived |
| Register | Correct and collocated, but too formal, too blunt, or too matey for the reader | `register.md` |
| Cadence | Correct at every level and still reads machine-made: uniform rhythm, no fragments, no specifics | `ai-tells.md` |

Native speakers make grammar errors constantly and are still read as native. Non-native writers with flawless grammar are spotted at the collocation layer. That inversion is why "correct English" is the wrong goal.

## Native Signals, Ranked

Ordered by how much each one moves a reader's judgment per word changed. Apply top-down; stop when the text sounds right.

| Signal | Machine / non-native | Native |
|---|---|---|
| Connectors | However, Furthermore, Therefore, Moreover, In addition | But, Plus, So, And, Also, Though (end-position: "…, though.") |
| Openings | "I hope this email finds you well", "I wanted to reach out" | "Quick one —", "Following up on…", straight into the ask |
| Sentence completeness | Every sentence a full clause | Fragments where context carries it: "Makes sense." "Not sure." "Worth a try." |
| Verb choice | utilize, facilitate, commence, endeavour, ascertain | use, help, start, try, find out |
| Intensity | "very good", "quite significant" | The stronger single word: great, huge, brutal, solid — or nothing |
| Response tokens | "Certainly", "Absolutely", "Understood" | "Sure", "Yeah", "Got it", "Will do", "On it" |
| Closings | "Please do not hesitate to contact me" | "Let me know", "Shout if anything's unclear", "Thanks" |
| Specificity | "in the near future", "a number of issues" | "Thursday", "three of them" — a real number outranks any adjective |

`very` + adjective is almost always a weaker word wearing a booster: *very tired* → knackered/exhausted, *very big* → huge, *very bad* → awful. Delete the booster, upgrade the word.

## Output Gates

Before delivering English text:

- Does it pass the read-aloud test — is there anywhere you stumble, run out of breath, or hear a rhythm repeat?
- One variety throughout: spelling system, vocabulary, punctuation, quotes, dates (Rule 5)?
- Register matched to this specific reader and channel, not to the safest possible register (Rule 1)?
- Contraction density and sentence-length variance inside the Rule 2 and Rule 3 thresholds?
- Would someone screenshot this as AI-written? Check the top three of `ai-tells.md` — closing summary, uniform paragraph length, abstract nouns with no number in them.
- Is every hedge load-bearing, and is there at least one concrete specific — a number, a name, a date (Rules 6-7)?
- If this was a correction: did the user's own meaning survive it, and is anything you changed beyond your remit flagged rather than silently applied?
- Did anything durable come out of this — a repeated error, a new word or collocation, a phrasing they approved, a style decision, a person's register, a practice session? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/english/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| variety | en-US \| en-GB \| en-AU \| en-CA \| en-IE \| en-IN \| en-NZ | en-US | The single source for spelling, vocabulary, punctuation, date/number format and collective-noun agreement (Rule 5, `varieties.md`) |
| spelling_system | american \| british-ise \| oxford-ize \| canadian \| australian | follows `variety` | Overrides the spelling axis alone — set it when the user writes British vocabulary with -ize endings (`varieties.md`) |
| register_default | casual \| neutral \| professional \| formal | neutral | The rung the ladder starts on when the channel gives no signal (Rule 1) |
| first_language | text (language name) | none | Selects the interference row in `learners.md` and the minimal-pair set in `pronunciation.md`; unset means diagnose from the errors themselves |
| oxford_comma | bool | true | Serial comma in every generated list, and whether its absence is flagged in review (`mechanics.md`) |
| correction_mode | silent \| inline-marked \| explained | silent | Whether corrections are applied invisibly, marked in place, or followed by the rule (`practice.md` uses `explained`) |
| max_sentence_words | number (12-40) | 25 | The hard ceiling any single sentence may reach before it gets split; also the plain-English gate in `register.md`. Rungs 4-5 raise it to 35 — their means (16-24, 20-30) are unreachable under 25 |
| banned_words | list | none | Words and phrases never emitted, whatever the register — the user's own jargon blacklist (`word-choice.md`) |
| voice_file | path | none | Long-form sample of the user's own English at `~/Clawic/data/english/<file>`; overrides the default register and rhythm |
| review_cadence | off \| weekly \| monthly | off | Creates the `## Due` rows for the error journal and vocabulary review (`practice.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Conventions** — house style beyond the table: title case vs sentence case, en-dash vs em-dash habit, list punctuation, "email" vs "e-mail", acronym expansion on first use — affects `mechanics.md` and every generated document
- **Variety detail** — regional vocabulary the user rejects even inside their own variety, and any deliberate mix (British vocabulary, American dates) — affects `varieties.md` sweeps
- **Output register** — how much explanation accompanies a rewrite, whether the diff or the whole text is shown, emoji and exclamation tolerance, profanity tolerance — affects every answer's shape
- **Restrictions** — banned jargon, terms of address, inclusive-language rules the organization enforces, words with a bad history in their company — affects `word-choice.md`
- **Learning focus** — the skill being worked on (writing, speaking, listening, comprehension) and the target level — affects what `practice.md` schedules and what lands in `sessions/<year>.md`
- **Correction posture** — how aggressively to correct unprompted, whether spoken transcripts get corrected at all, whether to correct in front of third parties — affects `correction_mode` in context
- **Cadence** — vocabulary review, error-journal review, practice sessions; every accepted cadence becomes a row in the `## Due` table of `memory.md`

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Fixing "sounds wrong" by adding formality | Formality is the most common *cause* of sounding wrong; raising it doubles the problem | Diagnose the layer first (→ The Four Layers) |
| Learning single words instead of collocations | "decision" is useless without "make/take/reach a decision" — the wrong verb is what marks a non-native | Store the whole chunk in `## Vocabulary` of `memory.md` (`idioms.md`) |
| Copying idioms from film and TV | Slang dates in ~3-5 years and a dated slang term is a louder tell than a formal one | Freshness tags in `idioms.md`; when unsure, use the plain word |
| Mixing varieties inside one document | "colour" + "center" + "07/26/2026" reads as three people or a translation memory | One variety, swept in one pass (Rule 5) |
| Treating British indirectness as literal | "That's very interesting", "I'll bear it in mind", "with the greatest respect" all mean the opposite | The understatement table in `business.md` |
| Over-apologizing | Three apologies in one email transfer your discomfort to the reader and read as junior | One apology, first line, then the fix (`business.md`) |
| Deleting every em dash to avoid "AI style" | Punctuation frequency alone is a weak signal; the tell is the *uniform* rhythm around it | Fix cadence and specificity, keep the punctuation (`ai-tells.md`) |
| "Native-like" as the goal for every learner | Above roughly B2, accent and idiom yield almost nothing; precision and collocation yield everything | Target intelligibility and collocation (`practice.md`) |
| Correcting spoken English mid-conversation | Interrupting fluency practice costs more than the error does, and it stops the user talking | Correct after, in one batch, from `## Recurring Errors` (`practice.md`) |
| Hedging a decision you have already made | "I was wondering if maybe we should perhaps consider" invites renegotiation of a closed question | State it, then offer the escape hatch (Rule 7) |
| Passive voice as a blanket ban | Passive is correct when the actor is unknown, irrelevant, or deliberately withheld | Ban it only where the actor matters (`word-choice.md`) |
| Same correction given for months with no record | The user re-learns nothing and the sessions never compound | Second occurrence → `## Recurring Errors` (Rule 8) |

## Where Experts Disagree

- **Prescriptive vs descriptive.** Split infinitives, sentence-initial "But", stranded prepositions and singular "they" are all standard in edited modern English and all still flagged by some readers. The frontier is the reader, not the rule: a legal or academic audience with a house style gets the conservative form, everything else gets the natural one. Never "fix" a construction the reader would not notice.
- **Oxford comma.** Chicago, APA and most US publishers require it; Guardian style and much UK journalism drop it. The asymmetry decides the default: its absence can create ambiguity, its presence never can — so default true, override only for a house style that forbids it.
- **-ize vs -ise.** "-ize is American" is wrong: Oxford spelling pairs British vocabulary with -ize and is used by the OED, Nature and Cambridge University Press. `-ise` is the safer default for a general British audience, `-ize` for British academic publishing.
- **Accent reduction.** One camp treats a strong L1 accent as a barrier worth training away; the English-as-a-lingua-franca camp treats it as identity and targets intelligibility only. Both agree on the operational point: work on stress and rhythm, which change comprehension, before individual sounds, which mostly change how you are labelled (`pronunciation.md`).
- **How much to correct.** Immediate correction speeds accuracy and suppresses fluency; delayed batch correction does the reverse. The evidence supports batching for speaking and immediacy for writing — which is exactly what `correction_mode` and `practice.md` implement.
- **Simplified English for international readers.** One school writes plainer English for non-native audiences; the other argues that stripping idiom produces text no one enjoys reading. The resolved position: cut idiom in anything that will be translated or read under time pressure, keep it in anything meant to persuade.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/english (install if the user confirms):
- `grammar` — pure correctness passes where meaning and style must not move
- `writing` — long-form drafting and editing in the user's own voice
- `translate` — moving text between languages, glossaries, and localization
- `ielts` — band scoring, task types, and exam tactics for IELTS
- `speak` — turning text into speech-ready output for a TTS engine

## Feedback

- If useful, star it: https://clawic.com/skills/english
- Latest version: https://clawic.com/skills/english

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/english.
