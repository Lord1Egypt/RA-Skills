# Citation Styles

`ct-literature` supports five citation styles (`--citation-style`), implemented in `scripts/format_citations.py`. It reads `merged.json` and reuses existing fields (title / authors / year / publication / volume / issue / page / doi / url) to assemble each citation. Exports `references.bib` (BibTeX) + `references.ris` (RIS).

> The applied style is labeled at the top of the report and `references_<style>.md` for traceability.

## 1. APA (7th) — default
```
Author, A. A., & Author, B. B. (Year). Title of article. *Journal Name*, *Vol*(Issue), Pages. https://doi.org/DOI
```
- Authors: surname, initials; multiple authors joined with `, &`.
- Journal name italic; volume italic, issue in parentheses.

## 2. Nature
```
Author1 AB, Author2 CD. Title of article. Journal Name Vol, Pages (Year). https://doi.org/DOI
```
- Given name first, abbreviated to initials (no dots); surname last; comma-separated.
- Inline style for numbered journals; year in trailing parentheses.

## 3. Vancouver (sequential numeric)
```
Author1 AB, Author2 CD. Title of article. Journal Name. Year;Vol(Issue):Pages. doi:DOI
```
- Up to 6 authors listed in full; beyond that, close with `et al.` (this implementation lists all, for clean Bib/RIS round-tripping).
- Year followed by `;Vol(Issue):Pages`.

## 4. IEEE
```
Author1, "Title of article," Journal Name, vol. Vol, no. Issue, pp. Pages, Year. doi: DOI.
```
- Article title in double quotes; `vol.` / `no.` / `pp.` explicit.

## 5. GB/T 7714 (PRC national standard)
```
Author. Title[J]. Journal, Year, Vol(Issue):Pages. DOI:DOI.
```
- **Chinese branch**: full-width Chinese punctuation (。、[J]、，、：); authors separated by Chinese comma 「，」.
- When mixing with the English styles (apa/nature/vancouver/ieee), branch on `style == 'gb7714'` so Chinese punctuation is not swallowed by the English templates.

## Field mapping (merged.json → citation)
| Citation element | merged.json field |
|---|---|
| Authors | `authors` (list; tolerates string/None) |
| Year | `year` |
| Title | `title` |
| Journal | `publication` |
| Volume / Issue / Pages | `volume` / `issue` / `page` |
| DOI / Link | `doi` / `url` |

## Notes
- Purely local generation; does not touch the fetch layer. Styles are layout templates only, not formal typographic validation.
- Author-name resolution handles both `Surname, Given` and `Given Surname`; Chinese names are preserved as a single token.
