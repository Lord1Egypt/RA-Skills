## Description:

Use when live speech translation is needed with Alibaba Cloud Model Studio Qwen LiveTranslate models, including bilingual meetings, realtime interpretation, and speech-to-speech or speech-to-text translation flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare Alibaba Cloud Qwen LiveTranslate request payloads and guidance for bilingual meetings, live subtitles, realtime interpretation, and call-center translated captions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Translation request payloads and response summaries may be saved locally under output/aliyun-qwen-livetranslate/.

Mitigation: Avoid confidential conversations unless a retention and cleanup process is in place for generated files.

## Reference(s):

- [Alibaba Cloud Qwen LiveTranslate documentation](https://help.aliyun.com/document_detail/2976526.html)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [Artifact sources](references/sources.md)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-qwen-livetranslate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script writes local request payloads and expects translation session payloads and response summaries under output/aliyun-qwen-livetranslate/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
