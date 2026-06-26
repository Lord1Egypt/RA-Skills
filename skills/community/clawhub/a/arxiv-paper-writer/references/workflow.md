# arXiv Paper Workflow

Use this reference when the user asks to create a new paper project or reproduce the full Claude Code paper-writing loop.

## Stage 1: Define the paper

Clarify:

- paper type: survey, benchmark, methods, position, tutorial, or report
- topic and scope
- intended reader
- target length
- expected contribution claims
- required output: `.tex`, `.bib`, `.pdf`, figures, tables, or documentation

Produce a short plan before writing files.

## Stage 2: Initialize the project

Create this structure unless the user gives a different layout:

```text
paper-project/
├── main.tex
├── references.bib
├── figures/
├── sections/
└── output/
```

Copy `templates/arxiv_survey_main.tex` to `main.tex` and replace placeholders. Copy `templates/references.bib` to `references.bib` as a smoke-test bibliography.

## Stage 3: Build the bibliography

Before writing long sections, build a reference set:

- 15-25 core references for a short paper
- 35-60 references for a survey paper
- stable BibTeX keys such as `vaswani2017attention`
- no invented metadata
- uncertain entries marked for verification

## Stage 4: Write the paper incrementally

Write in this order:

1. title and outline
2. Introduction
3. Background
4. main body sections
5. challenges/future work
6. conclusion
7. abstract last

After each major section, compile or perform static checks.

## Stage 5: Add figures and tables

Prefer reproducible LaTeX-native artifacts:

- TikZ architecture diagram
- TikZ timeline
- `booktabs` comparison table
- benchmark or taxonomy table

Every figure/table should support a claim in the text.

## Stage 6: Compile and repair

Linux preferred command:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Output directory variant:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=output main.tex
```

Windows MiKTeX fallback:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

If compilation fails, read the `.log` file and fix the source. Do not guess blindly.

## Stage 7: Review

Check:

- PDF exists
- bibliography appears
- no undefined citations
- no undefined references
- figures and tables render
- contribution claims are clear
- related work coverage is credible
- limitations are explicit
- arXiv compatibility is preserved through `\pdfoutput=1`
