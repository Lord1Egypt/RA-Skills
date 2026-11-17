# Word Choice — Precision, Confusables, and What to Cut

Two failures live here and they pull in opposite directions: the *wrong* word (a confusable, a false precision) and the *empty* word (a nominalization, a filler, a hedge). Fix the wrong ones first — an empty sentence is merely long, a wrong word is a mistake.

**Contents:** [Confusable Pairs](#confusable-pairs) · [Words That Do Not Mean What They Are Used To Mean](#words-that-do-not-mean-what-they-are-used-to-mean) · [Nominalizations](#nominalizations) · [Words That Add Nothing](#words-that-add-nothing) · [Precision Over Intensity](#precision-over-intensity) · [Jargon and Corporate Fog](#jargon-and-corporate-fog) · [Inclusive and Neutral Language](#inclusive-and-neutral-language) · [Passive Voice, Honestly](#passive-voice-honestly)

**Before a word-level pass**, read `banned_words` in `config.yaml` and `## Glossary` in `~/Clawic/data/english/memory.md` (or `glossary.md` if `## Boxes` points there): the user's own vetoed terms and their agreed rendering of domain nouns live there, and re-deciding them mid-document produces a text that contradicts the last one.

## Confusable Pairs

| Pair | Rule that settles it |
|---|---|
| affect / effect | *affect* is the verb (to influence), *effect* the noun (a result). Exceptions exist (*to effect change*, *flat affect*) and are rare enough to look up |
| fewer / less | *fewer* for countable items, *less* for mass quantities. *Fewer bugs*, *less risk*. Time, money and distance take *less* (*less than five miles*) |
| that / which | Essential clause → *that*, no comma. Non-essential → *which*, commas (`mechanics.md`) |
| who / whom | *whom* where *him* would fit: *To whom did you send it?* (you sent it to him). Below rung 4, *who* is fine everywhere |
| its / it's | Possessive has no apostrophe. No exceptions |
| lay / lie | *lay* takes an object (*lay the book down*), *lie* does not (*lie down*). Past of *lie* is *lay*, which is why nobody gets this right |
| compliment / complement | *Compliment* = praise; *complement* = completes |
| principal / principle | *Principal* = main, or a person; *principle* = a rule |
| discreet / discrete | *Discreet* = tactful; *discrete* = separate |
| ensure / insure / assure | *Ensure* = make certain; *insure* = buy insurance; *assure* = reassure a person |
| imply / infer | The speaker implies, the listener infers |
| comprise / compose | The whole comprises the parts; the parts compose the whole. *Comprised of* is widely used and widely flagged — write *consists of* and skip the argument |
| farther / further | *Farther* = physical distance; *further* = degree or extent. UK uses *further* for both |
| historic / historical | *Historic* = significant in history; *historical* = relating to the past |
| continual / continuous | *Continual* = repeatedly; *continuous* = without a break |
| e.g. / i.e. | *e.g.* = for example; *i.e.* = in other words |
| alternate / alternative | *Alternate* = every other one; *alternative* = another option. US usage blurs them |
| biannual / biennial | *Biannual* = twice a year; *biennial* = every two years. Ambiguous enough that "twice a year" is the correct answer |
| enquire / inquire | UK: *enquire* = ask, *inquire* = investigate. US: *inquire* for both |
| practice / practise | UK: *practice* noun, *practise* verb. US: *practice* for both (`varieties.md`) |
| licence / license | Same UK split; US uses *license* for both |
| program / programme | US *program* everywhere. UK *programme* except computer programs. AU *program* everywhere |

## Words That Do Not Mean What They Are Used To Mean

| Word | Common use | Actual meaning | Use instead |
|---|---|---|---|
| literally | as an intensifier | actually, not figuratively | Delete it, or say *really* |
| ironic | unfortunate or coincidental | the opposite of what is expected or stated | *unlucky*, *coincidental* |
| decimate | destroy completely | reduce heavily (originally by one tenth) | *devastate*, or a number |
| nonplussed | unbothered (US colloquial) | bewildered | Ambiguous now; avoid |
| begs the question | raises the question | assumes the conclusion in the premise | *raises the question* |
| disinterested | uninterested | impartial | *uninterested* for bored, *disinterested* for neutral |
| enormity | enormous size | great wickedness or a grave crime | *enormousness*, *scale* |
| peruse | skim | to read carefully | *skim* or *read closely* — say which |
| fulsome | abundant and generous | excessive to the point of insincerity | *full*, *detailed* |
| momentarily | in a moment (US) | for a moment (UK) | Rewrite for an international audience (`varieties.md`) |
| penultimate | the very last | second to last | *final* |
| refute | dispute | disprove with evidence | *dispute*, *deny*, *reject* |
| bemused | amused | confused | *amused* |

## Nominalizations

A nominalization is a verb wearing a noun costume, and it drags in a weak verb plus a preposition to hold it up. Threshold: more than **one -tion / -ment / -ance / -ity noun per 30 words** and the text reads bureaucratic no matter how short the sentences (SKILL.md Rule 6).

| Nominalized | Verb |
|---|---|
| make a decision about | decide |
| conduct an investigation into | investigate |
| provide assistance to | help |
| carry out an assessment of | assess |
| give consideration to | consider |
| reach an agreement on | agree |
| perform an analysis of | analyse |
| have a discussion about | discuss |
| is in violation of | violates |
| take into consideration | consider |
| make an application | apply |
| effect an improvement in | improve |

The mechanical test: find the *action* in the sentence, then check whether it is the verb. In *"We made a decision to postpone"*, the action is deciding and the verb is *made* — so *decide* is being wasted as a noun. Rewritten: *"We decided to postpone."* Four words become two, and the sentence gains a subject that acts.

## Words That Add Nothing

Delete on sight unless the sentence collapses without them.

**Intensifier fillers**: very, really, quite, rather, somewhat, pretty, fairly, extremely, actually, basically, definitely, certainly, truly, simply, just, literally, absolutely.

**Empty adjectives**: key (as an adjective), crucial, essential, vital, significant, robust, comprehensive, various, numerous, certain, respective, appropriate, relevant.

**Padding phrases → replacement**: in order to → *to* · due to the fact that → *because* · at this point in time → *now* · in the event that → *if* · for the purpose of → *to* · with regard to → *about* · in terms of → *(delete)* · it is important to note that → *(delete)* · there is/are … that → *(recast)* · the fact that → *that* · on a daily basis → *daily* · in the process of → *(delete)* · a number of → *some* or the number · at your earliest convenience → a date.

**Doublets** — two words that mean the same thing, a habit inherited from legal English: each and every, first and foremost, null and void, various and sundry, hopes and dreams, safe and secure. Keep one.

*Very* deserves its own rule: it is a weaker word asking for help. *very tired* → exhausted · *very big* → huge · *very bad* → awful · *very important* → critical, or a reason. Delete the booster and upgrade the word.

## Precision Over Intensity

A specific replaces an adjective and is shorter.

| Vague | Precise |
|---|---|
| significantly faster | 12 seconds, down from 40 |
| in the near future | by Thursday |
| a number of issues | three issues |
| most users | 78% of accounts |
| recently | last Tuesday |
| a large file | 2.4 GB |
| soon | before the 15th |
| several people said | Ana and Tom said |
| industry-leading | the only one that does X |

When the number is unknown, say so — *roughly forty* and *I don't have the number* are both honest; *significant* is neither. An approximator is more precise than an adjective (`register.md`).

## Jargon and Corporate Fog

Jargon is efficient inside a group and hostile outside it. The test is a single question: **would a competent person from the next team over understand this without asking?** If not, expand it once or replace it.

| Fog | Plain |
|---|---|
| leverage (verb) | use |
| utilize | use |
| synergies | shared work, cost savings — say which |
| circle back / touch base | talk again on Thursday |
| take this offline | discuss after the meeting |
| bandwidth | time, capacity |
| low-hanging fruit | the easy ones, named |
| move the needle | change the number, named |
| going forward | from now on, or delete |
| at the end of the day | delete |
| holistic | complete, or delete |
| best practice | what most teams do, which may be wrong here |
| align on | agree |
| socialize an idea | show it to people before deciding |
| reach out | email, call, message — say which |
| deep dive | go through it in detail |

Two euphemisms that damage trust and should be named plainly: *rightsizing / restructuring* for layoffs, and *learnings* for lessons. Both mark the writer as hiding.

Jargon that is *correct* and should stay: domain terms with a precise meaning (*idempotent*, *escrow*, *tort*, *p99*, *cohort*) when the reader is in the domain. Expand on first use, then use freely (`mechanics.md`).

## Inclusive and Neutral Language

| Instead of | Use | Why |
|---|---|---|
| chairman, spokesman, manpower | chair, spokesperson, staffing | Occupational terms are neutral in current standard English |
| he (generic), he/she | singular *they* | Standard since the 14th century and accepted by AP, Chicago, APA and Merriam-Webster; takes a plural verb: *they are* |
| guys (mixed group) | everyone, folks, team, all | Reads as inclusive in some US contexts and not in others; low cost to change |
| blacklist / whitelist | blocklist / allowlist | Also clearer — the action is in the word |
| master/slave | primary/replica, leader/follower | Standard in most technical style guides now |
| the disabled, an autistic | disabled people / people with disabilities; an autistic person | Communities differ on identity-first vs person-first; when the person has stated a preference, follow it |
| suffers from X | has X | *Suffers* assigns an experience |
| crazy, insane, lame (as evaluations) | wild, unreasonable, weak | Costs nothing to swap in professional writing |
| foreign (of people) | international, non-UK, non-US | *Foreign* is fine for objects and policy, marked for people |

The operative rule: these are register decisions with a real audience cost and near-zero writing cost, not moral positions. When an organization mandates a term, it goes in the style sheet; when the user rejects one, it goes in `banned_words`.

## Passive Voice, Honestly

The blanket ban is wrong. Passive is the correct choice in four situations:

1. **The actor is unknown**: *The server was compromised on Tuesday.*
2. **The actor is irrelevant**: *The samples were refrigerated for 12 hours.*
3. **The object is the topic**: *The API is called once per session* — the API is what the paragraph is about.
4. **The actor is deliberately withheld and everyone knows it**: institutional writing, some legal drafting.

Passive is wrong when the actor matters and is being hidden — *mistakes were made*, *your account was closed*, *it was decided*. The test: ask "by whom?" If the answer matters to the reader and the sentence does not supply it, make it active.

Ratio, not ban: **under ~10% of sentences passive** in most professional prose, higher in scientific writing where convention favours it. Counting is the diagnosis; each individual passive still gets judged on the four cases above.

**Write the terms that were decided, not the ones that were merely used.** A domain noun with an agreed English rendering (a product name, a job title, a technical term the team argued about) goes in `## Glossary` in `~/Clawic/data/english/memory.md`, with the rejected alternative in the same row so nobody reopens it; a word the user vetoed goes in `banned_words` in `config.yaml`. Past ~15 glossary rows it becomes `glossary.md` with the same headings and its `## Boxes` line, in the same turn (`memory-template.md`).
