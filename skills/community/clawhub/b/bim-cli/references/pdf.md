# bim pdf: drawing sets, Revit PDFs, PDF-BIM packages

Full verb list: `bim describe --driver pdf --json`. Domain notes: `https://bimcli.com/pdf/llms.txt` (where it disagrees with `describe`, trust `describe`). No extra software is needed; `render` uses a bundled pdfium.

## First look at any PDF

```bash
bim pdf info  <file>     # pages, version, scanned vs text, textCoverage, embedded attachments
bim pdf pages <file>     # per-page mediaBox/cropBox, rotation, OCG layers
```

- `scanned: true` / `textCoverage: 0` means image-only pages. Text verbs will return nothing; render the page and read it visually instead.
- A non-empty `attachments` list containing `elements.json`, `marks.json`, `titleblock.json` etc. means it is a **PDF-BIM package** (see below).

## Which verb for which question

| Question | Verb |
|---|---|
| What sheets are in this set? (plain issued set) | `set.extract <file>`: sheets, sheet index, callouts, detail targets |
| Does the set hang together? | `set.check <file>`: index completeness, callout resolution, titleblock consistency |
| Sheet numbers/names from a PDF-BIM package | `bim.extract-titleblock <file>` |
| Find a word or tag and where it is | `search <file> --pattern <regex>` (also `--dir` / `--files` for many PDFs) |
| Pull named values (permit no., dates) | `extract <file> --field NAME=REGEX ...` |
| A schedule or table as rows | `table <file> --page N` |
| Raw text with coordinates | `text <file> --page N` |
| Revit element IDs on a sheet | `marked <file> --page N` |
| How many doors/rooms/walls in a package | `bim.extract <file> --name elements.json --out e.json`, then count `class` with code (no counting verb) |
| A picture of a page or region | `render <file> --page N [--dpi 150] [--bbox x0,y0,x1,y1 --out img.png]` |

## Page operations

- **One or some sheets into one new PDF:** `page.collect <file> --pages 1,3,5-8 --out out.pdf`.
- **Every page (or every N pages) into separate files:** `page.split <file> --out-dir DIR [--span N | --by-bookmark]`. It has no `--pages`/`--out`.
- Also: `page.merge`, `page.rotate`, `page.crop`, `stamp.add` / `stamp.remove`, `optimize`, `form.fields` / `form.fill` / `form.flatten`, `bookmark.*`, `attach.*`, `security.*`.

Single-file results go to `--out`, multi-file results to `--out-dir`; both default to a new file or a temp dir, never the input.

**Page operations drop PDF-BIM sidecars.** Collecting, splitting or merging pages of a package produces a plain PDF with no attachments. Say so when you hand the file over. If the user needs the result to stay a package, re-embed sidecars with `bim.pack` (check `bim describe --driver pdf --verb bim.pack --json`).

## PDF-BIM packages

A PDF-BIM package is the printed drawing set plus JSON sidecars exported from the model, embedded as PDF/A-3 attachments.

```bash
bim pdf bim.list <file>                                   # which sidecars are inside
bim pdf bim.extract <file> --name README-agent.md         # read this first
bim pdf bim.extract <file> --name elements.json --out elements.json
bim pdf bim.extract-room-schedule <file>
bim pdf bim.validate <file>
```

**Authority rule (from the packages' own README-agent.md):** the printed sheets are the contractual document. Sidecar counts, names and type taxonomies come from the model database and routinely differ from what schedules and legends print. When they differ, report both figures and say which source each came from. When the set prints nothing to check against (no matching schedule, `search` finds no hits), report the figure as model-derived and unconfirmed by the drawings.

## Pitfalls

- **Revit PDFs use a centered origin**, so coordinates are often negative (`mediaBox: [-1512,-1080,1512,1080]`). When a negative number is a flag value, separate it with `--` or `=` as the verb's help says.
- **`text` returns fragments, not lines.** Revit glyph runs come back as many small `{text,x,y}` pieces. For "what does the sheet say", prefer `search`, `extract`, `table`, or `set.extract`; use `text` when you need positions.
- **`set.extract` on a PDF-BIM package** has been seen returning empty sheet numbers for Revit exports. Use `bim.extract-titleblock` for packages.
- **`marked`** returns `null` element_id for elements from linked models.
- **Big sets:** write output to a file (`> out.json`) and summarise it with code; a 100-sheet `text` dump will flood your context.
