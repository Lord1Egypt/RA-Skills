## Description:

Bilibili Up To Kb converts Bilibili videos and UP channels into cleaned, indexed text knowledge bases using AI subtitles or local whisper.cpp transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanjiaming](https://clawhub.ai/user/shanjiaming)

### License/Terms of Use:


## Use Case:

Developers, researchers, and knowledge workers use this skill to turn Bilibili videos or full creator channels into local transcript files, metadata, and an index for search and downstream summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Bilibili video titles can trigger the title-handling bug described by security evidence.

Mitigation: Review and patch transcribe.sh before using the skill with untrusted URLs.

Risk: The batch workflow can fall back to Chrome browser cookies for restricted content.

Mitigation: Require explicit user consent and prefer a dedicated browser profile or cookie file for any cookie-based access.

Risk: Transcript cleaning can disclose transcript text to an external model through opencode.

Mitigation: Avoid cleaning private, paid, confidential, or sensitive media unless that external data flow is acceptable.

Risk: Whisper fallback and batch processing can create high local compute load.

Mitigation: Use the documented low whisper concurrency settings and monitor long-running jobs before increasing parallelism.

## Reference(s):

- [Dependency Installation Guide](references/dependencies.md)
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp.git)
- [whisper.cpp small model](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin)
- [whisper.cpp medium model](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin)
- [Hugging Face mirror for China users](https://hf-mirror.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and generated text, JSON metadata, and Markdown index files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates per-video transcript files, per-video metadata JSON, an index.md file, and hidden raw transcript files when run by the user.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
