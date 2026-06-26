## Description: <br>
Transcribe, diarize, translate, post-process, and structure audio or video with AssemblyAI-oriented workflows for local files or URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to transcribe recordings, add speaker labels or translations, and produce transcript bundles for downstream automation. It is most useful when the workflow needs AssemblyAI-specific speech-to-text, LLM Gateway extraction, subtitles, or normalized agent JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio or video files, transcript text, prompts, schemas, and related metadata may be sent through the SkillBoss/HeyBoss API hub rather than only AssemblyAI-branded services. <br>
Mitigation: Review backend, retention, region, and compliance terms before use; avoid confidential, regulated, or customer recordings until those terms are verified. <br>
Risk: The skill requires sensitive credentials through SKILLBOSS_API_KEY. <br>
Mitigation: Inject credentials through the execution environment, avoid exposing keys in chat logs or output files, and rotate credentials if they may have been disclosed. <br>
Risk: Transcription, upload, and LLM requests can send data to external services and may create costs or persistent outputs. <br>
Mitigation: Use dry-run first when practical, choose explicit output paths, and inspect generated bundles before sharing them downstream. <br>


## Reference(s): <br>
- [AssemblyAI documentation](https://www.assemblyai.com/docs) <br>
- [Capabilities reference](references/capabilities.md) <br>
- [Workflow recipes](references/workflows.md) <br>
- [Output formats](references/output-formats.md) <br>
- [Speaker mapping reference](references/speaker-mapping.md) <br>
- [LLM Gateway notes](references/llm-gateway.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; CLI outputs Markdown, JSON, text, SRT/VTT, and bundle manifest files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write bundle directories containing transcript Markdown, normalized agent JSON, raw JSON, subtitles, paragraphs, sentences, and manifests.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
