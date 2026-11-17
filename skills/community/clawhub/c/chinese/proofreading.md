# Proofreading Existing Chinese

**Before reviewing someone's text**, read `### Corrections` and `### Terms` in the glossary box `## Boxes` in `~/Clawic/data/chinese/memory.md` names: a rendering already settled is not re-litigated, and a correction already received is not re-made.

Review in passes, cheapest and most objective first. Mixing them produces a review that argues about style while a wrong number goes out.

**Contents:** [The Pass Order](#the-pass-order) · [Pass 1 — Encoding and Rendering](#pass-1--encoding-and-rendering) · [Pass 2 — 错别字 From Pinyin Input](#pass-2--错别字-from-pinyin-input) · [Pass 3 — Punctuation and Typography](#pass-3--punctuation-and-typography) · [Pass 4 — Facts and Numbers](#pass-4--facts-and-numbers) · [Pass 5 — Grammar and Variant](#pass-5--grammar-and-variant) · [Pass 6 — Register and Tells](#pass-6--register-and-tells) · [Reporting a Review](#reporting-a-review) · [What Gets Written Down](#what-gets-written-down)

## The Pass Order

| Pass | Finds | Why here |
|---|---|---|
| 1 Encoding | Mojibake, tofu, missing glyphs | A rendering fault makes every later pass unreliable |
| 2 错别字 | Homophone substitutions from pinyin input | Mechanical, checkable, and the most common defect in native text |
| 3 Punctuation | Half-width marks, wrong quotes, 、 as a comma | Mechanical, and the loudest signal |
| 4 Facts | Numbers, dates, names, titles, amounts | Objective and consequential; do it before style |
| 5 Grammar and variant | 的地得, 了, 把/被, mixed variant vocabulary | Rule-based |
| 6 Register and tells | Formality drift, AI fingerprints, flat vocabulary | Judgement; last, because it is the only arguable one |

## Pass 1 — Encoding and Rendering

| Symptom | Cause | Fix |
|---|---|---|
| 锟斤拷 | UTF-8 replacement characters (EF BF BD) re-decoded as GBK | Recover from the original source; the text is already lossy |
| 烫烫烫 | Uninitialised stack memory (0xCC) in an MSVC debug build | A program bug, not a text bug — the content was never written |
| 屯屯屯 | Uninitialised heap memory (0xCD), same family | Same |
| 涓枃 or similar gibberish | UTF-8 bytes decoded as GBK | Find the one hop that assumes a legacy encoding |
| ??? where characters should be | Lossy conversion to a single-byte charset at an export or database boundary | Column charset and connection charset, then re-export |
| Empty boxes (tofu) | Font lacks the glyph — rendering, not encoding | Check the font's coverage; rare characters and 繁體 variants are the usual victims |
| Mixed font weight mid-sentence | Some characters falling back to a different font | Same cause; often the giveaway that the text mixes 简体 and 繁體 (`regions.md`) |

GB18030 is the mandatory mainland encoding standard and covers the full Unicode repertoire; UTF-8 is what everything else uses. A file that opens correctly in one tool and not another is an encoding declaration problem, not a content problem — never "fix" mojibake by retyping the characters, because the underlying pipeline will corrupt the next document too.

## Pass 2 — 错别字 From Pinyin Input

Pinyin IMEs substitute homophones, so native Chinese text has a characteristic error profile that has nothing to do with fluency. The high-frequency set:

| Confused | Distinction |
|---|---|
| 的 / 地 / 得 | By what follows (SKILL.md Rule 7) |
| 在 / 再 | 在 = location or progressive · 再 = again, then |
| 做 / 作 | 做 concrete actions (做饭, 做事) · 作 abstract and compounds (作为, 工作, 作出) |
| 已 / 己 / 巳 | 已经 · 自己 · rare |
| 帐 / 账 | 账 for money (账单, 账号) · 帐 for cloth (帐篷) |
| 需 / 须 | 需要 (need) · 必须 (must) |
| 象 / 像 / 相 | 现象 · 好像, 图像 · 相片, 互相 |
| 那 / 哪 | 那 = that · 哪 = which |
| 他 / 她 / 它 / 祂 | Male / female / non-human / deity; only written, never audible |
| 即 / 既 | 即 = namely, immediately · 既 = since, both |
| 以 / 已 | 以为 (thought) · 已经 (already) |
| 应 / 因 | 应该 · 因为 |
| 权利 / 权力 | Right (entitlement) · power (authority) |
| 反应 / 反映 | Reaction · to report or reflect |
| 制定 / 制订 | Formulate and finalise · draft |
| 部署 / 布署 | 部署 is correct; 布署 is not a word |
| 一如既往 / 一如继往 | 既往 is correct |
| 甘拜下风 / 甘败下风 | 拜 is correct |

Two mechanical checks worth running on any long text: search for 的地得 occurrences and verify each against the following word, and search for 在/再 and verify each against its clause.

## Pass 3 — Punctuation and Typography

Against `punctuation.md`. The checklist, in order of frequency:

- Half-width `,` `.` `?` `!` `:` `;` inside Chinese text.
- ASCII `"` quotes instead of “ ” or 「」, and the wrong pair for the variant.
- `...` instead of ……, `—` (single) instead of ——.
- 、 joining clauses instead of separating list items.
- A space after full-width punctuation.
- Han-Latin spacing applied inconsistently — some occurrences spaced, some not.
- Titles in quotes instead of 《》.
- English numbering (`1.` `a.`) in a formal Chinese document where 一、（一） is expected.

## Pass 4 — Facts and Numbers

- Every number re-derived, not re-read: 万/亿 conversions are where a factor of ten hides (`numbers-and-names.md`).
- Amounts carry a currency and a 含税 status where relevant.
- Dates: check the weekday against the date, and check 农历 versus solar where a festival is named.
- Names, titles and company names against the glossary — a colleague renamed between paragraphs is the defect readers notice first.
- Percentages versus 百分点.
- 倍 constructions restated unambiguously.
- In a paper: figure and table numbers against their references, and citation numbers against the reference list (`academic.md`).

## Pass 5 — Grammar and Variant

Against `grammar.md` and `regions.md`:

- 的/地/得, 了 placement and count, 把 with a bare verb, 被 on a non-adverse verb.
- Measure words: every 个 that should be specific.
- Word order: time before place, duration after the verb, prepositional phrases before the verb.
- Variant consistency: one script throughout, one vocabulary set throughout. A converted text shows up as 繁體 characters with mainland words.
- The one-to-many characters (SKILL.md Rule 2) checked individually in any converted text — this is a per-character check and no tool does it reliably.

## Pass 6 — Register and Tells

- Register held for the whole text; check the opener, the body and the closing formula separately, since drift usually lives at the seams (`register.md`).
- The `ai-tells.md` sweep, all six passes.
- Address form consistent with previous texts to the same reader (`## Recipients`).
- Slang datable and inside `slang_appetite` (`slang.md`).
- 成语 checked for actual meaning, not surface meaning (`idioms.md`).

## Reporting a Review

Separate what is wrong from what is a preference. Mixing them is what makes a reviewer's comments get ignored wholesale.

| Category | Meaning | How to present |
|---|---|---|
| 错误 | Objectively wrong: 错别字, wrong number, broken grammar, wrong name | Fix it and list it |
| 不当 | Correct but wrong for this context: register, variant, a term that contradicts the glossary | Fix it and say why |
| 建议 | Preference: a stronger word, a shorter sentence | Offer it, do not apply it |

A review is delivered as the corrected text plus the list, not as the list alone — the writer wants the artifact, not homework. When the text is someone else's and the user is the reviewer, invert that: the list is the deliverable, so it goes to `artifacts/review-<what>.md`.

Scoring, when a number is wanted: state the formula rather than an impression. `errors per 1,000 字`, counting 错误 and 不当 separately, is enough — and any score without its formula is an opinion wearing a number.

## What Gets Written Down

- **Every correction the user accepts** → `### Corrections` in the glossary, with the wrong form, the right form and the date. This is what stops the same edit being made every session.
- **A review of someone else's text, when the user is the reviewer** → `artifacts/review-<what>.md`, with the error counts and the categories, and its `## Boxes` line in the same turn.
- **A recurring error pattern in the user's own writing** → `## Profile` or `### Corrections`, so later drafts are checked for it first. Three occurrences of the same 错别字 is a pattern, not an accident.
- **An encoding or tool problem and its workaround** → `## Environment`, because the same pipeline will corrupt the next document too.
