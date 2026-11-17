---
name: dairy-market-report
version: 3.0.0
description: Use when the user asks to generate a China dairy market intelligence report (乳制品市场行情报告). Reads dairy industry monthly PDFs (e.g. 艾格农业-中国乳业研究月报) plus any supplementary documents in the working directory, then produces a single, magazine-style PDF report covering raw milk prices, feed costs, China vs overseas milk prices, dairy production & import YTD, exports, GDT auction results, GDT-to-warehouse landed cost calculations (AMF/WMP/SMP, contract-2 pricing), outlook, deep-dive analysis, deep-processing innovation, and corporate/policy events. Layout: continuous flow (no forced page break per section), 12 numbered sections, KPI cards, banded tables, color-coded change pills (涨红跌绿), AI takeaway callouts, and a cover + two-column TOC.
agent_created: true
license: Internal
---

# Dairy Market Report (乳制品市场行情报告)

## Overview

This skill ingests one or more Chinese-language dairy industry monthly PDFs (e.g. 艾格农业《中国乳业研究月报》) and any related `.docx` policy briefs in the working directory, extracts the relevant data, and produces a complete, multi-section **乳制品市场行情报告** as a **single PDF document** (`乳制品市场行情报告_YYYYMM.pdf`).

The report follows a fixed 12-section structure (see `references/report-template.md`) and embeds GDT-to-warehouse landed-cost calculations per the user's formulas.

### Visual identity (magazine-style, continuous flow)

The default PDF aesthetic is a **professional business-magazine look** — not a default reportlab dump. Concretely:

- **Cover page** (page 1): deep navy band with the report title + period in gold, followed by a米色 "CORE TAKEAWAYS · 核心结论" card with bulleted one-liners.
- **Two-column TOC** under the cover, listing all 12 sections.
- **Body sections flow continuously** — no `PageBreak` per section. The renderer (reportlab + `STSong-Light` CJK font) handles natural pagination. Typical output is 8–10 pages.
- **Section header**: `SECTION 0X / 12` ordinal on the left, large dark-navy title, a short gold rule under it.
- **KPI cards**: 3–4 per section, each = small label + large value + colored change pill (e.g. `+3.8%` red ↑ or `-9.4%` green ↓).
- **Data tables**: navy header band, banded rows (white / 米 alternating), soft 0.25pt borders, numeric right-aligned.
- **Change pills**: filled with light red/green/grey, same-color border, ↑/↓/→ glyph.
- **AI 解读 callout**: 3pt gold left bar + 浅米 background, italic 解读 line.
- **Source footer** under every data-bearing section in small grey type.
- **Page footer**: hairline rule + report title + `— N —` page number on every body page.

Color tokens (use these exactly; renderer has them baked in):

| Token | Hex | Use |
|---|---|---|
| `INK` | `#1B2733` | body text |
| `NAVY` | `#0E2A47` | primary brand, section titles, table header |
| `ACCENT` | `#D4A24C` | gold accents, callout bar, cover subtitle |
| `SOFT_BG` | `#F4F1EA` | callout background, zebra row B |
| `RED` | `#B0322B` | price-up (Chinese stock convention) |
| `GREEN` | `#1F7A4D` | price-down |

**Do not** insert a hard `PageBreak` between sections, and do not wrap every section in `KeepInFrame`. The renderer already balances density; forcing a page break per section leaves large white gaps.

### Data schema (what `render_pdf.py` consumes)

`render_pdf.py --data <data.json>` expects a single JSON object. The schema lives at the top of `scripts/render_pdf.py` and is mirrored in `references/data-schema.md`. The minimum fields are:

```json
{
  "meta": {
    "title": "乳制品市场行情报告",
    "period": "2023年10月",
    "generated_at": "2026-06-26",
    "sources": ["艾格农业《中国乳业研究月报》202310", "农业农村部"]
  },
  "key_takeaways": ["国内奶价 ...", "GDT 反弹 ...", "..."],
  "sections": [
    { "title": "乳业整体形势概览", "kpis": [...], "tables": [...], "callout": "...", "source": "..." },
    { "title": "生鲜乳",          "kpis": [...], "tables": [...], "callout": "...", "source": "..." },
    ...
    { "title": "乳业重要事件及乳品企业动态资讯", "events": [...], "source": "..." }
  ]
}
```

Each `kpis` entry is `{label, value, change}` (change string is parsed for `+/-` or `↑/↓` to pick the pill color). Each `tables` entry is `{header: [str], rows: [[str, ...]]}`. `callout` is a single string.

## When to use this skill

Trigger this skill when the user asks for any of the following, especially when Chinese-language dairy PDFs are present in the working directory:

- 生成乳制品市场行情报告 / 乳业月报 / 乳业研究月报
- 解读艾格农业《中国乳业研究月报》/ 制作对应行情报告
- 跑一遍乳业月报 → 输出 PDF
- 生鲜乳 / 饲料 / GDT / 进口乳制品 / 乳品深加工 综合行情

Do NOT use this skill for: ad-hoc single-data-point questions, English-language dairy market reports (use the English-language equivalent skill), or topics unrelated to dairy commodities.

## Bundled resources

Read these on demand — they are not all needed up front.

| File | Read it when |
|---|---|
| `references/report-template.md` | You are about to draft the report — it defines each of the 12 sections, expected data points, narrative guidance, and a "deep takeaway" expectation per section |
| `references/data-schema.md` | You are about to assemble the data JSON for the renderer — it documents every key (`meta`, `key_takeaways`, `sections[*].kpis/tables/callout/source/events`) and the change-pill sign convention |
| `references/data-sources.md` | You need to look up a number but the PDF didn't spell it out — covers 农业农村部, 国家统计局, 海关总署, GDT, USDA, Dairy Australia, Eurostat, DCANZ, AHDB, etc. |
| `references/gdt-formulas.md` | You are filling section 8 (GDT → 入仓成本) — restates the user's formulas and shows the example worked-out numbers |
| `scripts/extract_pdf_text.py` | You need raw text from a `.pdf` (e.g. 艾格农业月报). Usage: `python extract_pdf_text.py <pdf> [out.txt]` |
| `scripts/extract_docx_text.py` | You need raw text from a `.docx` (e.g. 政策文件). Usage: `python extract_docx_text.py <docx> [out.txt]` |
| `scripts/gdt_calculator.py` | You are computing section 8 numbers. Usage: `python gdt_calculator.py --contract2-amf <price> --contract2-wmp <price> --contract2-smp <price> --fx <CNY/USD> --out <csv>` |
| `scripts/render_pdf.py` | You have the filled data dict and need to emit the magazine-style PDF. Usage: `python render_pdf.py --data <data.json> --out <report.pdf>`. Uses `reportlab` + built-in CJK font (`STSong-Light`); no Chromium/Playwright required. **Do not modify the layout logic in this file** — it is the canonical visual spec for the report. |
| `assets/styles.css` | **(DEPRECATED)** — kept for reference only; the PDF is generated natively and does not need CSS |
| `assets/report-template.html` | **(DEPRECATED)** — kept for reference only; the PDF is generated natively and does not need an HTML template |

## Workflow

Follow these steps in order. Stop and ask the user only if a required input is genuinely missing — most inputs are recoverable from the PDFs themselves.

### 1. Discover input documents

List the working directory (`ls` / Glob for `*.pdf`, `*.docx`, `*.txt`, `*.md`, `*.xlsx`, `*.csv`). For each:
- **PDF** that looks like a dairy monthly (e.g. 艾格农业《中国乳业研究月报》YYYYMM) → primary source, must extract
- **DOCX** with policy / industry-event language → supplementary source
- Other files (CSVs, Excel) → may be raw data dumps; peek inside if small

Ask the user only if the report target month / year is not obvious from the filenames.

### 2. Extract text from all PDFs and DOCX

Run the bundled extractors on every relevant file:

```bash
python scripts/extract_pdf_text.py "艾格农业-中国乳业研究月报202310.pdf" work/202310.txt
python scripts/extract_docx_text.py "农业农村部召开科技创新....docx" work/policy.txt
```

Place the text files in a `work/` subfolder (scratch space). Read them fully (or in slices) to identify which sections of `references/report-template.md` each PDF covers. One monthly typically covers raw milk, feed, production, imports, exports, GDT, and policy; a single PDF rarely has everything, so cross-check.

### 3. Fill the 12-section report

Open `references/report-template.md` and `references/data-sources.md`. For each section:

1. Read the **section spec** (what data points are mandatory)
2. Find the matching numbers in the extracted text
3. If a number is missing in the PDF, consult `data-sources.md` for the official source URL — but **do not fabricate**. Mark it as "数据待补充" (data TBD) if truly unavailable.
4. Write the prose in **Chinese**, with English/Latin terms (GDT, AMF, WMP, SMP, YTD, YoY, MoM) allowed.
5. End each data-heavy section with a 1–3 sentence **AI 解读 / 关键洞察** callout.

Special handling for **section 8 (GDT → 入仓成本)**:
- Identify the most recent GDT event from the PDF (event number, date, contract-2 results for AMF, WMP, SMP).
- Use current CNY/USD midpoint from the PDF (or `data-sources.md`). Mark the FX source.
- Call `scripts/gdt_calculator.py` with those three contract-2 prices + FX to produce the landed-cost table.
- Embed the resulting CNY/吨 numbers in the report, with the formula in a footnote.

Special handling for **section 11 (AI 深度解读 key takeaways)**:
- This section is purely synthesis. Read every other section first, then write 5–8 numbered insights that connect dots across sections (e.g. "国内生鲜乳价格 X 月连降 + GDT 拍卖连续 Y 次下跌 → 进口替代窗口期打开").
- Tie each insight to a number, not a vibe.

### 4. Build a data structure for the PDF

Assemble the filled content into a **single JSON object** matching the schema in `references/data-schema.md` (mirrored in the docstring of `scripts/render_pdf.py`). Top-level keys:

- `meta` — `{title, period, generated_at, sources}` (cover band + footer)
- `key_takeaways` — list of 3–6 short strings, bulleted on the cover card
- `sections` — ordered list of 12 entries, each with:
  - `title` (Chinese)
  - `kpis` — list of `{label, value, change}`; `change` is a free-form string like `+3.8%` or `-9.4% YoY`; the renderer auto-colors it (red for `+`/`↑`, green for `-`/`↓`, grey otherwise)
  - `tables` — list of `{header: [str, ...], rows: [[str, ...], ...]}`
  - `callout` — a single string, becomes the gold-bar 解读 box
  - `source` — a single string, becomes the grey footer line
  - (last section may also carry `events` — a list of `{date, title, body}` cards)

Rules:
- Currency: **CNY 元 / 吨** as the default unit; show USD alongside when quoting GDT.
- Color convention: 上涨 (price up YoY) → **red**; 下跌 → **green** — Chinese stock-market convention. Just set the sign in the `change` string and the renderer handles the rest.
- No external chart libraries — tables with directional pills are enough; if a section has a time series, you may add a list of `(date, value)` tuples under a `sparkline` key and the renderer will draw an inline SVG-like bar.
- **Do not** add `PageBreak` markers between sections. The renderer takes care of pagination.
- **Do not** wrap sections in `KeepInFrame` mode=`shrink` — that was an old attempt and produces cramped sections.

### 5. Render the PDF

```bash
python scripts/render_pdf.py --data work/report_data.json --out "乳制品市场行情报告_202310.pdf"
```

The renderer uses `reportlab` + the built-in `STSong-Light` CJK font, so **no Chromium / Playwright / wkhtmltopdf installation is required**. If `reportlab` is missing, install it with `pip install reportlab`.

Expected page count for a full 12-section report: **8–10 pages** (cover + body). If you see 13+ pages, you have added a per-section page break somewhere — remove it.

### 6. Present results

Use the `present_files` tool to show the PDF (it previews as an artifact card). In the chat reply, give a 3–4 line summary of which sections came from which input PDFs and one highlighted takeaway from section 11.

## Conventions & guardrails

- **Numbers over vibes.** Every claim in the report must be backed by a number from an input PDF, an official source in `data-sources.md`, or the GDT calculator. If a number is genuinely missing, write "数据待补充" — do not invent.
- **Cite inline.** Each section ends with a "数据来源" footer (e.g. "数据来源: 农业农村部; 艾格农业《中国乳业研究月报》202310").
- **No fabrication of future events.** Section 10 (走势预测) is forward-looking, but every prediction must be conditioned on a stated driver ("if GDT 投放量 continues to rise…"); do not give a single point estimate without a driver.
- **Honor user's formulas exactly.** GDT-to-warehouse formulas in section 8 are:
  - AMF: `(contract2_price + 165) * FX * 1.13 + 300`
  - WMP / SMP: `(contract2_price + 115) * FX * 1.13 + 300`
  - Contract-2 is the main contract, delivery 1–2 months out. If the PDF reports a different contract period, call it out.
- **Stay in Chinese** for prose. Allow English/Latin acronyms (GDT, AMF, WMP, SMP, USDA, NZX, AHDB, Fonterra).
- **One report per period.** If the user has multiple monthlies, generate one consolidated report for the latest month (with comparison vs. prior month) unless they ask for a multi-month roll-up.
- **Layout discipline.** No per-section `PageBreak`. No `KeepInFrame` shrink-mode per section. The renderer already produces a balanced 8–10 page magazine layout. If your output is 13+ pages, you have re-introduced one of those — fix the data builder, not the renderer.
- **Color discipline.** Use the bake-in tokens (`NAVY` / `ACCENT` / `SOFT_BG` / `RED` / `GREEN`) — do not invent new colors. Pill color is auto-driven by the `+/-` sign in the `change` string, so you do not pick the color manually.

## Quick-start (minimal example)

```text
User: "帮我跑一下 10 月的乳业月报"
→ Skill: detects 艾格农业-中国乳业研究月报202310.pdf
→ Extracts text → fills 12 sections → assembles data dict (per references/data-schema.md)
→ Calls scripts/render_pdf.py --data work/report_data.json --out 乳制品市场行情报告_202310.pdf
→ Presents: 乳制品市场行情报告_202310.pdf (8–10 pages, magazine style)
```

See `references/report-template.md` for the authoritative section spec, and `references/data-schema.md` for the data JSON schema the renderer expects.

