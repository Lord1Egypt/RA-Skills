# Mechanics — Punctuation, Capitalization, Numbers, and Dates

Mechanics is where a house rule beats a correctness argument. Most of what follows has two defensible answers; the failure is not picking the "wrong" one, it is applying both in the same document.

**Contents:** [Commas](#commas) · [Semicolons, Colons, Dashes](#semicolons-colons-dashes) · [Quotation Marks](#quotation-marks) · [Apostrophes](#apostrophes) · [Hyphens and Compounds](#hyphens-and-compounds) · [Capitalization and Titles](#capitalization-and-titles) · [Numbers](#numbers) · [Dates, Times, Currency](#dates-times-currency) · [Abbreviations](#abbreviations) · [Lists and Bullets](#lists-and-bullets)

**Before settling any rule below**, read `artifacts/style-sheet.md` if `## Boxes` in `~/Clawic/data/english/memory.md` points to one, plus `oxford_comma` and `variety` in `config.yaml`. A rule already decided is not re-litigated; a rule decided here for the first time gets written down.

## Commas

The five jobs a comma does. Anything outside these five is probably a pause you heard, not a comma the sentence needs.

| Job | Rule | Example |
|---|---|---|
| Join two clauses | Comma **before** the coordinator (and, but, or, so, yet) when both sides are independent | *She wrote the draft, and he edited it.* No comma if the second side has no subject: *She wrote the draft and edited it.* |
| Separate a list | Serial/Oxford comma before the final *and* — `oxford_comma`, default true | *red, white, and blue* |
| Fence a non-essential clause | Commas both sides, or neither. Test: remove it — if the sentence still identifies the same thing, fence it | *My brother, who lives in Leeds, called.* (one brother) vs *My brother who lives in Leeds called.* (several brothers) |
| Follow an introductory element | After anything before the main subject longer than ~4 words | *After the third release, we froze the API.* |
| Set off direct address and tags | *Thanks, Sam.* · *Let's eat, Grandma.* | The second one is the classic |

**Comma splice** — two independent clauses joined by a bare comma — is the most common punctuation error in confident writing. Test: put a full stop where the comma is. If both halves stand alone, it is a splice. Four fixes: full stop · semicolon · add a coordinator (*, and*) · subordinate one half (*Because…*). *However*, *therefore*, *thus* and *moreover* are **not** coordinators: *It was late, however we finished* is a splice → *It was late; however, we finished.*

**Which vs that** (US convention, and the clearest rule in either variety): *that* introduces an essential clause with no comma; *which* introduces a non-essential clause with commas. *The file that failed is in /tmp* (identifies which file) vs *The file, which failed, is in /tmp* (one file, extra fact). British usage permits *which* for both, but the comma still marks the difference — the comma is the real signal.

## Semicolons, Colons, Dashes

| Mark | Use | Test |
|---|---|---|
| Semicolon | Joins two independent clauses that belong together; also separates list items that already contain commas | Both sides must survive as sentences. If one is a fragment, use a colon or a dash |
| Colon | Introduces what the first half promised: a list, an explanation, a quotation | The part before the colon must be a complete sentence in formal writing |
| Em dash — | Interruption, dramatic aside, or a summary appositive. Closed (no spaces) in US style; UK style often uses a spaced en dash instead | Stronger than commas, less formal than parentheses |
| En dash – | Ranges (*2019–2024*, *pages 10–14*) and compound relationships (*the Paris–Berlin route*) | Never a substitute for a hyphen inside a word |
| Hyphen - | Joins words (→ Hyphens and Compounds) | The shortest of the three; not interchangeable |
| Parentheses | Aside the reader may skip | If deleting it damages the sentence, it does not belong in parentheses |

A range written with an en dash never also takes *from* or *between*: *from 2019 to 2024* or *2019–2024*, never *from 2019–2024*.

## Quotation Marks

| Point | US | UK |
|---|---|---|
| Outer marks | "double" | 'single' or "double" by house style; Oxford and most books use single |
| Nested | 'single' inside "double" | "double" inside 'single' |
| Period / comma | **Always inside**, whether or not it is part of the quote | Inside only if it belongs to the quoted material (logical punctuation) |
| Colon / semicolon | Always outside | Always outside |
| Question mark | Inside if the quote is the question; outside if the sentence is | Same rule |

Example of the transatlantic split: US *He called it "unworkable."* — UK *He called it 'unworkable'.* Both are correct in their own system, and mixing them in a document is the tell (`varieties.md`).

Scare quotes around a word signal distance or irony, and one per page is the budget. A term being introduced takes italics on first use, not quotes.

## Apostrophes

| Case | Form | Note |
|---|---|---|
| Singular possessive | the dog's bowl | |
| Plural ending in -s | the students' union | Apostrophe after the s, no second s |
| Irregular plural | the children's books | Treated as singular |
| Singular name ending in -s | James's car (Chicago, most UK) / James' car (AP) | Pick one, record it in `artifacts/style-sheet.md` |
| Joint vs separate possession | Anna and Ben's flat (shared) / Anna's and Ben's flats (separate) | |
| Decades | the 1990s, the '90s | Never *1990's* |
| Plural of acronyms and letters | CEOs, URLs, the three Rs | Apostrophe only for lowercase letters: *mind your p's and q's* |
| **its vs it's** | *its* = belonging to it; *it's* = it is / it has | No exceptions. The possessive pronoun never takes an apostrophe, like *hers*, *theirs*, *yours* |
| whose vs who's | *whose* = belonging to whom; *who's* = who is | Same pattern |

## Hyphens and Compounds

Three rules cover nearly all of it.

1. **Hyphenate a compound modifier before the noun, not after.** *a well-known author* / *the author is well known*. *a five-year-old child* / *the child is five years old*. *a state-of-the-art system* / *the system is state of the art*.
2. **Never hyphenate after an -ly adverb.** *a highly rated film*, *a rapidly growing market* — the -ly already shows the adverb attaches to the adjective. Exception: adjectives that end in -ly (*a friendly-looking dog*).
3. **Hyphenate to prevent a misreading.** *re-cover* (cover again) vs *recover*; *a small-business owner* vs *a small business owner*; *twenty-odd people* vs *twenty odd people*.

Compounds age from open → hyphenated → closed (*data base* → *data-base* → *database*). Currently closed in most style guides: email, online, website, database, checkbox, startup (noun), login (noun), setup (noun), workflow, filename. Still open as verbs: *log in*, *set up*, *back up*, *check out* — the noun is closed and the verb is two words. *"Please login"* is wrong; *"Please log in"* is right and *"the login page"* is right.

Prefixes are closed by default (*preorder*, *reopen*, *nonstandard*, *multiuser*), hyphenated when the prefix meets the same vowel (*re-enter*, *co-owner*), before a capital or numeral (*post-2020*, *anti-American*), or when the closed form already means something else (*re-sign* vs *resign*).

## Capitalization and Titles

**Sentence case** — only the first word and proper nouns — is the modern default for headings, UI labels, and most documentation. **Title Case** survives in book titles, article titles in citations, and some house styles.

Title Case rule, when you need it: capitalize the first and last word, all nouns, verbs (including *Is*, *Are*, *Be*), adjectives, adverbs and pronouns; lowercase articles (*a, an, the*), coordinating conjunctions (*and, but, or, nor, for, yet, so*) and prepositions — of four letters or fewer under AP, of any length under Chicago. So AP writes *A Room With a View* and Chicago writes *A Room with a View*. Pick one, record it in `artifacts/style-sheet.md`.

Capitalize: proper nouns and names, days, months, languages, nationalities, brand names as the brand writes them (*iPhone*, *eBay*), the first word of a full-sentence quotation, and job titles **before** a name (*CEO Ada Lovelace*) but not after (*Ada Lovelace, the chief executive*).

Do not capitalize: seasons, directions unless a region (*north* vs *the North*), generic uses of a discipline (*she studies economics*), "the internet" in most current style guides, or a common noun for emphasis (*our Platform*, *the Customer*) — this last one is the most common corporate-writing error and reads as legalese.

## Numbers

| Rule | AP | Chicago |
|---|---|---|
| Spell out | one through nine | one through one hundred, plus round numbers |
| Numerals from | 10 | 101 |
| Sentence start | Always spell out, or rewrite the sentence | Same |
| Percentages | 5 percent (spell the word) | 5 percent in prose, 5% in technical writing |
| Large numbers | 1 million, 3.4 billion | Same |
| Decimals | Always numerals, with a leading zero: 0.5 | Same |
| Thousands separator | 1,000 in English varieties — never a period, which is the decimal mark | Same |

Mixed in one sentence: if one item in a comparison needs numerals, use numerals for all of them (*8 of the 12 tests*).

Ordinals in dates: *26 July* or *July 26*, never *July 26th* in written dates — the *-th* belongs in speech.

Units: a space between the number and the unit (*5 kg*, *20 °C*, *64 GB*), no space before *%*, *°* alone, or a currency symbol. Ranges keep both units when ambiguity is possible (*5–10 kg*).

## Dates, Times, Currency

| Format | Reads as | Use when |
|---|---|---|
| 26 July 2026 | Unambiguous everywhere | UK/international prose — the safest human-readable form |
| July 26, 2026 | Unambiguous, US convention | US prose; comma after the year too if the sentence continues |
| 2026-07-26 | ISO 8601, unambiguous, sortable | Filenames, data, logs, international technical documents |
| 07/26/2026 | US only | Never in international text — 07/08 is 7 August to most of the world |
| 26/07/2026 | UK and most of the world | Never in US-facing text |

Numeric all-digit dates are the single most reliable way to be misread across varieties. Default to a spelled month or ISO.

**Times.** US *7:30 p.m.* (Chicago) or *7:30 pm* (AP); UK *7.30pm* or *19:30*. 24-hour time is standard outside the US and unambiguous everywhere. Always attach a timezone in anything scheduling across borders (*15:00 UTC*, *3pm CET*) — a bare time is the most common cause of a missed international meeting.

**Currency.** Symbol before the number, no space (*$50*, *£50*, *€50*). Disambiguate when more than one country uses the symbol: *US$50*, *A$50*, *C$50*. In tables and any text that another skill may sum, write the ISO code inside the value (*50 USD*) — the shared-box unit rule.

## Abbreviations

- **e.g.** = for example; **i.e.** = that is; **etc.** = and so on. Never *e.g.* and *etc.* in the same list — the *e.g.* already says the list is partial.
- US style puts a comma after *e.g.,* and *i.e.,*; UK style usually does not. Both usually italicize neither.
- **Full stops in abbreviations**: US keeps them (*Mr.*, *Dr.*, *U.S.*, *a.m.*); UK drops them when the abbreviation ends with the word's final letter (*Mr*, *Dr*, *St*) and keeps them otherwise (*Prof.*, *etc.*).
- **Acronyms**: expand on first use with the acronym in parentheses, then use the acronym alone. Do not expand universally known ones (*NASA*, *HTML*, *CEO*). *a* or *an* follows the **sound** of the first letter: *an FBI agent*, *a NATO summit*, *an MP*.
- **Latin abbreviations** (*viz.*, *cf.*, *N.B.*, *ibid.*) are rung 4-5 only; in general writing use the English (*namely*, *compare*, *note*).

## Lists and Bullets

- **Parallel grammar**: every item in a list starts with the same part of speech. Mixing noun phrases and full sentences is the most common list defect.
- **Punctuation**: full sentences take a full stop each; fragments take none. Never a semicolon at the end of each item followed by *and* — that convention is legal drafting.
- **Lead-in**: if the stem is a complete sentence, use a colon; if the items complete the stem grammatically, use no punctuation and no capital letters on the items.
- **Length**: a list of two is usually a sentence; a list above seven needs sub-grouping or a table.
- **Numbers vs bullets**: numbers only when order or count matters, or when items will be referenced by number.

**Write every mechanics decision the moment it is made** — Oxford comma, quote style, title case, date format, the possessive of names ending in -s, closed or open compounds the user cares about. The two with variables (`oxford_comma`, and the format implied by `variety`) go in `config.yaml`; everything else goes in `artifacts/style-sheet.md`, with its `## Boxes` line added in the same turn (`memory-template.md`). A style sheet is one file that ends every recurring argument; without it, each document reopens all of them.
