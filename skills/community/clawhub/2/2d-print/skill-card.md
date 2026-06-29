## Description: <br>
Controls 2D printing on macOS by using CUPS commands to send images, PDFs, and text files to local or configured printers with options for printer selection, copies, paper size, orientation, color mode, print quality, queue inspection, and cancellation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayf3](https://clawhub.ai/user/mayf3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to prepare safe macOS CUPS print commands for local or configured printers, including selecting a printer, setting copies and media options, checking queues, and cancelling jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent could submit a print job with the wrong file, printer, copy count, color mode, or destination. <br>
Mitigation: Require the agent to show the printer name, file path, copy count, color mode, and destination before submitting the job. <br>
Risk: The agent could cancel active local print jobs too broadly. <br>
Mitigation: Ask the agent to show the specific job ID or printer queue before cancellation, and avoid blanket cancellation unless explicitly intended. <br>
Risk: Remote or cloud printer destinations could send documents outside the local environment. <br>
Mitigation: Confirm the selected destination before printing and use remote or cloud printers only when that destination is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mayf3/2d-print) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mayf3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target macOS CUPS printers and should identify printer name, file path, copy count, color mode, destination, and cancellation target when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
