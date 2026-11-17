## Description:

Azure语音转写专业版 helps agents guide enterprise speech-to-text workflows using Azure, including real-time streaming transcription, diarization, batch queues, custom models, and transcript export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and enterprise teams use this skill to configure Azure-based speech transcription for meetings, customer-service calls, and video subtitle workflows. It is intended for explicit speech-to-text tasks that may include real-time transcription, speaker separation, batch processing, and SRT, VTT, JSON, or plain-text outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trigger scope may route translation or localization requests to a speech transcription skill.

Mitigation: Use the skill only for explicit speech-to-text transcription tasks and reject translation-only or localization-only requests.

Risk: Audio sent to Azure and transcript files may contain confidential calls, meetings, or personal data.

Mitigation: Confirm the audio is approved for the target Azure environment, protect generated transcripts, and avoid exposing sensitive content in logs or shared paths.

Risk: Transcript exports can be written to local output paths chosen during use.

Mitigation: Set output directories deliberately and review file permissions before processing sensitive recordings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-transcription-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus transcript output formats such as SRT, VTT, JSON, and plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Azure transcription credentials, network access to Azure services, and deliberate handling of transcript output paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
