## Description:

Baidu Yijian Vision helps agents route image and video analysis tasks to Baidu Yijian skills for object detection, safety monitoring, industrial inspection, SOP compliance, and operational analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yijian-baidu](https://clawhub.ai/user/yijian-baidu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external operators use this skill to select or invoke Baidu Yijian vision capabilities against images or video frames, including object detection, ROI and tripwire monitoring, industrial quality inspection, safety monitoring, OCR, pose estimation, and tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send selected local images, video frames, prompts, and workspace skill metadata to Baidu Yijian using the configured API key.

Mitigation: Use only approved inputs, avoid sensitive media unless policy permits sharing it with Baidu Yijian, and keep API keys scoped and rotated according to local credential policy.

Risk: The security summary notes that the client can upload any local file path it is given and lacks clear file-scope safeguards.

Mitigation: Run the skill in a constrained workspace, avoid letting untrusted prompts choose file paths, and review planned file paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yijian-baidu/skills/baidu-yijian-vision)
- [Baidu Yijian platform](https://yijian-next.cloud.baidu.com)
- [Baidu Yijian API key setup](https://yijian-next.cloud.baidu.com/apaas/)
- [ROI workflow](roi-workflow.md)
- [Tripwire workflow](tripwire-workflow.md)
- [Grid guide](grid-guide.md)
- [Types guide](types-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON responses; generated PNG and JSON files for grids, ROI previews, tripwire previews, and visualized detections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and YIJIAN_API_KEY; uses Baidu Yijian APIs and may create local preview or grid artifacts.]

## Skill Version(s):

0.9.42 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
