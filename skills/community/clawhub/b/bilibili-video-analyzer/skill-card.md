## Description: <br>
Analyzes Bilibili academic/educational videos to extract knowledge points and generate clean-style study notes with screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[railgun9983](https://clawhub.ai/user/railgun9983) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External learners, educators, and developers use this skill to analyze Bilibili educational videos, extract structured knowledge points, and generate Markdown learning notes with screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports a local-code-execution bug in frame-rate parsing. <br>
Mitigation: Use the skill only in an isolated environment and fix the eval-based frame-rate parsing issue before routine use. <br>
Risk: Bilibili login or session use can expose account credentials or cookies. <br>
Mitigation: Use a dedicated session, protect cookies as secrets, and avoid sharing or committing login artifacts. <br>
Risk: Downloaded videos and transcripts may contain private, sensitive, or unauthorized content. <br>
Mitigation: Analyze only videos the user is allowed to download and share, and review or redact transcripts before sending them to any LLM. <br>


## Reference(s): <br>
- [Best Practices Guide](references/BEST_PRACTICES.md) <br>
- [Quick Quality Checklist](references/QUICK_QUALITY_CHECKLIST.md) <br>
- [References Index](references/README.md) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/railgun9983/bilibili-video-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with JSON analysis structures, command examples, and generated screenshot file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local video, subtitle, screenshot, JSON, and Markdown report files during the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
