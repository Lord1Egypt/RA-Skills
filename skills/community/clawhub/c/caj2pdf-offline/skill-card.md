## Description:

将知网 CAJ / KDH / NH 文献高保真转换为 PDF（保留文字层可选中 + 目录书签）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to convert local CNKI CAJ, KDH, or NH literature files into PDF files while preserving original source files. It supports single-file and batch conversion, reports failures, and points users to the official CNKI fallback when conversion is not reliable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses opaque embedded Windows DLLs for document decoding.

Mitigation: Run conversions only in a restricted account or disposable Windows environment, and avoid processing sensitive documents unless the runtime is sandboxed.

Risk: The setup flow can install Python packages from a package mirror.

Mitigation: Review dependency installation before use and prefer a controlled package source or prebuilt isolated environment for managed deployments.

Risk: The bundled project contains optional registry integration behavior.

Mitigation: Use only the conversion workflow and avoid the registry installer unless it has been separately reviewed and approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/j-levee/skills/caj2pdf-offline)
- [CNKI](http://cnki.net/)
- [CAJViewer](http://cajviewer.cnki.net/)
- [caj2pdf upstream project](https://github.com/caj2pdf/caj2pdf)
- [caj2pdf-restructured repository](https://github.com/zombie110year/caj2pdf-restructured/)
- [MuPDF](https://mupdf.com/index.html)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PDF files with terminal text summaries and fallback guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates one PDF per successful input file; original CAJ/KDH/NH files are preserved.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
