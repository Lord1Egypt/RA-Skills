## Description: <br>
Arxiv Paper Writer helps an agent plan, scaffold, compile, debug, and review arXiv-style academic papers using LaTeX, BibTeX, TikZ figures, tables, and PDF output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[16miku](https://clawhub.ai/user/16miku) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical writers use this skill to have an agent create or maintain arXiv-style paper projects, including LaTeX structure, BibTeX references, figures, tables, compile-debug loops, and final quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate broadly for paper-writing, compilation, debugging, or review tasks. <br>
Mitigation: Define the target paper directory and requested scope before allowing file edits. <br>
Risk: The skill can suggest system package installation, MiKTeX configuration, or uv commands as part of LaTeX setup. <br>
Mitigation: Review each command before execution, especially commands using sudo or changing TeX package manager settings. <br>
Risk: Progress summaries default to Chinese, which may not fit all users or review workflows. <br>
Mitigation: Ask the agent to report progress in the preferred language at the start of the task. <br>


## Reference(s): <br>
- [arXiv Paper Workflow](references/workflow.md) <br>
- [Agent Survey Practice Guide](references/agent_survey_practice.md) <br>
- [Bibliography Reference](references/bibliography.md) <br>
- [Figures and Tables Reference](references/figures_and_tables.md) <br>
- [LaTeX Environment Reference](references/latex_environment.md) <br>
- [Linux TeX Live Full Reference](references/linux_texlive_full.md) <br>
- [Quality Review Reference](references/quality_review.md) <br>
- [Prompt Templates](references/prompt_templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with LaTeX, BibTeX, and shell command snippets; may also create or edit project files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Progress summaries are requested in Chinese by the skill unless the user asks otherwise.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
