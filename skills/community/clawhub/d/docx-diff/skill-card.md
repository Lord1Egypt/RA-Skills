## Description: <br>
Compares two local Word .docx documents for text, image, and style changes, then generates highlighted DOCX, HTML, and plain-text diff reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mypicko](https://clawhub.ai/user/mypicko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and document reviewers use this skill to compare two local .docx files and summarize changed paragraphs, images, and formatting without relying on an online comparison service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML, DOCX, and TXT reports may contain sensitive document text or embedded images. <br>
Mitigation: Compare only documents the user intends to process, choose the output directory deliberately, and handle generated reports as sensitive files. <br>
Risk: The skill requires installing the python-docx dependency before use. <br>
Mitigation: Install dependencies in a trusted environment, preferably a virtual environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Analysis, Guidance] <br>
**Output Format:** [Markdown summary plus generated DOCX, HTML, and TXT report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may include document text and embedded images from the compared files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
