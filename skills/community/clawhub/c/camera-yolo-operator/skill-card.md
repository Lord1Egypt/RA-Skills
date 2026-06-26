## Description: <br>
Runs local webcam YOLO object detection, object tracking, and DA3Metric depth estimation while storing models in a shared cache and visual outputs in the OpenClaw workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moroiser](https://clawhub.ai/user/moroiser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to test local cameras, run YOLO detection and tracking on webcam or video input, estimate object distance with DA3Metric depth, and save annotated visual outputs for inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a webcam or selected local video files and may capture sensitive visual data. <br>
Mitigation: Run it only against intended cameras or videos, confirm the camera index or source path before execution, and close unrelated camera-using applications. <br>
Risk: The skill saves raw captures, annotated images, and annotated videos to local output directories. <br>
Mitigation: Review output directories and save limits before running, use a dedicated workspace path when needed, and delete retained visual files after review. <br>
Risk: The skill downloads ML models from external sources. <br>
Mitigation: Use a virtual environment, download models from the documented sources, and review the shared model cache before running inference. <br>
Risk: The Linux chmod 666 camera-device troubleshooting command can broaden local device access. <br>
Mitigation: Prefer adding the user to the video group or restoring device permissions after testing; use chmod 666 only when the permission impact is understood. <br>


## Reference(s): <br>
- [YOLO Skill Deployment Guide](references/deployment.md) <br>
- [Platform Notes](references/platform.md) <br>
- [Ultralytics YOLO Models](https://docs.ultralytics.com/models/yolo11) <br>
- [Depth Anything DA3Metric-Large](https://huggingface.co/depth-anything/DA3Metric-Large) <br>
- [Ultralytics on Hugging Face](https://huggingface.co/ultralytics/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash and Python command examples; runtime scripts save JPG images, annotated MP4 video, and console statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are local by default under ~/.openclaw/workspace/projects/camera-yolo-operator, with configurable model paths, camera indices, runtime duration, confidence thresholds, save limits, and output directories.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
