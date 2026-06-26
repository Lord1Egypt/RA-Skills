## Description: <br>
智能A3试卷PDF切分工具，自动识别页面中间空白位置，将横向或纵向A3试卷PDF切分为A4 PDF以便打印。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boxertan](https://clawhub.ai/user/boxertan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, students, office staff, and agents assisting them use this skill to split local A3 exam or document PDFs into ordered A4 pages for printing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The output path may overwrite an existing file. <br>
Mitigation: Confirm the destination path before running and use a distinct filename for converted output. <br>
Risk: Broad trigger wording could cause the skill to be used for generic PDF or printing requests. <br>
Mitigation: Confirm that the user specifically wants A3-to-A4 PDF splitting before invoking the tool. <br>
Risk: The skill installs and runs Python PDF-processing dependencies locally. <br>
Mitigation: Install dependencies in a virtual environment and process only PDFs the user intends to provide. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boxertan/a3-pdf-splitter) <br>
- [README](artifact/README.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Text guidance with command examples; the tool writes a PDF file to the requested output path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local input and output file paths, renders pages at 400 DPI, and preserves page order by appending each split half to the output PDF.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
