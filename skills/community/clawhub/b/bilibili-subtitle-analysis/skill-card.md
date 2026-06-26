## Description: <br>
Downloads Bilibili official or ASR subtitles, analyzes subtitle content, and generates structured summary reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guige821](https://clawhub.ai/user/guige821) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content analysts use this skill to fetch Bilibili subtitles, analyze transcript statistics and keywords, and produce readable content reports from video subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests Bilibili browser cookies, which can expose account sessions if pasted into chat, logs, or shared environments. <br>
Mitigation: Do not paste full browser cookies into chat or logs; use a disposable account or session for testing and keep credentials out of persistent transcripts. <br>
Risk: The skill runs external downloader code and ASR processing through local commands. <br>
Mitigation: Run only in a constrained environment, set an explicit trusted biliSub path, and inspect or pin the external biliSub code before allowing downloads or ASR processing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guige821/bilibili-subtitle-analysis) <br>
- [biliSub Project](https://github.com/lvusyy/biliSub) <br>
- [Bilibili](https://bilibili.com) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Markdown reports, text analysis, subtitle files such as JSON/TXT/SRT/ASS/VTT, and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Bilibili login cookies, an external biliSub checkout, Python dependencies, and optional ASR tooling.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
