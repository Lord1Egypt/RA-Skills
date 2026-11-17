# Style guide: Chinese sci-tech report exhibits

Numbers below are the values that survive review in practice; adapt them only after measuring the target document.

## Page and text width

Measure first: A4 is 21 × 29.7 cm; margins are often 3.175 cm left/right and 2.54 cm top/bottom, leaving **14.65 cm** of usable width. Every figure and full-width table is set to that width (14.5 cm is a safe round value). Mixed widths — one image at 15.59 cm, the next at 14.5 cm — read as a mistake even when nobody can name it.

## Three-line tables (三线表)

| Property | Value |
|---|---|
| Border above header | 1.5 pt (`w:sz="12"`, unit is 1/8 pt) |
| Border under header | 0.75 pt (`w:sz="6"`) |
| Border at table bottom | 1.5 pt |
| Vertical / inner borders | none |
| Table body text | 9 pt, 宋体 for Chinese + Times New Roman for digits, single spacing |
| Header text | same size, bold, centered |
| Cell margins | 85 dxa left/right, 40 dxa top/bottom |
| Column widths | fixed; total = table width; set both `tblW` and each `gridCol`/`tcW` |
| Row policy | `cantSplit` on every row, `tblHeader` on row 1 |

Caption **above** the table, centered, 10.5 pt bold, `keep_with_next`, numbered `表1　标题` (ideographic space, no colon). Note **below** the table, 9 pt, left aligned, starting `注：`.

Implementation traps:

- `python-docx` appends `tblBorders`/`tblCellMar` after `w:tblLook`, which is invalid OOXML order. Insert them with `tblPr.insert_element_before(el, "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook")` and pass tag **strings**, not `qn()`.
- `table.autofit = False` already writes `w:tblLayout`; do not add a second one.
- Without `cantSplit`, a long table splits and the header does not repeat on the next page.

## Figures

- Insert at the text width, centered, no first-line indent, `keep_with_next` so the caption stays attached.
- Caption **below**, centered, 12 pt (matching body size, no bold), `图1　标题`; note below the caption, 9 pt.
- Chart text sizes: base 9 pt, labels 9 pt, tick labels 8.5 pt. Draw the canvas at the final physical size (14.5 cm wide) so nothing is rescaled after insertion.
- Fonts: `font.family = ["Times New Roman", "SimSun"]` gives Times digits and SimSun Chinese without a per-text override. SimSun has no bold face — avoid `fontweight="bold"` in charts (matplotlib warns and falls back).
- Do not insert thousands separators inside chart labels if the source text writes “41121”; the report's own formatting is the authority.
- Palette that prints well in grayscale: `#2E5A88` (primary), `#1F3A56` (dark), `#9DB7D0` (light), `#8C8C8C` (neutral), `#A34A3F` (alert/reference line), grid `#D9D9D9`.
- Spines: left + bottom only. Grid: horizontal only, behind data. Add value labels above bars; a chart that needs a table to be read is not doing its job.

## Choosing the form

| Content | Form |
|---|---|
| Targets vs. actuals, terms, ratings across ≥2 countries/years | Table |
| One magnitude across 3–6 categories | Vertical bars with value labels |
| Shares of a total, 3–6 items, long Chinese labels | Horizontal bars, 0–100 % axis |
| Supply vs. demand, gap to a threshold | Bars + dashed reference line + labelled gap |
| Causal chain / reinforcing loop | Box-and-arrow schematic, monochrome + one accent color |

Avoid pie charts, 3-D bars, dual axes with two units, and charts whose only message is “several things exist”.

## Text integration

- Reference every exhibit in the body: `（见表1）` / `（见图2）`, inserted before the sentence's final `。` in the paragraph the exhibit supports.
- One reference per exhibit; if two exhibits support the same paragraph, write both in one parenthesis: `（见图4、图5）`.
- Never reword the sentence to mention the exhibit. The reference is an insertion, nothing else.
- Notes carry two jobs: explain any derived value (`注：缺口为需求与可用供给之差。`) and name the source (`资料来源：根据本节正文数据整理。`). Do not cite external literature the report does not cite.

## Derived values

Allowed: difference, ratio, share within a stated total, sum of listed components. Not allowed: growth rates over unstated baselines, per-capita figures needing unstated populations, currency conversions, interpolations between years.

Always show the arithmetic in the delivery message, e.g. `66.5% = 16 422 / 24 699`, `254 MW = 2 400 − 2 146`, `7.3 pp = 23% − 15.75%`. If the report itself already states the rounded result (“接近三分之二”, “约 14% 的差距”), prefer that wording in the note.

## Page flow

Word decides pagination; you only check it. A table that cannot fit moves to the next page and leaves white space — acceptable. A caption stranded on the previous page is not: it means `keep_with_next` is missing. A table split across pages is not: it means `cantSplit` is missing. Look at every exhibit page as an image before delivering.

## Exporting a preview

Windows with Word installed (fastest, keeps fonts):

```powershell
$w = New-Object -ComObject Word.Application
$w.Visible = $false; $w.DisplayAlerts = 0
$doc = $w.Documents.Open($src, $false, $true)
$doc.ExportAsFixedFormat($pdf, 17)   # 17 = wdExportFormatPDF
Start-Sleep -Milliseconds 800
Get-Process WINWORD | Stop-Process -Force   # Close() often throws 0x800706BE after a successful export
```

Elsewhere: `soffice --headless --convert-to pdf report.docx`. Then render with `scripts/verify_layout.py` and read the page images.
