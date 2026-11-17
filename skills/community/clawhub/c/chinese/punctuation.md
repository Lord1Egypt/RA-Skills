# Punctuation and Typography

Chinese punctuation is full-width, occupies one character cell each, and carries its own spacing. Getting it wrong is the most visible non-native mark in the text and it survives every round of style editing (SKILL.md Rule 8).

**Contents:** [The Full-Width Set](#the-full-width-set) · [、 Is Not a Comma](#-is-not-a-comma) · [Quotes and Titles](#quotes-and-titles) · [Ellipsis and Dash](#ellipsis-and-dash) · [Han-Latin Spacing](#han-latin-spacing) · [Numbers and Digits Inside Chinese Text](#numbers-and-digits-inside-chinese-text) · [Lists and Headings](#lists-and-headings) · [Line Breaking](#line-breaking) · [Where the Rules Change](#where-the-rules-change) · [What Gets Written Down](#what-gets-written-down)

## The Full-Width Set

| Mark | Character | Notes |
|---|---|---|
| Period | 。 | U+3002. A small circle, not a dot. Dropped at the end of chat messages (`chat.md`) |
| Comma | ， | U+FF0C. Between clauses |
| Enumeration comma | 、 | U+3001. Between items inside a list, never between clauses |
| Semicolon | ； | Between parallel clauses, common in formal Chinese |
| Colon | ： | After 称呼 in letters, before quotations and lists |
| Question mark | ？ | |
| Exclamation | ！ | |
| Parentheses | （） | Full-width when wrapping Chinese; half-width `()` when wrapping Latin text |
| Book title marks | 《》 and 〈〉 | Titles of books, films, articles, laws. 〈〉 nests inside 《》 |
| Interpunct | · | Separates parts of a foreign name: 史蒂夫·乔布斯 |
| Wave dash | ～ | Ranges in casual and Taiwanese writing: 3～5天 |

**No space after any of them.** The character cell already includes the space. `你好， 请问` with a space is doubly wrong.

## 、 Is Not a Comma

- 苹果、香蕉、橙子 ✓ — items in one list.
- 我去了公司、他去了学校 ✗ — those are clauses; use ，.
- In numbered formal text the 顿号 is built into the number: 一、二、三、 (`documents.md`).
- Between two-item pairs joined by 和 or 与, no 、 is needed: 中国和美国, not 中国、和美国.

## Quotes and Titles

| Variant | Outer quotes | Inner quotes |
|---|---|---|
| Mainland (simplified, horizontal) | “ ” | ‘ ’ |
| Taiwan and Hong Kong | 「」 | 『』 |
| Any vertical text | 「」 | 『』 |

- Straight ASCII quotes `"` inside Chinese text are a defect; so is a mainland document using 「」 unless it is deliberately quoting Taiwanese source text.
- **Titles take 《》, not italics and not quotation marks.** 《红楼梦》, 《流浪地球》, 《中华人民共和国合同法》. English keeps italics; Chinese has no italic tradition, and italicised Chinese characters render badly.
- Emphasis in Chinese is bold or 着重号 (a dot under each character), never italics.

## Ellipsis and Dash

- Ellipsis is **……** — two U+2026 characters, six dots, one full-width pair of cells. Three ASCII dots is a Latin ellipsis and reads as imported.
- Dash is **——** — two U+2014 characters. One em dash alone is too short in a Chinese line.
- In chat, …… means hesitation or displeasure rather than omission (`chat.md`).
- A dash sets off an explanation; a colon introduces one; a parenthesis subordinates one. Chinese uses the colon more and the dash less than English does.

## Han-Latin Spacing

There is **no national standard requiring a space** between Chinese characters and Latin letters or digits. The dominant web typography convention adds one half-width space on each side; many print houses do not. This is a house style, governed by `latin_spacing`:

- On: 使用 Docker 部署，版本 24.0。
- Off: 使用Docker部署，版本24.0。

Rules that hold either way:

- Never a space between a Chinese character and full-width punctuation.
- Never a space inside 《》 or 「」.
- Half-width Latin punctuation stays attached to its Latin text: `Node.js v20` keeps its dot.
- Whichever way `latin_spacing` goes, **apply it to every occurrence in the document**. Mixed spacing looks like a merge conflict, which is worse than either convention.

## Numbers and Digits Inside Chinese Text

- Arabic numerals for quantities, dates, versions, money, measurements: 3个人, 2026年, 15%.
- Chinese numerals for idioms, approximations, ordinals in formal headings, and legal amounts: 三三两两, 十几个, 一、二、三、, 人民币壹万元整.
- Never mix inside one construction: 3千 is wrong; 3,000 or 三千.
- Grouping is by four (万/亿), not by three (SKILL.md Rule 3, `numbers-and-names.md`).
- Percentages use %, and 百分之三十 is the written-out formal alternative. 30%的用户 takes no space before 的.

## Lists and Headings

Formal Chinese documents have their own numbering hierarchy, and using the English one marks the document as translated:

| Level | Marker | Note |
|---|---|---|
| 1 | 一、二、三、 | 顿号 built in, no bracket |
| 2 | （一）（二） | Full-width brackets, no 顿号 after |
| 3 | 1. 2. 3. | Arabic with a half-width period |
| 4 | （1）（2） | |

Bullets with • or - are normal in email, chat and social copy, and out of place in a 公文 (`documents.md`).

## Line Breaking

禁则 (kinsoku) rules — a renderer that respects them exists in most publishing tools and in none of the plain-text ones:

- A line never **starts** with 。，、；：？！）」』》 or a closing quote.
- A line never **ends** with （「『《 or an opening quote.
- …… and —— are never split across lines.
- A number and its unit stay together: 30% and 5kg do not break.

If the output will be pasted into a tool that does not respect this, keep lines short enough that it does not arise rather than inserting manual breaks — manual breaks survive into contexts where they are wrong.

## Where the Rules Change

| Context | Difference |
|---|---|
| Chat | Final 。 dropped, internal ， often a space or a line break (`chat.md`) |
| Social copy | Emoji act as bullets; ！ and ～ are frequent; 。 still dropped at line ends on 小红书 |
| Taiwan / Hong Kong | 「」 quotes; wave dash more common; full-width punctuation is often **centred** in the cell rather than left-aligned, which is a font behaviour, not something to type |
| Vertical text | 「」 quotes and the dash rotates; only relevant for print and calligraphy |
| Code and technical text | Half-width everything inside code, always; the surrounding prose stays full-width (`academic.md`) |

## What Gets Written Down

- **A typography convention the user states** — quote style, spacing, indent versus blank line, 星期六 versus 周六 → its key in `config.yaml` under `conventions`, never in `memory.md` (`memory-template.md`).
- **A platform or tool that mangles punctuation** — an editor that converts full-width quotes, a CMS that strips 。, a font missing 、 → `## Environment` in `memory.md`, because the workaround will be needed again.
