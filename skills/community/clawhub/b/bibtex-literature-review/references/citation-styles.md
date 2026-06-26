# Citation and Bibliography Styles

Use this file when the user asks for APA, MLA, Chicago, IEEE, Vancouver, Harvard, GB/T 7714, or other common citation formats.

## Important Distinction

This skill has two separate layers:

- **Body citation mechanism**: default is clickable numeric Word `REF` fields, displayed as superscript `[1]`, `[3-5]`, or `[10,11]`.
- **Bibliography formatting style**: the text after each bibliography number can be formatted as GB/T 7714, APA, MLA, Chicago, IEEE, Vancouver, or Harvard.

APA and MLA normally use author-date or author-page in-text citations, not numeric Word cross-references. If the user still requires clickable Word `REF` fields, keep the numeric REF mechanism and apply APA/MLA only to the bibliography text. If the user asks for pure APA/MLA in-text citations, clarify that it will no longer be the same numeric REF cross-reference workflow unless a custom bookmark strategy is designed.

## Supported Bibliography Styles

Use `scripts/sources_to_json.py --style STYLE`.

Supported values:

- `gbt7714`: GB/T 7714-like numeric bibliography strings.
- `apa`: APA-like reference list strings.
- `mla`: MLA-like works-cited strings.
- `chicago`: Chicago notes/bibliography-like strings.
- `ieee`: IEEE-like numbered-reference strings.
- `vancouver`: Vancouver-like biomedical strings.
- `harvard`: Harvard-like author-date strings.

Example:

```bash
python scripts/sources_to_json.py refs.bib --style apa --out candidates_apa.json
```

The output keeps the formatted reference in both `gbt` and `formatted` for compatibility with the DOCX builder.

## Style Requirements

The bundled formatter is a deterministic baseline. Before delivery, inspect the generated reference list against the requested style and correct obvious metadata, punctuation, and capitalization issues in the curated review JSON.

### GB/T 7714

- Use numeric order matching first citation order unless the user requests author/year sorting.
- Use source type markers such as `[J]`, `[M]`, `[C]`, `[D]`, `[R]`, or `[EB/OL]` when metadata supports them.
- Chinese names and titles should be preserved as provided.
- English article titles should preserve meaningful proper nouns and protected capitalization from the source export.
- Journal articles should prefer: `作者. 题名[J]. 刊名, 年, 卷(期): 页码.`
- Books should prefer: `作者. 书名[M]. 出版地: 出版者, 年.`
- Do not invent place, publisher, volume, issue, pages, DOI, URL, or access dates.

### APA

- APA normally uses author-date in-text citations. If the document must keep clickable Word `REF` citations, use APA only for bibliography text.
- Reference list author names should be family name plus initials, with an ampersand before the final author when appropriate.
- Year appears in parentheses after authors; use `n.d.` only when the year is genuinely unavailable.
- Article and book titles use sentence case: capitalize the first word, subtitle first word, and proper nouns.
- Journal titles use title case; volume is normally italic and issue appears in parentheses. Plain DOCX text may not preserve italics unless manually styled.
- DOI should be rendered as a URL when present, for example `https://doi.org/...`.

### MLA

- MLA normally uses author-page in-text citations. Keep numeric Word `REF` citations only when the user prioritizes Word cross-reference behavior.
- Works Cited entries normally use title case for English titles.
- Article titles are quoted; containers such as journals/books are styled as source titles.
- Include version/volume/number, publisher, date, and location/page fields when present.
- Preserve author order and use `et al.` only when the style/user permits it.

### Chicago

- Clarify whether the user wants notes-bibliography or author-date. The bundled `chicago` output is a simplified bibliography-like reference.
- English titles should use headline/title case unless source metadata requires another convention.
- Article/chapter titles are quoted; container titles normally use title case.
- Include publisher/place for books and volume/issue/pages for journal articles when present.

### IEEE

- IEEE uses numeric in-text references, so it fits this skill's default numeric REF workflow well.
- Bibliography order should follow first citation order.
- Article titles are usually in quotation marks; journal/conference titles are abbreviated when the source metadata already provides accepted abbreviations.
- Use initials before family names for English author names when metadata allows.
- Include volume, number, pages, month/year, and DOI when present.

### Vancouver

- Vancouver is numeric and fits the default REF workflow.
- Bibliography order should follow first citation order.
- Author names usually use family name followed by initials without periods.
- List up to six authors, then `et al.` when appropriate.
- Journal titles are often abbreviated; use official abbreviations only if they are present in the source export or supplied by the user.
- Use compact year/volume/issue/page punctuation when metadata supports it.

### Harvard

- Harvard normally uses author-date in-text citations. If clickable Word `REF` citations are required, apply Harvard only to bibliography text.
- Author names remain in author-date order, year follows authors, and titles/source fields should preserve style-appropriate capitalization.
- Article/book titles are commonly sentence case, while journal titles retain title case.
- Include DOI or URL only when present and required by the user's institution.

## Capitalization Rules

- Prefer the capitalization preserved by Zotero/CSL/BibTeX metadata.
- Do not force lowercase globally. This can destroy proper nouns, acronyms, gene names, dataset names, product names, and title-protected BibTeX braces.
- For APA/Harvard sentence case, only normalize manually when you are confident; otherwise preserve source title capitalization and flag it for review.
- For MLA/Chicago title case, preserve source title capitalization unless the user asks for strict title-case normalization.
- Keep Chinese titles unchanged except for obvious whitespace and punctuation cleanup.
- Keep acronyms such as AI, HRM, ESG, DNA, OECD, and country/organization names uppercase.

## Quality Notes

The bundled formatter is deterministic and suitable for draft production, but it is not a full CSL engine. For publication-grade APA/MLA/Chicago output:

- Inspect capitalization, italics, author particles, edition data, translators, access dates, and DOI formatting.
- Preserve missing-field honesty; do not invent metadata.
- If the user provides an official style requirement, follow that over the simplified bundled formatter.
- When strict style compliance matters, prefer exporting formatted references from Zotero/Better BibTeX/CSL and using this skill primarily for selection, review drafting, DOCX REF generation, and validation.

## Practical Recommendations

- Chinese theses: use `gbt7714`.
- Engineering papers with numeric references: use `ieee` while keeping numeric REF body citations.
- Medical or biomedical documents: use `vancouver`.
- International management/social science drafts: use `apa` or `harvard`.
- Humanities drafts: use `mla` or `chicago`, but ask before replacing numeric REF citations with author-page style.
