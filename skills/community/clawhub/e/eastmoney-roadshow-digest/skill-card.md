## Description: <br>
EastMoney Roadshow Digest (Transcript + Summary)｜东方财富路演纪要生成 turns public EastMoney roadshow replay pages into structured transcript, clean transcript, summary, brief, metadata, and run report files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunxq1017-hash](https://clawhub.ai/user/sunxq1017-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research support teams use this skill to process public EastMoney roadshow replay URLs into local transcript and summary artifacts. It is scoped to public replay pages and records downgrade paths when subtitles, ASR, or optional LLM enhancement are unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: When supported provider keys are present, public transcript text or intermediate cleaned text may be sent to an external LLM service for enhancement. <br>
Mitigation: For local-only processing, run in an environment without those provider keys and review outputs/run_report.md to confirm whether LLM enhancement was disabled. <br>
Risk: Transcript quality can degrade when subtitles are unavailable or ASR dependencies such as ffmpeg, faster-whisper, or av are missing or fail. <br>
Mitigation: Keep dependencies patched and available, and review transcript quality notes and downgrade details in outputs/run_report.md before relying on summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunxq1017-hash/eastmoney-roadshow-digest) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/sunxq1017-hash) <br>
- [EastMoney public roadshow example](https://roadshow.eastmoney.com/luyan/5149204) <br>
- [EastMoney roadshow detail API](https://roadshow.lvb.eastmoney.com/LVB/api/Roadshow/Detail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Local files: meta.json, transcript.md, clean_transcript.md, summary.md, brief.md, and run_report.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional external LLM enhancement is used only when a supported provider key is present; otherwise the skill falls back to rule-based outputs and records the path in run_report.md.] <br>

## Skill Version(s): <br>
v0.1.2-rc1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
