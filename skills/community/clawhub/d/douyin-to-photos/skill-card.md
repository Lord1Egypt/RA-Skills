## Description: <br>
Build and maintain an Apple Shortcuts workflow that takes a Douyin share link, resolves a no-watermark MP4 URL via configurable backend APIs, saves the video into the Photos app, and cleans temporary cache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahnxu](https://clawhub.ai/user/vahnxu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and iOS Shortcuts builders use this skill to create a one-tap workflow that accepts Douyin links from the Share Sheet or clipboard, resolves an MP4 through configured providers, saves it to Photos, and cleans temporary files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected Douyin links are sent to tikwm.com or another configured resolver endpoint. <br>
Mitigation: Use the skill only when that disclosure is acceptable, and configure a fallback endpoint only if it is trusted. <br>
Risk: The workflow can download and store media that the user may not have rights to keep. <br>
Mitigation: Process only content the user is allowed to download and store, and do not use it to bypass paid, member-only, or protected access controls. <br>
Risk: Broader Photos access or persistent storage would increase privacy exposure. <br>
Mitigation: Keep Photos permission add-only, avoid telemetry or history, and delete temporary media files after import or failure. <br>


## Reference(s): <br>
- [Douyin-to-Photos Shortcut Build Guide](references/shortcut-build-guide.md) <br>
- [Douyin To Photos ClawHub Listing](https://clawhub.ai/vahnxu/douyin-to-photos) <br>
- [Primary Resolver Endpoint](https://www.tikwm.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with JSON configuration and Bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve configurable API endpoints, timeout handling, Photos add-only permission, and temporary-file cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
