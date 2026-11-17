## Description:

ClawPDF Master helps agents extract PDF text and tables, convert PDFs to Markdown, batch extract or merge folders of PDFs, and generate heuristic document summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to process user-selected PDFs, including extracting content, converting documents to Markdown, merging batches, and producing quick document summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed or floating PDF-processing dependencies can change behavior or expand attack surface.

Mitigation: Install in an isolated environment and pin or review dependencies before use.

Risk: Scripts read PDFs and folders selected by the operator and may process unintended files if pointed at the wrong path.

Mitigation: Run the skill only on PDFs and directories intentionally chosen for the task.

Risk: Output paths can overwrite existing files.

Mitigation: Review output destinations before execution and write to a dedicated result directory when possible.

Risk: Advertised OCR and form-filling behavior is incomplete in the artifact because referenced support files are not present.

Mitigation: Treat OCR and form workflows as unavailable unless the missing files are added and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/clawpdf-master)
- [Northcap Group publisher profile](https://clawhub.ai/user/northcap-group)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, plain text, Python snippets, shell command examples, and generated PDF or text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected PDF operation and may include extracted text, Markdown conversions, merged PDFs, or heuristic summaries.]

## Skill Version(s):

1.0.13 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
