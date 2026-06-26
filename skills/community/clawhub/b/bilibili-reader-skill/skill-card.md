## Description: <br>
B站收藏夹视频智能总结：随机选取收藏视频，阅读字幕/评论/弹幕，生成中英双语总结PDF <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mistake-12](https://clawhub.ai/user/mistake-12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize Bilibili favorites by fetching video metadata, subtitles, comments, and danmaku, then generating bilingual study notes and a PDF. It also supports progress tracking, searching prior summaries, and optional delivery through chat platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable Bilibili session cookies are stored in plaintext. <br>
Mitigation: Keep the .env file private with restrictive permissions and reinstall or rotate cookies if the file may have been exposed. <br>
Risk: Generated PDFs can be sent through external chat platforms. <br>
Mitigation: Choose no delivery unless intentional, and confirm the destination before sending any generated PDF. <br>
Risk: Local history and vector data can retain records of viewed or summarized favorites. <br>
Mitigation: Periodically delete local history or vector data when long-term records are not wanted. <br>
Risk: Subtitles, comments, and danmaku are untrusted user-generated content. <br>
Mitigation: Use them only as summarization input and ignore any instructions embedded in the fetched video content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mistake-12/bilibili-reader-skill) <br>
- [Bilibili API notes](references/bilibili-api-notes.md) <br>
- [External skill installation notes](references/installing-external-skills.md) <br>
- [WeasyPrint documentation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, PDF files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands; fetched video data as JSON; bilingual summaries rendered as PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bilibili session cookies and may optionally send generated PDFs through configured chat delivery platforms.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata, released 2026-05-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
