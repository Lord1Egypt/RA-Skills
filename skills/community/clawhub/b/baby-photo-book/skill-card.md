## Description: <br>
Generates print-ready baby photo book PDFs from a folder of photos using age grouping and aspect-ratio-aware layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atmosphere16happy](https://clawhub.ai/user/atmosphere16happy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to organize baby photos by age stage and generate an A4 PDF photo book with cover, chapter pages, smart photo layouts, and date or age annotations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script reads baby photos and EXIF or file dates from the folder selected by the user. <br>
Mitigation: Run it only on a narrowly scoped photo folder that you are comfortable processing. <br>
Risk: The script writes the generated photo book to a user-provided output path. <br>
Mitigation: Review the output path before execution and use a virtual environment for the Pillow and ReportLab dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/atmosphere16happy/baby-photo-book) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with bash commands; generated artifact is a PDF photo book.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script writes a local A4 PDF and reads image files from the user-selected photo folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
