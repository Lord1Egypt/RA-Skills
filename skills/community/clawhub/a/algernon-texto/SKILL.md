---
name: algernon-texto
version: "1.0.0"
description: >
  Block-by-block reading mode for OpenAlgernon materials. Use when the user
  runs `/algernon texto SLUG`, `/algernon paper SLUG`, says "quero ler [material]",
  "vamos ler [topic] bloco a bloco", "modo texto", or "leitura guiada". Also
  activates when the user is mid-session and selects /continue between blocks.
  Paper mode adds structured reflection between major sections.
---

# algernon-texto

You deliver material content block by block with an interactive tool menu after
each block. The goal is active reading — the user engages with each block before
moving on.

## Constants

```bash
ALGERNON_HOME="${ALGERNON_HOME:-$HOME/.openalgernon}"
DB="${ALGERNON_HOME}/data/study.db"
MATERIALS="${ALGERNON_HOME}/materials"
NOTION_CLI="${NOTION_CLI:-notion-cli}"
```

## Step 1 — Load Material

```bash
sqlite3 "$DB" "SELECT id, name, local_path FROM materials WHERE slug = 'SLUG';"
```

If no result, stop: "Material 'SLUG' not found. Run `list` to see installed materials."

Read `LOCAL_PATH/algernon.yaml` to get:
- `content`: list of content files
- `sections`: section titles mapped to file names

Read all content files and split into blocks of approximately 300 words each.
Preserve section boundaries — never split mid-sentence at a section change.

## Step 2 — Display Session Header

```
================================================
 SLUG — mode: texto (or: paper)
 N blocks total
================================================
```

## Step 3 — Block Delivery Loop

For each block, display:

```
────────────────────────────────────────────────
 Block N/TOTAL · SECTION_TITLE
────────────────────────────────────────────────

[Block content]

────────────────────────────────────────────────
 /continue    /explain [term]    /example
 /analogy     /summarize         /test
 /map         /deep-dive
────────────────────────────────────────────────
```

Present as an AskUserQuestion with the tool options above.

### Tool Behaviors

| Tool          | What to do                                                                 |
|---------------|----------------------------------------------------------------------------|
| `/continue`   | Advance to the next block                                                  |
| `/explain X`  | Define X at N1 level first. Ask if user wants N2 before going deeper.     |
| `/example`    | Give a concrete real-world example of the main concept in this block       |
| `/analogy`    | Create an original analogy that maps the concept to something familiar     |
| `/summarize`  | Summarize the block in 2-3 sentences; ask user to add anything missed      |
| `/test`       | Ask 1 quick comprehension question about this block; give feedback         |
| `/map`        | Show how this concept connects to others already covered in this material  |
| `/deep-dive`  | Expand the block's core concept to N2/N3 depth; note as focus for cards   |

After any tool response, re-display the current block menu so the user can
continue or use another tool.

### Paper Mode Additions

In paper mode, content is structured as:
Abstract → Methodology → Results → Implications

Between sections, before showing the first block of the new section:
> "Summarize what you understood from [previous section] before we continue."
(Free text — acknowledge and move on without grading.)

Track which terms the user used `/explain` or `/deep-dive` on. Pass this list
to card generation at the end as additional focus concepts.

## Step 4 — Session End

When the last block is delivered and the user selects /continue:

```
Material complete: MATERIAL_NAME
Sections covered: N
Key concepts explored: [list of terms where user used /explain or /deep-dive]
```

### Generate Cards

Generate cards for this material. Follow the card generation rules in
`algernon-content`:
- Distribution: 50% flashcard, 30% dissertative, 20% argumentative
- All cards start at N1
- Prioritize concepts from the `/explain` and `/deep-dive` list

### Save to Notion (optional)

If `$NOTION_CLI` is available and `$NOTION_PAGE_ID` is set:

```bash
"$NOTION_CLI" append --page-id "$NOTION_PAGE_ID" --content "MARKDOWN"
```

Content to include: key concepts (N1/N2/N3), concepts the user explored deeply,
flashcards generated. This step is skipped silently if Notion is not configured.

### Save Memory

Append a summary to today's conversation log:

```bash
echo "[HH:MM] texto session -- MATERIAL_NAME | Blocks: N/TOTAL | Cards: N" \
  >> "${ALGERNON_HOME}/memory/conversations/YYYY-MM-DD.md"
```
