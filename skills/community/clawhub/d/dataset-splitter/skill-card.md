## Description:

Split image datasets into train, validation, and test sets with configurable ratios, optional stratification, annotation handling, YOLO output layout, and reproducible random seeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingo-318](https://clawhub.ai/user/mingo-318)

### License/Terms of Use:


## Use Case:

Developers and machine learning engineers use this skill to prepare image datasets for model training by creating train, validation, and test splits while keeping corresponding annotation files aligned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default split operation moves image and label files, which can alter the source dataset or leave it partially relocated if execution fails.

Mitigation: Run on a backup, prefer the --copy option, and choose an empty output directory before splitting.

Risk: Existing files in the output location can be overwritten or mixed with prior split contents.

Mitigation: Use a new empty output directory and review split counts before relying on the generated dataset.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mingo-318/skills/dataset-splitter)
- [Publisher Profile](https://clawhub.ai/user/mingo-318)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline bash commands and file path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create train, validation, and test dataset folders, with optional YOLO images and labels layout, when the splitter script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
