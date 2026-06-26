# Agent Survey Practice Guide

This reference condenses the successful `papers/agent-survey` run into reusable steps for future arXiv-style survey papers.

## Proven outcome

The source experiment produced:

| Item | Result |
|------|--------|
| Topic | Evolution of AI Agents |
| Output | 15-page English PDF |
| References | 39 real BibTeX entries |
| Visuals | 2 TikZ figures + 2 LaTeX tables |
| Structure | Abstract, Keywords, 9 main sections, References |
| Toolchain | Claude Code + LaTeX + BibTeX + TikZ |

## Core workflow

```text
Plan topic and scope
  -> initialize LaTeX project
  -> build real BibTeX library
  -> write section skeleton
  -> draft one or two sections at a time
  -> add TikZ figures and LaTeX tables
  -> compile with pdflatex/bibtex or latexmk
  -> read logs and repair errors
  -> perform final academic and arXiv checks
```

## Recommended project layout

```text
paper-project/
├── main.tex
├── references.bib
├── sections/          # optional; useful for long papers
├── figures/           # external figures only if needed
└── output/            # generated PDF and build outputs
```

For conceptual survey papers, prefer TikZ figures embedded in `main.tex` and LaTeX tables over external images. This keeps the source self-contained and easier to submit to arXiv.

## Windows MiKTeX loop

Enable automatic package installation before long compile loops:

```bash
initexmf --set-config-value="[MPM]AutoInstall=yes"
initexmf --admin --set-config-value="[MPM]AutoInstall=yes"
```

Compile manually when `latexmk` is unavailable:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Read `main.log` after failures. Do not guess LaTeX fixes without checking the exact error.

## Optional Python / uv setup

Python is not required for the basic paper loop when using TikZ and BibTeX directly. Use it only for helper scripts, data plots, or batch metadata processing.

```bash
uv python install 3.11
uv venv .venv
uv pip install requests matplotlib
```

## Literature strategy

For a standard survey, target 35-60 references. Cover:

1. foundational work;
2. representative systems/frameworks;
3. recent surveys;
4. benchmarks and evaluation papers;
5. challenge, safety, and future-direction papers.

Build `references.bib` before heavy prose writing. Use stable keys such as `authorYYYYshorttitle`. Do not invent metadata. If a DOI, venue, or page range is uncertain, mark it outside the BibTeX entry for later verification.

## Proven 9-section survey structure

The agent-survey paper used this reusable structure:

1. Introduction
2. Background and Definitions
3. Early Foundations
4. LLM-Based Agents
5. Agent Frameworks and Toolkits
6. Multi-Agent Systems
7. Applications and Case Studies
8. Challenges and Future Directions
9. Conclusion

Use `templates/full_survey_main.tex` when a user wants a richer survey scaffold instead of the smaller `templates/arxiv_survey_main.tex` starter.

## Visual artifact pattern

The successful paper used four high-value artifacts:

1. an architecture diagram showing core components;
2. a historical timeline;
3. a framework comparison table;
4. a benchmark comparison table.

Reusable snippets are in `templates/agent_survey_figures_tables.tex`.

## Final checks

Before calling the paper complete:

- PDF exists.
- Bibliography appears.
- No fatal LaTeX errors remain.
- No undefined citations remain.
- No undefined references remain.
- Figures and tables render.
- Abstract matches the final paper and is written last.
- Contribution claims are explicit and defensible.
