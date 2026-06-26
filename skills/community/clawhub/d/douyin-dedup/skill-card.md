## Description: <br>
Downloads Douyin videos from supplied URLs, removes watermarks and audio, and transforms the video to reduce duplicate-content matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxueda](https://clawhub.ai/user/hanxueda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to process Douyin video URLs into locally saved MP4 files with watermark removal, visual transformations, and audio stripping. It should be used only for videos the user owns or is authorized to modify and repost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remove attribution signals and alter videos to avoid duplicate-content matching. <br>
Mitigation: Use it only for videos the user owns or is authorized to modify and repost, and retain required attribution and platform compliance checks outside the skill. <br>
Risk: The skill downloads remote Douyin content and writes processed MP4 files to local storage. <br>
Mitigation: Run it in a controlled workspace, review supplied URLs before execution, and clear generated files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanxueda/douyin-dedup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Command-line execution with local MP4 file output and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MP4 files under ~/video-dedup/output and temporary workspace files under ~/video-dedup/workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
