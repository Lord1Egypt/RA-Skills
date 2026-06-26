---
name: arxiv-paper-writer
description: Use this skill whenever the user wants Claude Code to write, scaffold, compile, debug, or review an arXiv-style academic paper, especially survey papers with LaTeX, BibTeX citations, TikZ figures, tables, and PDF output. This skill should trigger for requests like writing a full paper, creating an arXiv paper project, turning a research topic into a LaTeX manuscript, reproducing the Paper-Write-Skill-Test agent-survey workflow, or setting up a Windows/Linux Claude Code paper-writing loop.
---

# arxiv-paper-writer

This skill guides Claude Code through an end-to-end arXiv-style paper workflow: plan the paper, initialize a LaTeX project, build a BibTeX library, write sections incrementally, create figures/tables, compile, debug, and perform a final quality review.

## Core principle

Treat paper writing as an engineering loop, not a one-shot generation task. Work in small verifiable stages: plan, scaffold, cite, write, compile, inspect, repair, and review.

## When starting a paper project

1. Clarify topic, paper type, target length, audience, and whether the user wants a survey, methods paper, benchmark paper, position paper, or tutorial.
2. Create or reuse a paper directory with `main.tex`, `references.bib`, `figures/`, `sections/`, and `output/`.
3. Use `templates/arxiv_survey_main.tex` for a compact starter survey, or `templates/full_survey_main.tex` when the user wants the richer 9-section scaffold proven in the Agent Survey experiment.
4. Read `references/workflow.md` for the full staged process.
5. Read only the reference files needed for the current phase.
6. When the user asks to reproduce the Paper-Write-Skill-Test workflow, use `references/agent_survey_practice.md`, `templates/agent_survey_references.bib`, and `templates/agent_survey_figures_tables.tex` as concrete examples.

## Workflow phases

### Phase 1: Plan

Create a concrete paper plan before writing prose. Include title candidates, scope, contribution claims, section outline, target references, expected figures/tables, and verification commands.

### Phase 2: Scaffold

Create a compilable LaTeX skeleton first. The first milestone is a PDF that compiles even before the paper is complete.

### Phase 3: Build bibliography

Construct `references.bib` before heavy writing. Prefer real, verifiable papers. Use stable BibTeX keys. Avoid invented citations. If uncertain about a reference, mark it for verification rather than fabricating metadata.

### Phase 4: Write sections incrementally

Write one or two sections at a time. After each substantial section, compile or at least check citations and LaTeX syntax. Write Abstract last.

### Phase 5: Create figures and tables

Prefer TikZ and LaTeX tables for reproducible academic artifacts. Keep figures information-dense and directly connected to claims in the text.

### Phase 6: Compile and debug

Use `latexmk` on Linux when available. On Windows MiKTeX, use `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`. Read `.log` files before guessing fixes.

### Phase 7: Final review

Check PDF generation, citation completeness, undefined references, figure/table placement, academic tone, contribution clarity, and arXiv compatibility.

## Environment guidance

- For Windows MiKTeX and Linux TeX Live basics, read `references/latex_environment.md`.
- For fuller Linux cloud setup and verification, read `references/linux_texlive_full.md`.
- For BibTeX construction, read `references/bibliography.md`.
- For figure and table design, read `references/figures_and_tables.md` and optionally reuse `templates/agent_survey_figures_tables.tex`.
- For final review, read `references/quality_review.md`.
- For reusable task prompts, read `references/prompt_templates.md`.

## Output style

When writing project files, edit the actual `.tex`, `.bib`, and documentation files. Do not merely describe what should be written. When explaining progress to the user, summarize briefly in Chinese and reference exact file paths.
