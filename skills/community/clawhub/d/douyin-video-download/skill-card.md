## Description: <br>
Downloads Douyin videos from single links or batches, with duplicate handling, no-watermark download paths, and fallback download backends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to download public Douyin videos individually or from a link list, with options for output directory, filename, concurrency, and timeout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the skill under-discloses behavior and recommends a risky privileged installer for yt-dlp. <br>
Mitigation: Review before installing; avoid one-line sudo curl installation and install yt-dlp through a trusted package manager or verified download. <br>
Risk: The skill downloads media from external Douyin URLs using browser automation and downloader backends. <br>
Mitigation: Run only with trusted Douyin URLs in a low-privilege environment and review output paths before batch downloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/franklu0819-lang/douyin-video-download) <br>
- [Publisher profile](https://clawhub.ai/user/franklu0819-lang) <br>
- [yt-dlp releases](https://github.com/yt-dlp/yt-dlp/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and downloaded media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local video files in a configured output directory when the commands are run.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
