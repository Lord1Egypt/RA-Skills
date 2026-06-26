# arxiv-paper-writer

`arxiv-paper-writer` is a Claude Code skill for creating, compiling, debugging, and reviewing arXiv-style academic papers, especially survey papers written in LaTeX with BibTeX citations, TikZ figures, and reproducible PDF output.

This skill was extracted from the successful `papers/agent-survey` experiment in the Paper-Write-Skill-Test project, where Claude Code produced a 15-page AI Agent survey paper with real references, TikZ figures, tables, and a compiled PDF.

## What this skill does

It guides Claude Code through a staged paper engineering loop:

```text
plan → scaffold → bibliography → section writing → figures/tables → compile → debug → review
```

The skill is designed to avoid one-shot paper generation. It instead encourages small verified steps and repeated compile/debug cycles.

## Directory layout

```text
arxiv-paper-writer/
├── SKILL.md
├── README.md
├── templates/
│   ├── arxiv_survey_main.tex
│   ├── full_survey_main.tex
│   ├── references.bib
│   ├── agent_survey_references.bib
│   └── agent_survey_figures_tables.tex
├── references/
├── scripts/
├── assets/
└── evals/
```

## Main capabilities

- Create an arXiv-style LaTeX paper project.
- Build and maintain a BibTeX bibliography.
- Write survey sections incrementally.
- Generate TikZ figures and LaTeX tables.
- Compile with Linux TeX Live or Windows MiKTeX.
- Diagnose common LaTeX and BibTeX errors.
- Review academic quality and arXiv readiness.
- Reuse the proven `papers/agent-survey` workflow through `references/agent_survey_practice.md`, `templates/full_survey_main.tex`, `templates/agent_survey_references.bib`, and `templates/agent_survey_figures_tables.tex`.

## Recommended usage

Example user prompts:

```text
用 Claude Code 帮我写一篇 10-15 页 arXiv 风格的英文综述论文，主题是 LLM agents。
```

```text
请把这个研究主题初始化成一个 LaTeX 论文项目，并创建 main.tex 和 references.bib。
```

```text
我的论文编译失败了，请读取 main.log 并修复 undefined citation 和 LaTeX 宏包冲突。
```

## Reused Agent Survey assets

The skill now includes selected reusable assets from the completed `papers/agent-survey` experiment:

- `references/agent_survey_practice.md`: condensed practice guide for the proven Claude Code paper-writing loop.
- `references/linux_texlive_full.md`: fuller Linux cloud TeX Live setup and validation guide.
- `references/prompt_templates.md`: reusable prompts for planning, scaffolding, bibliography, section writing, figure/table creation, compile-debug, and final review.
- `templates/full_survey_main.tex`: richer 9-section survey scaffold derived from the final Agent Survey structure.
- `templates/agent_survey_references.bib`: 39-entry example bibliography from the completed paper.
- `templates/agent_survey_figures_tables.tex`: reusable TikZ and table patterns.
- `assets/generate_paper_flowchart.png`: workflow diagram from the Windows Claude Code paper-writing run.
## Validation scripts

Check skill structure:

```bash
uv run python scripts/check_skill_structure.py
```

Check BibTeX:

```bash
uv run python scripts/check_bibtex.py path/to/references.bib
```

Check LaTeX log:

```bash
uv run python scripts/check_latex_log.py path/to/main.log
```

## Repository status

This skill is published as a standalone repository and linked from the parent project as a Git submodule.

- GitHub: `https://github.com/16Miku/arxiv-paper-writer-skill.git`
- ClawHub: `https://clawhub.ai/16miku/arxiv-paper-writer`

