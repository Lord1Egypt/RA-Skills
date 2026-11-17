## Description:

Generates GB/T-style engineering drawings and CAD deliverables, including frames, title blocks, dimensions, isometric entities, DXF, PDF, and optional DWG conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hegenerkondo335-dot](https://clawhub.ai/user/hegenerkondo335-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering-drawing users use this skill to produce formal Chinese GB/T-style CAD drawings, templates, dimensions, technical notes, and PDF/DXF/DWG deliverables from structured drawing inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional DWG export path can download and execute an external ODA File Converter AppImage.

Mitigation: Prefer PDF/DXF-only operation unless the converter has been independently installed and verified in the target environment.

Risk: Release automation can stage, commit, and push repository contents.

Mitigation: Run release automation only in reviewed repositories that do not contain private drawings, credentials, or customer data.

Risk: Font troubleshooting guidance includes administrator-level repair commands.

Mitigation: Treat administrator commands as manual troubleshooting steps to be reviewed and executed by a qualified user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hegenerkondo335-dot/skills/gb-cad-figure)
- [Publisher profile](https://clawhub.ai/user/hegenerkondo335-dot)
- [ezdxf documentation](https://ezdxf.mozman.at/)
- [ODA File Converter](https://www.opendesign.com/guestfiles/oda_file_converter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; generated agent workflows may produce PDF, DXF, and DWG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [DWG output depends on optional ODA File Converter and Xvfb setup; PDF/DXF generation can run without the DWG converter.]

## Skill Version(s):

1.2.6 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
