## Description:

FREE voice recognition using Groq's complimentary Whisper API. Transcribe audio messages to text in 50+ languages at no cost. Perfect for voice-to-text automation, meeting transcriptions, and accessibility features. Requires free Groq API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huixionghexiyi](https://clawhub.ai/user/huixionghexiyi)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to transcribe audio messages, voice notes, recordings, meeting audio, and accessibility-related voice input through Groq's Whisper transcription API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found unsafe credential-storage advice for Groq API keys.

Mitigation: Use a protected environment variable or secret manager for GROQ_API_KEY, and rotate any key that was pasted into a shared or project file.

Risk: Selected audio files are sent to Groq for transcription, and the security review identified a misleading privacy claim about third-party data sharing.

Mitigation: Install only when sending the selected audio to Groq is acceptable, and avoid submitting sensitive audio unless approved for the user's use case.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huixionghexiyi/skills/free-groq-voice)
- [Groq Console](https://console.groq.com/)
- [Groq Audio Transcriptions API Endpoint](https://api.groq.com/openai/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text transcription output with Markdown setup guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GROQ_API_KEY; accepts an audio file path, optional language hint, and optional GROQ_PROXY.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
