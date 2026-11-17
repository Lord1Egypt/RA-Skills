## Description:

ChatTTS Local converts text, especially Chinese text, into local speech audio using the ChatTTS model, with configurable generation parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wodecanyun66-spec](https://clawhub.ai/user/wodecanyun66-spec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate local Chinese text-to-speech audio for QQ voice replies, document narration, notification audio, or long text narration without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First use can install unpinned Python packages.

Mitigation: Review and pin dependencies before installation, and run the skill in a dedicated virtual environment.

Risk: Model files may be downloaded from hf-mirror.com without artifact-level verification.

Mitigation: Manually download model artifacts from trusted sources where possible and verify checksums before use.

Risk: The skill is framed as local-only, but first use may require network downloads.

Mitigation: Preinstall and verify required model files before using the skill in restricted or production environments.

Risk: Advertised voice controls may not meet the needs of a specific workflow.

Mitigation: Test required speed, pitch, seed, and sampling behavior before relying on generated audio.

## Reference(s):

- [chattts_local ClawHub listing](https://clawhub.ai/wodecanyun66-spec/skills/chattts-local)
- [wodecanyun66-spec publisher profile](https://clawhub.ai/user/wodecanyun66-spec)
- [2Noise ChatTTS model repository](https://huggingface.co/2Noise/ChatTTS)
- [Hugging Face mirror used by model download scripts](https://hf-mirror.com)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Audio files such as WAV or MP3, file paths wrapped in <qqvoice> tags, and Markdown with inline shell commands for setup or invocation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio uses a 24000 Hz sample rate; long text is recommended to be split into segments under 500 Chinese characters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
