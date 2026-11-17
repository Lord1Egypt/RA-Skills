## Description:

Professional LaTeX writing assistant for scanning existing LaTeX templates, reading reference materials, drafting content that follows template requirements, and compiling PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dayunyan](https://clawhub.ai/user/dayunyan)

### License/Terms of Use:

Proprietary

## Use Case:

External academic authors and developers use this skill to analyze LaTeX templates, read reference material, draft template-conforming LaTeX content, and compile PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can read and overwrite arbitrary paths.

Mitigation: Constrain read_reference, scan_template, write_latex, and compile_pdf to trusted project files and require confirmation before overwriting files.

Risk: The setup asks for privileged host package installation.

Mitigation: Install only in an isolated project workspace or container/VM and review any sudo package installation separately.

Risk: Unpinned dependencies can change behavior across installations.

Mitigation: Pin Python and LaTeX-related dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dayunyan/skills/academic-writer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with LaTeX snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write LaTeX files and trigger PDF compilation in the user's project workspace.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
