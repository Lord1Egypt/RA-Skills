## Description: <br>
Visualize bounding boxes and class labels on images with support for COCO, YOLO, VOC, and LabelMe annotation formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mingo-318](https://clawhub.ai/user/Mingo-318) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, data annotation teams, and machine learning engineers use this skill to inspect image datasets by rendering bounding boxes and labels for quality checks and debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch processing can write many visualization files to disk. <br>
Mitigation: Use a separate output directory and review input and output paths before running a batch job. <br>
Risk: The script depends on Pillow for image processing. <br>
Mitigation: Install Pillow from a trusted package source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mingo-318/annotation-visualizer) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Visualization script](artifact/scripts/visualize.py) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline bash commands; generated outputs are image files with rendered annotations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local image and annotation files and writes visualization images to a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
