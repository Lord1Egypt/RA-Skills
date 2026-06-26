## Description: <br>
Converts computer vision annotation files between COCO, YOLO, Pascal VOC, and LabelMe formats with format detection and batch folder conversion support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mingo-318](https://clawhub.ai/user/Mingo-318) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and computer vision engineers use this skill to convert annotation datasets between common training and labeling formats before model training, evaluation, or dataset migration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted input file can cause converted output to be written outside the selected output folder. <br>
Mitigation: Run the converter only on trusted annotation files, use a temporary output directory, and review generated files before relying on them. <br>
Risk: Python dependencies and local file processing can affect the user's environment. <br>
Mitigation: Install dependencies in an isolated Python environment and run conversions in a workspace that does not contain sensitive files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mingo-318/annotation-format-converter) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated annotation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create JSON or text annotation files in the requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
