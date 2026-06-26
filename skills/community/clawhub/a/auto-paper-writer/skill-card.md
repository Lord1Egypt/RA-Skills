## Description: <br>
Auto Paper Writer guides an agent through searching recent arXiv papers, drafting an IEEEtran LaTeX research paper with figures, compiling a PDF, and saving the project files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myjackcat](https://clawhub.ai/user/myjackcat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical writers use this skill to create a research-paper scaffold with references, figures, LaTeX source, and a PDF draft for later review and completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup step can delete unrelated PowerShell, Python, or presentation files from a user's Desktop. <br>
Mitigation: Run the skill only in a dedicated project or temporary folder, change cleanup commands to target exact files created by the current run, and require user confirmation before deletion. <br>
Risk: The workflow uses hard-coded Windows and TeX Live paths that may not match the user's environment. <br>
Mitigation: Confirm local paths, output folders, and LaTeX tooling before running commands. <br>
Risk: Generated academic claims, methods, and experiment sections may be incomplete, inaccurate, or unsupported. <br>
Mitigation: Treat drafts as scaffolding and require human review, citation checks, and real experiment results before submission or distribution. <br>


## Reference(s): <br>
- [Auto Paper Writer on ClawHub](https://clawhub.ai/myjackcat/auto-paper-writer) <br>
- [IEEEtran paper template](references/ieee_template.md) <br>
- [LaTeX academic writing guide](references/latex_guide.md) <br>
- [Scientific figure guide](references/figure_guide.md) <br>
- [arXiv API query endpoint](https://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell, Python, and LaTeX code blocks plus generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a paper project containing LaTeX source, figures, reference notes, downloaded PDFs, and an optional compiled PDF.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
