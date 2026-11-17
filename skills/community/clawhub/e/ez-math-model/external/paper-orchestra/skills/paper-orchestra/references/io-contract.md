# I/O Contract

Reference for the orchestrator. Defines the workspace layout and the schema of
every input and intermediate artifact.

## Workspace layout

```
workspace/
├── inputs/                              # User-provided
│   ├── idea.md                          # I — Sparse or Dense idea (markdown)
│   ├── experimental_log.md              # E — setup, raw numeric data, observations
│   ├── template.tex                     # T — conference LaTeX template
│   ├── conference_guidelines.md         # G — formatting rules, page limit, sections
│   └── figures/                         # F — optional pre-existing figures (PNG/PDF)
├── outline.json                         # Step 1 output
├── figures/                             # Step 2 output (generated)
│   ├── <figure_id>.png
│   ├── ...
│   └── captions.json                    # {figure_id: caption_text, ...}
├── refs.bib                             # Step 3 output
├── citation_pool.json                   # Step 3 output (verified S2 metadata)
├── drafts/
│   ├── intro_relwork.tex                # Step 3 output
│   └── paper.tex                        # Step 4 output (then mutated by Step 5)
├── refinement/                          # Step 5 working dir
│   ├── worklog.json
│   ├── iter1/{paper.tex,paper.pdf,review.json,score.json}
│   ├── iter2/...
│   └── iter3/...
├── final/                               # Accepted snapshot + compiled PDF
│   ├── paper.tex
│   └── paper.pdf
└── provenance.json                      # Input/output hashes for reproducibility
```

## Input file schemas

### `idea.md` — Idea Summary (I)

Markdown. Two valid variants (the paper distinguishes them in App. C.3).

**Sparse variant** (high-level concept note, no math):

```markdown
## Problem Statement
(Precise definition of the technical problem.)

## Core Hypothesis
(The proposed solution / intuition.)

## Proposed Methodology (High-Level Technical Approach)
(Conceptual description; describe modules by function, not their math.)

## Expected Contribution
(Intended theoretical or practical value.)
```

**Dense variant** (preserves math, equations, variable definitions):

```markdown
## Problem Statement
## Core Hypothesis
## Proposed Methodology (Detailed Technical Approach)
   - includes LaTeX equations, variable definitions, architectural choices
## Expected Contribution
```

The Outline Agent automatically handles both. Dense produces more rigorous
methodology sections; Sparse exercises the system's robustness (per the
paper's ablation, App. E).

### `experimental_log.md` — Experimental Log (E)

Markdown. Strict structure required:

```markdown
# Experimental Log

## 1. Experimental Setup
* **Datasets:** ...
* **Evaluation Metrics:** ...
* **Baselines Compared:** ...
* **Implementation Details:** ...

## 2. Raw Numeric Data
(Tables in markdown format. Section-Writing Agent extracts these into LaTeX
booktabs tables. Use plain markdown table syntax — | col | col | — with no
references to "Table N" or "Figure N".)

## 3. Qualitative Observations
* (factual statements like "training loss converged after 200 epochs",
  "method X failed on test case Y", etc.)
```

**Critical rules** (from App. F.2 Experimental Log Generation prompt):

- No references to figure or table numbers ("See Table 1", "as shown in Fig. 5")
- Past-tense persona ("We ran...", "The results were...")
- Self-contained: no citations, no URLs, no author names
- Numeric values must be 100% accurate — they become the ground truth for
  the Refinement Agent's hallucination check

### `template.tex` — LaTeX Template (T)

A conference LaTeX template (CVPR, ICLR, NeurIPS, ICML, etc.) with empty
`\section{...}` placeholders. The Section Writing Agent fills the empty
sections in-place; the preamble (`\documentclass`, `\usepackage`, etc.) is
preserved verbatim.

### `conference_guidelines.md` — Conference Guidelines (G)

Markdown describing:

- Page limit (in pages, integer)
- Mandatory sections (e.g., "must have an Abstract, Introduction, Methods,
  Experiments, Conclusion")
- Formatting requirements (single-column vs two-column, font, margins)
- Submission deadline date (used to derive `cutoff_date` for the literature
  review and section writing agents)

### `inputs/figures/` — Pre-existing Figures (F)

Optional. PNG or PDF files. If present, the Plotting Agent will reuse them
where the outline plan permits and only generate the missing ones. If empty,
the Plotting Agent generates everything from scratch (the paper calls this
mode `PlotOff`; the GT-figure mode is `PlotOn`).

## Intermediate artifact schemas

### `outline.json`

See `skills/outline-agent/references/outline-schema.md` and the JSON Schema at
`skills/outline-agent/references/outline_schema.json`.

### `figures/captions.json`

```json
{
  "fig_framework_overview": "Plain-text caption here, no markdown, no 'Figure N:' prefix.",
  "fig_main_results": "..."
}
```

The Section Writing Agent splices these into `\caption{...}` commands.

### `citation_pool.json`

Internal record produced by the Literature Review Agent of every verified
citation, with full Semantic Scholar metadata. Schema:

```json
{
  "papers": [
    {
      "paperId": "abc123...",                  // S2 unique ID
      "bibtex_key": "vaswani2017attention",
      "title": "Attention Is All You Need",
      "authors": [{"name": "A. Vaswani"}, ...],
      "year": 2017,
      "venue": "NeurIPS",
      "abstract": "...",
      "externalIds": {"DOI": "...", "ArXiv": "1706.03762"},
      "verified_via": "semantic_scholar",
      "match_score": 100,                       // Levenshtein ratio
      "discovered_for": ["intro", "related_work"]
    }
  ],
  "cutoff_date": "2024-11-01",
  "min_cite_paper_count": 27                    // 90% of len(papers), rounded down
}
```

### `refinement/worklog.json`

```json
{
  "iterations": [
    {
      "iter": 1,
      "timestamp": "2026-04-09T12:34:56Z",
      "review": { "strengths": [...], "weaknesses": [...], "questions": [...] },
      "score": { "overall": 67, "axes": {...} },
      "actions_taken": ["Rewrote Section 3.2 for clarity", ...],
      "decision": "accept"
    },
    ...
  ],
  "halted_because": "iteration_cap_reached" | "overall_decreased" | "tie_with_negative_subaxis_delta" | "no_new_weaknesses",
  "best_iter": 2
}
```

### `provenance.json`

```json
{
  "created_at": "2026-04-09T12:34:56Z",
  "inputs": {
    "idea.md":               {"sha256": "...", "bytes": 1234},
    "experimental_log.md":   {"sha256": "...", "bytes": 5678},
    "template.tex":          {"sha256": "...", "bytes": 9012},
    "conference_guidelines.md": {"sha256": "...", "bytes": 345}
  },
  "outline.json": {"sha256": "..."},
  "refs.bib":     {"sha256": "...", "n_entries": 59},
  "figures": {
    "fig_framework_overview.png": {"sha256": "..."},
    ...
  },
  "final": {
    "paper.tex": {"sha256": "..."},
    "paper.pdf": {"sha256": "..."}
  },
  "skill_versions": {
    "paper-orchestra": "0.1.0"
  }
}
```

This is an out-of-paper improvement for reproducibility. Optional but
recommended.
