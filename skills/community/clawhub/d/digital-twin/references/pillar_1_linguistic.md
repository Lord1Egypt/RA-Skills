# Pillar 1: Linguistic Profiling

## Purpose

Capture HOW the target person communicates — not what they say, but the structural and stylistic
fingerprint of their language. The goal is to build a linguistic filter that can take any message
content and make it "sound like" the person wrote or said it.

**Source applicability:** This pillar applies to every source type — transcripts, emails, chat
messages, and authored documents. Spoken sources (transcripts) reveal verbal tics, turn-taking, and
conversational dynamics; written sources (email, chat, docs) reveal punctuation habits, formatting,
greetings/sign-offs, and message-length patterns. Analyze what the source actually shows. Where a
person's spoken and written voice differ, capture both and tag them by medium.

---

## Analysis Framework

For each sample, analyze the target person's contributions across these dimensions. Use direct
observations from the text — do not infer or generalize beyond what the sample shows.

### 1.1 Sentence Architecture

Examine the structural patterns of how they build sentences:

- **Average sentence length**: Short and punchy (5-10 words), medium (10-20), or long and complex (20+)?
- **Sentence complexity**: Simple (subject-verb-object), compound (joined with and/but/or), or complex (subordinate clauses, embedded qualifications)?
- **Fragmentation**: Do they speak/write in complete sentences or use fragments, trailing off, or starting new thoughts mid-sentence?
- **List behavior**: When they enumerate, do they use explicit numbering ("first... second... third"), casual listing ("so there's X, there's Y, and then Z"), bullet points (in writing), or do they avoid lists entirely and weave points into narrative?

Record 2-3 representative sentence structures verbatim from the sample as exemplars.

### 1.2 Vocabulary & Register

Examine their word choices:

- **Formality level**: Casual/colloquial ("gonna," "kinda," "like"), professional standard, or formal/elevated?
- **Jargon density**: How much domain-specific or technical language do they use? Do they assume shared vocabulary or explain terms?
- **Filler words and verbal tics**: "Basically," "essentially," "right," "you know," "I mean," "look," "so," "actually" — identify their specific fillers and approximate frequency. (In written sources, look for the written equivalents: stock openers, recurring connectors, habitual qualifiers.)
- **Intensifiers and hedges**: Do they amplify ("absolutely," "definitely," "massive") or hedge ("probably," "I think," "maybe," "sort of")?
- **Profanity/casualism**: Any casual language, slang, or mild profanity patterns?
- **Signature phrases**: Recurring expressions unique to them (e.g., someone who always says "at the end of the day" or "the reality is" or "what I would say is").
- **Written-source markers** (email/chat/docs): greeting and sign-off habits, emoji/emoticon use, capitalization and punctuation style (e.g., minimal punctuation, em-dash habit, exclamation frequency), and typical message length.

### 1.3 Rhetorical Patterns

How they structure arguments and make points:

- **Opening moves**: How do they start a response? Do they acknowledge the previous speaker first ("Yeah, great point..."), dive straight in ("So here's the thing..."), ask a clarifying question, or reframe? (In email/chat, note their habitual opener.)
- **Closing moves**: How do they end a thought? Summarize, ask for input, trail off, give a directive, or hand off? (In email/chat, note their habitual closer/sign-off.)
- **Transition style**: How do they move between points? Explicit transitions ("building on that..."), abrupt topic changes, or organic flow?
- **Reasoning exposition**: Do they show their work ("The reason I think this is...") or just state conclusions?
- **Storytelling vs. data**: When making a point, do they default to anecdotes/examples or to data/metrics?
- **Question style**: When they ask questions, are they Socratic (leading), genuine (curious), rhetorical, or challenging?

### 1.4 Conversational Dynamics

How they interact in the flow of a live exchange. *Observable mainly in interactive sources
(transcripts, chat threads); for one-directional sources like documents, skip what isn't present.*

- **Turn-taking behavior**: Do they wait for clear openings, interject, or dominate the floor?
- **Response latency style**: Quick reactor or thoughtful pauser? (Inferred from conversational flow, e.g., "Let me think about that..." signals a pauser.)
- **Acknowledgment patterns**: How do they validate others' input before responding? ("That's a great point," "I hear you," "Right, so..." or they skip acknowledgment entirely?)
- **Disagreement style**: How do they push back? Directly ("I disagree because..."), diplomatically ("I see it a bit differently..."), or through questions ("Have we considered...")?
- **Humor patterns**: Do they use humor? If so, what kind — self-deprecating, dry/sarcastic, situational, or they stay serious?

### 1.5 Directness Calibration

Map their position on key directness spectra:

- **Directness vs. hedging** (1-10, where 1 = "I was maybe wondering if perhaps we might consider..." and 10 = "We need to do X. Period.")
- **Assertiveness vs. tentativeness** (1-10, where 1 = presents everything as a question, 10 = presents everything as established fact)
- **Conciseness vs. elaboration** (1-10, where 1 = single-sentence answers, 10 = multi-paragraph explorations)

---

## Per-Sample Output Format

For each sample, produce:

```
## Linguistic Analysis — [Title] ([Date]) — [Source type: transcript/email/chat/document]

### Sentence Architecture
- Average length: [short/medium/long]
- Complexity: [simple/compound/complex/mixed]
- Fragmentation: [complete/frequent fragments/occasional fragments]
- List behavior: [explicit numbering/casual listing/bullets/narrative weave/varies]
- Exemplar sentences: [2-3 verbatim quotes showing typical structure]

### Vocabulary & Register
- Formality: [casual/standard/formal/shifts between]
- Jargon density: [low/medium/high]
- Key fillers: [list with approximate frequency per 100 words]
- Intensifier/hedge ratio: [amplifier-heavy/balanced/hedge-heavy]
- Signature phrases: [list any recurring expressions]
- Written markers (if applicable): [greeting/sign-off, emoji, punctuation/capitalization style, typical length]

### Rhetorical Patterns
- Opening move type: [acknowledgment/direct dive/reframe/question]
- Closing move type: [summary/directive/question/trail-off/handoff]
- Reasoning style: [show work/state conclusions/mixed]
- Evidence preference: [anecdote/data/authority/mixed]
- Question style: [Socratic/genuine/rhetorical/challenging]

### Conversational Dynamics (interactive sources only)
- Turn-taking: [waits/interjects/dominates/balanced]
- Acknowledgment: [frequent validator/occasional/skips]
- Disagreement style: [direct/diplomatic/questioning/avoidant]
- Humor: [type and frequency, or none observed]

### Directness Calibration
- Directness: [1-10]
- Assertiveness: [1-10]
- Conciseness: [1-10]
```

---

## Compositing Instructions

When merging across all samples:

1. **Core patterns** (60%+ of samples): These go into the primary linguistic style guide as "always apply" rules.
2. **Situational patterns** (appear in some samples with identifiable context triggers): These become conditional rules, e.g., "In 1:1 meetings, directness increases to 8-9; in group settings, drops to 5-6" or "In email, sentences lengthen and fillers disappear; in chat, fragments and lowercase dominate."
3. **Outliers** (appear in only 1 sample): Discard unless the single instance is dramatically distinctive (a pattern so unique it's clearly "them").
4. **Directness scores**: Average across samples, but note standard deviation. If deviation > 2.0, this dimension is context-dependent — map which contexts (and which media) push it higher or lower.
5. **Spoken vs. written voice**: If the person's transcripts and their written communication diverge meaningfully, document both as distinct modes and tie each to its medium, so the generated twin can switch voice based on whether it's drafting an email vs. speaking in a meeting.
6. **The linguistic style guide** should be written as actionable instructions, not observations. Not "John tends to use short sentences" but "Keep sentences to 8-15 words. Use fragments for emphasis. Avoid complex subordinate clauses."
