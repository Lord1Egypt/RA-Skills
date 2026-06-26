## Description: <br>
Cleans Excel spreadsheets by removing empty rows and columns, deduplicating rows, sorting by the first column, and generating a summary report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfxia](https://clawhub.ai/user/sfxia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and office teams use this skill to clean selected Excel files and save a new cleaned workbook or report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package appears incomplete because the referenced Excel processing module is missing, so cleanup may fail at runtime. <br>
Mitigation: Confirm the complete package includes the Excel handler before purchase or installation and test the skill on a copy of a spreadsheet. <br>
Risk: Automatic cleanup can remove duplicates, delete empty rows, or reorder data in ways that may not match the user's intent. <br>
Mitigation: Keep the original spreadsheet, confirm the cleanup criteria, and inspect the generated file before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sfxia/excel-auto-clean) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [Cleaned Excel workbook with text status message or payment link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves a new cleaned file after purchase verification when the Excel processing package is complete.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
