---
name: pdf-document
version: 1.0.0
description: Create multi-page PDF documents with Canvora — brochures, reports, one-pagers, company profiles, proposals, menus, catalogs, ebooks, worksheets and cheat sheets. Use when the user wants a PDF, a printable document, a brochure, a lead magnet, or anything paginated rather than a social post.
homepage: https://canvora.ai/for-agents
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":["canvora"],"env":["CANVORA_API_KEY"]}}}
---

# Multi-page documents and PDFs

Canvora has a dedicated **document mode**: `document_page` runs through the
structured pipeline with print layout rather than slide layout — margins,
reading order, and typography built for a page, not a screen. This is the
format behind "make me a brochure / report / company profile / proposal /
menu / catalog / lead magnet". Nobody guesses the ID, so you have to know it.

Setup and credits: see the `canvora` skill.

## Format map

| Want | Format | Notes |
|---|---|---|
| A multi-page document of any kind | `document_page` | 3:4, 816×1056 (US Letter portrait). **Carousel format — `--slides` = number of pages.** 15 credits per page. |
| A single-page one-pager | `one_pager` | 816×1056, single image, 10 credits |
| An exec summary page | `executive_summary` | 816×1056 |
| A cheat sheet / reference card | `cheat_sheet` | 816×1056 |
| A worksheet / workbook page | `worksheet` | 3:4 1200×1600 |
| An ebook / report cover | `ebook_cover` | 3:4 1600×2133 |
| A visual mind map | `mind_map` | 4:3 1600×1200 |

Rule: **more than one page → `document_page` with `--slides`.** Exactly one
page → the specific single-page format. Cover + pages → `ebook_cover` in the
same call as `document_page`.

## Intake

1. **What is the document?** (brochure, report, proposal, menu, profile…) —
   this goes into the brief verbatim; the pipeline uses it to pick the layout
   language.
2. **How many pages?** If unknown: brochure 4, company profile 6, report 8,
   menu 2. Max 10 per call — for longer, run consecutive calls and merge at
   export.
3. **Source?** A written doc or PDF is ideal (`--file-url`), otherwise
   `--input` for their copy or `--idea` for a topic.
4. **Brand kit?** Documents are the format where an off-brand result is most
   obvious. `--brand` + `--logo`.

## The canonical runs

```bash
# Company brochure from existing copy
ID=$(canvora generate --input "$COMPANY_COPY" \
  --format document_page --slides document_page=6 \
  --brand $BRAND --logo --style corporate | head -1)
canvora status "$ID" --json    # repeat every ~30s until completed

# Report PDF from a source document
ID=$(canvora generate --file-url https://example.com/annual-review.pdf \
  --format document_page --slides document_page=8 \
  --brand $BRAND --logo | head -1)
canvora status "$ID" --json

# Lead magnet: cover + 4 pages in one generation
ID=$(canvora generate --idea "The 2026 SEO audit checklist for small e-commerce stores" \
  --format ebook_cover,document_page --slides document_page=4 \
  --brand $BRAND --logo --cta | head -1)
canvora status "$ID" --json

# Restaurant menu, exact prices preserved (2 pages — short enough for --wait)
canvora generate --input "$MENU_TEXT" --exact \
  --format document_page --slides document_page=2 --wait --json
```

Documents are 15 credits per page — say the total in the same message as the
run (a 6-page brochure = 90), announcing it rather than asking permission. When
the page count came from the defaults above rather than from the user, confirm
that number with them first. Anything over 2 pages is 3+ outputs, so fire and
poll `status` instead of `--wait`: your harness likely kills a shell command at
120s while the pages carry on rendering server-side. Never re-run `generate`
after a timeout; that starts a second, separate job. See the `canvora` skill's
"Long runs" section.

## Things that ruin documents (avoid)

- **Paraphrasing the source.** Documents carry facts: prices, names, figures,
  legal lines. Pass the file or use `--input`, and add `--exact` whenever the
  wording is not yours to change.
- **Treating pages like slides.** Don't ask for a "hook" page. Documents open
  with a title/cover and proceed in reading order.
- **Forgetting the CTA page.** Brochures, proposals and lead magnets should end
  on one → `--cta`.
- **Landscape.** `document_page` is portrait by design. If they want landscape,
  they want a deck — use the `pitch-deck` skill.

## Delivering the PDF

The user asked for a *PDF*, not for images. Finish the job:

- **MCP clients:** `export_visuals(generation_id, format: "pdf")` returns the
  assembled multi-page PDF. This is the correct final step.
- **CLI-only:** `canvora download <id> --dir ./doc` saves the pages in order —
  then tell the user to export the PDF from their Canvora dashboard, because
  the CLI has no export command.

Either way, sort by `sortOrder` first — page order is the whole point.

## Quality checklist

- [ ] `document_page` with `--slides` = page count (not separate calls)
- [ ] Source passed directly; `--exact` when facts/prices/legal text must survive
- [ ] Brand kit + logo applied
- [ ] `--cta` on anything persuasive
- [ ] Delivered as an actual PDF (MCP export) or the export route explained
