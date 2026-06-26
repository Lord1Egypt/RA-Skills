## Description: <br>
Download Douyin short videos from supported Douyin URLs by using a headless browser to extract the video source and curl to save the MP4. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lskun](https://clawhub.ai/user/lskun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to have an agent download a Douyin video from a direct video, search modal, share, or note URL into a local MP4 file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted URLs, filenames, or page data could cause unintended local shell commands to run. <br>
Mitigation: Review before installing, use only trusted Douyin links and simple filenames or paths, and prefer a revised version that avoids shell=True and validates Douyin and media URLs. <br>
Risk: Downloaded media may come from temporary CDN links and user-provided pages. <br>
Mitigation: Download promptly after extraction, confirm the destination path, and inspect downloaded files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lskun/douyin-dl) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local MP4 file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires agent-browser, curl, network access, and a user-provided Douyin URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
