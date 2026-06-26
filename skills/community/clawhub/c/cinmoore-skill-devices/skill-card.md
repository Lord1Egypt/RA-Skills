## Description: <br>
Cinmoore Skill Devices controls smart camera devices, records and processes video, queries events, and uses LLM/VLM analysis for natural-language automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buaalingming](https://clawhub.ai/user/buaalingming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and device operators use this skill to query and control Cinmoore smart camera devices, manage PTZ actions, record or analyze video, and automate supported device operations from natural language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Opaque downloaded binaries handle camera credentials and can record video or change device settings. <br>
Mitigation: Install only from trusted publisher evidence, independently verify binaries where possible, and test first with least-privilege camera credentials. <br>
Risk: The skill can record video, move cameras, calibrate devices, and change detection settings. <br>
Mitigation: Require explicit user confirmation before device movement, recording, calibration, or detection-setting changes. <br>
Risk: Credential files may contain SDK and model API secrets. <br>
Mitigation: Avoid storing production secrets in shared environment files and keep credentials scoped to the minimum access needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buaalingming/cinmoore-skill-devices) <br>
- [Cinmoore skill homepage](http://192.168.8.60/system/algorithm/cinmoore-skill-devices) <br>
- [Linux executable download](https://super-acme-shoot-sh.oss-cn-shanghai.aliyuncs.com/skill-tools/exe/cinmoore-skill-devices-ubuntu) <br>
- [Windows executable download](https://super-acme-shoot-sh.oss-cn-shanghai.aliyuncs.com/skill-tools/exe/cinmoore-skill-devices-windows.exe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke downloaded executables that interact with camera devices, video files, credentials, and model APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
