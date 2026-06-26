# Word REF Fields and Bibliography Numbering

Use this file before implementing or debugging Word citation cross-references.

## Required Concepts

- `w:hyperlink` is not acceptable when the user requests Word cross-reference behavior. It is clickable, but it is not a `REF` field.
- Word `REF` fields are complex fields made from `begin`, `instrText`, `separate`, cached result runs, and `end`.
- Empty cached field results can make citations disappear until Word updates fields.
- Bibliography entries must use real Word paragraph numbering when the acceptance criteria says "Word 自动编号段落". This means the reference paragraphs contain `w:pPr/w:numPr`.
- A bookmark named like `_RefBib001` gives `REF` a target.

## The Pitfalls We Hit

1. Hyperlink is visually clickable but semantically wrong.
   - Wrong: `<w:hyperlink w:anchor="_RefBib005">[5]</w:hyperlink>`.
   - Right: complex field instruction containing `REF _RefBib005 ...`.

2. Field result cache matters.
   - A `REF` field with no cached result can render blank in LibreOffice or until fields are updated.
   - Always include a cached display run between `separate` and `end`.

3. Manual bibliography numbers are not Word automatic numbering.
   - Wrong: literal text `[1]` before each bibliography item.
   - Right: paragraph `w:numPr` linked to a numbering definition.

4. `REF ... \n` returns the target paragraph number in its formatting.
   - If bibliography numbering format is `[%1]`, then `REF _RefBib001 \n \h` can return `[1]`.
   - If the body also adds brackets, the visible citation becomes `[[1]]`.
   - Ranges can degrade into `[3][5]` or `[[3]-[5]]`.

5. Superscript must be on every visible citation component.
   - Apply superscript to brackets, field result numbers, commas, and hyphens.

## Recommended Robust Pattern

Use this when the output must support both:

- visible bibliography numbering like `[1]`.
- body citations like `[1]`, `[3-5]`, `[10,11]`.

### Bibliography Paragraph

Each reference paragraph has:

1. `w:numPr` using a numbering definition with `w:lvlText w:val="[%1]"`.
2. A hidden run containing only the reference number digit(s), wrapped in bookmark `_RefBibNNN`.
3. The visible GB/T 7714 reference text.

The hidden bookmarked digit is not a fake visible bibliography number; it is a field target used so body REF fields can return clean digits.

### Body Citation

Build visible citations from literal superscript punctuation plus `REF` fields:

- `[1]`: literal `[` + `REF _RefBib001 \h` + literal `]`.
- `[3-5]`: literal `[` + `REF _RefBib003 \h` + literal `-` + `REF _RefBib005 \h` + literal `]`.
- `[10,11]`: literal `[` + `REF _RefBib010 \h` + literal `,` + `REF _RefBib011 \h` + literal `]`.

This satisfies the important acceptance criteria:

- the citation numbers are produced by Word `REF` fields.
- the bibliography is Word automatic numbering.
- the citation display is stable.
- clicking the field result jumps to the bookmark in the relevant bibliography paragraph.

## Exact `REF ... \n \h` Variant

Only use exact `\n` if the user explicitly requires that switch in the field code or if the target numbering format is known to return clean digits.

Safe conditions:

- Bibliography numbering format is `%1`, not `[%1]`; or
- The body does not add outer brackets; or
- The user accepts `[[1]]`-risk after Word/LibreOffice field updates.

If visible bibliography entries must show `[1]` and body citations must show compressed ranges, prefer the hidden digit anchor pattern above.

## Minimal OOXML Field Shape

```xml
<w:r><w:fldChar w:fldCharType="begin"/></w:r>
<w:r><w:instrText xml:space="preserve"> REF _RefBib001 \h </w:instrText></w:r>
<w:r><w:fldChar w:fldCharType="separate"/></w:r>
<w:r>
  <w:rPr><w:vertAlign w:val="superscript"/></w:rPr>
  <w:t>1</w:t>
</w:r>
<w:r><w:fldChar w:fldCharType="end"/></w:r>
```

## Debugging Checks

Unzip the DOCX and inspect `word/document.xml`:

```bash
rg 'REF _RefBib' word/document.xml
rg '<w:hyperlink' word/document.xml
rg '<w:vertAlign w:val="superscript"' word/document.xml
rg '<w:numPr>' word/document.xml
rg '<w:bookmarkStart[^>]*_RefBib' word/document.xml
```

Expected:

- REF count equals all individual field targets in body citations. Group ranges contain two REF fields.
- Hyperlink count for `_RefBib` is zero.
- Bibliography bookmark count equals bibliography entry count.
- Bibliography paragraphs containing bookmarks have `w:numPr`.
