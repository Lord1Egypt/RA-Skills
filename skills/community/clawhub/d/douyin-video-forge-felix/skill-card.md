## Description: <br>
Douyin Video Forge Felix helps operators collect Douyin trend data, analyze short-video patterns, generate production scripts, optionally call Kling for video generation, and assemble finished clips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felixlam10](https://clawhub.ai/user/felixlam10) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators and content teams use this skill to plan Douyin campaigns, gather trend and competitor evidence, produce short-video scripts and prompts, and optionally generate and stitch vertical videos with local tools and Kling API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring jobs may continue scraping, downloading, calling APIs, and writing files after a multi-day plan is created. <br>
Mitigation: Require explicit schedule review before enabling automation, confirm job and output locations, and document how to disable or delete created jobs. <br>
Risk: Kling API usage may incur costs and uses credentials from the local environment. <br>
Mitigation: Confirm API mode, expected volume, and credential configuration before video generation; use script-only mode when API generation is not intended. <br>
Risk: Downloaded third-party Douyin videos and transcriptions may include content with unclear rights or privacy expectations. <br>
Mitigation: Use collected material for analysis and reference only, review generated scripts for originality, and avoid copying source content verbatim. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/felixlam10/douyin-video-forge-felix) <br>
- [Douyin hot list](https://www.douyin.com/hot) <br>
- [Kling API site](https://klingai.com) <br>
- [Browser navigation reference](references/browser-navigation.md) <br>
- [Douyin algorithm reference](references/douyin-algorithm.md) <br>
- [Trend analysis reference](references/trend-analysis.md) <br>
- [Script templates reference](references/script-templates.md) <br>
- [Kling prompt guide](references/kling-prompt-guide.md) <br>
- [Seedance prompt guide](references/seedance-prompt-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown reports and scripts with inline bash commands, JSON helper-script status, and optional local media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and yt-dlp for core workflows; optional Python, Kling API environment variables, and faster-whisper enable video generation and transcription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
