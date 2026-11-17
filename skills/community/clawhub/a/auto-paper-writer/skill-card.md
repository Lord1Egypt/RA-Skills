## Description:

Auto Paper Writer guides an agent through an end-to-end academic paper drafting workflow that searches ArXiv, summarizes prior-work limitations, proposes a model, drafts IEEEtran LaTeX, generates matplotlib figures, and compiles a PDF draft for user review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myjackcat](https://clawhub.ai/user/myjackcat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to draft an academic paper package from a research direction, including literature notes, LaTeX source, figures, and a compiled PDF draft. The generated research claims, novelty framing, and experiment details require user review and completion before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cleanup commands can delete unrelated PowerShell, Python, and presentation files from the user's Desktop.

Mitigation: Run cleanup only inside a dedicated paper workspace after showing the exact files to be deleted and obtaining user confirmation.

Risk: The generated paper may include unverified novelty claims, method details, or experiment results.

Mitigation: Require expert review, source checking, and replacement or completion of experiment details before publication or submission.

## Reference(s):

- [Auto Paper Writer ClawHub Page](https://clawhub.ai/myjackcat/skills/auto-paper-writer)
- [IEEEtran Paper Template](references/ieee_template.md)
- [LaTeX Academic Writing Guide](references/latex_guide.md)
- [Scientific Figure Guide](references/figure_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with PowerShell, Python, and LaTeX code blocks plus generated LaTeX, PDF, PNG, and reference files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected paper package includes paper.tex, paper.pdf, generated figures, a literature list, and downloaded source PDFs; generated academic content requires user verification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
