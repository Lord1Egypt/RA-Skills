## Description:

Extracts electronic component specifications from supplied datasheet PDFs with page- and table-level citations, including pinout, voltage, I2C address, timing, register map, and electrical characteristics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baorepo](https://clawhub.ai/user/baorepo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and electronics engineers use this skill to inspect component datasheets, extract design-relevant parameters, and distinguish PDF-supported values from missing or uncertain information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local PDF processing can expose sensitive datasheets or generated page images to the agent workspace.

Mitigation: Process only PDFs intended to be shared with the agent, keep render_page output paths inside a workspace or temporary directory, and avoid important existing files.

Risk: PDF extraction may be inaccurate for image-only pages, complex tables, merged cells, rotated text, or graph-only values.

Mitigation: Cross-check extracted values against rendered pages or page text, cite the source page/table, and mark uncertain or absent values rather than guessing.

Risk: Installing PDF dependencies system-wide can create avoidable environment and privilege risk.

Mitigation: Install dependencies in a virtual environment and avoid running pip as administrator or root.

## Reference(s):

- [README.md](README.md)
- [PDF_STRATEGY.md](PDF_STRATEGY.md)
- [TEMPLATES.md](TEMPLATES.md)
- [scripts/pdf_tools.py](scripts/pdf_tools.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown datasheet analysis with cited tables, source page references, and optional JSON template blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires source-backed values from the provided PDF; missing values are reported as NOT SPECIFIED IN DATASHEET with an acquisition path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
