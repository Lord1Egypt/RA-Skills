## Description: <br>
Intel RealSense D455 箱体点云数据采集工具，用于采集箱体 RGB 彩色图和深度图数据集，支持手动和自动采集模式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qujingyang28](https://clawhub.ai/user/qujingyang28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to collect and process RGB-D datasets from an Intel RealSense D455 camera for box point clouds, bin picking data preparation, deep learning dataset creation, and camera calibration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The collection script accesses a connected RealSense camera and records RGB and depth data to local disk. <br>
Mitigation: Run it only in an approved capture environment and confirm that the scene does not include sensitive visual information before saving frames. <br>
Risk: The default output path is hardcoded for a Windows Administrator OpenClaw workspace. <br>
Mitigation: Review and change the output directory before execution if that path is not appropriate for the local machine. <br>
Risk: Depth capture quality depends on range, camera focus, and other programs using the camera. <br>
Mitigation: Follow the documented capture range guidance, verify camera focus, and close other RealSense applications before collection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qujingyang28/box-pointcloud-collector) <br>
- [Publisher profile](https://clawhub.ai/user/qujingyang28) <br>
- [API 参考](references/api_reference.md) <br>
- [数据集结构详解](references/dataset_structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash and Python code blocks; generated runtime files include PNG color images, uint16 depth raw files, and JSON metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Intel RealSense D455 camera, USB 3.0, Windows 10/11, and local Python dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
