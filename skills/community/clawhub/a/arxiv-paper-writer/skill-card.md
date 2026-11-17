## Description:

Creates, compiles, debugs, and reviews arXiv-style academic papers using LaTeX, BibTeX citations, TikZ figures, tables, and PDF output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[16miku](https://clawhub.ai/user/16miku)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical writers use this skill to plan, scaffold, write, compile, debug, and review arXiv-style LaTeX paper projects, especially survey papers with BibTeX citations and reproducible figures and tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LaTeX setup guidance may lead to persistent administrator-level TeX environment changes.

Mitigation: Review environment setup commands before running them, avoid administrator-wide MiKTeX auto-install unless intended, and prefer per-user or isolated TeX environments with reviewed dependencies.

Risk: Paper-generation workflows can create or modify project files and may introduce inaccurate claims, citations, or metadata.

Mitigation: Review file diffs, verify cited paper metadata against authoritative sources, and compile/check the paper before treating outputs as publication-ready.

## Reference(s):

- [arXiv Paper Workflow](references/workflow.md)
- [Bibliography Reference](references/bibliography.md)
- [Figures and Tables Reference](references/figures_and_tables.md)
- [LaTeX Environment Reference](references/latex_environment.md)
- [Linux TeX Live Full Reference](references/linux_texlive_full.md)
- [Quality Review Reference](references/quality_review.md)
- [Prompt Templates Reference](references/prompt_templates.md)
- [Agent Survey Practice Guide](references/agent_survey_practice.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with LaTeX, BibTeX, and shell command blocks; may also create or edit project files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce or modify .tex, .bib, figure/table, documentation, and build-output files in a user-selected paper project.]

## Skill Version(s):

0.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
