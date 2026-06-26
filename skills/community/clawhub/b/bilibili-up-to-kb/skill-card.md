## Description: <br>
Convert Bilibili videos and channels into cleaned, structured text knowledge bases using Bilibili subtitles or local whisper.cpp transcription with optional LLM transcript cleaning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanjiaming](https://clawhub.ai/user/shanjiaming) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to transcribe single Bilibili videos or batch-process creator channels into a local text knowledge base with cleaned transcripts, metadata, and an index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access Chrome Bilibili session cookies when direct downloads fail. <br>
Mitigation: Prefer public-only downloads or an explicit exported cookie file, and use authenticated cookies only for content you are authorized to process. <br>
Risk: Transcript cleaning can send transcript text to the configured external LLM cleaning provider. <br>
Mitigation: Disable remote cleaning for private or sensitive media, or review the provider configuration before processing transcripts. <br>
Risk: Long-running batch jobs launched with nohup can continue processing unexpectedly. <br>
Mitigation: Supervise background jobs, record log locations, and stop jobs explicitly when processing should pause. <br>
Risk: High whisper.cpp concurrency can overload local GPU or CPU resources. <br>
Mitigation: Use the lower concurrency settings recommended by the skill for whisper fallback and monitor system load during large channel processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shanjiaming/bilibili-up-to-kb) <br>
- [Dependency Installation Guide](references/dependencies.md) <br>
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp.git) <br>
- [whisper.cpp small model](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin) <br>
- [whisper.cpp medium model](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated knowledge-base files include cleaned text transcripts, JSON metadata, raw transcript text, and a Markdown index.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch scripts are resumable, support configurable concurrency, and may use browser cookies or an external LLM cleaning provider depending on the run configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
