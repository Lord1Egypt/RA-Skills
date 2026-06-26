## Description: <br>
Capture screenshots and screen recordings when a user needs to capture the screen, a window, or a region for tutorials or documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support teams, and content creators can use this skill to capture local screenshots, selected windows, screen regions, and delayed captures for documentation or troubleshooting. Screen recording support is limited and may require platform-specific tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots can capture private or sensitive information visible on the screen. <br>
Mitigation: Review the visible screen before capture, prefer narrow region or window captures, and delete generated files that contain private information. <br>
Risk: Custom output paths on Windows may be unsafe because PowerShell path handling is under-scoped. <br>
Mitigation: Avoid custom output paths on Windows until the path handling is fixed. <br>
Risk: Full screen recording support is limited and may require platform-specific tools such as ffmpeg. <br>
Mitigation: Confirm required local tools are installed and review recording behavior before relying on it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dinghaibin/dinghaibin-screenshot-tool) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Local image files, console status text, and Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Screenshot files may contain sensitive visible screen contents; recordings require platform-specific setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
