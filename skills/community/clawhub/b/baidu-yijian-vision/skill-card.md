## Description: <br>
Baidu Yijian Vision helps agents route image and video analysis requests to Baidu Yijian vision skills for object detection, safety monitoring, industrial inspection, and ROI or tripwire workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linpower](https://clawhub.ai/user/linpower) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to call Baidu Yijian vision APIs from an agent, choose public or workspace vision skills by intent, analyze selected images, and define ROI or tripwire regions for inspection, safety, and monitoring tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, ROI or tripwire coordinates, prompts, and related metadata are sent to Baidu Yijian using the user's API key. <br>
Mitigation: Use only with data approved for that external service, and avoid confidential, regulated, or surveillance images unless the organization has approved the data flow. <br>
Risk: The skill requires a sensitive YIJIAN_API_KEY credential. <br>
Mitigation: Store the API key in the agent environment, avoid committing it to files or logs, and rotate it if exposure is suspected. <br>
Risk: Incorrect ROI or tripwire coordinates can cause misleading detection results. <br>
Mitigation: Preview grid, ROI, or tripwire overlays and confirm the region before invoking a production vision skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linpower/baidu-yijian-vision) <br>
- [Baidu Yijian Platform](https://yijian-next.cloud.baidu.com) <br>
- [Baidu Yijian API Key Setup](https://yijian-next.cloud.baidu.com/apaas/) <br>
- [ROI Workflow](roi-workflow.md) <br>
- [Tripwire Workflow](tripwire-workflow.md) <br>
- [Type Definitions](types-guide.md) <br>
- [Grid Input Guide](grid-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance, shell commands, JSON API responses, and optional generated image or metadata files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and YIJIAN_API_KEY; outputs may include detections, bounding boxes, confidence scores, ROI or tripwire overlays, grid images, and workspace skill lists.] <br>

## Skill Version(s): <br>
0.9.42 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
