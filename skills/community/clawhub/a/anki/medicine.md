# Medicine — High-Volume Decks, Shared Decks, And Board Timelines

Medical students are the heaviest Anki users because the material is high-volume arbitrary recall with a hard exam date. Everything here is a volume-management problem first and a card-writing problem second.

## Volume Math Before Anything Else

A comprehensive premade deck runs into the tens of thousands of cards. Do the arithmetic before adopting one (SKILL.md Workload Math):

```
25,000 cards over 24 months  → 25,000 / 730 ≈ 35 new/day
35 new/day × ~10 reviews/card ≈ 350 reviews/day steady state
350 reviews × ~10 s          ≈ 1 hour/day, every day, for two years
```

That hour is the real commitment, and it is on top of lectures and question banks. If the number does not fit your day, the deck must shrink before it starts — cutting later means abandoning cards you already paid to learn.

## Premade Decks: The Unsuspend Workflow

Comprehensive community decks (the AnKing/Zanki lineage and its descendants) are professionally curated and tagged by source, lecture, and exam relevance. They fail for one reason: students study them unsuspended.

1. Import, then **suspend everything**: in Browse search `deck:Med`, select all, Suspend.
2. After each lecture or chapter, unsuspend by that tag only: `deck:Med tag:source::lecture-14 is:suspended` → unsuspend.
3. Never unsuspend forward. Cards on material not yet taught become leeches, and leech load compounds.
4. Keep a `status::skipped` tag for material your school does not cover — a decision recorded once beats re-deciding every time a card surfaces.
5. Re-tag with your own `content::` axis as you go; your school's sequence is not the deck author's.

Vendor note-types and subscription platforms bake rendering into the deck. Export a plain-note-type copy before a subscription lapses.

## Class Deck vs Boards Deck

Do not maintain both as separate collections of the same facts. One deck, two tags: `exam::class` and `exam::boards`, with filtered decks selecting what a given week needs (`deck:Med tag:exam::boards`). Duplicated facts across two decks are duplicated reviews forever and inconsistent edits.

When the two conflict — school details the boards will not test — card the boards version and let the class detail live in your notes. Class detail is needed for weeks; boards facts are needed for years.

## Card Patterns By Subject

| Subject | Pattern that works |
|---|---|
| Pharmacology | One card per drug × one attribute (mechanism, one classic toxicity, one contraindication, one monitoring test). Never "side effects of X" |
| Microbiology | Organism → one distinguishing feature; and the reverse: distinguishing feature → organism. Both directions genuinely earn their place here |
| Anatomy | Image Occlusion on the atlas figure, plus function/innervation cards that reference the same figure |
| Biochemistry | Enzyme → reaction step, deficiency → clinical finding, rate-limiting steps as their own set |
| Pathology | Buzzword → diagnosis, and histology image → diagnosis (occlusion or image on the front) |
| Physiology | Cause → direction of change ("↑ aldosterone → serum K⁺ does what?"), never whole cascades on one card |
| Clinical / rotations | Presentation → next best step; management ladders as one card per rung |

## Question Banks Feed The Deck

The highest-yield cards a medical student writes come from questions they got wrong.

- Card the **reason you missed it**, not the question. A missed question usually hides one fact or one distinction; that is the card.
- Never paste the vignette. Vignettes teach pattern-matching on that vignette.
- Tag them `source::qbank` and watch that tag's Again-rate: it is the highest-signal subset in the collection.
- Skip carding the explanation's background paragraphs. If the concept needs a paragraph, you need study, not a card.

## The Timeline

| Phase | Deck posture |
|---|---|
| Preclinical, exam >6 months out | Full new-card rate; unsuspend by lecture; build habit consistency |
| Dedicated study (weeks out) | New cards to 0 or near it; all capacity to reviews; leech threshold halved |
| Final 3 weeks | No new cards that must mature — 21 days is the maturity floor; triage instead |
| Rotations / clinical | New cards low or 0 on some days; protect reviews only. A missed review day is recoverable; an abandoned collection is not |
| Post-exam | Suspend exam-only tags, restore limits at half rate, keep the boards-relevant core alive |

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Unsuspending a whole premade deck at once | Thousands of cards on untaught material; backlog by day three | Unsuspend by lecture tag |
| Making your own deck "because making cards is learning" at this volume | Authoring 25k cards costs more hours than studying them | Premade for volume, self-made for what you keep missing |
| Carding whole qbank vignettes | Memorizes the vignette, not the discrimination | Card the missed fact |
| Two decks for class and boards | Duplicate reviews forever, edits drift apart | One deck, two tags |
| Skipping reviews during rotations, then a marathon | Retention on rushed reviews is poor and burnout follows | Fixed cap, new cards to 0 |
| Keeping every card after the exam | The collection becomes a monument you stop opening | Suspend by `exam::` tag, keep the clinical core |
