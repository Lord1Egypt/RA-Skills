## Description:

Downloads arXiv paper PDFs or LaTeX source archives by arXiv ID or URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninganme](https://clawhub.ai/user/ninganme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and other external users use this skill to download arXiv PDFs or LaTeX source archives by providing an arXiv ID or arXiv URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted --name value can cause downloads to overwrite files outside the intended download folder.

Mitigation: Use only plain filenames, keep downloads in a dedicated folder, reject path components in --name, and enforce that the final output path remains under the chosen output directory.

Risk: Unattended downloads from untrusted arguments can create unexpected files or overwrite existing files.

Mitigation: Review arguments before execution, avoid silent overwrites, and add streaming downloads with a size limit before unattended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ninganme/skills/arxiv-downloader)
- [arXiv abstract URL example](https://arxiv.org/abs/2301.12345)
- [arXiv PDF download pattern](https://arxiv.org/pdf/{id}.pdf)
- [arXiv LaTeX source download pattern](https://arxiv.org/e-print/{id})

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance and terminal output from a Python download script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces downloaded PDF files or LaTeX source archives in a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
