## Description:

Generates Python data processing scripts from user-provided Excel templates and ERP export data, with guided confirmation of files, mappings, paths, naming, encoding, and Excel report constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangxiao971208-star](https://clawhub.ai/user/yangxiao971208-star)

### License/Terms of Use:

MIT-0

## Use Case:

Business users, analysts, and developers use this skill to turn Excel report templates and ERP CSV or Excel exports into repeatable Python automation scripts for cleaning, mapping, calculating, and generating reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Excel or CSV samples may contain business data that is broader than needed for report-script generation.

Mitigation: Share only the sample files, sheets, and columns needed to define the report workflow.

Risk: Generated Python scripts may read or write local files using user-provided paths.

Mitigation: Review generated scripts before running them and confirm all local paths and output locations.

Risk: Incorrect mappings, encoding assumptions, or naming conventions can produce inaccurate reports.

Mitigation: Confirm mappings, file naming, CSV encoding, and processing rules, then test the generated script before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangxiao971208-star/skills/data-processing-script-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scripts should keep editable path variables near the top, try common CSV encodings, preserve Excel template formatting where possible, and include delivery instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
