## Description:

Byted Las Asr Pro helps agents use Volcengine LAS to transcribe audio or video files, with optional subtitles, speaker-separated utterances, language detection, and emotion or gender metadata through an asynchronous submit-and-poll workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to submit media to Volcengine LAS for speech-to-text transcription, diarized utterance extraction, subtitle or caption preparation, and optional speech metadata analysis. The workflow also guides agents through credential checks, local media validation, price estimation, task submission, polling, and result presentation.

### Deployment Geography for Use:

China regions supported by Volcengine LAS: cn-beijing and cn-shanghai

## Known Risks and Mitigations:

Risk: The skill can automatically install or update the Volcengine-hosted SDK from a remote URL.

Mitigation: Install only after trusting the SDK source; prefer a release that pins and verifies the SDK package before use.

Risk: Audio, transcripts, and task metadata are uploaded to or retrieved from the provider service using local credentials.

Mitigation: Use only approved recordings, protect LAS_API_KEY and related Volcengine credentials, and avoid storing credentials in shared transcripts or logs.

Risk: Detached background polling can continue with credential access after the initiating interaction ends.

Mitigation: Prefer managed, cancellable polling where available and monitor or terminate background polling jobs when no longer needed.

Risk: Transcription jobs can incur provider billing and the selected rate may depend on service configuration or request parameters.

Mitigation: Estimate cost from media duration and pricing references, disclose that the estimate may differ from the provider bill, and require user confirmation before task submission.

## Reference(s):

- [las_asr_pro API reference](references/api.md)
- [Volcengine LAS pricing reference](references/prices.md)
- [Volcengine LAS pricing documentation](https://www.volcengine.com/docs/6492/1544808)
- [ClawHub skill listing](https://clawhub.ai/volcengine-skills/skills/byted-las-asr-pro)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request templates, transcript text, result JSON, and optional utterance CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local output directories containing result.json, transcript.txt, utterances.json, utterances.csv, poll logs, and completion status files.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
