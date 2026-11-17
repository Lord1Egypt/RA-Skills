## Description:

Renders content containing mathematical formulas into PDF documents using HTML, MathJax, and Microsoft Edge headless mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nahida-robin](https://clawhub.ai/user/nahida-robin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create reports, notes, course materials, technical documents, and other PDFs that need correctly rendered mathematical formulas. It is most relevant for Windows workflows that can use Microsoft Edge headless mode and MathJax.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The enhanced conversion script can terminate all Microsoft Edge processes during retry cleanup or when --kill-edge is used, which may close unrelated user browser sessions.

Mitigation: Prefer the basic workflow that does not kill Edge processes, or modify cleanup to terminate only the headless browser process launched by the skill.

Risk: The PDF workflow loads MathJax from a CDN, which may fail in restricted networks and may be unsuitable for sensitive or offline documents.

Mitigation: Use a local MathJax copy for sensitive, offline, or network-restricted documents, and verify the generated PDF for unrendered LaTeX text.

## Reference(s):

- [Formula PDF lessons learned](references/lessons_learned.md)
- [MathJax TeX CHTML component](https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js)
- [ClawHub skill page](https://clawhub.ai/nahida-robin/skills/formula-pdf)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with HTML, PowerShell, Python, and PDF file workflow outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or guides creation of HTML source files and PDF documents; optional verification checks for unrendered LaTeX text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
