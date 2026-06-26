## Description: <br>
Combines ordered images from a folder into an A3 landscape PDF with two A4-sized images placed side by side on each page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangchuang9523-gif](https://clawhub.ai/user/wangchuang9523-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-preparation users use this skill to convert numbered image files into printable A3 landscape PDFs with two A4 images per page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local script reads image files from a user-selected folder and writes a PDF to the requested output path. <br>
Mitigation: Run it only on folders you control and choose the output path carefully before execution. <br>
Risk: Image parsing depends on Pillow, so outdated image-processing dependencies can carry security exposure. <br>
Mitigation: Keep Pillow updated and process only trusted image files when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangchuang9523-gif/a4-to-a3-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and Python script guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local PDF files when the referenced Python script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
