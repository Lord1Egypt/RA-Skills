## Description: <br>
Intelligent workplace inspection system with guided setup, configurable inspection tasks, AI-powered image analysis, and Feishu alerting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsygcn](https://clawhub.ai/user/wsygcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Workplace operations, security, and facilities teams use this skill to configure camera-based inspection tasks, analyze captured workspace images with an AI vision model, and send alerts for employee presence, security patrol, or facility inspection findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workplace camera monitoring can expose employee surveillance images without adequate authorization, notice, or consent. <br>
Mitigation: Install only where monitoring is authorized, confirm workplace notice or consent requirements, and scope inspections to approved spaces and purposes. <br>
Risk: Camera credentials, Feishu credentials, and alert recipients can create secret-storage and data-disclosure exposure. <br>
Mitigation: Use least-privilege credentials, restrict alert recipients, verify token storage locations, lock down file permissions, and review AI and Feishu retention policies before sending workplace images. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wsygcn/employee-off-duty-detection-2) <br>
- [README](artifact/README.md) <br>
- [EZVIZ Cloud Capture API Endpoint](https://open.ys7.com/api/open/cloud/v1/capture/save) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Console text, JSON configuration, AI analysis text, and alert messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workplace images and camera or Feishu configuration values during execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
