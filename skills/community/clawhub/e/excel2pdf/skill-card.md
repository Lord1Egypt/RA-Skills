## Description: <br>
Converts Excel .xlsx sign-in sheets and rosters into print-ready A4 PDFs with table formatting and Chinese font support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncepuee](https://clawhub.ai/user/ncepuee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and office users can use this skill to convert local Excel sign-in sheets, rosters, and tables into printable PDFs while preserving Chinese text and table layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local conversion script reads user-selected Excel files and may overwrite an existing PDF when the default or chosen output path already exists. <br>
Mitigation: Run it only on intended local files and review or set the --out path before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ncepuee/skills/excel2pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with command examples and PDF file output from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local .xlsx input file, openpyxl, reportlab, and a Chinese-capable font; by default, the PDF is written beside the input file with a .pdf extension.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
