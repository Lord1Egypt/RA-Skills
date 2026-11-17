# 桌游规则书汉化 · Board Game Rulebook ZH

Turns English board-game PDF rulebooks into Chinese, while **illustrations, boards, card art, icons, table rules and the original layout stay exactly in place**.

This is an Agent Skill (`SKILL.md`) that can also be used directly as a command-line tool:

- Built-in board-game glossary (worker placement / deck-building / meeple / token / exhaust …);
- Erases only the text layer, never bitmaps/vector graphics;
- Table cells, two-column layouts, headers/footers and inline icons are handled separately;
- After rendering it automatically compares bitmap/vector digests, and reports an error outright if any text drifts onto art;
- Outputs a QA report + side-by-side preview for page-by-page visual checking.

![Example: original on the left, translation on the right](examples/demo_page1.png)

> The demo is a synthetic sample shipped with this repo (`examples/make_sample.py`); it contains no copyrighted rulebook.

[简体中文 README](README.zh-CN.md)

## Links

- GitHub: https://github.com/C0S1N3/boardgame-rulebook-zh
- ClawHub: `boardgame-rulebook-zh` (page: https://clawhub.ai/C0S1N3/skills/boardgame-rulebook-zh ; the first release needs a security scan, so if it 404s for now, please try again later)

## Why it never scrambles the art

1. Every text line is redacted with `fill=False`, `images=NONE`, `graphics=NONE`: only the glyphs are erased, all images and lines preserved.
2. The translation is written back into the original paragraph bbox; when space runs short it only borrows whitespace downwards, never entering other text, images or table cells.
3. Translations for table cells are kept inside the cell; inline icons get text wrapped around them.
4. After rendering, the output PDF is reopened and compared:
   - bitmap count, content digests, positions;
   - vector graphic count/digests;
   - page size, rotation, page count;
   - whether the translation is complete, and whether it has overlapped any art/text/table rules.

If any item fails, `report.md` reports an error, and the job must not be delivered.

## Installation

```bash
python -m pip install -r requirements.txt
```

- Python 3.9+
- PyMuPDF (tested with 1.26.5)
- Pillow

The Chinese font is chosen automatically: Microsoft YaHei / SimHei / SimSun (Windows), PingFang / STHeiti (macOS), Noto Sans CJK / WQY (Linux); if none of these exists, PyMuPDF's built-in CJK font is used.

## Quick start

```bash
python scripts/extract.py rulebook.pdf -o work
# read work/source.md and fill in work/translations.tsv
# check/complete work/termbase.tsv
python scripts/render.py rulebook.pdf -w work -o out
# look at out/qa/report.md and out/qa/pages/page_*.png
```

Final files:

- `out/rulebook_zh.pdf` — the in-place localized PDF
- `out/qa/report.md` — the QA report (Chinese)
- `work/termbase.tsv` — the project termbase
- `out/qa/pages/*.png` — side-by-side previews

Deliver only when QA reports **error = 0**; every warning must be reviewed one by one.

## Using it as a Skill

Drop the whole directory into the agent's skills directory, e.g. for Qoder:

```text
~/.qoder-cn/skills/boardgame-rulebook-zh/SKILL.md
```

Or install it following the ClawHub/OpenClaw skill directory convention.  
When an agent gets a request like "localize a board-game rulebook / translate board game rulebook PDF / terminology must be accurate / images must not shift", it should use this skill.

## Terminology

- `references/glossary.csv`: recommended renderings + avoid + wrong, for script lookups and QA.
- `references/glossary-notes.md`: explanations of easily confused terms (deck/deck-building, token/marker/counter, meeple/pawn, exhaust/tap, reveal/flip…).
- `references/style.md`: Chinese style, sentence patterns, measure words, punctuation, card-name rules.
- `references/official-titles.md`: official/common Chinese titles of well-known games; not used for automatic replacement.

Projects pin down their renderings in `work/termbase.tsv`; official Chinese editions take priority. QA reports an error for clear mistranslations named in the glossary (e.g. rendering *meeple* as *mipu*), and info for merely suggested renderings.

## Layout fixes

When it doesn't fit automatically:

1. Tighten the translation first;
2. then adjust the safe layout box via `work/layout_overrides.json`;
3. only then accept a smaller font size.

```json
{
  "p003_s008": {
    "box": [28, 423, 292, 540],
    "font_size": 10.0,
    "align": "left",
    "note": "widen by 10pt so the comma doesn't land at line start"
  }
}
```

Overrides for table cells are clamped back into the cell; they never cross the border.

## Self-test

```bash
python examples/selftest.py --negative
```

- Positive: a synthetic two-column rulebook (tables, bitmaps, vector icons, inline icons) → 34 paragraphs, 9 table cells, 2 inline icons, 0 error / 0 warning; bitmaps, vector graphics and page geometry all unchanged.
- Negative: deliberately wrong terminology (*mipu* for *meeple*), missing translations, table overflow, missing emoji glyphs; QA blocks it with exit code 1.

One page of a real publisher rulebook (*Age of Conan*, FFG, 42 paragraphs, two columns, full-page parchment background, large character illustrations, bulleted lists) has been verified locally: 0 error / 0 warning (with one layout override to fix line-leading punctuation), bitmap/vector digests unchanged. The original PDF is copyrighted and is not distributed with the repo.

## Not supported

- Scanned / image-only PDFs and vector-outlined text: no overlay-style localization is done, see `references/scanned-pdfs.md`.
- Line-by-line vertical text: the original is kept and a warning is raised.
- Complex forms, annotations, nested tables: these need manual review.
- Re-flowing pages / changing paper size: this tool only does in-place localization, it does not redesign the layout.

## Directory

```text
SKILL.md
scripts/
  extract.py
  render.py
  pdf_common.py
references/
  glossary.csv
  glossary-notes.md
  style.md
  layout-and-qa.md
  qa-checklist.md
  scanned-pdfs.md
  official-titles.md
examples/
  make_sample.py
  selftest.py
  demo_page1.png
```

## License

MIT. Only for documents you have the right to translate; do not commit copyrighted original rulebooks or full-page translations to public repositories.
