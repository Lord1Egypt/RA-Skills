# Languages — Vocabulary, Audio, Scripts, And Sentence Mining

Anki is a vocabulary and pattern machine. It does not produce fluency; it removes the lookup that stops you mid-sentence. Design the deck around that boundary and it works for years.

## The Vocabulary Note

| Field | Required | Why |
|---|---|---|
| Target word | yes | With its article/gender/tone baked in: `die Tür`, `el problema`, `māma (mā)` — a bare noun teaches half the word |
| Meaning | yes | The ONE sense you met, not the dictionary entry (`run` has dozens; card the one you read) |
| Example sentence | yes | The sentence you actually met it in; it is what makes the meaning stick |
| Audio | if the language is spoken | Generated once into a media file, never rendered live |
| Pronunciation / IPA / tone | script or tonal languages | Tone is part of the word, not decoration |
| Part of speech + inflection | inflected languages | Plural, past form, aspect pair — the irregularity is the fact |
| Frequency / CEFR tag | yes | Drives study order and lets you cut the tail later |

## Frequency Order Is The Highest-Leverage Choice

Word-frequency coverage (Nation's vocabulary research, general corpora): the most frequent ~1,000 word families cover the large majority of everyday spoken discourse; ~2,000-3,000 gets you into comfortable conversation coverage; beyond ~5,000 you are buying diminishing, domain-specific returns. Exact percentages vary by corpus and by what counts as a word — the ordering is what matters and it is stable across every corpus.

Consequences: study a frequency list before mining, tag every card with its band (`freq::1k`, `freq::3k`), and never let rare words from an interesting text jump the queue. When workload gets heavy, you delete from the bottom of the frequency order, not at random.

## Recognition vs Production

Two different skills, two different cards, twice the cost — so choose per word.

| Word type | Cards to make |
|---|---|
| Everything you read | L2 → L1 recognition only |
| The 1-2k core you must speak | Both directions |
| Words you keep failing to produce | L1 → L2 with a first-letter hint in the question |
| Passive/technical vocabulary | Recognition only, forever |

Production cards need controlled prompts: "say 'to give up' (phrasal, informal)" beats "say 'quit'", which has five acceptable answers and will be graded inconsistently — and inconsistent grading is what breaks the scheduler (SKILL.md The Four Buttons).

## Sentence Mining

The i+1 principle: mine sentences where exactly ONE element is unknown. Two unknowns make a card that fails for reasons you cannot attribute.

1. Read or watch real material; capture sentences containing one unknown word.
2. Make a cloze over that word, keeping the whole sentence visible.
3. Add audio of the full sentence, not the isolated word — prosody is part of the memory.
4. Cap the intake: mining generates faster than you can review; the frequency band decides which mined sentences get in.

Popup-dictionary and mining tools push cards into Anki through AnkiConnect, which is why field discipline matters — automated cards inherit whatever template you set up once.

## Audio

- Generate to media files once; do not depend on a runtime add-on, which does not exist on mobile clients.
- Human recordings (community pronunciation databases, native speakers, the source audio of what you mined) beat TTS for prosody; TTS beats nothing and is consistent.
- **Listening cards** are a separate card, not a field: audio on the front, meaning on the back. If you only ever see the word, you will not recognize it spoken — this is the single most common gap in self-built decks.
- Audio on the ANSWER side of every card costs nothing and reinforces pronunciation at zero extra review time.

## Grammar

Do not card rules. Card examples that instantiate the rule, and one card for the rule's trigger.

```
Bad :  When is the subjunctive used in Spanish?
Good:  Espero que {{c1::vengas}} mañana.        (esperar que → subjunctive)
Good:  [ES grammar] Which mood follows "espero que"? → subjunctive
```

Conjugation tables: card the pattern (one card per ending set), plus the high-frequency irregular forms you will actually say. One card per cell of a 6×12 table is 72 cards for a pattern you can learn in two.

## Scripts And Tones

- Character languages: card the character → meaning+reading, and separately the word → character (production) only for what you must write. Components/radicals get their own small deck — they are the alphabet of the system and pay back across thousands of characters.
- Handwriting is a motor skill: use paper, and keep Anki for recognition and readings (SKILL.md, When Anki Is The Wrong Tool).
- Tonal languages: the tone belongs inside the answer and inside the audio. A card graded correct with the wrong tone is teaching the wrong word.
- Minimal pairs deserve contrast cards: two words differing only in tone, length, or one phoneme, tested against each other rather than separately.

## False Friends And Confusable Pairs

```
[ES→EN] "embarazada" means…       → pregnant  (embarrassed = avergonzada)
[ES→EN] "actualmente" means…      → currently (actually = en realidad)
```

Always name the trap on the answer. A false-friend card without the contrast teaches the correct meaning and leaves the wrong association intact.

## Regional Variation

Pick one variety as the default for your deck and tag the exceptions (`region::latam`, `region::rioplatense`). Cards that list three regional synonyms as the answer are list cards; the card that works is "which word for 'car' in Spain?" with the region in the question.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Bare noun without article/gender | You learn half a word and produce it wrong | Bake the article into the target field |
| Dictionary entry as the answer | Five senses on one card = list card | One sense per card, the one you met |
| Both directions for every word | Doubles a deck you will abandon | Production only for the core you must speak |
| No listening cards | Words recognized on paper vanish in speech | Audio-front cards for the core vocabulary |
| Mining faster than reviewing | The backlog kills the habit within a month | Cap intake by frequency band (SKILL.md rule 5) |
| Sentence cards with two unknowns | Failure cannot be attributed | i+1 only |
| Grading a production card loosely | Synonym today, strict tomorrow: the scheduler fits noise | Controlled prompts, one accepted answer |
