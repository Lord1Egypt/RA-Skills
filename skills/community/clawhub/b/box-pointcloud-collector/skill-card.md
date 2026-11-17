## Description:

Intel RealSense D455 箱体点云数据采集工具，用于采集箱体 RGB 彩色图和深度图数据集，支持手动和自动采集模式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qujingyang28](https://clawhub.ai/user/qujingyang28)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to collect RGB-D box datasets with an Intel RealSense D455 camera for bin picking, deep learning dataset creation, point-cloud preparation, and camera calibration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The collection script captures RGB and depth views from a connected camera and stores them locally under a fixed Windows workspace path.

Mitigation: Run it in a least-privileged Python environment and collect only scenes where the local storage location and retention policy are acceptable.

Risk: Unpinned Python dependencies can change behavior across environments.

Mitigation: Install dependencies in an isolated environment and pin pyrealsense2, opencv-python, and numpy versions before operational use.

## Reference(s):

- [API Reference](references/api_reference.md)
- [Dataset Structure](references/dataset_structure.md)
- [ClawHub Skill Page](https://clawhub.ai/qujingyang28/skills/box-pointcloud-collector)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for running local collection and processing scripts; generated datasets contain RGB PNG images, raw uint16 depth frames, camera intrinsics, dataset configuration, and capture statistics.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
