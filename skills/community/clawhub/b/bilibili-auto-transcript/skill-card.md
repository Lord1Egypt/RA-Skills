## Description:

B站视频转录+收藏夹扫描。三级降级（CC→AI→Whisper），AI摘要生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[54lynnn](https://clawhub.ai/user/54lynnn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Bilibili users use this skill to transcribe individual Bilibili videos or monitor a Bilibili favorites folder for new videos, generating local transcript files, reports, and optional AI summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use browser session cookies for Bilibili access.

Mitigation: Run it in a dedicated or low-privilege environment and avoid exposing broad browser session cookies.

Risk: API keys and summary provider settings may be stored in a local .env file.

Mitigation: Keep .env private, restrict file permissions, use a limited API key with spending controls, and set SUMMARY_API_URL only to a trusted HTTPS provider.

Risk: Transcripts and summaries are retained locally and may be sent to an external AI summary API when enabled.

Mitigation: Review content sensitivity before enabling summaries and confirm retention expectations for the local transcript database and output directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/54lynnn/skills/bilibili-auto-transcript)
- [Architecture Reference](references/architecture.md)
- [Bilibili Favorites API Reference](references/bilibili-fav-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, local text transcript files, SQLite records, and CSV reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May retain transcripts and summaries locally and may call a configured OpenAI-compatible summary API when enabled.]

## Skill Version(s):

5.2.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
