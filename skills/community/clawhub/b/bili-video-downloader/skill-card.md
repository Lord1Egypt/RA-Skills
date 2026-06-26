## Description: <br>
Downloads Bilibili videos to a specified folder with yt-dlp and requires an explicit output path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zitao666](https://clawhub.ai/user/zitao666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare safe yt-dlp commands for downloading Bilibili videos or collections into a user-selected directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloads may be saved to an unintended directory if the output path is omitted or incorrect. <br>
Mitigation: Provide a specific save folder and review the generated command before execution. <br>
Risk: The skill depends on installing and running yt-dlp from pip. <br>
Mitigation: Install yt-dlp only in an environment where that dependency is acceptable and review the generated command before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zitao666/bili-video-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yt-dlp and a user-provided save folder.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
