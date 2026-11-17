## Description:

Convert local annotation datasets between COCO, YOLO, Pascal VOC, and LabelMe formats with format selection and folder-oriented workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingo-318](https://clawhub.ai/user/mingo-318)

### License/Terms of Use:


## Use Case:

Developers and computer vision engineers use this skill to convert annotation files for dataset migration, model training preparation, and interoperability across common vision tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted COCO file_name field can cause YOLO text output to be written outside the chosen output directory.

Mitigation: Review annotation files before conversion, reject absolute paths and parent-directory components, and verify outputs remain inside the selected output folder.

Risk: Conversion can overwrite writable annotation files when output paths collide with existing files.

Mitigation: Run conversions in a dedicated workspace and confirm destination paths before processing files from other people.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingo-318/skills/annotation-format-converter)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands and local annotation outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files may be JSON, TXT, or XML annotation artifacts depending on the selected conversion.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
