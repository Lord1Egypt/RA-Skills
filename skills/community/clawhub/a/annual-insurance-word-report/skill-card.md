## Description: <br>
Generates annual insurance welfare Word reports from the gh_hg_bscyearall_dues MySQL table by extracting a target year, reading column comments, mapping business fields into a bundled template, and writing a .docx report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lin-shiwu](https://clawhub.ai/user/lin-shiwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or operations staff use this skill to generate annual insurance welfare .docx reports from a configured MySQL reporting table and a fixed Word template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a MySQL reporting table using provided database credentials. <br>
Mitigation: Use a dedicated read-only, least-privilege database account and avoid production credentials. <br>
Risk: The mysql CLI fallback may expose credentials through local process handling. <br>
Mitigation: Prefer the PyMySQL execution path and provide the CLI fallback only in controlled environments. <br>
Risk: The generated .docx may overwrite an existing file at the selected output path. <br>
Mitigation: Choose an output path where replacement is acceptable or write to a new filename. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lin-shiwu/annual-insurance-word-report) <br>
- [Annual insurance configuration](references/annual-insurance-config.json) <br>
- [Placeholder enums](references/placeholder-enums.json) <br>
- [Schema comment query](references/schema-comment-query.sql) <br>
- [Word template mapping](references/word-template-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration] <br>
**Output Format:** [Word .docx report with command-line status or error output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to outputs/annual-insurance-report-<year>.docx by default unless an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
