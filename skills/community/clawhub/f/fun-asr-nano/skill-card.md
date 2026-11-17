## Description:

Fun-ASR-Nano transcribes audio files locally with sherpa-onnx and supports Chinese dialects, English, Japanese, lyrics, and rap speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengzhendong](https://clawhub.ai/user/pengzhendong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to transcribe audio files into text on a local machine. It is intended for speech-to-text workflows involving common audio formats and multilingual or dialect-heavy content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime model download may occur before the skill can operate offline.

Mitigation: Prefetch and verify the ModelScope model in a controlled environment, then run with network access disabled after setup.

Risk: Unpinned Python packages can change behavior across installs.

Mitigation: Pin and review dependency versions for sherpa-onnx, soundfile, and modelscope before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pengzhendong/skills/fun-asr-nano)
- [ClawHub publisher profile](https://clawhub.ai/user/pengzhendong)
- [ModelScope model identifier: pengzhendong/Fun-ASR-Nano-int8](https://modelscope.cn/models/pengzhendong/Fun-ASR-Nano-int8)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text transcription output with optional timestamp lines and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI accepts one or more audio files and exposes decoding options such as provider, thread count, language, hotwords, sampling controls, and inverse text normalization.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
