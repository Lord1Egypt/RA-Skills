## Description: <br>
Download Douyin videos via the TikHub API without requiring Douyin login. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mfang0126](https://clawhub.ai/user/mfang0126) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to identify Douyin links or video IDs, retrieve a TikHub-parsed video URL, and optionally save the video as an MP4 file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires storing a TikHub API token locally. <br>
Mitigation: Keep the token in the local OpenClaw config file and do not paste it into chat, logs, or shared outputs. <br>
Risk: Douyin links or video IDs are sent to TikHub for parsing. <br>
Mitigation: Use the skill only when sending the target Douyin link or ID to TikHub is acceptable. <br>
Risk: The script may download video files when the download option is used. <br>
Mitigation: Confirm the destination directory before downloading and use a specific output directory when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mfang0126/douyin-video-dl) <br>
- [TikHub user registration](https://user.tikhub.io/register) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, URLs, and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print a Douyin modal_id and direct video URL, or save an MP4 file to the configured download directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
