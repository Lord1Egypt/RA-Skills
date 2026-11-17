# easy-html

> Turn any content into a polished single-page website — then publish it.

An [agent skill](https://github.com/Songhonglei/html-tool-suite) that takes Markdown,
plain text, Excel, Word, tables or images and produces a **self-contained, well-designed
HTML page**: semantic skeleton → data visualisation → one of 19 themes → title & favicon → publish.

Part of the [html-tool-suite](https://github.com/Songhonglei/html-tool-suite).

🌐 **[Live landing page →](https://songhonglei.github.io/html-tool-suite/easy-html/)** — browse all
19 themes and click any card to recolour the whole site (the page is its own demo).

---

## Why

Most "content → HTML" tools give you a wall of text with a stylesheet bolted on.
`easy-html` treats your content as **design material**:

- A mandatory **visualisation scan** turns key numbers, ratios, rankings, trends and
  timelines into KPI cards, progress bars, donuts and real charts — not another table.
- **Layout and colour are separated.** Themes carry colour only; layout, spacing and
  components ship with the skill. Swapping themes never breaks the page.
- When your input **already has a good layout** (an exported slide deck, a design-mockup
  HTML, a poster screenshot), it switches to *layout inheritance*: the original structure
  is kept 1:1 and only the palette is re-mapped. No more "the rebuild looks worse than the original".

---

## Install

```bash
pip install html-golive     # provides the 19-theme CSS engine (+ optional publishing)
pip install openpyxl        # optional, only needed to read .xlsx
```

Then drop the skill into your agent:

| Agent | Install |
|---|---|
| **OpenClaw** | `clawhub install easy-html` |
| **Claude Code** | `cp -r easy-html ~/.claude/skills/` |
| **Cursor** | `cp -r easy-html .cursor/skills/` |
| **Manual** | Copy this directory into your agent's skills folder |

---

## Quick start

```bash
# 1 · normalise the input
python3 scripts/ingest.py report.xlsx > blocks.json

# 2 · (the agent writes a semantic HTML skeleton from blocks.json)

# 3 · inject layout + visual components + chart helper
python3 scripts/apply_layout.py page.html

# 4 · pick one of 19 themes
python3 scripts/apply_style.py --list
python3 scripts/apply_style.py page.html --style bloomberg -o out.html

# 5 · title + favicon
FAV=$(python3 scripts/make_favicon.py --emoji 📊)
python3 scripts/set_meta.py out.html --title "Q3 Report" --favicon "$FAV"

# 6 · publish (optional)
golive publish out.html --name "Q3 Report"
```

**Layout inheritance** (input already looks good):

```bash
python3 scripts/inherit_layout.py deck.html --check              # verify the --eh-* contract
python3 scripts/inherit_layout.py deck.html --style palace -o out.html
```

---

## Features

| | |
|---|---|
| **Input formats** | Markdown · plain text · `.xlsx` · `.docx` · pasted/MD tables · stdin · images |
| **19 themes** | minimal · apple · cowork · morandi · fresh · earthy · glass · dreamy · macaron · carbon · vivid · newspaper · bloomberg · ink · steampunk · palace · cyberpunk · xhs · xhs-fun |
| **Visual components** | KPI cards · progress bars · rings · comparison bars · donuts · flow · timeline · tag cloud · VS blocks · info bars |
| **Real charts** | Chart.js line / bar / pie / radar with 4-source CDN fallback and graceful degradation |
| **Two paths** | Rebuild (loose content) · Layout inheritance (already-elegant input) |
| **Output** | Self-contained single-file HTML — host it anywhere |

---

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `EASY_HTML_OUT` | Output directory | `./output/easy-html` |
| `EASY_HTML_CSS_ENGINE` | Explicit path to `css_style_enhancer.py` | unset |
| `EASY_HTML_GOLIVE_HOME` | `html-golive` source tree (when not pip-installed) | unset |
| `window.EH_CHART_CDN` | In-page JS: custom Chart.js CDN list (offline/private networks) | 4 public CDNs |

The CSS engine is resolved in that order and **never downloaded silently** — if none is
found, the script exits with explicit install guidance.

---

## Scripts

| Script | Purpose |
|---|---|
| `scripts/ingest.py` | Input normalisation → structured JSON blocks |
| `scripts/apply_layout.py` | Inject layout base + component library + chart helper |
| `scripts/apply_style.py` | Apply one of 19 themes (rebuild path) |
| `scripts/inherit_layout.py` | Re-map colours onto an existing layout (inheritance path) |
| `scripts/set_meta.py` | Idempotent `<title>` / favicon |
| `scripts/make_favicon.py` | Emoji or glyph → SVG data-URI favicon |
| `scripts/_engine.py` | CSS theme engine resolution layer |

Deeper guidance for agents lives in `references/` (design tokens, visualisation
selection table, component snippets, chart recipes, `data-role` conventions).

---

## Not in scope

- Database / BI querying — bring your own data
- Full BI dashboards — use a dashboard tool
- Legacy binary `.xls` / `.doc` — convert to `.xlsx` / `.docx` first

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

## License

[MIT](./LICENSE) © 2026 Evan Song

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
