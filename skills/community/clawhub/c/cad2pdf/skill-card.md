## Description:

Converts DWG and DXF CAD drawings into vector PDFs with automatic page splitting, Chinese text decoding, dimension repair, hatch rendering, and black-and-white print output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgx281227231](https://clawhub.ai/user/lgx281227231)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and CAD users use this skill to convert DWG or DXF drawings into shareable PDF files for review, printing, or delivery when recipients may not have CAD software. It is especially oriented to multi-frame engineering drawings that need automatic page splitting and readable Chinese annotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can make system-wide package changes and install dependencies with root privileges.

Mitigation: Install in a controlled VM or container, verify the ODA File Converter source and checksum, and prefer a Python virtual environment for Python dependencies.

Risk: DWG conversion may process extra CAD files located in the same input folder.

Mitigation: Place the target DWG in a folder without unrelated or confidential drawings before conversion.

## Reference(s):

- [CAD2PDF ClawHub skill page](https://clawhub.ai/lgx281227231/skills/cad2pdf)
- [ODA File Converter dependency](https://www.opendesign.com/guestfiles/get?filename=ODAFileConverter_QT6_lnxX64_8.3dll_27.1.deb)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with shell commands and generated PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output PDFs are generated from local DWG or DXF inputs; paper size and DPI can be configured by command-line flags.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
