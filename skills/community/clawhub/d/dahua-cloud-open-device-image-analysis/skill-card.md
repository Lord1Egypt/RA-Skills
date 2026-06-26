## Description: <br>
Captures images from authorized Dahua IoT devices, saves them locally, and sends them to Dahua Cloud AI for image analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doynkdeveloper](https://clawhub.ai/user/doynkdeveloper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to capture images from authorized Dahua cameras and ask Dahua Cloud AI to detect people, vehicles, objects, PPE, smoke, fire, falls, or intrusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized or inappropriate camera capture can expose surveillance images. <br>
Mitigation: Use the skill only with Dahua devices you are authorized to access and only for approved monitoring or analysis workflows. <br>
Risk: Dahua Cloud Product ID, Access Key, and Secret Key are sensitive credentials. <br>
Mitigation: Store credentials in environment variables, use least-privilege Dahua credentials, rotate them regularly, and do not print or share AK/SK values. <br>
Risk: Captured camera images are saved locally and sent to Dahua Cloud for analysis. <br>
Mitigation: Confirm the data-sharing posture is acceptable for the deployment and regularly delete unneeded files from captured_images. <br>
Risk: Troubleshooting commands may echo sensitive environment values in shared or logged terminals. <br>
Mitigation: Avoid echo-based credential checks on shared systems or terminals with retained logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/doynkdeveloper/dahua-cloud-open-device-image-analysis) <br>
- [Dahua Cloud Developer Platform](https://open.cloud-dahua.com/) <br>
- [README.md](artifact/README.md) <br>
- [FAQ.md](artifact/FAQ.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON-like analysis results, and local image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Dahua Cloud Product ID, Access Key, Secret Key, device serial number, prompt, and optional channel number.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
