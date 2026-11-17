---
name: "apa-7-referencing"
description: "Clean generic APA 7 referencing (English conventions): reference lists, in-text citations, DOIs, secondary sources, quotes, tables. Use for any paper requiring APA 7 style."
---

# APA 7 Referencing

Build correct APA 7th edition references and in-text citations in English. This is generic APA 7 with no institutional deviations. For the Swedish SHH variant, see the sibling skill `swedish-apa-referencing`.

## Steps

1. Read `references/apa7-quickref.md` for the operative templates, then match the source type:

   - Journal: `Author, A. A. (Year). Title of article. Journal Name, Volume(Issue), pages. https://doi.org/...`
   - Book: `Author, A. A. (Year). Title of work: Subtitle (2nd ed.). Publisher.`
   - Chapter: `Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.), Book title (pp. xx-xx). Publisher.`
   - Web page: `Author, A. A. (Year, Month Day). Title. Site Name. URL`

2. In-text: parenthetical `(Author, Year)` or `(Author, Year, p. X)`; narrative `Author (Year)`. Two authors: `(Smith & Jones, 2024)` in parentheses, `Smith and Jones (2024)` in narrative. Three or more authors: `(Smith et al., 2024)` from the first citation.

3. Apply the structural rules that generic tools get wrong:
   - Reference list: 1-20 authors listed, `&` before the last; 21+: first 19, ellipsis, final author
   - Sentence case for article and book titles; title case only for journal names
   - DOI always as a full `https://doi.org/...` link; no publisher location anywhere
   - `n.d.` when no date; group authors written out in full
   - `pp.` for page ranges in chapters and articles (`pp. 707-745`), `p.` for single pages

4. Secondary sources: cite only what you read. In-text: `(Eriksson, 1984, as cited in Willman, 2022, p. 203)`. Reference list: only Willman (2022).

5. Quotations: under 40 words run inline with double quotation marks and `(Author, Year, p. X)` after; 40+ words as an indented block without quotation marks, citation after the final punctuation.

6. Verify: every in-text citation has a matching list entry (same lead author and year) and vice versa; alphabetical order; same author + year gets `2024a`/`2024b` suffixes in both text and list; no fabricated or unverified references.

## Pitfalls

- APA 7 dropped publisher location; do not add city.
- `Retrieved from` appears only when content changes over time and a retrieval date is needed.
- Volume is italic in journals, the issue number is not: `Journal Name, 12(3), 45-60.`
- The reference list contains only sources cited in text; never pad it.

## Provenance

Clean-room summary of APA 7 (Publication Manual of the American Psychological Association, 7th ed.) conventions for agent use, authored 2026-09-03. Pairs with `swedish-apa-referencing` for institutional SHH deviations.