## Description:

Transcribe audio files using AIMLAPI speech-to-text endpoints with polling and optional transcript saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aimlapihello](https://clawhub.ai/user/aimlapihello)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to transcribe user-provided audio messages or local audio files through AIMLAPI and return or save transcript text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio recordings are sent to AIMLAPI for transcription.

Mitigation: Use the skill only for audio that may be shared with AIMLAPI, and avoid confidential or sensitive recordings unless AIMLAPI's data handling terms meet the use case.

Risk: The skill requires an AIMLAPI API key.

Mitigation: Keep the key scoped to this service where possible and provide it through AIMLAPI_API_KEY or a protected key file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aimlapihello/skills/aiml-voice)
- [AIMLAPI API base endpoint](https://api.aimlapi.com/v1)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands]

**Output Format:** [Plain text transcript, optionally written to a text file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and AIMLAPI_API_KEY; uploads selected audio to AIMLAPI and polls until completion or timeout.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
