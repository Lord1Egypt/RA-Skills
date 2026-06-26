## Description: <br>
Split image datasets into train, validation, and test sets with random or stratified ratios, annotation handling, YOLO output structure, and reproducible seeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mingo-318](https://clawhub.ai/user/Mingo-318) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and machine learning engineers use this skill to prepare image datasets for model training by splitting images and matching label files into train, validation, and test folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The split operation moves source image and annotation files by default. <br>
Mitigation: Back up the dataset first or use the copy option when the original dataset must be preserved. <br>
Risk: Dataset outputs may not match the expected training pipeline if annotations or YOLO structure are misconfigured. <br>
Mitigation: Use the YOLO option when matching label files should be split with images, then verify the generated folders before deleting originals or updating training jobs. <br>
Risk: Optional image statistics require Pillow in the runtime environment. <br>
Mitigation: Install dependencies in a virtual environment when using statistics or image inspection features. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mingo-318/dataset-splitter) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text] <br>
**Output Format:** [Markdown with bash command examples and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying utility can create train, validation, and test folders, optionally in YOLO format, and can copy or move source files depending on user options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
