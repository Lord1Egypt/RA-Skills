## Description:

Runs a Python-based device health inspection that reviews monitoring alerts, writes a Markdown report, normalizes host and problem JSON, and exports a four-sheet Excel workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lerwee](https://clawhub.ai/user/lerwee)

### License/Terms of Use:

MIT-0

## Use Case:

Operations engineers and infrastructure support teams use this skill to inspect monitored device health, review current or historical alerts, and return both a Markdown inspection conclusion and an Excel workbook from the same data set.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses API credentials and live monitoring data.

Mitigation: Install only in a trusted internal environment, require HTTPS for LWJK_API_URL, and keep LWJK_API_SECRET out of shared files.

Risk: The workflow generates and executes a temporary Excel export script.

Mitigation: Inspect or replace the temporary exporter workflow before deployment and execute only scripts generated from the trusted template.

Risk: Generated reports and intermediate JSON files can retain sensitive infrastructure data.

Mitigation: Restrict the output directory and delete intermediate JSON and temporary files when they are no longer needed.

## Reference(s):

- [Excel export template](artifact/references/export_excel_template.py)
- [ClawHub skill page](https://clawhub.ai/lerwee/skills/alert-inspection)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown report text, JSON file paths, shell commands, and an Excel workbook path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a Markdown report, normalized hosts/problems JSON files, and one Excel workbook with four required sheets.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
