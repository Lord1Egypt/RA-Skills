# Quality Review Reference

Use this reference before calling a paper complete.

## Compile checks

- PDF exists.
- BibTeX bibliography appears.
- No fatal LaTeX errors remain.
- No undefined citations remain.
- No undefined references remain.
- Figures and tables render.
- Hyperlinks and cross-references work.

## Academic checks

- The paper has a clear scope and does not pretend to cover more than it covers.
- Contribution claims are explicit and defensible.
- Related work includes both foundational and recent papers.
- The structure has a coherent narrative, not just a list of summaries.
- Tables and figures add synthesis rather than decoration.
- Limitations and open problems are discussed explicitly.
- The abstract accurately summarizes the final paper and is written last.

## arXiv-style checks

- `\pdfoutput=1` is present.
- The paper can compile from source without hidden local dependencies.
- Figure paths are relative.
- Generated intermediate files are not required for compilation unless intentionally included.
- The bibliography file is included.

## Suggested final commands

Linux:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Windows fallback:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Log scan:

```bash
grep -E "Undefined|undefined|Fatal|Emergency|Error" main.log || true
```
