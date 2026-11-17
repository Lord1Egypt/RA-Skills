# Varieties — US, UK, Australian, Canadian, Irish, Indian, and the Rest

There is no "correct English", only a variety chosen and then held. `variety` decides all six axes below; a document that mixes them is the most visible defect in shipped English, and the most common — because spell-checkers only police the first axis.

**Contents:** [The Six Axes](#the-six-axes) · [Spelling Systems](#spelling-systems) · [Vocabulary That Actually Diverges](#vocabulary-that-actually-diverges) · [Grammar That Splits by Variety](#grammar-that-splits-by-variety) · [The Dangerous Words](#the-dangerous-words) · [Beyond US and UK](#beyond-us-and-uk) · [Choosing a Variety](#choosing-a-variety) · [The Consistency Sweep](#the-consistency-sweep)

**Before enforcing a variety on a document you have seen before**, read `artifacts/style-sheet.md` if `## Boxes` in `~/Clawic/data/english/memory.md` points to one: deliberate exceptions (British vocabulary with ISO dates, American spelling with UK legal terms) are recorded there and must not be "corrected".

## The Six Axes

| Axis | Example split | Where it is set |
|---|---|---|
| 1 Spelling | colour / color, organise / organize, centre / center | `spelling_system` (defaults from `variety`) |
| 2 Vocabulary | flat / apartment, lorry / truck, holiday / vacation | `variety` |
| 3 Punctuation | quote-and-period order, single vs double quotes, Mr / Mr. | `variety` (`mechanics.md`) |
| 4 Grammar | got / gotten, "the team are" / "the team is", at / on the weekend | `variety` |
| 5 Date and number format | 26/07/2026 vs 07/26/2026; 1,000.5 vs 1.000,5 | `variety` (`mechanics.md`) |
| 6 Register conventions | "Cheers" as a sign-off, "Regards" vs "Best" | `variety` + `register.md` |

Axes 3-6 are the ones that survive a spell-checker, and therefore the ones that give a document away.

## Spelling Systems

Seven rules cover roughly all of it. Apply the whole set or none — half a system is worse than the wrong one.

| Rule | US | UK / IE / AU / NZ | Canada | Notes |
|---|---|---|---|---|
| -or / -our | color, honor, labor | colour, honour, labour | -our | The single most visible axis |
| -ize / -ise | -ize always | -ise (Oxford spelling: -ize) | -ize | See below — "-ize is American" is false |
| -er / -re | center, theater, meter | centre, theatre, metre | -re | UK "meter" = the measuring device; "metre" = the unit and poetic metre. US uses "meter" for all three |
| -og / -ogue | catalog, dialog | catalogue, dialogue | -ogue | US "dialogue" is common in prose |
| -l doubling before a suffix | traveled, canceling, modeled | travelled, cancelling, modelled | doubled | UK doubles a final -l even when the syllable is unstressed |
| -se / -ce | defense, license (n and v), practice (n and v) | defence, licence (n) / license (v), practice (n) / practise (v) | UK pattern | The noun/verb split is a real UK rule, not an option |
| -ae / -oe | anemia, fetus, encyclopedia | anaemia, foetus, encyclopaedia | mixed | Medical texts often keep the digraph in all varieties |

**Oxford spelling** is British vocabulary and punctuation with **-ize** endings, following the Oxford English Dictionary's etymological argument (the suffix comes from Greek *-izein*). It is house style at the OED, Oxford University Press, Nature and, historically, much British academic publishing. So "organize" beside "colour" is not an error — set `spelling_system: oxford-ize` and stop flagging it. What *is* always an error: -ize with "center", or -ise with "color".

Exceptions that never take -ize in any variety, because their roots are not Greek *-izein*: advertise, advise, arise, comprise, compromise, despise, devise, exercise, improvise, revise, supervise, surprise, televise. "Analyse/analyze" splits by variety (UK -yse, US -yze).

## Vocabulary That Actually Diverges

The short list where using the other variety's word marks the text immediately.

| US | UK | Note |
|---|---|---|
| apartment | flat | |
| elevator | lift | |
| truck | lorry | |
| gas / gasoline | petrol | |
| sidewalk | pavement | UK "pavement" is US "sidewalk"; US "pavement" is the road surface |
| trash / garbage | rubbish | UK "rubbish" also means nonsense |
| line | queue | "Queue" is also the standard technical term in both |
| vacation | holiday | UK "holiday" covers both time off and public holidays |
| fall | autumn | "Autumn" is understood everywhere; "fall" is not neutral |
| resume / résumé | CV | |
| math | maths | |
| period | full stop | Punctuation mark |
| parentheses | brackets | US "brackets" = UK "square brackets" |
| cell phone | mobile | |
| mail | post | UK "post" as verb and noun |
| schedule | timetable | "Schedule" exists in UK for appointments |
| store | shop | |
| movie | film | |
| soccer | football | |
| zip code | postcode | |
| first floor | ground floor | Genuine off-by-one: UK first floor = US second floor |

## Grammar That Splits by Variety

| Point | US | UK | Note |
|---|---|---|---|
| Past participle of *get* | gotten (change), got (possess) | got | "I've gotten better" is US only; "I've got a car" is both |
| Collective nouns | singular: "the team is" | often plural: "the team are" | UK chooses by whether the group acts as one; US does not |
| Present perfect vs past simple | "I just ate", "Did you eat yet?" | "I've just eaten", "Have you eaten yet?" | With *just*, *already*, *yet* |
| Weekend | on the weekend | at the weekend | |
| Dates in speech | July 26th | the 26th of July | |
| Ranges | Monday through Friday | Monday to Friday | US "through" is unambiguous; UK "to" can exclude the endpoint |
| *Different* | different from / than | different from / to | "different than" reads wrong in UK |
| Address a letter | write me | write to me | |
| -t vs -ed past forms | learned, dreamed, spelled, burned | learnt, dreamt, spelt, burnt | UK accepts both; US only -ed |
| *shall* | dead outside legal text | alive in offers and questions: "Shall I…?" | |
| Tag questions | rare, "right?" | common: "isn't it?", "won't you?" | Indian English uses "isn't it?" invariantly |
| Titles | Mr., Dr., Mrs. (with period) | Mr, Dr, Mrs (no period) | Rule: no full stop when the abbreviation ends in the word's last letter |

## The Dangerous Words

Words where the other variety's meaning is not merely different but wrong, rude, or the exact opposite. Check these before shipping across the Atlantic.

| Word | US meaning | UK meaning | Consequence |
|---|---|---|---|
| pants | trousers | underwear | Comic in a clothing product; embarrassing in a work email |
| fanny | backside (mild) | vulgar | Never use; "fanny pack" → "bum bag" for UK audiences |
| rubber | condom | eraser | Stationery copy needs "eraser" |
| pissed | angry | drunk | "He was pissed at the meeting" changes meaning entirely |
| table a motion | postpone it | bring it forward for discussion | Reverses a meeting outcome — say "postpone" or "put on the agenda" |
| quite good | very good | fairly good, mediocre | A UK "quite good" review is not praise |
| momentarily | in a moment | for a moment | "The train will depart momentarily" is alarming in the UK |
| homely | plain-looking (of a person) | cosy, welcoming | Insult vs compliment |
| bird | bird | slang for a woman (dated, unwelcome) | Avoid in UK copy |
| first floor | floor above ground | ground floor | Wrong floor, literally |
| chips / crisps | fries / chips | chips / crisps | Menu copy fails |
| public school | state school | private fee-paying school | Reverses the entire meaning |

## Beyond US and UK

| Variety | Spelling | Distinctive features |
|---|---|---|
| Canadian | -our + -ize + -re (colour, organize, centre) | US vocabulary mostly (truck, gas, apartment) with UK "cheque", "grey", "kilometre"; "eh" as a tag; French-influenced official terms |
| Australian | -our + -ise (strongly) + -re | "program" not "programme"; diminutives (arvo, servo, brekkie, defo); "reckon", "heaps", "no worries", "good on ya"; informality one rung below UK in professional contexts |
| New Zealand | as Australian | Māori loanwords in official and everyday use (kia ora, whānau, aotearoa); "sweet as", "chur" |
| Irish | UK spelling | "grand" = fine; "I'm after eating" = have just eaten; "amn't I?"; "your man" for a third party; "press" for cupboard; "give out" = complain |
| Scottish | UK spelling | "wee", "aye", "outwith" (= outside of, standard in Scottish official writing) |
| Indian | UK spelling | "do the needful", "revert" = reply, "prepone" = bring forward, "out of station" = away, "cousin brother/sister", lakh (100,000) and crore (10,000,000); progressive with stative verbs ("I am having two children"); invariant tag "isn't it?" |
| Singapore / Malaysia | UK spelling | Formal register is standard British; colloquial Singlish uses particles (lah, leh, meh) and perfective "already" — never mix the two in one document |
| South African | UK spelling | "robot" = traffic light, "just now" = shortly (not immediately), "braai", "lekker" |
| Nigerian | UK spelling | "well done" as a greeting to someone working, "flash" = ring and hang up, "sorry" as sympathy for any mishap (not an apology) |

Indian, Nigerian, Singaporean and South African English are standard varieties with their own reference works, not deviations from British English. Treat their features as variety, not error — the only fault is mixing them into a document declared as `en-US` or `en-GB`.

## Choosing a Variety

Decide once, from these in order:

1. **The reader's location**, if the text goes to one place. A UK regulator reading American spelling reads it as an untranslated import.
2. **The organization's existing corpus.** Match what is already published — inconsistency across a site costs more than the "wrong" variety.
3. **The market majority** for global products: `en-US` is the default because it is the most widely encountered variety in software and the least likely to be read as a regional choice.
4. **Neutral international English** when the audience is genuinely mixed: `en-US` spelling, zero regional idiom, ISO dates (`2026-07-26`), 24-hour or explicit times, and no cultural references that need local knowledge. This is a real fourth option, not a failure to choose.

Set the answer in `variety` the first time the user states or implies it, and stop re-deriving it.

## The Consistency Sweep

Run once per document, in this order — earlier axes cause later ones.

1. **Spelling system**: sweep the seven rules above, whole-word, in one pass. A single "organized" in a `-ise` document is the tell.
2. **Vocabulary**: check the divergent list, then the dangerous list.
3. **Dates and numbers**: one format throughout; ambiguous numeric dates (07/08) rewritten as `26 July 2026` or ISO (`mechanics.md`).
4. **Punctuation**: quote-and-period order, single vs double quotes, abbreviation full stops (`mechanics.md`).
5. **Grammar splits**: participles, collective nouns, present perfect, prepositions of time.
6. **Register conventions**: sign-offs and greetings match the variety, not the writer's habit.

Quoted material is exempt from all six: never re-spell a quotation, a proper noun, or a product name. "The Labour Party" stays "Labour" in an American document; "World Health Organization" stays -ization in a British one.

**Write every variety decision that took a judgment call** — the variety itself, the spelling system, and every deliberate exception, with the reason in one clause. The variety and spelling system go in `config.yaml`; the exceptions go in `artifacts/style-sheet.md` with its `## Boxes` line in `~/Clawic/data/english/memory.md`, in the same turn (`memory-template.md`). Without the style sheet, the next session "corrects" the exception and the document oscillates.
