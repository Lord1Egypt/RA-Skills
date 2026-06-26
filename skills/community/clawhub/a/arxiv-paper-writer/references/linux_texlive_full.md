# Linux TeX Live Full Reference

Use this reference when running Claude Code paper writing on Ubuntu, Debian, or a Linux cloud server.

## Goal

Build a minimum viable LaTeX environment that can:

| Capability | Verification |
|------------|--------------|
| Basic LaTeX compile | `pdflatex main.tex` creates a PDF |
| BibTeX citations | `bibtex main` processes `references.bib` |
| TikZ figures | PDF renders TikZ diagrams |
| Automatic multi-pass compile | `latexmk -pdf main.tex` completes |
| Common paper packages | `natbib`, `booktabs`, `hyperref`, `cleveref`, `newtxtext`, `newtxmath` are available |

## Recommended stack

```text
TeX Live
latexmk
BibTeX
TikZ / PGF
Claude Code
```

TeX Live is preferred on Linux because it is command-line friendly, reliable for unattended builds, and avoids GUI package-install prompts.

## System preflight

```bash
uname -a
cat /etc/os-release
which bash
which curl
which git
which make
```

Install base tools if needed:

```bash
sudo apt update
sudo apt install -y curl git make ca-certificates
```

## Minimal Ubuntu / Debian install

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

If disk space is not constrained, this is the simplest low-friction option:

```bash
sudo apt install -y texlive-full latexmk biber
```

## Verify installed commands and packages

```bash
pdflatex --version
bibtex --version
latexmk --version
kpsewhich article.cls
kpsewhich tikz.sty
kpsewhich newtxtext.sty
kpsewhich newtxmath.sty
kpsewhich cleveref.sty
kpsewhich natbib.sty
kpsewhich booktabs.sty
```

Expected result: command version output and `.cls` / `.sty` paths. Missing output from `kpsewhich` means the package is unavailable.

## Minimal compile test

Create this structure:

```text
latex-cloud-test/
├── main.tex
├── references.bib
└── output/
```

Compile with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Or keep generated files in `output/`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=output main.tex
```

Clean generated files:

```bash
latexmk -c
```

## Common Linux failures

### Missing `.sty`

Check the package first:

```bash
kpsewhich missing-package.sty
```

Then install the relevant TeX Live package group or switch to `texlive-full` if this keeps recurring.

### Undefined citations

Use a full multi-pass build:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

If building manually:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### `newtxmath` / `amssymb` `\Bbbk` conflict

Place this after loading `amssymb`:

```latex
\let\Bbbk\relax
```

### Server has no sudo

Ask the administrator to preinstall TeX Live, or use TinyTeX / official TeX Live installer under the user directory. For skill-generated docs, make the dependency explicit rather than silently assuming `sudo` exists.
