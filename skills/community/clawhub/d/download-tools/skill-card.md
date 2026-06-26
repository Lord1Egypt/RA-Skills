## Description: <br>
CLI download tools for YouTube audio and WeChat articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jqlong17](https://clawhub.ai/user/jqlong17) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and command-line users use this skill to download YouTube audio as MP3 files and save WeChat articles as text files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to user-provided URLs and relies on third-party downloader tools. <br>
Mitigation: Install only if comfortable using yt-dlp and ffmpeg through Homebrew, and review URLs before execution. <br>
Risk: Output names can affect where downloaded files are written. <br>
Mitigation: Use simple output names rather than paths and avoid running the scripts in sensitive directories. <br>
Risk: Browser-cookie troubleshooting options can expose an authenticated browser session to yt-dlp. <br>
Mitigation: Use browser-cookie options only when intentionally authorizing yt-dlp to access that session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jqlong17/download-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown with bash command examples and local shell script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local TXT or MP3 files from user-provided URLs and requires curl, yt-dlp, and ffmpeg.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
