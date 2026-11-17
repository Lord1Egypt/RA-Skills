## Description:

Byted Text To Speech converts text into audio with the Volcengine Doubao speech synthesis API, including voice selection, speech controls, Markdown filtering, and LaTeX reading options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to synthesize speech for narration, voiceover, read-aloud audio, and multilingual text playback. It is useful when an agent needs to generate a playable local audio file from supplied text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text and API credentials are sent to a configured third-party TTS provider endpoint.

Mitigation: Use the skill only with text appropriate for the configured provider, keep the default provider endpoint unless a trusted alternative is required, and avoid submitting sensitive content.

Risk: Live API keys may be written to a workspace .env file and later committed or shared.

Mitigation: Store credentials in a secrets manager or protected environment variables, keep .env files out of version control, and rotate any key that may have been exposed.

Risk: The credential fallback can list or create API keys when alternate ARK credentials are present.

Mitigation: Remove or gate the fallback behind explicit user consent before broad deployment, and review generated keys after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-text-to-speech)
- [Volcengine Doubao Speech product documentation](https://www.volcengine.com/docs/6561/1257543)
- [HTTP Chunked/SSE unidirectional streaming V3 API](https://www.volcengine.com/docs/6561/1598757)
- [Voice list](https://www.volcengine.com/docs/6561/1257544)
- [API key usage guide](https://www.volcengine.com/docs/6561/1816214)
- [Setup guide](references/setup-guide.md)
- [Documentation index](references/docs-index.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [JSON status output and local audio files, with Markdown guidance for setup and troubleshooting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio output can be MP3, PCM, or Ogg Opus and includes a local_path value when synthesis succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
