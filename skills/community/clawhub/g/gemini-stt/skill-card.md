## Description:

Transcribe audio files using Google's Gemini API or Vertex AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[araa47](https://clawhub.ai/user/araa47)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to transcribe local audio files, including voice-message formats, through Google Gemini API or Vertex AI authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio files are uploaded to Google Gemini or Vertex AI for transcription.

Mitigation: Only transcribe recordings that your organization permits to be processed by those Google services.

Risk: The skill uses a Gemini API key or Google Cloud Application Default Credentials to make requests.

Mitigation: Use scoped, managed credentials and follow local key-handling rules before running the transcription command.

## Reference(s):

- [Gemini API Models](https://ai.google.dev/gemini-api/docs/models)
- [ClawHub Skill Page](https://clawhub.ai/araa47/skills/gemini-stt)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text transcription with Markdown usage guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an audio file path and either GEMINI_API_KEY or Google Cloud Application Default Credentials.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
