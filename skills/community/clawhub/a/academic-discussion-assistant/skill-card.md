## Description:

Transforms small academic discussion recordings, such as advisor-student meetings and graduate group reports, into transcripts, structured notes emphasizing teacher feedback, action items, and a brief spoken summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinhao-96](https://clawhub.ai/user/xinhao-96)

### License/Terms of Use:

MIT-0

## Use Case:

External users and academic teams use this skill to process short research group meetings or advisor-student discussion recordings, identify likely teacher and student contributions, and produce transcript files, structured meeting notes, and an audio summary. It is intended for two to three person academic discussions where teacher feedback, student responses, required revisions, and next actions are the main outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive recordings and generated summaries are uploaded to SenseAudio and raw transcripts are stored locally.

Mitigation: Use only non-confidential material or approved recordings, and review local output retention before deployment.

Risk: The configurable SenseAudio API base can send recordings to an unexpected endpoint if misconfigured.

Mitigation: Set SENSEAUDIO_API_BASE only to a trusted official endpoint, or leave the default endpoint in place.

Risk: Runtime package installation can change the execution environment during use.

Mitigation: Prefer an environment where required dependencies are preinstalled and reviewed before running the skill.

## Reference(s):

- [Academic Discussion Summary Prompt](references/summary_prompt.md)
- [ClawHub skill page](https://clawhub.ai/xinhao-96/skills/academic-discussion-assistant)
- [SenseAudio API endpoint](https://api.senseaudio.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown response with transcript file paths, structured notes, a MEDIA attachment line, JSON transcript artifacts, text transcripts, and an audio summary file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY. The skill writes raw ASR JSON, plain transcript text, diarized transcript text, LLM input text, and a short TTS audio summary under an outputs directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
