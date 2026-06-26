## Description: <br>
FFBox helps agents guide users through FFBox multimedia transcoding, batch processing, remote transcoding, and HTTP API automation with safety checks around files, local services, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ttqftech](https://clawhub.ai/user/ttqftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, media operators, and FFBox users use this skill to plan and automate video, audio, and image conversion workflows. It helps with installation checks, FFBoxService API calls, batch queue management, remote transcoding, webhook notifications, and polling-based completion notices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FFBoxService can control media transcoding tasks and may be exposed beyond the local machine if configured that way. <br>
Mitigation: Keep FFBox bound to localhost where possible, set a password before network exposure, and require explicit approval before connecting to a remote FFBox service. <br>
Risk: Transcoding outputs can overwrite existing files or operate on unintended paths. <br>
Mitigation: Confirm output paths before overwriting, avoid wildcard-based file selection, and operate only on files the user has authorized. <br>
Risk: Remote uploads, webhook listeners, scheduled polling, and external notification targets can move data or leave background automation running. <br>
Mitigation: Ask for explicit approval before uploads, webhook setup, scheduled polling, or external notifications, and clean up listeners or schedules after completion. <br>


## Reference(s): <br>
- [FFBox on ClawHub](https://clawhub.ai/ttqftech/ffbox) <br>
- [FFBox Website](https://ffbox.ttqf.tech) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>
- [FFBox API Reference](references/API.md) <br>
- [FFBox Quick Guide](https://my.feishu.cn/wiki/Yiz3wkSMtiIQVzk1O25ckU2KnVc) <br>
- [FFBox FAQ](https://my.feishu.cn/wiki/W00pwqicLicathkujk5cNBnin6m) <br>
- [FFBox License and Terms](references/FFBox_LICENSE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline PowerShell, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local FFBox API requests, webhook listener setup, or polling steps after user approval.] <br>

## Skill Version(s): <br>
0.1.5-3-003 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
