## Description: <br>
Scrapes Douyin creator videos, downloads audio with Playwright and ffmpeg with yt-dlp fallback, and transcribes the audio with Whisper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GPTtang](https://clawhub.ai/user/GPTtang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations users use this skill to track Douyin creator accounts, collect recent video metadata, download audio, and generate Chinese transcript Markdown for review or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles authenticated Douyin session cookies. <br>
Mitigation: Use a dedicated Douyin account and virtual environment, keep .douyin_cookies.json private and out of source control, and delete or rotate cookies after use. <br>
Risk: The skill installs and runs external scraping and media-processing tooling. <br>
Mitigation: Review and pin dependencies, review MediaCrawler before use, and run the workflow in an isolated environment. <br>
Risk: Browser-cookie fallback can expose broader browser session data. <br>
Mitigation: Avoid browser-cookie fallback unless necessary and prefer a dedicated browser profile for collection work. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/GPTtang/douyin-content-tracker) <br>
- [Pipeline Reference](references/pipeline.md) <br>
- [Troubleshooting Reference](references/troubleshooting.md) <br>
- [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated CSV, audio, and transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written under OUTPUT_BASE_DIR; transcript outputs are Markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
