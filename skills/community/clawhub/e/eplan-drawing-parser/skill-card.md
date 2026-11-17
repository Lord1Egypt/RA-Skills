## Description:

Extracts text, vector line geometry, component designators, per-page wiring counts, preview images, and BOM cross-check reports from EPLAN/CAD vector PDF electrical drawings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[727583550-coder](https://clawhub.ai/user/727583550-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and electrical engineering teams use this skill to run local parsing workflows for EPLAN/CAD vector PDFs, inspect extracted component and wire data, and compare drawings against Excel BOMs. Outputs should support review workflows and should be manually checked before engineering, procurement, or compliance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may present heuristic extraction and reporting as authoritative for electrical topology, model, quantity, title-block, terminal-table, or UL compliance decisions.

Mitigation: Treat outputs as review aids and manually validate them against the source drawing, BOM, and applicable compliance records before engineering, procurement, or compliance use.

Risk: Local PDF and Excel processing may expose sensitive drawings or BOM data to unnecessary files, dependencies, or runtime permissions.

Mitigation: Pin and review the PyMuPDF and openpyxl dependencies, then run the scripts with access limited to the intended drawing and BOM files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/727583550-coder/skills/eplan-drawing-parser)
- [OpenClaw metadata homepage](https://github.com/openclaw-skills/eplan-drawing-parser)
- [PyMuPDF documentation](https://pymupdf.readthedocs.io/)
- [EPLAN symbol knowledge](knowledge/eplan_symbols.md)
- [Usage examples](examples/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; generated files may include JSON, PNG previews, console summaries, and XLSX reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on vector PDFs and optional Excel BOM files; no credential environment variables are declared in the release evidence]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
