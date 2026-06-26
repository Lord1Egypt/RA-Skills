## Description: <br>
Bilibili Subtitles helps an agent use yt-dlp to extract existing or auto-generated subtitles from public Bilibili videos without downloading the full video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ScottLiu007](https://clawhub.ai/user/ScottLiu007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content analysts use this skill to retrieve available Bilibili subtitle tracks for summarization, translation, or question answering. It is intended for public or otherwise authorized videos that already provide subtitle tracks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting may use browser cookies or a cookies.txt file, which can enable authenticated Bilibili access if used without clear user intent. <br>
Mitigation: Use cookies only with explicit user consent, prefer a narrowly scoped cookies.txt file, and never paste cookie contents or account secrets into chat. <br>
Risk: The skill runs yt-dlp locally and writes generated subtitle files into the selected working folder. <br>
Mitigation: Run the commands only for expected Bilibili URLs in a folder where generated subtitle files are intended, then review the files before relying on them. <br>


## Reference(s): <br>
- [Bilibili subtitle troubleshooting reference](reference.md) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated subtitle artifacts are typically VTT, SRT, or plain text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local yt-dlp installation and may require user-provided cookies for authenticated Bilibili access; it does not transcribe videos that have no subtitle track.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
