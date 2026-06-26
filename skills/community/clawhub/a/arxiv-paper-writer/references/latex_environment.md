# LaTeX Environment Reference

Use this reference when setting up or debugging local/cloud LaTeX compilation.

## Windows: MiKTeX

Recommended commands:

```bash
pdflatex --version
bibtex --version
```

Enable automatic package installation to avoid GUI prompts during Claude Code compile loops:

```bash
initexmf --set-config-value="[MPM]AutoInstall=yes"
initexmf --admin --set-config-value="[MPM]AutoInstall=yes"
```

Compile sequence:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Linux: TeX Live

Recommended Ubuntu/Debian minimal install:

```bash
sudo apt update
sudo apt install -y \
  texlive-latex-base \
  texlive-latex-recommended \
  texlive-latex-extra \
  texlive-fonts-recommended \
  texlive-fonts-extra \
  texlive-pictures \
  texlive-bibtex-extra \
  latexmk \
  biber
```

Verify packages:

```bash
pdflatex --version
bibtex --version
latexmk --version
kpsewhich tikz.sty
kpsewhich newtxtext.sty
kpsewhich cleveref.sty
```

Preferred compile command:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

## Common issues

### Missing `.sty`

If LaTeX reports `File 'xxx.sty' not found`, run:

```bash
kpsewhich xxx.sty
```

Install the package group that contains it, or use full TeX Live if disk space is not constrained.

### `\Bbbk` conflict

If `newtxmath` and `amssymb` conflict, include this after loading `amssymb`:

```latex
\let\Bbbk\relax
```

### Undefined citations

Run BibTeX or use `latexmk`. Check that every `\citep{key}` or `\citet{key}` has a matching BibTeX key.
