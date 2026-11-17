## Description:

Webcam YOLO and depth detection. 摄像头 YOLO 目标检测与 DA3Metric 深度估计；模型放 modules 缓存，输出放 projects。

This skill is ready for commercial/non-commercial use.

## Publisher:

[moroiser](https://clawhub.ai/user/moroiser)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run local webcam capture, YOLO object detection, YOLO plus DA3Metric depth overlays, and object tracking workflows. It helps test camera access, download required models, configure runtime paths, and save annotated images or videos under a workspace project directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses local camera input and can save raw or annotated visual media to disk.

Mitigation: Run it only where camera capture is expected, review the configured output directory, and delete captured media when it is no longer needed.

Risk: The documented Linux troubleshooting path can weaken webcam permissions with chmod 666.

Mitigation: Use video-group membership or per-user ACL access instead of world-writable device permissions.

Risk: The skill downloads or loads external YOLO and DA3Metric model assets.

Mitigation: Review model sources, pin dependency and model versions where possible, and run the skill in a virtual environment.

## Reference(s):

- [Deployment Guide](references/deployment.md)
- [Platform Notes](references/platform.md)
- [DA3Metric-Large model](https://huggingface.co/depth-anything/DA3Metric-Large)
- [Ultralytics YOLO models](https://docs.ultralytics.com/models/yolo11)
- [Ultralytics on Hugging Face](https://huggingface.co/ultralytics/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python commands; runtime scripts can save JPEG images, annotated video, and console status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime outputs may include local camera captures, annotated detection images, depth overlay images, annotated videos, and object-count summaries.]

## Skill Version(s):

1.3.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
