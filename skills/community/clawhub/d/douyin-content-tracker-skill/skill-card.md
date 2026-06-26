## Description: <br>
This skill helps agents scrape Douyin (TikTok China) creator content, download audio, transcribe it with Whisper, and guide setup, incremental tracking, cookie refresh, and debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GPTtang](https://clawhub.ai/user/GPTtang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to track Douyin creator accounts, collect recent video metadata, extract audio, and generate Chinese-language transcript Markdown. It also guides setup, dependency installation, cookie refresh, and troubleshooting for the scraping and transcription pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses Douyin login cookies. <br>
Mitigation: Use a dedicated Douyin account where possible, protect or delete .douyin_cookies.json after use, and avoid syncing or committing the cookie file. <br>
Risk: The skill depends on MediaCrawler and Python packages that are installed locally. <br>
Mitigation: Install in a trusted or isolated environment, review and pin MediaCrawler and Python dependencies, and run only the pipeline commands needed for the task. <br>
Risk: Local file handling can be affected by untrusted account or creator names. <br>
Mitigation: Fix or review blogger-name path handling before processing untrusted account data. <br>


## Reference(s): <br>
- [Pipeline Reference](artifact/references/pipeline.md) <br>
- [Troubleshooting Reference](artifact/references/troubleshooting.md) <br>
- [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) <br>
- [ClawHub Release Page](https://clawhub.ai/GPTtang/douyin-content-tracker-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and generated CSV, audio, and transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated outputs are written under OUTPUT_BASE_DIR, including cleaned CSV metadata, .m4a audio files, per-video transcript Markdown, and per-creator transcript summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
