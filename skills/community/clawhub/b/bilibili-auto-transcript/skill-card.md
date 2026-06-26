## Description: <br>
B站视频转录+收藏夹扫描。三级降级（CC→AI→Whisper），AI摘要生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[54lynnn](https://clawhub.ai/user/54lynnn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to transcribe Bilibili videos or monitor a public Bilibili favorites list for new videos, then generate local transcript files, optional summaries, and processing reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use Bilibili browser login cookies to access subtitles. <br>
Mitigation: Use a dedicated browser profile and avoid exporting cookies to shared temporary paths. <br>
Risk: Transcript excerpts may be sent to the configured AI summary provider when OPENAI_API_KEY or .env credentials are present. <br>
Mitigation: Leave OPENAI_API_KEY unset for local-only transcription, or review the configured provider before enabling summaries. <br>
Risk: Scheduled scanning can automatically process new favorites and create local transcripts, reports, logs, and database entries. <br>
Mitigation: Review cron jobs before enabling them and disable schedules that are not needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/54lynnn/bilibili-auto-transcript) <br>
- [Architecture reference](references/architecture.md) <br>
- [Bilibili favorites API reference](references/bilibili-fav-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcripts with metadata and optional structured summaries, plus CSV reports and local SQLite records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are organized by video publish year and month when batch processing is used.] <br>

## Skill Version(s): <br>
5.2.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
