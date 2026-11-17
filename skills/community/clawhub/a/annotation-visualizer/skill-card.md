## Description:

Visualize bounding boxes and class labels on images with support for COCO, YOLO, VOC, and LabelMe annotation formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingo-318](https://clawhub.ai/user/mingo-318)

### License/Terms of Use:


## Use Case:

Developers and dataset maintainers use this skill to visualize bounding boxes and labels for quality checking and debugging image annotation datasets in COCO, YOLO, VOC, and LabelMe formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: COCO annotations can reference file paths that cause reads or overwrites outside the intended dataset folders.

Mitigation: Run COCO mode only on trusted datasets or harden filename handling before processing untrusted COCO JSON.

Risk: Dependency installation may be inconsistent because Pillow is not pinned in a reviewed requirements file.

Mitigation: Pin Pillow in a reviewed requirements file before deployment.

## Reference(s):

- [Annotation Visualizer ClawHub Skill Page](https://clawhub.ai/mingo-318/skills/annotation-visualizer)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash code blocks and generated annotated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes visualized images to a chosen output directory and requires Pillow plus local image and annotation files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
