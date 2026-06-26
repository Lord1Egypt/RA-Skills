## Description: <br>
Interactive CSV data cleaning CLI that supports automatic type inference, missing-value handling, duplicate detection, and cleaned CSV export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data practitioners, and external users use CSV Wizard to inspect CSV files, clean missing values and duplicates, standardize column names, and write cleaned CSV outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleaning options can remove rows, change values, or overwrite cleaned dataset outputs if used carelessly. <br>
Mitigation: Keep original CSV files backed up, prefer writing to a new output file, and review lossy options such as dropping rows, filling missing values, and removing duplicates before running them on important data. <br>


## Reference(s): <br>
- [CSV Wizard on ClawHub](https://clawhub.ai/antonia-sz/csv-wizard) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with CLI command examples and CSV file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include dataset summaries, previews, cleaning recommendations, and cleaned CSV files written to a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
