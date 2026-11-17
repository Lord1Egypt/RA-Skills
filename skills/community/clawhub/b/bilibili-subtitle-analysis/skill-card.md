## Description:

Downloads Bilibili subtitles, analyzes subtitle content, and generates structured Chinese summary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guige821](https://clawhub.ai/user/guige821)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download Bilibili video subtitles, analyze subtitle text, and produce structured Chinese reports from subtitle files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact asks users to paste a live Bilibili cookie into chat, exposing an account credential.

Mitigation: Use a local secret store or another local-only authentication flow, and treat any Bilibili cookie as an account credential.

Risk: The artifact runs external Python code through shell-based command construction.

Mitigation: Pin and verify the external biliSub code and Python dependencies, and replace shell string execution with safe argument-vector execution before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guige821/skills/bilibili-subtitle-analysis)
- [biliSub GitHub repository](https://github.com/lvusyy/biliSub)
- [Bilibili](https://bilibili.com)
- [FFmpeg download documentation](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and console text with command examples, generated reports, subtitle file paths, and JavaScript API guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create subtitle outputs in JSON, TXT, SRT, ASS, or VTT formats when the external downloader succeeds.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
